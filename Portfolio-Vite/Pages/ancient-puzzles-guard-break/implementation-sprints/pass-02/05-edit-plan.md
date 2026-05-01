# Edit Plan

### story-structure.json

- Reason: Add enemy tuning fields for the sentry archetype
- Exact change: Add enemies.archetypes.sentry: {"visionRange":150, "visionAngle":60, "stunSeconds":1.2}
- Invariant: Preserve story-structure shape
- Verification command: python3 -m json.tool Pages/ancient-puzzles-guard-break/story-structure.json

### game.js

- Reason: Add stun bookkeeping and pulse reaction
- Exact change: Add enemy.stunned and stunTimer, modify triggerPulse to set stun, updateEnemies to handle timer decrement and skip actions while stunned
- Invariant: Preserve existing patrol and movement code
- Verification command: node --check Pages/ancient-puzzles-guard-break/game.js
