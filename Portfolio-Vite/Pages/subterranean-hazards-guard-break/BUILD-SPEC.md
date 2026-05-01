# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Hazards Controls

## Targeted Files

### game.js

- Action: update
- Reason: Implement sentry archetype and detection/pursuit logic
- Unchanged: Core renderer, camera, and input handling remain unchanged

### story-structure.json

- Action: update
- Reason: Add enemy tuning parameters (visionRange, visionAngle, stunSeconds)
- Unchanged: Seed and brainstorm payload remain unchanged

## Patch Specs

### game.js

				- Problem: No enemy vision/pursuit behavior and no integration with ember pulse
				- Intended behavior: Enemies patrol, detect the player within a vision cone, pursue, and can be stunned by pulses
				- Specific change: Extend createEnemies() to include patrol routes and vision params; update updateEnemies() to check vision cone and switch to pursuit state; apply stun when pulse affects enemy
				- Invariants: Do not alter player movement API or global game state shape
				- Patch units:

- Add patrol route data to enemies
- Add vision cone check in updateEnemies
- Respect stun state set by pulse

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Subterranean Hazards: Guard Break.
		- Pass goal: Implement one enemy archetype (Ember Sentry) that interacts with ember pulses and hazards.
		- Active feature: One Enemy Archetype
		- Plan steps:

- Edit game.js: add patrol and vision logic
- Edit story-structure.json: add enemy tuning parameters
- Run node --check and boot page for a quick runtime check

		- Simulated checkpoints:

- game.js passes node --check
- An enemy patrols in the scene
- Pulse stuns the enemy for stunSeconds

		- Implementation actions:

- Apply game.js patches
- Update story-structure.json parameters

		- Implementation notes:
		Keep enemy logic small and easily tunable; avoid companion AI this pass.
