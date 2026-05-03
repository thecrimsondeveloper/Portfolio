# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Spin Controls
- Sprint Controls

## Targeted Files

### game.js

- Action: modify
- Reason: Inject spin-dash logic and visual rotation.
- Unchanged: Input handling and basic Three.js setup.

### story-structure.json

- Action: modify
- Reason: Update score labels to 'Refine' and 'Rhythm'.
- Unchanged: Core arena and enemy configs.

## Patch Specs

### game.js

				- Problem: Generic dash with no 'spin' flavor.
				- Intended behavior: The player mesh should rotate rapidly around its Y axis during a dash.
				- Specific change: Update updatePlayer to increment player.mesh.rotation.y by a dash-speed multiplier.
				- Invariants: Player position and base movement speed remain consistent with DESIGN.md.
				- Patch units:

- Implement Movement
- Validate Movement

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Dock Spin: Swarm Break.
		- Pass goal: Implement the movement slice so the player can reliably feel spin under shock.
		- Active feature: Movement
		- Plan steps:

- Identify dash block in game.js
- Insert rotation logic
- Update status message strings

		- Simulated checkpoints:

- Player spins on shift key
- Status text says 'Refine'

		- Implementation actions:

- Editing game.js to add `this.player.mesh.rotation.y += delta * 20` during dashes.
- Editing story-structure.json to rename 'Gates' to 'Refine Gates'.

		- Implementation notes:
		Keeping the spin speed at 20 rad/s for a punchy feel.
