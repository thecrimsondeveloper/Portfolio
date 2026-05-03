# Petal Change Packet

			## Sprint Objective

			Implement the petal slice so the player can reliably feel petal under route hazards.

			## Player Promise

			The player immediately feels how petal improves the route and unlocks route unlocks.

			## Why This Branch Exists

			Petal is a distinct, testable slice backed by the canonical brainstorm packet and should land without widening scope.

			## Detail Fractalization

			- Petal core slice
  - Implement the petal behavior in the main loop.
  - Wire petal data into story-structure.json and runtime state.
- Petal feedback pass
  - Expose clear HUD and overlay feedback for petal.
  - Validate that petal stays readable during pressure spikes.

			## Simulated Checkpoints


- Petal is driven by canonical brainstorm data rather than ad hoc prompt output.
- Petal is visible in live play within the first minute of a run.

			## Acceptance Signals


- The player can describe what petal does after one run.
- Petal remains readable without breaking the current arena loop.

			## Change Packet Scope


- game.js
- story-structure.json
- index.html

			## Risks And Unknowns


- Petal could sprawl beyond the canonical build packet if extra systems are added.
- Petal could reduce readability if feedback does not stay compact.

			## Implementation Notes

			- Keep this packet isolated to the current game folder.
			- Use the checkpoints as simulated gates before full implementation.
			- Treat each branch slice as a sub-sprint, not as a merged refactor.
