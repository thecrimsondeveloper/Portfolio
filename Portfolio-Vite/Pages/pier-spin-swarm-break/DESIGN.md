
		# DESIGN

		## Pier Spin: Swarm Break

		**Description:** A expansive arcade game set between pier and peak, where the player uses spin and stack actions to outmaneuver swarm forces and drive an expand-to-upgrade progression arc.

		**Objective:** Use spin and stack to resolve guard-driven pressure, complete the active objective chain, and turn each run into expand, pulse progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: mechanical festival rescue
- Genres: escort resource run
- Environments: rooftop maintenance rails
- Settings: foggy morning
- Character motivations: repair broken machinery
- Movement mechanics: cargo balancing, mirror walking
- Core loops: evade patrols while searching
- Progression loops: power up a device
- Completion loops: ceremony completion
- Rewards: upgrade module, story fragments
- Antagonists: mischievous spirits
- Visual styles: textured industrial
- Audio styles: breathy wind soundscape
- Interaction patterns: inventory-lite object use
- Production focus: prototype in directory with JSON and HTML only
- Camera modes: over-the-shoulder danger-tilt
- Arena shapes: maze with shortcuts
- Primary verbs: redirect through hazards
- Scoring models: time attack near miss bonus
- Failure modes: core overheated after warning
- Enemy behaviors: block routes phase-shifted
- Objective structures: activate sequence after miniboss
- Resource systems: stamina combo refill
- Level progression: escalating waves with secret exits
- Twist constraints: shared health inside safe zone

		## Core Fantasy

		A expansive arcade game set between pier and peak, where the player uses spin and stack actions to outmaneuver swarm forces and drive an expand-to-upgrade progression arc.

		## Why This Game Is Distinct

		A guardian who masters elemental flow and dynamic balance to dismantle overwhelming swarms.

		## Player Actions

- spin
- stack
- dash

		## Core Loop

- Spin an obstacle to deflect incoming projectiles while stacking resources to fortify your position against swarms.
- Maneuver across compact terrain while managing limited charges, utilizing unique moves to create space for rapid repositioning.
- Climb upward to access high-visibility objectives and upgrade tools that modify future swarm compositions.
- Teach spin movement and introduce guard reads in a low-risk pier route.
- Layer stack interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite guard encounters, and a final expand choice.

		## Pressure And Opposition

- guard
- sentinel
- storm
- pier
- peak
- ice

		## Rewards And Progression

- expand
- pulse
- upgrade
- ascend
- Each run converts performance into expand, pulse upgrades and route unlocks.

		## Failure States

- Get overwhelmed by guard.
- Run out of time before the completion condition unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- The world blends pier, peak, ice into a hostile traversal space patrolled by swarm, commander, pulse.
- Dynamic lighting on exposed stone surfaces contrasts with the icy textures of peaks; depth is created through particle effects and atmospheric fog.
- pier
- peak
- ice
- harbor

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a dash burst for repositioning.
- Space converts spin and stack pressure into crowd control.
- Press Enter to deploy. Use WASD or Arrow keys to move, Shift to dash, and Space to pulse.
- health
- charge meter

		## JSON Data Hooks

- scene layout
- enemy waves
- objective rewards
- goal unlock state
- brainstorm final spec
- player controller

		## Sprint Builder Branches
		### Movement

				- Player promise: The player immediately feels how movement improves the route and unlocks expand.
				- Sprint objective: Implement the movement slice so the player can reliably feel spin under guard.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks pulse.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel stack under sentinel.
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

				- Player promise: The player immediately feels how one route hazard improves the route and unlocks upgrade.
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel dash under storm.
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

		- Assessment: yes - Pier Spin: Swarm Break has a readable arcade core built around spin, stack against guard, sentinel with a clear payoff in expand, pulse.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a dash burst for repositioning.

