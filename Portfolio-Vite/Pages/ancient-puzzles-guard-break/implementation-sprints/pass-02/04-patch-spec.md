# Patch Spec

		## Per-File Patch Units

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
