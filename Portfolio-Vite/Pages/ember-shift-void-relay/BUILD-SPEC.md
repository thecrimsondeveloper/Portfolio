# Build Spec

## Implementation Chapters

- Core Movement Loop
- Threat Pressure Pass
- Reward And Goal Flow
- Presentation And Overlay Polish

## Targeted Files

### game.js

- Action: modify
- Reason: Add state logic.
- Unchanged: physics loop

## Patch Specs

### game.js

				- Problem: No shift state exists.
				- Intended behavior: Toggle player state on input.
				- Specific change: Add this.player.isShifted = false in initPlayer and toggle in updatePlayer.
				- Invariants: Movement remains unaffected.
				- Patch units:

- Implement Root
- Validate Root

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Ember Shift: Void Relay.
		- Pass goal: Implement the core 'Shift' dimension mechanic and visual feedback.
		- Active feature: Root
		- Plan steps:

- Update initPlayer with isShifted: false.
- Modify consumePulse handler to toggle state.
- Add color transition to updatePlayer.

		- Simulated checkpoints:

- Color change on press.
- HUD update.

		- Implementation actions:

- Injecting shift logic into game.js

		- Implementation notes:
		Used the Pulse key as the Shift trigger to keep controls simple.
