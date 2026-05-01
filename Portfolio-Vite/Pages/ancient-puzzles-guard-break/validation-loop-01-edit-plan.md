
		# Validation Loop 01 Edit Plan

		### story-structure.json

- Reason: Expose ember and enemy tuning
- Exact change: Add player.emberMax (100) and player.pulseCost (25); add enemies.archetypes.sentry tuning keys: visionRange=150, visionAngle=60, stunSeconds=1.2
- Invariant: Preserve other story fields
- Verification command: python3 -m json.tool Pages/ancient-puzzles-guard-break/story-structure.json

### game.js

- Reason: Implement ember gating and enemy stun
- Exact change: Initialize player.ember=this.player.emberMax; modify triggerPulse to check and subtract pulseCost; add enemy.stunned and stunTimer and decrement logic in updateEnemies
- Invariant: Preserve input mapping and existing flow
- Verification command: node --check Pages/ancient-puzzles-guard-break/game.js

### index.html

- Reason: Add Ember HUD label
- Exact change: Add Ember Charge display element to existing HUD cluster with id 'ember-charge'
- Invariant: Preserve layout
- Verification command: (visual) open the page in a browser
