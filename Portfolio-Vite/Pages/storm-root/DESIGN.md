
		# DESIGN

		## Storm Root

		**Description:** A rain-soaked extraction run across a hostile pier where relic chains unlock a storm gate.

		**Objective:** Collect relics, survive the patrols, and open the exit beacon.

		**Seed Summary:**
		Generated game seed combination:
- Themes: hidden society infiltration
- Environments: subterranean library
- Settings: dusk
- Character motivations: learn a forgotten ritual
- Movement mechanics: rhythm-based stepping, slide and vault
- Core loops: collect scattered pieces
- Progression loops: build a safe path
- Completion loops: tower climb to trigger signal
- Rewards: story fragments, artifact sets
- Antagonists: patrolling automatons
- Visual styles: cinematic noir lighting
- Audio styles: dripping water motifs
- Interaction patterns: inventory-lite object use
- Production focus: create a human-readable design spec

		## Core Fantasy

		An expansive arcade game set between subterranean and tree, where the player uses pieces and ember actions to outmaneuver guard forces and drive a evolve-to-unify progression arc.

		## Why This Game Is Distinct

		An evolved guardian using elemental powers to reclaim the earth's depths from relentless threats

		## Player Actions

- pieces
- ember
- crash

		## Core Loop

- Evolve pieces and ember abilities to gain tactical advantages against aggressive enemies
- Use pieces and ember interactions to survive, reposition, and secure objectives.
- Convert each run into evolve gains that unlock stronger options and open the next challenge band.
- Teach pieces movement and introduce guard reads in a low-risk subterranean route.
- Layer ember interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite guard encounters, and a final unify choice.

		## Pressure And Opposition

- guard
- sentry
- fort
- subterranean
- tree
- pier

		## Rewards And Progression

- unify
- evolve
- discover
- expand
- Each run converts performance into unify, evolve upgrades and route unlocks.

		## Failure States

- Get overwhelmed by guard.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- The world blends subterranean, tree, pier into a hostile traversal space patrolled by guard, sentry, fort
- Lean on subterranean, tree, and guard motifs for strong silhouettes, readable threat zones, and punchy arcade contrast.
- subterranean
- tree
- pier
- forest

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a crash burst for repositioning.
- Space converts pieces and ember pressure into crowd control.
- health
- charge meter
- route objective

		## JSON Data Hooks

- scene layout
- enemy waves
- relic rewards
- goal unlock state
- brainstorm final spec
- player controller

		## Sprint Builder Branches
		### Pieces

				- Player promise: Understand and effectively use pieces to gain advantages in gameplay
				- Sprint objective: Establish a solid foundation for piece manipulation and interaction
				- Change packet scope: Focus on 2D piece movement for now, Do not add any piece-specific abilities yet
				- Simulated checkpoints: Basic piece movement functioning, Piece rotation working, Piece queueing system integrated

				#### Detail Fractalization
				- Piece Movement
  - Implement basic piece movement controls
  - Add piece rotation functionality
  - Create piece queueing system

### Ember

				- Player promise: Use ember abilities to enhance piece manipulation and overcome obstacles
				- Sprint objective: Integrate ember abilities and interactions into the gameplay loop
				- Change packet scope: Limit initial abilities to simple enhancements, Do not integrate ember abilities with pieces yet
				- Simulated checkpoints: First ember ability functioning, All basic abilities integrated, Cooldown system working

				#### Detail Fractalization
				- Ember Abilities
  - Design basic ember abilities
  - Integrate abilities into gameplay
  - Add ability cooldowns

### Crash

				- Player promise: Master the crash system to gain advantages and unlock new content
				- Sprint objective: Create a crash system that challenges players and rewards skill
				- Change packet scope: Limit initial crash rewards to basic unlocks, Do not integrate crash system with pieces or ember abilities yet
				- Simulated checkpoints: Crash system functioning, Crash rewards integrated, Players can complete crashes

				#### Detail Fractalization
				- Crash Mechanics
  - Design crash system
  - Integrate crash system into gameplay
  - Add crash-specific rewards

		## Delivery Notes

		- Keep this game self-contained inside its own page folder.
		- Keep the HTML entry point and story JSON in the same folder.
		- Preserve a three.js + Rapier prototype structure.
		- Favor game-specific logic over shared systems.
		- Use branch-specific change packets to plan the next sprint in isolated slices.

## Fun Game Assessment

		- Assessment: The concept of Storm Root sounds exciting and has the potential to be a fun and engaging arcade game. The core fantasy of an expansive game set between subterranean and tree environments, where the player uses pieces and ember actions to outmaneuver guard forces and drive an evolve-to-unify progression arc, is intriguing and unique.

		### Things Needed To Make This Game Fun

- A wide variety of pieces with unique abilities to keep the gameplay fresh and engaging
- Ember abilities that integrate seamlessly into the gameplay loop and offer strategic options
- A crash system that challenges players and rewards skill, creating a sense of accomplishment
- A sense of progression and evolve-to-unify arc that keeps players motivated to continue playing
- Enemy diversity and aggressive AI that provides a sense of challenge and requires players to strategize and adapt

