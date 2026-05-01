# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: Pulse is currently not gated by ember and does not consume resource
				- Intended behavior: Pulse requires enough ember and subtracts pulseCost from player.ember
				- Specific change: Initialize player.ember from player.emberMax and add a check in triggerPulse: if (this.player.ember >= pulseCost) { this.player.ember -= pulseCost; apply pulse } else return;
				- Invariants: Do not change movement input handling otherwise
				- Patch units:

- Initialize player.ember in constructor
- Read player.pulseCost from story config
- Modify triggerPulse to check and consume ember

### story-structure.json

				- Problem: No ember tuning fields currently exposed
				- Intended behavior: Expose player.emberMax and player.pulseCost for tuning
				- Specific change: Add player.emberMax and player.pulseCost (numbers) under player object
				- Invariants: Keep existing player fields intact
				- Patch units:

- Implement Movement
- Validate Movement
