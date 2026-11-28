# VYBE TODO

Legend: [ ] not started · [/] in progress · [x] verified complete · [!] blocked

## P0 — Foundation
- [x] Inspect existing repository, permissions, architecture and deployment.
- [x] Run baseline Playwright smoke test (desktop, iPad, mobile).
- [x] Confirm toolbox/ and zaeem-tower/ are already absent from tracked files.
- [x] Create rebuild plan and task ledger.

## P1 — Core experience
- [ ] Refactor fragile monolithic frontend code into maintainable modules.
- [ ] Fix routing, playback fallbacks, mobile navigation and accessibility.
- [ ] Improve Shorts, search, channel pages and responsive states.

## P2 — User features
- [ ] Complete local interactions and data export/import.
- [ ] Add threaded comments, notification state and reporting UI.
- [ ] Finish Bengali translations and system theme behavior.

## P3 — Backend
- [ ] Harden YouTube Worker and API caching/quota handling.
- [ ] Harden Supabase schema and RLS; implement optional auth/sync.
- [!] YouTube API integration end-to-end — waiting for API key and Worker deployment.
- [!] Cloud accounts and cross-device sync — waiting for Supabase project credentials.

## P4 — Release quality
- [ ] Expand automated browser tests and accessibility checks.
- [ ] Verify live GitHub Pages deployment after changes.
- [ ] Update README and deployment guide with exact implemented status.
