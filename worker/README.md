# YouTube API proxy

Deploy index.js as a Cloudflare Worker and add YOUTUBE_API_KEY as a Worker secret. Set the frontend API_BASE to the deployed URL. Supported endpoints: /api/health, /api/search?q=term, /api/channel?id=UC.... Metadata only; playback remains through official embeds.
