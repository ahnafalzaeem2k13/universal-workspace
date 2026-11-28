# VYBE — independent video platform

VYBE is an independent, responsive video discovery and sharing frontend. It is not affiliated with YouTube.

## Run locally

Serve the repository root over HTTP:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Implemented frontend features

- Responsive home feed, category chips, video cards and official YouTube privacy-enhanced embeds.
- Watch pages, related videos, Shorts-style vertical playback, trending, channel discovery and local search.
- Search filters for content type, duration, upload date and view count.
- Device-local likes, subscriptions, watch history, saved videos, comments, notifications, playlists and profile.
- Local data backup export as JSON.
- Manual YouTube URL and HTTPS direct MP4 import. YouTube playback uses the official embed player; only import media you own or are authorized to share.
- System/light/dark theme selection and an English/Bengali language toggle foundation.
- Offline shell cache and responsive layouts.

Local state stays in the current browser/device. It is not account-backed and does not sync across devices.

## Automated browser tests

With Python Playwright and Chromium installed:

```bash
python qa/smoke_test.py
python qa/feature_test.py
```

The smoke suite covers desktop, iPad, mobile, category filtering, watch pages, comments, Shorts and mobile navigation. The feature suite covers search date filters, theme selection, local backup export, HTTPS-only MP4 imports and YouTube Shorts URL parsing.

## Hosting

GitHub Pages is the current public host. The workflow is `.github/workflows/deploy-pages.yml`; repository Pages must be enabled with **Settings → Pages → Source → GitHub Actions**.

Cloudflare Pages is an alternative static host. See [DEPLOYMENT.md](DEPLOYMENT.md).

## YouTube Data API

The optional proxy is in `worker/index.js`. Deploy it as a Cloudflare Worker, add `YOUTUBE_API_KEY` as a Worker secret, and set `window.VYBE_CONFIG.API_BASE` in `config.js` to the Worker URL. Never put API keys in frontend code or GitHub. Endpoints currently include `/api/health`, `/api/search?q=term` and `/api/channel?id=UC...`. API-backed imports are not live until the Worker and secret are configured.

YouTube API quotas and provider free tiers can change. VYBE does not download or scrape YouTube videos.

## Accounts and database

`supabase/schema.sql` is a starting schema for profiles, channels, videos, subscriptions, likes, comments, notifications, playlists, watch history and reports. The frontend is not yet connected to Supabase authentication or remote syncing. A Supabase project URL and anon key are required before cloud accounts can be enabled.

## Current limitations

- No cloud login or cross-device sync yet.
- No live YouTube API results until a Worker URL and API key are configured.
- No production moderation pipeline or server-persisted comments/likes.
- Automatic detection of which short-duration uploads are actually Shorts is not provided by the YouTube Data API; do not treat all videos under three minutes as Shorts.
- Free-tier quotas, policies and availability are controlled by providers and are not guaranteed.

See [PLAN.md](PLAN.md), [TODO.md](TODO.md) and [DEPLOYMENT.md](DEPLOYMENT.md) for the build roadmap and setup notes.
