# Feature Sprint Spec

## All Feature Packets

### Movement

		- Sprint objective: Implement the movement slice so the player can reliably feel while under commander.
		- Player promise: The player immediately feels how movement improves the route and unlocks discover.
		- Branch reason: Movement is a distinct, testable slice backed by the canonical brainstorm packet and should land without widening scope.

		#### Branch Slices
		- Movement core slice
  - Implement the movement behavior in the main loop.
  - Wire player controller data into story-structure.json and runtime state.
- Movement feedback pass
  - Expose clear HUD and overlay feedback for movement.
  - Validate that movement stays readable during pressure spikes.

		#### Checkpoints

- Movement is driven by canonical brainstorm data rather than ad hoc prompt output.
- Movement is visible in live play within the first minute of a run.

		#### Acceptance Signals

- The player can describe what movement does after one run.
- Movement remains readable without breaking the current arena loop.

		#### Scope

- game.js
- story-structure.json
- index.html

		#### Risks

- Movement could sprawl beyond the canonical build packet if extra systems are added.
- Movement could reduce readability if feedback does not stay compact.

### One Enemy Archetype

		- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel ember under leader.
		- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks evolve.
		- Branch reason: One Enemy Archetype is a distinct, testable slice backed by the canonical brainstorm packet and should land without widening scope.

		#### Branch Slices
		- One Enemy Archetype core slice
  - Implement the one enemy archetype behavior in the main loop.
  - Wire enemy director data into story-structure.json and runtime state.
- One Enemy Archetype feedback pass
  - Expose clear HUD and overlay feedback for one enemy archetype.
  - Validate that one enemy archetype stays readable during pressure spikes.

		#### Checkpoints

- One Enemy Archetype is driven by canonical brainstorm data rather than ad hoc prompt output.
- One Enemy Archetype is visible in live play within the first minute of a run.

		#### Acceptance Signals

- The player can describe what one enemy archetype does after one run.
- One Enemy Archetype remains readable without breaking the current arena loop.

		#### Scope

- game.js
- story-structure.json
- index.html

		#### Risks

- One Enemy Archetype could sprawl beyond the canonical build packet if extra systems are added.
- One Enemy Archetype could reduce readability if feedback does not stay compact.

### One Route Hazard

		- Sprint objective: Implement the one route hazard slice so the player can reliably feel sprint under warden.
		- Player promise: The player immediately feels how one route hazard improves the route and unlocks unify.
		- Branch reason: One Route Hazard is a distinct, testable slice backed by the canonical brainstorm packet and should land without widening scope.

		#### Branch Slices
		- One Route Hazard core slice
  - Implement the one route hazard behavior in the main loop.
  - Wire upgrade loop data into story-structure.json and runtime state.
- One Route Hazard feedback pass
  - Expose clear HUD and overlay feedback for one route hazard.
  - Validate that one route hazard stays readable during pressure spikes.

		#### Checkpoints

- One Route Hazard is driven by canonical brainstorm data rather than ad hoc prompt output.
- One Route Hazard is visible in live play within the first minute of a run.

		#### Acceptance Signals

- The player can describe what one route hazard does after one run.
- One Route Hazard remains readable without breaking the current arena loop.

		#### Scope

- game.js
- story-structure.json
- index.html

		#### Risks

- One Route Hazard could sprawl beyond the canonical build packet if extra systems are added.
- One Route Hazard could reduce readability if feedback does not stay compact.

## Active Packet Context

- Active feature: Movement
- Active packet reason: Movement is the best current packet for this pass.
- Active sprint objective: Implement the movement slice so the player can reliably feel while under commander.
- Active player promise: The player immediately feels how movement improves the route and unlocks discover.
- Current pass goal: Build the first playable implementation passes for Flooded While: Guard Break.
