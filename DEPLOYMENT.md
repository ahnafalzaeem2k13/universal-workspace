# Deployment

## Static hosting
Enable GitHub Pages for the repository root on main. The static app can be served without a paid host.

## YouTube API Worker
Create a Cloudflare Worker using worker/index.js. Add a secret named YOUTUBE_API_KEY. Set config.js API_BASE to the Worker URL. Worker quota/caching behavior is documented in worker/README.md.

## Database
Create a Supabase project and run supabase/schema.sql. The current frontend is not yet connected to Supabase; it continues to use browser-local state.

Never commit YouTube API keys, Supabase service-role keys, OAuth secrets, or private tokens.
