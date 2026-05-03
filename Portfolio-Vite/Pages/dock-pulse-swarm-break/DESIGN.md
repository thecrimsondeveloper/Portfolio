
		# DESIGN

		## Dock Pulse: Swarm Break

		**Description:** An expansive arcade game set between dock and canyon, where the player uses pulse and spike actions to outmaneuver swarm forces and drive an expand-to-upgrade progression arc.

		**Objective:** Use pulse and spike to survive swarm patrols, secure relic routes, and turn each run into expand, upgrade progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: urban parkour delivery
- Genres: survival arena
- Environments: rooftop maintenance rails
- Settings: midsummer heat
- Character motivations: protect the neighborhood
- Movement mechanics: mirror walking, momentum-based rolling
- Core loops: trace signal patterns
- Progression loops: gain movement upgrades
- Completion loops: boss hunt
- Rewards: resource caches, boss unlock
- Antagonists: ancient guardian
- Visual styles: hand-painted textures
- Audio styles: ambient hum
- Interaction patterns: environmental interaction first
- Production focus: prototype in directory with JSON and HTML only
- Camera modes: cinematic follow wide-read
- Arena shapes: patrol grid with bridges
- Primary verbs: repair around patrols
- Scoring models: delivery value no-hit bonus
- Failure modes: resource depleted while carrying
- Enemy behaviors: summon hazards slow pattern
- Objective structures: repair network with limited resource
- Resource systems: noise risk overflow
- Level progression: escalating waves with checkpoints
- Twist constraints: decaying floor for finale

		## Core Fantasy

		An expansive arcade game set between dock and canyon, where the player uses pulse and spike actions to outmaneuver swarm forces and drive an expand-to-upgrade progression arc.

		## Why This Game Is Distinct

		A strategist navigating a hostile environment with dual-action skills in compact but expressive runs.

		## Player Actions

- pulse
- spike
- dash

		## Core Loop

- Player uses pulse to stun enemies or spikes to disrupt formations while avoiding swarm hordes through compact runs.
- Progression unlocks new pulse abilities and spike variants that alter the tactical approach and expand gameplay depth over time.
- Convert each run into expand gains that unlock stronger options and open the next challenge band.
- Teach pulse movement and introduce swarm reads in a low-risk dock route.
- Layer spike interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite swarm encounters, and a final expand choice.

		## Pressure And Opposition

- swarm
- commander
- pulse
- dock
- canyon
- ember

		## Rewards And Progression

- expand
- upgrade
- pulse
- ascend
- Each run converts performance into expand, upgrade upgrades and route unlocks.

		## Failure States

- Get overwhelmed by swarm.
- Run out of time before the exit unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- Dock meets canyon under attack by swarms of pulse units.
- Dynamic traversal featuring dark industrial dock tones contrasted against stark canyon landscapes, enhanced by colorful pulse effects and sharp spike animations.
- dock
- canyon
- pulse
- ember

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a dash burst for repositioning.
- Space converts pulse and spike pressure into crowd control.
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
				- Sprint objective: Implement the movement slice so the player can reliably feel pulse under swarm.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks upgrade.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel spike under commander.
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

				- Player promise: The player immediately feels how one route hazard improves the route and unlocks pulse.
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel dash under pulse.
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

		- Assessment: yes - Dock Pulse: Swarm Break has a readable arcade core built around pulse, spike against swarm, commander with a clear payoff in expand, upgrade.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a dash burst for repositioning.

