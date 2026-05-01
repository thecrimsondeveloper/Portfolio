
		# DESIGN

		## Ancient Puzzles: Guard Break

		**Description:** A sprawling arcade game where ancient and tree environments host puzzle-based combat against guards, driving an evolve-to-unify arc.

		**Objective:** Use puzzles and ember to survive guard patrols, secure relic routes, and turn each run into evolve, unify progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: urban parkour delivery
- Genres: escort boss rush
- Environments: ancient quarry
- Settings: power outage
- Character motivations: reach a quiet sanctuary
- Movement mechanics: swinging from cables, momentum-based rolling
- Core loops: solve motion puzzles to advance
- Progression loops: unlock shortcuts
- Completion loops: ceremony completion
- Rewards: collectibles, story fragments
- Antagonists: self-learning barrier
- Visual styles: dusty pastel
- Audio styles: ambient hum
- Interaction patterns: combo navigation
- Production focus: focus on emergent loops
- Camera modes: isometric boss-focus
- Arena shapes: patrol grid with switchbacks
- Primary verbs: repair with timing
- Scoring models: artifact streak silver ladder
- Failure modes: timer expired after warning
- Enemy behaviors: block routes combo-triggered
- Objective structures: defuse core without alarm
- Resource systems: keys risk overflow
- Level progression: escalating waves with rerolls
- Twist constraints: moving goal during alarms

		## Core Fantasy

		A sprawling arcade game where ancient and tree environments host puzzle-based combat against guards, driving an evolve-to-unify arc.

		## Why This Game Is Distinct

		A master of logic and instinct who outsmarts relentless patrols in a hostile traversal world.

		## Player Actions

- puzzles
- ember
- solve

		## Core Loop

- Navigate tight corridors while solving environmental puzzles to disable guards before they engage.
- Manage resources like embers in an evolve-to-unify system that unlocks new abilities over time.
- Evolve into a more powerful form by clearing stronger enemies, gradually shifting from evasion to dominance.
- Teach puzzles movement and introduce guard reads in a low-risk ancient route.
- Layer ember interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite guard encounters, and a final evolve choice.

		## Pressure And Opposition

- guard
- sentry
- fort
- ancient
- tree
- pier

		## Rewards And Progression

- evolve
- unify
- discover
- expand
- Each run converts performance into evolve, unify upgrades and route unlocks.

		## Failure States

- Get overwhelmed by guard.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- A blend of ancient ruins, towering trees, and industrial piers forming a treacherous space patrolled by sentry fort units.
- High contrast between natural textures and gritty concrete with dynamic lighting effects.
- ancient
- tree
- pier
- forest

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a solve burst for repositioning.
- Space converts puzzles and ember pressure into crowd control.
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

				- Player promise: The player immediately feels how movement improves the route and unlocks evolve.
				- Sprint objective: Implement the movement slice so the player can reliably feel puzzles under guard.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks unify.
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

				- Player promise: The player immediately feels how one route hazard improves the route and unlocks discover.
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel solve under fort.
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

		- Assessment: yes - Ancient Puzzles: Guard Break has a readable arcade core built around puzzles, ember against guard, sentry with a clear payoff in evolve, unify.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a solve burst for repositioning.

