
		# Validation Loop 01 Edit Plan

		### game.js

- Reason: Link shift to invulnerability.
- Exact change: In enemy collision check: if (this.player.isShifted && enemy.type === 'void-shadow') return;
- Invariant: Other hazards still damage the player.
- Verification command: grep 'isShifted' game.js
