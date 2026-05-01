
		# DESIGN

		## Pier Spin: Swarm Break

		**Description:** A spin-based arcade where players outmaneuver swarm forces to unlock the peak.

		**Objective:** Use spin and sprint to survive glitch patrols, secure relic routes, and turn each run into unveil, unlock progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: street level mystery
- Genres: stealth puzzle
- Environments: abandoned factory
- Settings: late-night
- Character motivations: escape before dawn
- Movement mechanics: rhythm-based stepping, mirror walking
- Core loops: evade patrols while searching
- Progression loops: build a safe path
- Completion loops: relay activation
- Rewards: boss unlock, resource caches
- Antagonists: rival explorer
- Visual styles: textured industrial
- Audio styles: mechanical percussion
- Interaction patterns: inventory-lite object use
- Production focus: focus on motion and feel
- Camera modes: cinematic follow wide-read
- Arena shapes: shrinking zone with shortcuts
- Primary verbs: trade with timing
- Scoring models: survival timer speed bonus
- Failure modes: cargo shattered during overload
- Enemy behaviors: chase on sight light-triggered
- Objective structures: defuse core in split routes
- Resource systems: keys slow drain
- Level progression: single run with secret exits
- Twist constraints: rotating room inside safe zone

		## Core Fantasy

		A spin-based arcade where players outmaneuver swarm forces to unlock the peak.

		## Why This Game Is Distinct

		A master of the pier who wields spinning power against chaotic invaders.

		## Player Actions

- spin
- sprint
- pivot

		## Core Loop

- Spin a block to stack it; if a swarm is nearby, dodge or attack first.
- Survive compact but expressive runs filled with glitchy mechanics and pushing hazards.
- Unveil the peak's secrets by managing upgrades as you progress through layers.
- Teach spin movement and introduce glitch reads in a low-risk pier route.
- Layer sprint interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite glitch encounters, and a final unveil choice.

		## Pressure And Opposition

- glitch
- sentinel
- breach
- pier
- peak
- ice

		## Rewards And Progression

- unveil
- unlock
- expand
- upgrade
- pulse
- Each run converts performance into unveil, unlock upgrades and route unlocks.

		## Failure States

- Get overwhelmed by glitch.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- Ice-pier-peak terrain patrolled by relentless swarms and commanding pulses.
- Dynamic lighting, particle explosions, and high-speed camera shakes on spikes.
- pier
- peak
- ice
- harbor

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a pivot burst for repositioning.
- Space converts spin and sprint pressure into crowd control.
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

				- Player promise: The player immediately feels how movement improves the route and unlocks unveil.
				- Sprint objective: Implement the movement slice so the player can reliably feel spin under glitch.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks unlock.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel sprint under sentinel.
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

				- Player promise: The player immediately feels how one route hazard improves the route and unlocks expand.
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel pivot under breach.
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

		- Assessment: yes - Pier Spin: Swarm Break has a readable arcade core built around spin, sprint against glitch, sentinel with a clear payoff in unveil, unlock.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a pivot burst for repositioning.

