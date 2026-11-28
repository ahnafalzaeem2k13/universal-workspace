# VYBE rebuild plan

## Product direction
VYBE is an independent, responsive video platform. Preserve the existing static frontend and GitHub Pages deployment while evolving it in verified increments. Official YouTube embeds and YouTube Data API metadata are the only YouTube integration; never download or scrape protected videos. Direct MP4 imports must be user-authorized URLs.

## Constraints and architecture decisions
- Budget: $0; no credit card, paid service, or mandatory upgrade. Free-tier availability and quotas are not guaranteed and must be documented.
- Source of truth: this repository, main; Google Colab is the execution/QA environment, not persistent storage.
- Frontend: retain lightweight HTML/CSS/JavaScript unless a tested migration offers clear value. Avoid adding a framework merely for fashion.
- Hosting: GitHub Pages remains the current public host. The optional YouTube API proxy is a separately deployed Worker; API secrets stay in host secrets.
- Data/auth: Supabase is optional and credential-gated. Keep anonymous browsing usable. Local storage is a fallback, never describe it as cloud sync.
- Security: validate all external URLs and input; keep RLS enabled; no service-role or API secrets in browser code.

## Phase 1 — Inspect and prepare
- [x] Inspect repository, branch, permissions, existing files, deployment, worker, schema and tests.
- [x] Run existing browser smoke suite as baseline.
- [x] Confirm legacy toolbox/ and zaeem-tower/ directories are absent from the tracked tree; no deletion needed.
- [x] Add this plan and a truthful task ledger.

## Phase 2 — Core platform
- [ ] Improve application structure and accessible responsive navigation.
- [ ] Harden video cards, watch routes, playback errors and share links.
- [ ] Improve Shorts navigation and keyboard/touch controls.
- [ ] Add robust loading, empty, unavailable and offline states.

## Phase 3 — User features
- [ ] Improve search suggestions and filters for local and API results.
- [ ] Complete channel pages and selected-channel import management.
- [ ] Make local likes, subscriptions, history, saved videos, playlists and comments consistent and exportable.
- [ ] Add notification read/unread state and comment moderation/reporting affordances.
- [ ] Complete English/Bengali localization and system/light/dark themes.

## Phase 4 — Backend and API
- [ ] Review and harden Supabase schema, RLS, indexes and auth lifecycle.
- [ ] Integrate Supabase only when public project URL and anon key are supplied; never require credentials for anonymous browsing.
- [ ] Harden Worker API validation, caching, request deduplication, quota responses and CORS.
- [ ] Add API-backed import/refresh and normal/Shorts distinction without scraping.

## Phase 5 — Testing
- [ ] Expand Playwright coverage across desktop, iPad and mobile.
- [ ] Test search, filters, video/Shorts navigation, comments, subscriptions, playlists, imports and theme/language.
- [ ] Check console errors, accessibility basics, broken links/assets, overflow and API failure states.
- [ ] Verify production build/site after each deployment.

## Phase 6 — Publish
- [ ] Commit verified increments to the existing main branch.
- [ ] Confirm GitHub Actions deployment and live site.
- [ ] Document external account/secret setup and free-tier limitations.

## Known external blockers
- YouTube Data API key is not configured.
- Supabase project URL and anon key are not configured; schema alone does not provide accounts or cloud sync.
- Worker deployment and secret configuration require an authenticated Cloudflare account action.
- Free provider quotas, policies and availability may change.
