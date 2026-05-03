# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Pivot Controls
- Spin Controls

## Targeted Files

### game.js

- Action: modify
- Reason: Implement spin mechanic and deflection logic.
- Unchanged: InputManager, ArenaGame constructor, applyVisualTheme

## Patch Specs

### game.js

				- Problem: The current pulse mechanic is a one-shot burst. The game identity requires a sustained 'spin' move for route navigation.
				- Intended behavior: The player can hold or tap Space to enter a spinning state that deflects guards and builds 'stack' (which I will implement later).
				- Specific change: Transform triggerPulse into a sustained spin state update in updatePlayer.
				- Invariants: Player health and basic movement must remain functional.
				- Patch units:

- Add this.player.isSpinning and this.player.spinDuration.
- Update updatePlayer to handle spinning state.
- Update updateEnemies to check for spinning deflection.

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Pier Spin: Swarm Break.
		- Pass goal: Implement the Movement core slice with spin mechanics and guard deflection.
		- Active feature: Movement
		- Plan steps:

- Define spin constants in player object.
- Update updatePlayer loop to check for spin input and manage duration.
- Update updateEnemies to apply deflection if player is spinning.
- Test movement in the browser (mental simulation).

		- Simulated checkpoints:

- Spin state is active for a set duration after Space is pressed.
- Enemies are pushed back on contact during spin.

		- Implementation actions:

- Edit game.js to add spin properties to the player object.
- Edit game.js to update movement and collision logic.

		- Implementation notes:
		Keeping the spin duration short to maintain the 'arcade' rhythm. Deflection force will be normalized to avoid extreme launches.
