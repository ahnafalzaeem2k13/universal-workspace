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
- [x] Add local data backup export for likes, subscriptions, comments, playlists and history.
- [x] Build channel pages with Videos, Shorts and Playlists tabs and channel filtering.
- [ ] Fix routing, playback fallbacks, mobile navigation and accessibility.
- [ ] Improve Shorts navigation and playback controls.

## P2 — User features
- [x] Add mutually exclusive local likes/dislikes.
- [x] Add threaded local comment replies, sorting, comment likes and report capture.
- [x] Add notification read/unread state.
- [ ] Add validated local backup restore and full data portability.
- [ ] Finish Bengali translations.
- [ ] Implement optional authenticated cloud accounts and cross-device sync.

## P3 — Backend
- [x] Add a Supabase security migration with RLS hardening, reply validation, profile creation and FK indexes; SQL parser validation passed.
- [ ] Apply migration to a live Supabase project and test authenticated policies.
- [ ] Harden YouTube Worker and API caching/quota handling.
- [!] YouTube API integration end-to-end — waiting for API key and Worker deployment.
- [!] Cloud accounts and cross-device sync — waiting for Supabase project credentials.

## P4 — Release quality
- [x] Add repeatable Playwright feature regression coverage.
- [ ] Expand accessibility checks and test API failure states.
- [ ] Verify live GitHub Pages deployment after changes.
- [ ] Update README and deployment guide with exact implemented status.
