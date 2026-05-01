
		# DESIGN

		## Overgrown Systems: Guard Break

		**Description:** An expansive arcade game where players outmaneuver guard forces and drive an evolve-to-unify progression arc in a hostile overgrown world.

		**Objective:** Use blink and dash to survive commander patrols, secure relic routes, and turn each run into unify, discover progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: industrial salvage
- Genres: stealth arena
- Environments: overgrown greenhouse
- Settings: foggy morning
- Character motivations: reach a quiet sanctuary
- Movement mechanics: momentum-based rolling, mirror walking
- Core loops: rebuild broken systems
- Progression loops: rescue allies
- Completion loops: final escape sequence
- Rewards: boss unlock, collectibles
- Antagonists: patrolling automatons
- Visual styles: architectural minimalism
- Audio styles: field recording textures
- Interaction patterns: context-sensitive movement
- Production focus: focus on emergent loops
- Camera modes: isometric zoom-pulse
- Arena shapes: hub-and-spokes with switchbacks
- Primary verbs: chase with timing
- Scoring models: perfect route near miss bonus
- Failure modes: core overheated by patrols
- Enemy behaviors: summon hazards light-triggered
- Objective structures: reach exit before timer
- Resource systems: noise zone recharge
- Level progression: branching routes with hazard tiers
- Twist constraints: reversed controls zone after route split

		## Core Fantasy

		An expansive arcade game where players outmaneuver guard forces and drive an evolve-to-unify progression arc in a hostile overgrown world.

		## Why This Game Is Distinct

		A master of systems and ember actions who navigates the tree-filled terrain with precision.

		## Player Actions

- blink
- dash
- slide

		## Core Loop

- Confront enemies while utilizing system-based mechanics to survive compact but challenging runs.
- Evolve player abilities through ember actions to gain tactical advantage against growing threats.
- Navigate a unique traverse space where pushing forward is essential for survival.
- Teach blink movement and introduce commander reads in a low-risk overgrown route.
- Layer dash interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite commander encounters, and a final unify choice.

		## Pressure And Opposition

- commander
- industrial
- warden
- overgrown
- tree
- pier

		## Rewards And Progression

- unify
- discover
- evolve
- expand
- Each run converts performance into unify, discover upgrades and route unlocks.

		## Failure States

- Get overwhelmed by commander.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- Overgrown, tree-piercing space patrolled by hostile guards and sentries.
- Dynamic, expressive combat in an organic environment that blends urban and natural elements.
- overgrown
- tree
- pier
- forest

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a slide burst for repositioning.
- Space converts blink and dash pressure into crowd control.
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
				- Sprint objective: Implement the movement slice so the player can reliably feel blink under commander.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks discover.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel dash under industrial.
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
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel slide under warden.
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

		- Assessment: yes - Overgrown Systems: Guard Break has a readable arcade core built around blink, dash against commander, industrial with a clear payoff in unify, discover.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a slide burst for repositioning.

