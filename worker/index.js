const TTL_SECONDS = 300;
const pending = new Map();

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin");
  const allowed = env.ALLOWED_ORIGIN || "*";
  if (origin && allowed !== "*" && origin !== allowed) return null;
  return {
    "access-control-allow-origin": allowed === "*" ? "*" : (origin || allowed),
    "access-control-allow-methods": "GET, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    "vary": "Origin"
  };
}

function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      ...headers
    }
  });
}

async function youtubeApi(path, params, env) {
  const url = new URL("https://www.googleapis.com/youtube/v3/" + path);
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  }
  url.searchParams.set("key", env.YOUTUBE_API_KEY);

  const request = new Request(url.toString());
  const cache = globalThis.caches?.default;
  if (cache) {
    const cached = await cache.match(request);
    if (cached) return cached.json();
  }

  const cacheKey = url.toString();
  if (pending.has(cacheKey)) return pending.get(cacheKey);

  const task = (async () => {
    let response;
    try {
      response = await fetch(url.toString(), { signal: AbortSignal.timeout(12000) });
    } catch (error) {
      throw Object.assign(new Error("YouTube API is temporarily unreachable. Please try again."), { status: 502 });
    }

    let body;
    try {
      body = await response.json();
    } catch {
      throw Object.assign(new Error("YouTube API returned an unreadable response."), { status: 502 });
    }

    if (!response.ok) {
      const quotaExceeded = response.status === 403 &&
        /quotaExceeded|dailyLimitExceeded|rateLimitExceeded/i.test(JSON.stringify(body));
      throw Object.assign(
        new Error(quotaExceeded
          ? "YouTube API quota exhausted. Try again later; cached results may still be available."
          : (body.error?.message || "YouTube API request failed.")),
        { status: quotaExceeded ? 429 : (response.status >= 500 ? 502 : response.status) }
      );
    }

    if (cache) {
      await cache.put(
        request,
        new Response(JSON.stringify(body), {
          headers: {
            "content-type": "application/json; charset=utf-8",
            "cache-control": "public, max-age=" + TTL_SECONDS
          }
        })
      );
    }
    return body;
  })();

  pending.set(cacheKey, task);
  try {
    return await task;
  } finally {
    pending.delete(cacheKey);
  }
}

export default {
  async fetch(request, env) {
    const cors = corsHeaders(request, env);
    if (!cors) return json({ error: "Origin not allowed." }, 403);

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (request.method !== "GET") return json({ error: "Method not allowed." }, 405, cors);

    const url = new URL(request.url);
    if (url.pathname === "/api/health") {
      return json({ ok: true, configured: Boolean(env.YOUTUBE_API_KEY) }, 200, cors);
    }

    if (!["/api/search", "/api/channel"].includes(url.pathname)) {
      return json({ error: "Not found." }, 404, cors);
    }
    if (!env.YOUTUBE_API_KEY) {
      return json({ error: "Worker not configured. Add YOUTUBE_API_KEY as a Worker secret." }, 503, cors);
    }

    try {
      if (url.pathname === "/api/search") {
        const query = (url.searchParams.get("q") || "").trim();
        if (!query) return json({ error: "Search query is required." }, 400, cors);
        if (query.length > 100) return json({ error: "Search query must be 100 characters or fewer." }, 400, cors);
        const type = url.searchParams.get("type") === "channel" ? "channel" : "video";
        const data = await youtubeApi("search", {
          part: "snippet",
          type,
          maxResults: 20,
          q: query
        }, env);
        return json({ items: data.items || [], nextPageToken: data.nextPageToken || null }, 200, cors);
      }

      const channelId = (url.searchParams.get("id") || "").trim();
      if (!/^UC[A-Za-z0-9_-]{20,}$/.test(channelId)) {
        return json({ error: "A valid YouTube channel ID is required." }, 400, cors);
      }

      const channelData = await youtubeApi("channels", {
        part: "snippet,contentDetails,statistics",
        id: channelId
      }, env);
      const channel = channelData.items?.[0];
      if (!channel) return json({ error: "Channel not found." }, 404, cors);

      const uploadsPlaylist = channel.contentDetails?.relatedPlaylists?.uploads;
      if (!uploadsPlaylist) return json({ error: "Channel uploads are unavailable." }, 502, cors);

      const playlist = await youtubeApi("playlistItems", {
        part: "snippet,contentDetails",
        playlistId: uploadsPlaylist,
        maxResults: 50
      }, env);
      const ids = (playlist.items || [])
        .map(item => item.contentDetails?.videoId)
        .filter(id => /^[A-Za-z0-9_-]{11}$/.test(id || ""));

      let details = { items: [] };
      if (ids.length) {
        details = await youtubeApi("videos", {
          part: "snippet,contentDetails,statistics",
          id: ids.join(",")
        }, env);
      }

      return json({ channel, videos: details.items || [] }, 200, cors);
    } catch (error) {
      const status = Number.isInteger(error.status) ? error.status : 502;
      return json({
        error: error.message || "Unexpected API error.",
        quotaExhausted: status === 429
      }, status, cors);
    }
  }
};
