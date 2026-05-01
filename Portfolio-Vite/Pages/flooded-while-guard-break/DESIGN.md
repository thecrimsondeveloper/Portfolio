
		# DESIGN

		## Flooded While: Guard Break

		**Description:** An arcade game set between flooded and tree, where the player uses while and ember actions to outmaneuver guard forces.

		**Objective:** Use while and ember to survive commander patrols, secure relic routes, and turn each run into discover, evolve progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: hidden society infiltration
- Environments: flooded market district
- Settings: late-night
- Character motivations: escape before dawn
- Movement mechanics: rhythm-based stepping, precision jumping
- Core loops: evade patrols while searching
- Progression loops: power up a device
- Completion loops: ceremony completion
- Rewards: story fragments, artifact sets
- Antagonists: self-learning barrier
- Visual styles: muted earth tones
- Audio styles: field recording textures
- Interaction patterns: hold-and-release momentum
- Production focus: prepare for agent-driven expansion

		## Core Fantasy

		An arcade game set between flooded and tree, where the player uses while and ember actions to outmaneuver guard forces.

		## Why This Game Is Distinct

		A rogue survivor driving an evolve-to-unify progression arc through hostile terrain.

		## Player Actions

- while
- ember
- sprint

		## Core Loop

- Acquire resources to equip gear that unlocks new abilities for the next phase.
- Execute actions to outmaneuver enemies while navigating unstable flooded structures.
- Drive an evolve-to-unify progression arc through compact but expressive gameplay runs.
- Teach while movement and introduce commander reads in a low-risk flooded route.
- Layer ember interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite commander encounters, and a final discover choice.

		## Pressure And Opposition

- commander
- leader
- warden
- flooded
- tree
- pier

		## Rewards And Progression

- discover
- evolve
- unify
- expand
- Each run converts performance into discover, evolve upgrades and route unlocks.

		## Failure States

- Get overwhelmed by commander.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- Blends flooded, tree, and pier into a patrolled space by guard, sentry, fort.
- High contrast textures with dynamic environmental interactions during traversal runs.
- flooded
- tree
- pier
- forest

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a sprint burst for repositioning.
- Space converts while and ember pressure into crowd control.
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

				- Player promise: The player immediately feels how movement improves the route and unlocks discover.
				- Sprint objective: Implement the movement slice so the player can reliably feel while under commander.
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
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel ember under leader.
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

				- Player promise: The player immediately feels how one route hazard improves the route and unlocks unify.
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel sprint under warden.
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

		- Assessment: yes - Flooded While: Guard Break has a readable arcade core built around while, ember against commander, leader with a clear payoff in discover, evolve.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a sprint burst for repositioning.

