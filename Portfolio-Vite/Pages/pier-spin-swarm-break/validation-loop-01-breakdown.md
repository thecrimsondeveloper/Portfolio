
		# Validation Loop 01 Breakdown


- Patch story-structure.json with movement, sentry, and route-hazard tuning values so runtime changes are data-backed.
- Patch game.js in three slices: movement timing, sentry state machine, and a single rotating or locking route hazard tied to the level flow.
- Patch index.html only where needed to expose stable HUD labels for keys, dawn, relay, and alert state.
- Run JSON and JS validation after each focused edit rather than waiting for one large rewrite.
