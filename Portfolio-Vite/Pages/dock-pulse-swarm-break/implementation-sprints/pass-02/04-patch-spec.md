# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: Current enemies read as generic swarm pressure and do not claim route space in a distinct way.
				- Intended behavior: A commander enemy should patrol or anchor key bridge lanes, apply pressure to active relay routes, and briefly stagger when pulsed.
				- Specific change: Add one commander state machine with a readable warning radius, lane-control behavior, and a pulse-reactive interruption window.
				- Invariants: Do not replace the entire enemy system or remove the existing pulse input path.
				- Patch units:

- Add commander config and spawn data.
- Add lane-control or intercept behavior tied to active relay routes.
- Add pulse interruption feedback and status messaging.

### story-structure.json

				- Problem: The current data does not clearly explain how commander pressure shapes routing.
				- Intended behavior: The story payload should define commander pressure as a route-control threat rather than a generic damage sponge.
				- Specific change: Update enemy, objective, and fun-need text so commander behavior is named and mechanically legible.
				- Invariants: Keep the broader game identity and seed references unchanged.
				- Patch units:

- Name the commander role in the design-facing data.
- Describe pulse as the counter-window for lane control.
- Align objective text with route pressure language.

### index.html

				- Problem: The shell currently lacks concise feedback for lane-control pressure.
				- Intended behavior: The player should immediately understand when a commander is locking a route.
				- Specific change: Retain the current HUD structure but allow the status area to surface commander warnings in short, high-contrast copy.
				- Invariants: Do not add new major UI panels or clutter the overlay.
				- Patch units:

- Reserve the status line for commander warnings when active.
- Keep telemetry compact and readable.
- Avoid duplicating long instructional text.
