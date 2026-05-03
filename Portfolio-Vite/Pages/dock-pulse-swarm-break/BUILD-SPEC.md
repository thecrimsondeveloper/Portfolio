# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Pulse Controls

## Targeted Files

### game.js

- Action: update
- Reason: Enemy behavior lives in the runtime and needs one commander role with lane-control pressure.
- Unchanged: Keep the existing render loop, player movement, and baseline swarm presence.

### story-structure.json

- Action: update
- Reason: The story payload should describe the commander role and its interaction with pulse and relay routes.
- Unchanged: Preserve page identity and canonical brainstorm history.

### index.html

- Action: update
- Reason: The shell may need a short warning line or clearer telemetry labels for commander pressure.
- Unchanged: Preserve the existing responsive overlay and HUD layout.

## Patch Specs

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

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Dock Pulse: Swarm Break.
		- Pass goal: Add one readable commander archetype that locks bridge lanes and forces rerouting during the relay-repair run.
		- Active feature: One Enemy Archetype
		- Plan steps:

- Add commander behavior and pulse interruption in the runtime.
- Align story data with commander route-control pressure.
- Retune shell messaging so the player sees lane warnings clearly.

		- Simulated checkpoints:

- The commander appears and pressures at least one relay lane.
- Pulse creates an obvious interruption window against the commander.
- Status text reflects commander pressure when it matters.

		- Implementation actions:

- Patch commander data and behavior into game.js.
- Patch route-pressure enemy language into story-structure.json.
- Patch concise commander-warning copy into index.html or the runtime-fed status strings.

		- Implementation notes:
		This pass is sufficient to conclude the initial implementation planning loop because it covers the two biggest sources of sameness: generic movement framing and generic enemy pressure.
