# Sprint Review

		## Thoughts

		The next distinct improvement is one enemy archetype. A narrow sentry with patrol, cone detection, and brief stun windows will support the stealth-puzzle loop without rewriting the whole runtime.

		## Target Changes


- Expose sentry tuning in story-structure.json for sight range, cone angle, and stun duration
- Update game.js enemy setup so one sentry archetype patrols, detects the player, and chases on sight
- Surface sentry alert state in HUD or on-screen feedback only if a safe existing hook exists

		## Risks


- Sightline math can be noisy if the runtime lacks facing vectors
- Adding HUD alert text must avoid breaking existing DOM hooks

		## Acceptance Signals


- At least one enemy archetype has readable patrol, alert, and chase states
- The player can break or interrupt pressure briefly instead of facing nonstop generic pursuit
- game.js passes node --check and story-structure.json parses

		## Target Files Or Surfaces


- game.js
- story-structure.json
- index.html
