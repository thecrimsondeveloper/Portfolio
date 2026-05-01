# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: No enemy vision/pursuit behavior and no integration with ember pulse
				- Intended behavior: Enemies patrol, detect the player within a vision cone, pursue, and can be stunned by pulses
				- Specific change: Extend createEnemies() to include patrol routes and vision params; update updateEnemies() to check vision cone and switch to pursuit state; apply stun when pulse affects enemy
				- Invariants: Do not alter player movement API or global game state shape
				- Patch units:

- Add patrol route data to enemies
- Add vision cone check in updateEnemies
- Respect stun state set by pulse
