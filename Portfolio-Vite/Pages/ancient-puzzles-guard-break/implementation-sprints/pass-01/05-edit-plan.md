# Edit Plan

### game.js

- Reason: Gating pulse and ember bookkeeping
- Exact change: Initialize this.player.ember=this.player.emberMax; add check/consume in triggerPulse to use player.pulseCost
- Invariant: Preserve existing control mapping
- Verification command: node --check Pages/ancient-puzzles-guard-break/game.js

### story-structure.json

- Reason: Expose ember tuning for designers
- Exact change: Add player.emberMax and player.pulseCost keys with numeric defaults
- Invariant: Preserve story structure shape
- Verification command: python3 -m json.tool Pages/ancient-puzzles-guard-break/story-structure.json
