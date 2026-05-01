# Change Pack Plan

		## Sprint Objective

		Add one factory sentry archetype that patrols lanes, reacts to sightlines, and pressures the new movement rules.

		## Implementation Plan


- Add sentry tuning to story-structure.json
- Patch game.js enemy creation and update logic for patrol and chase states
- Add compact alert feedback only if a safe DOM target exists
- Run JS and JSON validation commands

		## Simulated Checkpoints


- story-structure.json parses successfully
- game.js passes syntax validation
- At least one enemy clearly transitions between patrol and alert pressure
