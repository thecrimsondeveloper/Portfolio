# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: No shift state exists.
				- Intended behavior: Toggle player state on input.
				- Specific change: Add this.player.isShifted = false in initPlayer and toggle in updatePlayer.
				- Invariants: Movement remains unaffected.
				- Patch units:

- Implement Root
- Validate Root
