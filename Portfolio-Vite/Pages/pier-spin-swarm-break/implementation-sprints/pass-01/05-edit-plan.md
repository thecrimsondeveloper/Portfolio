# Edit Plan

### story-structure.json

- Reason: Expose movement tuning for rhythm-step and mirror-walk behavior
- Exact change: Add player movement keys beatWindow, mirrorWindow, and dodgeCooldown with starter numeric defaults
- Invariant: Preserve current story content and JSON structure
- Verification command: python3 -m json.tool Pages/pier-spin-swarm-break/story-structure.json

### game.js

- Reason: Make movement feel distinct from a generic arena controller
- Exact change: Add player step timing state, apply on-beat speed modifiers, and add a short mirror-walk timer wired into movement handling
- Invariant: Preserve existing camera, render loop, and input bindings
- Verification command: node --check Pages/pier-spin-swarm-break/game.js

### index.html

- Reason: Match shell feedback to the factory stealth run
- Exact change: Update HUD labels or notes so they mention Keys, Dawn Timer, and Relay progress
- Invariant: Do not break existing DOM ids used by game.js
- Verification command: open Pages/pier-spin-swarm-break/index.html
