# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Spin Controls

## Targeted Files

### game.js

- Action: update
- Reason: Implement sentry patrol and detection states
- Unchanged: player core movement and unrelated reward loops

### story-structure.json

- Action: update
- Reason: Expose sentry tuning values
- Unchanged: existing story flow and objective metadata

### index.html

- Action: update
- Reason: Optionally add a compact alert label if the shell already supports status text
- Unchanged: page structure and script imports

## Patch Specs

### story-structure.json

				- Problem: Enemy tuning is too generic for a factory sentry archetype
				- Intended behavior: The JSON defines sentry visionRange, alertSeconds, chaseSpeed, and stunSeconds so the runtime can read one consistent archetype
				- Specific change: Add a sentry block under enemy or encounter tuning with numeric defaults for visionRange, alertSeconds, chaseSpeed, and stunSeconds
				- Invariants: Preserve existing JSON layout and non-enemy settings
				- Patch units:

- Add sentry tuning object
- Keep defaults conservative for a first playable pass

### game.js

				- Problem: Enemy behavior likely collapses into generic movement instead of readable stealth pressure
				- Intended behavior: Sentries patrol routes until the player enters a sight cone, then alert and chase for a short duration; pulse or dodge windows can interrupt pressure briefly
				- Specific change: Add sentry state fields for patrol, alertTimer, chaseTimer, and stunned; update the enemy loop to switch between patrol, alert, chase, and recover states based on distance and visibility
				- Invariants: Preserve existing render flow and avoid rewriting unrelated systems
				- Patch units:

- Initialize sentry state when enemies spawn
- Add sightline or facing-based detection helper
- Handle patrol-to-alert-to-chase state changes
- Support brief stun or interrupt windows

### index.html

				- Problem: The shell may not communicate when the player has been spotted
				- Intended behavior: If a safe status element exists, it can report alert pressure like 'Sentry Lock' or 'Hidden'
				- Specific change: Only add or rename a small status label if game.js already has or can safely target a status element
				- Invariants: Do not break existing DOM ids used by the scaffold
				- Patch units:

- Implement One Enemy Archetype
- Validate One Enemy Archetype

## Implementation Sequence

- Sprint goal: Build the first playable implementation passes for Pier Spin: Swarm Break.
		- Pass goal: Add one factory sentry archetype that patrols lanes, reacts to sightlines, and pressures the new movement rules.
		- Active feature: One Enemy Archetype
		- Plan steps:

- Add sentry tuning to story-structure.json
- Patch game.js enemy creation and update logic for patrol and chase states
- Add compact alert feedback only if a safe DOM target exists
- Run JS and JSON validation commands

		- Simulated checkpoints:

- story-structure.json parses successfully
- game.js passes syntax validation
- At least one enemy clearly transitions between patrol and alert pressure

		- Implementation actions:

- Update config first
- Implement sentry behavior in game.js
- Adjust HUD status text last if required

		- Implementation notes:
		Keep the enemy pass narrow and readable. Save route hazards and rotating-room pressure for validation follow-up or a later repair pass.
