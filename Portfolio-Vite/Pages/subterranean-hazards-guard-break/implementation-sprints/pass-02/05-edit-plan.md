# Edit Plan

### game.js

- Reason: Add sentry archetype and pulse interaction
- Exact change: Modify enemy creation to include route and vision params; add vision-based pursuit in updateEnemies; ensure pulse sets enemy.stun
- Invariant: Keep renderer and camera code unchanged
- Verification command: node --check Pages/subterranean-hazards-guard-break/game.js
