# Movement Change Packet

			## Sprint Objective

			Implement the movement slice so the player can reliably feel sprint under warden.

			## Player Promise

			The player immediately feels how movement improves the route and unlocks unify.

			## Why This Branch Exists

			Movement is a distinct, testable slice backed by the canonical brainstorm packet and should land without widening scope.

			## Detail Fractalization

			- Movement core slice
  - Implement the movement behavior in the main loop.
  - Wire player controller data into story-structure.json and runtime state.
- Movement feedback pass
  - Expose clear HUD and overlay feedback for movement.
  - Validate that movement stays readable during pressure spikes.

			## Simulated Checkpoints


- Movement is driven by canonical brainstorm data rather than ad hoc prompt output.
- Movement is visible in live play within the first minute of a run.

			## Acceptance Signals


- The player can describe what movement does after one run.
- Movement remains readable without breaking the current arena loop.

			## Change Packet Scope


- game.js
- story-structure.json
- index.html

			## Risks And Unknowns


- Movement could sprawl beyond the canonical build packet if extra systems are added.
- Movement could reduce readability if feedback does not stay compact.

			## Implementation Notes

			- Keep this packet isolated to the current game folder.
			- Use the checkpoints as simulated gates before full implementation.
			- Treat each branch slice as a sub-sprint, not as a merged refactor.
