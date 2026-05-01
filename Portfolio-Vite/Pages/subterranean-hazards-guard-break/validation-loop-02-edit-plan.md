
		# Validation Loop 02 Edit Plan

		### Pages/subterranean-hazards-guard-break/game.js

- Reason: Add ember resource and hazard pulse reactions
- Exact change: Introduce player.ember and pulseCost; modify triggerPulse() to check and consume ember; set hazard.stun on pulse; update updateHazards() to skip damage while hazard.stun>0; update updateHud() to display Ember Charge.
- Invariant: Preserve renderer, camera, and core input handling
- Verification command: node --check Pages/subterranean-hazards-guard-break/game.js

### Pages/subterranean-hazards-guard-break/story-structure.json

- Reason: Expose ember and enemy tuning parameters for iteration
- Exact change: Add player.emberMax, player.emberRechargeRate, player.pulseCost and optional enemy tuning (visionRange, visionAngle, stunSeconds) under scene rules or player/enemy configs.
- Invariant: Preserve seed and brainstorm final spec
- Verification command: python3 -m json.tool Pages/subterranean-hazards-guard-break/story-structure.json

### Pages/subterranean-hazards-guard-break/index.html

- Reason: Update overlay hint and HUD labels to surface Ember Charge
- Exact change: Change overlay-hint copy and add Ember Charge label in HUD so players see resource state.
- Invariant: Keep layout and CDN imports unchanged
- Verification command: grep -n Ember Pages/subterranean-hazards-guard-break/index.html || true
