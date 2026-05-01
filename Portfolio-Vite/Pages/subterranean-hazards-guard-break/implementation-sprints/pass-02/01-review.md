# Sprint Review

		## Thoughts

		Add a single sentry type with a simple patrol, vision cone detection, pursuit behavior, and stun reaction to ember pulses.

		## Target Changes


- Add sentry patrol with vision and pursuit
- Wire stun/reaction to ember pulse
- Expose enemy tuning parameters in story-structure.json

		## Risks


- Enemy detection tuning may need iteration
- Overly aggressive pursuit could frustrate early runs

		## Acceptance Signals


- A sentry patrols a route
- Sentry pursues when detecting the player
- Sentry is stunned by ember pulse

		## Target Files Or Surfaces


- game.js
- story-structure.json
