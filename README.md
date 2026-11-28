# VYBE — independent video platform

A responsive, installable video discovery app. VYBE is a separate brand and is not affiliated with YouTube.

## Run
Serve the repository root over HTTP: python -m http.server 8080, then open http://localhost:8080.

## Working now
- Responsive home feed, category chips, video cards, YouTube privacy-enhanced embeds.
- Watch pages, related videos, Shorts-style vertical embed view, search, trending and channel discovery.
- Device-local likes, subscriptions, watch history, saved videos, comments, notifications and profile.
- Manual YouTube URL / direct MP4 URL import (only share content you own or are authorized to share).
- Light/dark theme, language toggle foundation, offline shell cache.

Local state is stored only in this browser; it does not sync across devices.

## YouTube Data API
Deploy worker/index.js as a Cloudflare Worker. Add YOUTUBE_API_KEY in Worker Settings as a secret, never in frontend code or GitHub. Set window.VYBE_CONFIG.API_BASE in config.js to the Worker URL. Endpoints: /api/health, /api/search?q=term, /api/channel?id=UC.... The Worker caches successful API results for five minutes, coalesces duplicate requests and returns clear quota errors. It uses official API metadata and official embed playback; it does not download or scrape videos.

## Database and accounts
supabase/schema.sql is the initial schema and row-level security setup for profiles, channels, videos, subscriptions, likes, comments/replies, notifications, playlists, watch history and reports. Run it in a Supabase SQL editor after creating a project. The frontend has not yet been wired to Supabase authentication or remote syncing.

## Remaining production work
Cloud authentication and cross-device sync, server-persisted comments and likes, channel import/refresh UI, moderation workflows, full Bengali translations and truly personalized recommendations require backend credentials and additional integration. No credentials are included. Free-tier quotas and terms may change.
