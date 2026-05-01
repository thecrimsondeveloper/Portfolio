
		# Validation Loop 01 Breakdown


- Update story-structure.json to add player.emberMax and player.pulseCost and enemy tuning (visionRange, visionAngle, stunSeconds)
- Patch game.js to initialize this.player.ember, check/consume pulseCost in triggerPulse, and add stunTimer logic in updateEnemies
- Add Ember Charge display markup to index.html HUD cluster
