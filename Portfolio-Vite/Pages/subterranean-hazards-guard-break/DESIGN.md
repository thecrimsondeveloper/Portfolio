
		# DESIGN

		## Subterranean Hazards: Guard Break

		**Description:** An arcade game where you fight guards and burn embers to escape, evolving from simple combat into a unified survival experience.

		**Objective:** Use hazards and ember to survive guard patrols, secure relic routes, and turn each run into expand, uncover progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: noir investigation
- Environments: subterranean library
- Settings: twilight
- Character motivations: save a stranded companion
- Movement mechanics: precision jumping, momentum-based rolling
- Core loops: guide a companion through hazards
- Progression loops: power up a device
- Completion loops: relay activation
- Rewards: movement mastery, upgrade module
- Antagonists: self-learning barrier
- Visual styles: architectural minimalism
- Audio styles: dripping water motifs
- Interaction patterns: context-sensitive movement
- Production focus: prepare for agent-driven expansion

		## Core Fantasy

		An arcade game where you fight guards and burn embers to escape, evolving from simple combat into a unified survival experience.

		## Why This Game Is Distinct

		A rogue-like hero navigating dangerous caves while wielding powerful tools and weapons against hostile foes.

		## Player Actions

- hazards
- ember
- crash

		## Core Loop

- Defend against guard patrols using strategic placement of hazards while managing ember fuel for attacks.
- Progress through compact levels by surviving pushers and fortresses until your health is full or a key item is found.
- Unlock new abilities and evolve your gear to create a unified strategy that adapts to increasingly complex threats.
- Teach hazards movement and introduce guard reads in a low-risk subterranean route.
- Layer ember interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite guard encounters, and a final expand choice.

		## Pressure And Opposition

- guard
- sentry
- commander
- subterranean
- tree
- pier

		## Rewards And Progression

- expand
- uncover
- evolve
- unify
- discover
- Each run converts performance into expand, uncover upgrades and route unlocks.

		## Failure States

- Get overwhelmed by guard.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- A blend of subterranean caverns, lush forests, and industrial pier structures creating an ever-changing battlefield.
- Dark, atmospheric lighting with neon accents from burning embers to emphasize the contrast between life and death.
- subterranean
- tree
- pier
- forest

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a crash burst for repositioning.
- Space converts hazards and ember pressure into crowd control.
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

				- Player promise: The player immediately feels how movement improves the route and unlocks expand.
				- Sprint objective: Implement the movement slice so the player can reliably feel hazards under guard.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks uncover.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel ember under sentry.
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

				- Player promise: The player immediately feels how one route hazard improves the route and unlocks evolve.
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel crash under commander.
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

		- Assessment: yes - Subterranean Hazards: Guard Break has a readable arcade core built around hazards, ember against guard, sentry with a clear payoff in expand, uncover.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a crash burst for repositioning.

