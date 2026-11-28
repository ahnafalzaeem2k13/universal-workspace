# Deployment

## Recommended static host: Cloudflare Pages

VYBE is a plain HTML/CSS/JavaScript app. It does not need Gradio, a Node build, or a paid server for the frontend.

1. Open https://dash.cloudflare.com/ and sign in or create a free account.
2. Go to **Workers & Pages → Create → Pages → Connect to Git**.
3. Authorize GitHub and select `ahnafalzaeem2k13/universal-workspace`.
4. Set the production branch to `main`.
5. Choose **None** as the framework preset. Leave the build command empty and set the build output directory to `/` (repository root).
6. Deploy. Cloudflare will provide a `*.pages.dev` URL and automatically redeploy on future pushes to `main`.

The repository includes a `_headers` file for basic security headers and sensible cache behavior. The Cloudflare Pages Git connection is a one-time account-owner action; no Cloudflare token should be committed to GitHub.

## GitHub Pages (alternative)

The existing workflow is `.github/workflows/deploy-pages.yml`. To use it instead, open **Repository Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**.

## YouTube API Worker

The optional API backend is separate from static hosting. Deploy `worker/index.js` as a Cloudflare Worker. Add a secret named `YOUTUBE_API_KEY` in Worker Settings, then set `window.VYBE_CONFIG.API_BASE` in `config.js` to the Worker URL. Never put API keys in frontend code or GitHub. Endpoints: `/api/health`, `/api/search?q=term`, and `/api/channel?id=UC...`.

## Database and accounts

Create a Supabase project and run `supabase/schema.sql`. The current frontend is not yet connected to Supabase authentication or remote syncing; user data remains browser-local.

Never commit YouTube API keys, Supabase service-role keys, OAuth secrets, or private tokens.
