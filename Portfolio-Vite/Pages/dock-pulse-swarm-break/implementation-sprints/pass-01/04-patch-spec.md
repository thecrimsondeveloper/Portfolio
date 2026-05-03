# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: The runtime is built around relic collection and exit unlocks, which makes the game feel like a stock arena pickup loop.
				- Intended behavior: The player should move between relay nodes, spend pulse actions to repair them, and manage rising noise risk while surviving swarm pressure.
				- Specific change: Rename the collectible loop to relay nodes, track repaired nodes and noise or stability state, and rewrite status messages and win condition around finishing the network route.
				- Invariants: Do not remove the existing input handling, camera follow, or render/update structure.
				- Patch units:

- Rename relic state to relay state and update objective strings.
- Add a route-pressure meter tied to pulse usage and cooldown recovery.
- Swap the exit unlock condition for repairing the required relay count.

### story-structure.json

				- Problem: The scene data does not yet expose relay-specific labels or movement-pressure values.
				- Intended behavior: The story payload should describe relay nodes, noise pressure, and courier-readable objective text.
				- Specific change: Update objective, controls, fun-needs copy, and scene rules so the runtime can read relay count, pressure text, and route framing from data.
				- Invariants: Keep the canonical brainstorm and design sections intact unless a field is directly wrong for the implemented runtime.
				- Patch units:

- Rewrite objective and controls for relay repair.
- Add scene rule labels for relay goal and pressure meter.
- Align description text with the repaired shell copy.

### index.html

				- Problem: The shell still shows generic telemetry labels and an overloaded hint paragraph.
				- Intended behavior: The HUD should surface objective, route status, and telemetry in concise courier language.
				- Specific change: Replace generic labels and hint text with relay, noise, and stability framing while preserving the existing layout.
				- Invariants: Do not change the core canvas container or break the current responsive shell.
				- Patch units:

- Retitle HUD cards around route and telemetry.
- Shorten overlay hint copy into readable control guidance.
- Ensure overlay story text does not duplicate raw UI note strings.
