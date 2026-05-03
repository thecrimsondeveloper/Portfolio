# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: The current pulse mechanic is a one-shot burst. The game identity requires a sustained 'spin' move for route navigation.
				- Intended behavior: The player can hold or tap Space to enter a spinning state that deflects guards and builds 'stack' (which I will implement later).
				- Specific change: Transform triggerPulse into a sustained spin state update in updatePlayer.
				- Invariants: Player health and basic movement must remain functional.
				- Patch units:

- Add this.player.isSpinning and this.player.spinDuration.
- Update updatePlayer to handle spinning state.
- Update updateEnemies to check for spinning deflection.
