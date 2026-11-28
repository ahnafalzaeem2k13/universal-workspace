# VYBE TODO

Legend: [ ] not started · [/] in progress · [x] verified complete · [!] blocked

## P0 — Foundation
- [x] Inspect existing repository, permissions, architecture and deployment.
- [x] Run baseline Playwright smoke test (desktop, iPad, mobile).
- [x] Confirm toolbox/ and zaeem-tower/ are already absent from tracked files.
- [x] Create rebuild plan and task ledger.

## P1 — Core experience
- [/] Refactor fragile monolithic frontend code into maintainable modules.
- [x] Harden YouTube URL parsing and require HTTPS for direct MP4 imports.
- [x] Add upload-date filtering to search results.
- [x] Add system/dark/light theme cycling and system preference detection.
- [x] Add local data export for likes, subscriptions, comments, playlists and history.
- [ ] Fix routing, playback fallbacks, mobile navigation and accessibility.
- [ ] Improve Shorts navigation and channel pages.

## P2 — User features
- [ ] Complete local interactions and data import/restore.
- [ ] Add threaded comments, comment likes, sorting and reporting UI.
- [ ] Add notification read/unread state.
- [ ] Finish Bengali translations.

## P3 — Backend
- [ ] Harden YouTube Worker and API caching/quota handling.
- [ ] Harden Supabase schema and RLS; implement optional auth/sync.
- [!] YouTube API integration end-to-end — waiting for API key and Worker deployment.
- [!] Cloud accounts and cross-device sync — waiting for Supabase project credentials.

## P4 — Release quality
- [x] Add repeatable Playwright feature regression coverage.
- [ ] Expand accessibility checks and test API failure states.
- [ ] Verify live GitHub Pages deployment after changes.
- [ ] Update README and deployment guide with exact implemented status.
