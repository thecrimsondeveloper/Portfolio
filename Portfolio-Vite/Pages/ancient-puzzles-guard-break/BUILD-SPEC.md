# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Puzzles Controls

## Targeted Files

### game.js

- Action: update
- Reason: Add stun handling and pulse reaction
- Unchanged: patrol path definitions

## Patch Specs

### story-structure.json

				- Problem: Enemy tuning fields missing
				- Intended behavior: Expose visionRange, visionAngle, and stunSeconds for enemy archetype
				- Specific change: Add under enemies.archetypes["sentry"]: {"visionRange":150, "visionAngle":60, "stunSeconds":1.2}
				- Invariants: Preserve existing enemy definitions
				- Patch units:

- Implement One Enemy Archetype
- Validate One Enemy Archetype

### game.js

				- Problem: Enemies don't support stun or pulse reaction
				- Intended behavior: Pulse sets enemy.stunned=true and enemy.stunTimer=stunSeconds; updateEnemies skips active behavior while stunned and decrements timer
				- Specific change: Add enemy.stunned and enemy.stunTimer fields; modify triggerPulse to set stun on nearby enemies; change updateEnemies to handle stunTimer decrement and skip actions when stunned
				- Invariants: Do not change enemy movement paths or spawn logic
				- Patch units:

- Initialize stun fields where enemies are created
- Modify triggerPulse to iterate enemies and apply stun if within radius
- Change updateEnemies to decrement stunTimer and clear stunned flag when <=0

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Ancient Puzzles: Guard Break.
		- Pass goal: Implement a patrol sentry enemy that reacts to pulses and can be stunned.
		- Active feature: One Enemy Archetype
		- Plan steps:

- Update story-structure.json
- Patch game.js for stun and pulse reaction
- Run node --check

		- Simulated checkpoints:

- story-structure.json parses
- game.js syntax OK

		- Implementation actions:

- Apply JSON edits to story-structure.json
- Edit game.js per editPlan

		- Implementation notes:
		Keep AI simple: patrol -> detect -> chase; stun pauses behavior for stunSeconds.
