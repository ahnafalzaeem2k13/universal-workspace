import assert from "node:assert/strict";
import worker from "./index.js";

const cacheStore = new Map();
globalThis.caches = {
  default: {
    async match(request) {
      const value = cacheStore.get(request.url);
      return value ? value.clone() : undefined;
    },
    async put(request, response) {
      cacheStore.set(request.url, response.clone());
    }
  }
};

let apiCalls = 0;
globalThis.fetch = async input => {
  apiCalls += 1;
  const url = new URL(String(input));
  await new Promise(resolve => setTimeout(resolve, 25));
  if (url.searchParams.get("q") === "quota-test") {
    return new Response(JSON.stringify({
      error: { message: "quota exceeded", errors: [{ reason: "quotaExceeded" }] }
    }), { status: 403 });
  }
  return new Response(JSON.stringify({
    items: [{ id: { videoId: "abcdefghijk" }, snippet: { title: "Fixture result" } }]
  }), { status: 200 });
};

const env = {
  YOUTUBE_API_KEY: "test-secret-not-returned",
  ALLOWED_ORIGIN: "https://site.example"
};
const request = (path, method = "GET", origin = "https://site.example") =>
  new Request("https://worker.example" + path, {
    method,
    headers: origin ? { Origin: origin } : {}
  });

let response = await worker.fetch(request("/api/health"), {});
assert.equal(response.status, 200);
assert.deepEqual(await response.json(), { ok: true, configured: false });

response = await worker.fetch(request("/api/health", "GET", "https://evil.example"), env);
assert.equal(response.status, 403);

response = await worker.fetch(request("/api/health", "OPTIONS"), env);
assert.equal(response.status, 204);

response = await worker.fetch(request("/api/search?q=test", "POST"), env);
assert.equal(response.status, 405);

response = await worker.fetch(request("/api/search"), env);
assert.equal(response.status, 400);

response = await worker.fetch(request("/api/channel?id=not-a-channel"), env);
assert.equal(response.status, 400);

response = await worker.fetch(request("/api/search?q=test"), {});
assert.equal(response.status, 503);

const before = apiCalls;
const [first, second] = await Promise.all([
  worker.fetch(request("/api/search?q=fixture"), env),
  worker.fetch(request("/api/search?q=fixture"), env)
]);
assert.equal(first.status, 200);
assert.equal(second.status, 200);
assert.equal(apiCalls - before, 1, "concurrent identical searches should be deduplicated");
const payload = await first.json();
assert.equal(payload.items[0].snippet.title, "Fixture result");
assert.equal(first.headers.get("access-control-allow-origin"), "https://site.example");
assert.equal(JSON.stringify(payload).includes("test-secret-not-returned"), false);

response = await worker.fetch(request("/api/search?q=quota-test"), env);
assert.equal(response.status, 429);
const quota = await response.json();
assert.equal(quota.quotaExhausted, true);

console.log("PASS: Worker health, CORS allowlist, preflight, method/query validation, missing-key state, request deduplication, secret isolation and quota error handling");
