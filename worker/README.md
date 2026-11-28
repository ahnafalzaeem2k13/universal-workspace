# YouTube Data API proxy

Deploy `index.js` as a Cloudflare Worker. It uses official YouTube Data API metadata only; playback remains through YouTube's official embed player. It never downloads or scrapes videos.

## Configuration

- Add `YOUTUBE_API_KEY` as a Worker secret. Never put it in frontend code or GitHub.
- Set `ALLOWED_ORIGIN` to the exact VYBE website origin (the repository's default is `https://ahnafalzaeem2k13.github.io`). If hosting elsewhere, update `wrangler.toml` before deployment.
- Set `window.VYBE_CONFIG.API_BASE` in `config.js` to the deployed Worker URL.

## Endpoints

- `GET /api/health`
- `GET /api/search?q=term` (optional `type=channel`)
- `GET /api/channel?id=UC...` (latest 50 uploads)

The Worker validates methods and inputs, supports CORS allowlisting, caches successful API responses for five minutes, deduplicates concurrent identical requests, and returns a distinct 429 quota-exhaustion response. The YouTube API key is only sent from the Worker to Google and is never returned to the browser.

## Test locally

With Node.js installed, run:

```bash
node worker/test.mjs
```

The test uses mocked API responses; it does not consume YouTube API quota.
