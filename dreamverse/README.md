# DREAMVERSE: AFTERGLOW

A browser-playable 3D endless rail adventure built with Three.js. It lives in `/dreamverse/` so the existing VYBE homepage remains untouched.

## Play
- Desktop: A/D or ←/→ to change tracks; Space/W/↑ to boost; S/↓ to brake; P/Esc to pause.
- Touch: use the left/right and boost buttons.
- Goal: collect 30 signal shards. Avoid gates, drones and cargo; collisions damage the train. Every fifth shard repairs a little hull.

## Run locally
Serve the repository root over HTTP (ES modules do not run reliably from `file://`) and open `/dreamverse/`. Three.js is loaded from jsDelivr; no build step or API key is required.

## Technical notes
- Vanilla JavaScript + Three.js ES module; no framework or paid service.
- Procedural city blocks, skyline lights, rails, train, hazards and collectibles.
- Recycled city props and rail sleepers, capped device pixel ratio, delta-time movement.
- Responsive HUD, keyboard and pointer controls, pause/restart, local best score, synthesized sound.
- All game logic runs locally in the browser; no accounts, analytics or external game backend.

## Known limitations
- This is a polished playable first release, not a networked multiplayer game.
- Browser requires network access to load the pinned Three.js CDN module.
- Device tilt is not enabled by default; touch controls are the reliable mobile input.
