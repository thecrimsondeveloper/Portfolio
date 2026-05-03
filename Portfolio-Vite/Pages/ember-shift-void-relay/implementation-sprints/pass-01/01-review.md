# Sprint Review

		## Thoughts

		To make this feel like a 'Shift' game, the player needs a toggleable state that changes their interaction with the world. We'll start with a color shift and a simple flag.

		## Target Changes


- Add isShifted flag to player.
- Bind Shift key (Pulse) to toggle isShifted.
- Update player color based on shift state.

		## Risks


- Visual feedback might be too subtle.
- Toggle spamming could be jarring.

		## Acceptance Signals


- Player changes color when shifting.
- The shift status is displayed in the HUD.

		## Target Files Or Surfaces


- game.js
- story-structure.json
