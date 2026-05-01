
		# DESIGN

		## Overgrown Artifacts: Guard Break

		**Description:** Navigate overgrown and tree spaces with sprint and crash, survive warden-led pressure, and turn each run into unify progress.

		**Objective:** Use sprint and crash to survive warden patrols, secure relic routes, and turn each run into unify, evolve progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: industrial salvage
- Genres: chase
- Environments: overgrown greenhouse
- Settings: festival night
- Character motivations: unmask a hidden group
- Movement mechanics: wall-running, slide and vault
- Core loops: collect and combine artifacts
- Progression loops: assemble a map
- Completion loops: artifact assembly
- Rewards: movement mastery, story fragments
- Antagonists: mischievous spirits
- Visual styles: cinematic noir lighting
- Audio styles: ambient hum
- Interaction patterns: soft physics-based control
- Production focus: create a human-readable design spec
- Camera modes: top-down
- Arena shapes: vertical tower
- Primary verbs: redirect
- Scoring models: delivery value
- Failure modes: signal broken
- Enemy behaviors: patrol
- Objective structures: escort target
- Resource systems: battery
- Level progression: room ladder
- Twist constraints: decaying floor

		## Core Fantasy

		Navigate overgrown and tree spaces with sprint and crash, survive warden-led pressure, and turn each run into unify progress.

		## Why This Game Is Distinct

		Feel like a fast improviser navigating overgrown hazards while turning sentry pressure into opportunities.

		## Player Actions

- sprint
- crash
- combine

		## Core Loop

- Scout routes through overgrown spaces and identify guard pressure points.
- Use artifacts and ember interactions to survive, reposition, and secure objectives.
- Convert each run into evolve gains that unlock stronger options and open the next challenge band.
- Teach sprint movement and introduce warden reads in a low-risk overgrown route.
- Layer crash interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite warden encounters, and a final unify choice.

		## Pressure And Opposition

- warden
- leader
- industrial
- overgrown
- tree
- pier

		## Rewards And Progression

- unify
- evolve
- discover
- expand
- Each run converts performance into unify, evolve upgrades and route unlocks.

		## Failure States

- Get overwhelmed by warden.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- A stylized world blending overgrown, tree, and shifting threat territory.
- Lean on overgrown, tree, and guard motifs for strong silhouettes, readable threat zones, and punchy arcade contrast.
- overgrown
- tree
- pier
- forest

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a combine burst for repositioning.
- Space converts sprint and crash pressure into crowd control.
- Press Enter to deploy. Use WASD or Arrow keys to move, Shift to dash, and Space to pulse.
- health
- charge meter

		## JSON Data Hooks

- scene layout
- enemy waves
- relic rewards
- goal unlock state
- brainstorm final spec
- player controller

		## Sprint Builder Branches
		### Movement

				- Player promise: The player immediately feels how movement improves the route and unlocks unify.
				- Sprint objective: Implement the movement slice so the player can reliably feel sprint under warden.
				- Change packet scope: game.js, story-structure.json, index.html
				- Simulated checkpoints: Movement is driven by canonical brainstorm data rather than ad hoc prompt output., Movement is visible in live play within the first minute of a run.

				#### Detail Fractalization
				- Movement core slice
  - Implement the movement behavior in the main loop.
  - Wire player controller data into story-structure.json and runtime state.
- Movement feedback pass
  - Expose clear HUD and overlay feedback for movement.
  - Validate that movement stays readable during pressure spikes.

### One Enemy Archetype

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks evolve.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel crash under leader.
				- Change packet scope: game.js, story-structure.json, index.html
				- Simulated checkpoints: One Enemy Archetype is driven by canonical brainstorm data rather than ad hoc prompt output., One Enemy Archetype is visible in live play within the first minute of a run.

				#### Detail Fractalization
				- One Enemy Archetype core slice
  - Implement the one enemy archetype behavior in the main loop.
  - Wire enemy director data into story-structure.json and runtime state.
- One Enemy Archetype feedback pass
  - Expose clear HUD and overlay feedback for one enemy archetype.
  - Validate that one enemy archetype stays readable during pressure spikes.

### One Route Hazard

				- Player promise: The player immediately feels how one route hazard improves the route and unlocks discover.
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel combine under industrial.
				- Change packet scope: game.js, story-structure.json, index.html
				- Simulated checkpoints: One Route Hazard is driven by canonical brainstorm data rather than ad hoc prompt output., One Route Hazard is visible in live play within the first minute of a run.

				#### Detail Fractalization
				- One Route Hazard core slice
  - Implement the one route hazard behavior in the main loop.
  - Wire upgrade loop data into story-structure.json and runtime state.
- One Route Hazard feedback pass
  - Expose clear HUD and overlay feedback for one route hazard.
  - Validate that one route hazard stays readable during pressure spikes.

		## Delivery Notes

		- Keep this game self-contained inside its own page folder.
		- Keep the HTML entry point and story JSON in the same folder.
		- Preserve a three.js + Rapier prototype structure.
		- Favor game-specific logic over shared systems.
		- Use branch-specific change packets to plan the next sprint in isolated slices.

## Fun Game Assessment

		- Assessment: yes - Overgrown Artifacts: Guard Break has a readable arcade core built around sprint, crash against warden, leader with a clear payoff in unify, evolve.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a combine burst for repositioning.

