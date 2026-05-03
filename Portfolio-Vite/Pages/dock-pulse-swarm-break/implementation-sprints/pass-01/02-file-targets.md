# File Targets

		## Targeted Surfaces

		### game.js

- Action: update
- Reason: The main loop currently uses relic and goal logic that does not match the relay-repair design.
- Expected unchanged: Preserve the renderer, camera setup, scene boot sequence, and basic keyboard controls.

### story-structure.json

- Action: update
- Reason: The story payload still describes generic survive-and-upgrade goals and needs relay-specific runtime data.
- Expected unchanged: Preserve the page identity, seed history, and brainstorm packet references.

### index.html

- Action: update
- Reason: The HUD labels and overlay hint need to match relay repair, noise risk, and route stability.
- Expected unchanged: Preserve the page shell, canvas structure, and mobile-safe layout.
