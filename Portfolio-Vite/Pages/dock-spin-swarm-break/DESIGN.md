
		# DESIGN

		## Dock Spin: Swarm Break

		**Description:** Navigate dock and canyon spaces with spin and relay, solve shock-driven pressure, and turn each run into refine progress.

		**Objective:** Use spin and relay to resolve shock-driven pressure, complete the active objective chain, and turn each run into refine, rhythm progress.

		**Seed Summary:**
		Generated game seed combination:
- Themes: underground ruin exploration
- Genres: chase boss rush
- Environments: underground cavern
- Settings: festival night
- Character motivations: learn a forgotten ritual
- Movement mechanics: cargo balancing, mirror walking
- Core loops: evade patrols while searching
- Progression loops: power up a device
- Completion loops: boss hunt
- Rewards: movement mastery, secret area access
- Antagonists: roving security drones
- Visual styles: dusty pastel
- Audio styles: sparse piano
- Interaction patterns: inventory-lite object use
- Production focus: focus on emergent loops
- Camera modes: split-screen boss-focus
- Arena shapes: spiral climb with safe islands
- Primary verbs: dodge around patrols
- Scoring models: risk multiplier style bonus
- Failure modes: companion lost by patrols
- Enemy behaviors: mirror player spiral pattern
- Objective structures: activate sequence while chased
- Resource systems: battery enemy steal
- Level progression: unlockable shortcuts with route memory
- Twist constraints: no stopping after route split
- Weather effects: chrono-fog variation 28 variation 85 variation 96
- Ui aesthetics: paper sketch variation 33 variation 55
- Movement quirks: low gravity variation 13
- Environmental hazards: crushing walls variation 19
- Power sources: nuclear variation 25
- Lighting styles: dynamic strobes variation 42 variation 52
- Narrative tone: eerie
- Death animations: pixel explosion variation 10 variation 15 variation 69
- Crowd dynamics: gathering cultists variation 17 variation 29 variation 39 variation 40
- Map modifiers: infinite loop variation 27 variation 30
- Soundscapes: industrial clang variation 19 variation 23
- Color palettes: vaporwave pink
- Architecture: gothic revival variation 20
- Artifact types: encoded keys variation 10
- Game tempo: stop-and-go variation 21 variation 28 variation 72
- Boss mechanics: summoning adds variation 10 variation 28
- Player perks: health regen variation 25 variation 75 variation 85
- Enemy archetypes: rust hulks variation 14 variation 32
- Narrative stakes: avenge the mentor variation 13
- Post processing: vignette variation 99

		## Core Fantasy

		Navigate dock and canyon spaces with spin and relay, solve shock-driven pressure, and turn each run into refine progress.

		## Why This Game Is Distinct

		Feel like a fast improviser navigating dock hazards while turning commander pressure into opportunities.

		## Player Actions

- spin
- relay
- twist

		## Core Loop

- Scout routes through dock spaces and identify swarm pressure points.
- Use spin and stack interactions to survive, reposition, and secure objectives.
- Convert each run into expand gains that unlock stronger options and open the next challenge band.
- Teach spin movement and introduce shock reads in a low-risk dock route.
- Layer relay interactions, mixed enemy waves, and injection events from the exploration loops.
- Force mastery through stacked hazards, elite shock encounters, and a final refine choice.

		## Pressure And Opposition

- shock
- storm
- void
- dock
- canyon
- pulse

		## Rewards And Progression

- refine
- rhythm
- expand
- upgrade
- pulse
- unveil

		## Failure States

- Get overwhelmed by shock.
- Run out of time before the completion condition unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- A stylized world blending dock, canyon, and shifting threat territory.
- Lean on dock, canyon, and swarm motifs for strong silhouettes, readable threat zones, and punchy arcade contrast.
- dock
- canyon
- pulse
- harbor

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a twist burst for repositioning.
- Space converts spin and relay pressure into crowd control.
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

				- Player promise: The player immediately feels how movement improves the route and unlocks refine.
				- Sprint objective: Implement the movement slice so the player can reliably feel spin under shock.
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

				- Player promise: The player immediately feels how one enemy archetype improves the route and unlocks rhythm.
				- Sprint objective: Implement the one enemy archetype slice so the player can reliably feel relay under storm.
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
				- Sprint objective: Implement the one route hazard slice so the player can reliably feel twist under void.
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

		- Assessment: yes - Dock Spin: Swarm Break has a readable arcade core built around spin, relay against shock, storm with a clear payoff in refine, rhythm.

		### Things Needed To Make This Game Fun

- fast threat reads
- clear route ownership
- strong reward telegraphing
- WASD or Arrow keys move the player through the arena.
- Shift triggers a twist burst for repositioning.

