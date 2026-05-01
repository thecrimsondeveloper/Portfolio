# Patch Spec

		## Per-File Patch Units

		### story-structure.json

				- Problem: Enemy tuning is too generic for a factory sentry archetype
				- Intended behavior: The JSON defines sentry visionRange, alertSeconds, chaseSpeed, and stunSeconds so the runtime can read one consistent archetype
				- Specific change: Add a sentry block under enemy or encounter tuning with numeric defaults for visionRange, alertSeconds, chaseSpeed, and stunSeconds
				- Invariants: Preserve existing JSON layout and non-enemy settings
				- Patch units:

- Add sentry tuning object
- Keep defaults conservative for a first playable pass

### game.js

				- Problem: Enemy behavior likely collapses into generic movement instead of readable stealth pressure
				- Intended behavior: Sentries patrol routes until the player enters a sight cone, then alert and chase for a short duration; pulse or dodge windows can interrupt pressure briefly
				- Specific change: Add sentry state fields for patrol, alertTimer, chaseTimer, and stunned; update the enemy loop to switch between patrol, alert, chase, and recover states based on distance and visibility
				- Invariants: Preserve existing render flow and avoid rewriting unrelated systems
				- Patch units:

- Initialize sentry state when enemies spawn
- Add sightline or facing-based detection helper
- Handle patrol-to-alert-to-chase state changes
- Support brief stun or interrupt windows

### index.html

				- Problem: The shell may not communicate when the player has been spotted
				- Intended behavior: If a safe status element exists, it can report alert pressure like 'Sentry Lock' or 'Hidden'
				- Specific change: Only add or rename a small status label if game.js already has or can safely target a status element
				- Invariants: Do not break existing DOM ids used by the scaffold
				- Patch units:

- Implement One Enemy Archetype
- Validate One Enemy Archetype
