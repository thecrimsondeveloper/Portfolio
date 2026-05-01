# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Sprint Controls

## Targeted Files

### game.js

- Action: update
- Reason: Advance Movement.
- Unchanged: Unrelated systems remain unchanged.

### story-structure.json

- Action: update
- Reason: Advance Movement.
- Unchanged: Unrelated systems remain unchanged.

### index.html

- Action: update
- Reason: Advance Movement.
- Unchanged: Unrelated systems remain unchanged.

## Patch Specs

### game.js

				- Problem: Movement is blocked in game.js.
				- Intended behavior: game.js supports the next slice of Movement.
				- Specific change: Update game.js to support Movement.
				- Invariants: Unrelated systems remain unchanged.
				- Patch units:

- Inspect game.js
- Patch game.js for Movement

### story-structure.json

				- Problem: Movement is blocked in story-structure.json.
				- Intended behavior: story-structure.json supports the next slice of Movement.
				- Specific change: Update story-structure.json to support Movement.
				- Invariants: Unrelated systems remain unchanged.
				- Patch units:

- Inspect story-structure.json
- Patch story-structure.json for Movement

### index.html

				- Problem: Movement is blocked in index.html.
				- Intended behavior: index.html supports the next slice of Movement.
				- Specific change: Update index.html to support Movement.
				- Invariants: Unrelated systems remain unchanged.
				- Patch units:

- Inspect index.html
- Patch index.html for Movement

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Clocktower Pieces: Guard Break.
		- Pass goal: Build the first playable implementation passes for Clocktower Pieces: Guard Break.
		- Active feature: Movement
		- Plan steps:

- Implement the next slice of Movement.
- Validate the change for Movement.

		- Simulated checkpoints:

- Movement compiles cleanly.
- Movement behaves as intended.

		- Implementation actions:

- Implement the next slice of Movement.
- Validate the change for Movement.

		- Implementation notes:
		Pass 01 notes are pending.
