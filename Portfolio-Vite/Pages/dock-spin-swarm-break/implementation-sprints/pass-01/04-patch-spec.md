# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: Generic dash with no 'spin' flavor.
				- Intended behavior: The player mesh should rotate rapidly around its Y axis during a dash.
				- Specific change: Update updatePlayer to increment player.mesh.rotation.y by a dash-speed multiplier.
				- Invariants: Player position and base movement speed remain consistent with DESIGN.md.
				- Patch units:

- Implement Movement
- Validate Movement
