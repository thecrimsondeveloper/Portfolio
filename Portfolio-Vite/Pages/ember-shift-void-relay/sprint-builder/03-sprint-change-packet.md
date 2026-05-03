# Sprint Change Packet

			## Sprint Objective

			Implement the sprint slice so the player can reliably feel sprint under time pressure.

			## Player Promise

			The player immediately feels how sprint improves the route and unlocks new ability gains.

			## Why This Branch Exists

			Sprint is a distinct, testable slice backed by the canonical brainstorm packet and should land without widening scope.

			## Detail Fractalization

			- Sprint core slice
  - Implement the sprint behavior in the main loop.
  - Wire sprint data into story-structure.json and runtime state.
- Sprint feedback pass
  - Expose clear HUD and overlay feedback for sprint.
  - Validate that sprint stays readable during pressure spikes.

			## Simulated Checkpoints


- Sprint is driven by canonical brainstorm data rather than ad hoc prompt output.
- Sprint is visible in live play within the first minute of a run.

			## Acceptance Signals


- The player can describe what sprint does after one run.
- Sprint remains readable without breaking the current arena loop.

			## Change Packet Scope


- game.js
- story-structure.json
- index.html

			## Risks And Unknowns


- Sprint could sprawl beyond the canonical build packet if extra systems are added.
- Sprint could reduce readability if feedback does not stay compact.

			## Implementation Notes

			- Keep this packet isolated to the current game folder.
			- Use the checkpoints as simulated gates before full implementation.
			- Treat each branch slice as a sub-sprint, not as a merged refactor.
