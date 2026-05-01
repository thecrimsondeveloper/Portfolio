
		# DESIGN

		## Subterranean Artifacts: Guard Break

		**Description:** An arcade game blending subterranean and tree worlds where players use artifacts to outmaneuver guards.

		**Objective:** Use sprint and crash to survive commander patrols, secure relic routes, and turn each run into unify, expand progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: hidden society infiltration
- Environments: subterranean library
- Settings: midsummer heat
- Character motivations: learn a forgotten ritual
- Movement mechanics: momentum-based rolling, mirror walking
- Core loops: collect and combine artifacts
- Progression loops: unlock shortcuts
- Completion loops: vault extraction
- Rewards: boss unlock, upgrade module
- Antagonists: mischievous spirits
- Visual styles: cinematic noir lighting
- Audio styles: ambient hum
- Interaction patterns: inventory-lite object use
- Production focus: focus on emergent loops

		## Core Fantasy

		An arcade game blending subterranean and tree worlds where players use artifacts to outmaneuver guards.

		## Why This Game Is Distinct

		A warrior utilizing enchanted tools to forge unity across hostile terrains.

		## Player Actions

- sprint
- crash
- combine

		## Core Loop

- Player explores compact environments while evading patrols sentries and fortifications.
- Artifacts provide powers for combat, enabling the player to outmaneuver enemy commanders.
- A evolve-to-unify progression arc requires strategic use of powers across diverse terrains.
- Teach sprint movement and introduce commander reads in a low-risk subterranean route.
- Layer crash interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite commander encounters, and a final unify choice.

		## Pressure And Opposition

- commander
- guard
- sentry
- subterranean
- tree
- pier

		## Rewards And Progression

- unify
- expand
- evolve
- discover
- Each run converts performance into unify, expand upgrades and route unlocks.

		## Failure States

- Get overwhelmed by commander.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- A subterranean, tree, and pier environment patrolled by formidable guards.
- Expansive traversal with compact, expressive runs that challenge navigation.
- subterranean
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
				- Sprint objective: Implement the movement slice so the player can reliably feel sprint under commander.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks expand.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel crash under guard.
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
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel combine under sentry.
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

		- Assessment: yes - Subterranean Artifacts: Guard Break has a readable arcade core built around sprint, crash against commander, guard with a clear payoff in unify, expand.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a combine burst for repositioning.

