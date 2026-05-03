
		# DESIGN

		## Ember Shift: Void Relay

		**Description:** A high-stakes survival game in a collapsing nebula. Shift between dimensions to bypass unstable matter.

		**Objective:** Relay the core data to the extraction point before the nebula collapses.

		**Seed Summary:**
		Generated game seed combination:
- Themes: ritual archaeology
- Genres: escape arcade
- Environments: subterranean library
- Settings: high tide
- Character motivations: learn a forgotten ritual
- Movement mechanics: rhythm-based stepping, grapple and zipline
- Core loops: guide a companion through hazards
- Progression loops: assemble a map
- Completion loops: boss hunt
- Rewards: collectibles, resource caches
- Antagonists: rival explorer
- Visual styles: cinematic noir lighting
- Audio styles: sparse piano
- Interaction patterns: environmental interaction first
- Production focus: focus on emergent loops
- Camera modes: node-map lane-shift
- Arena shapes: lanes with safe islands
- Primary verbs: trade around patrols
- Scoring models: stealth rating resource bonus
- Failure modes: crushed by hazards
- Enemy behaviors: summon hazards combo-triggered
- Objective structures: repair network in split routes
- Resource systems: oxygen combo refill
- Level progression: single run with hard gates
- Twist constraints: reversed controls zone after route split
- Weather effects: gravity waves variation 11 variation 59
- Ui aesthetics: minimalist vector variation 19 variation 36 variation 63
- Movement quirks: teleport dashes variation 14 variation 43 variation 58
- Environmental hazards: crushing walls variation 19 variation 26 variation 41
- Power sources: battery cells variation 76
- Lighting styles: low-key variation 10 variation 24 variation 71
- Narrative tone: existential variation 19 variation 42
- Death animations: shattering glass variation 27 variation 72
- Crowd dynamics: curious wildlife variation 35 variation 45
- Map modifiers: infinite loop variation 12 variation 18 variation 23 variation 49 variation 50 variation 86
- Soundscapes: mechanical heartbeat variation 64 variation 83
- Color palettes: emerald toxic variation 15 variation 26 variation 92
- Architecture: modular space station variation 63 variation 84
- Artifact types: bio-samples variation 89 variation 92
- Game tempo: burst-driven variation 10 variation 31 variation 32
- Boss mechanics: phased transformation variation 18 variation 24 variation 47
- Player perks: invisibility cloak variation 13 variation 26 variation 50
- Enemy archetypes: tankers variation 23 variation 36
- Narrative stakes: prevent the collapse
- Post processing: depth of field variation 12 variation 26 variation 33

		## Core Fantasy

		Ember Shift: Void Relay turns the current seed into a readable arcade challenge.

		## Why This Game Is Distinct

		Ember Shift: Void Relay uses root, petal, sprint inside storm-lit arena lanes, high-contrast enemy silhouettes, rainy neon reflections.

		## Player Actions

- root
- petal
- sprint

		## Core Loop

- Enter the route and read the first threat.
- Use the core verb set to resolve the active pressure.
- Convert the current room into progression gain.
- Trigger the completion condition and finish the playfield.

		## Pressure And Opposition

- enemy pressure
- route hazards
- time pressure

		## Rewards And Progression

- Relay the core data to the extraction point before the nebula collapses.
- route unlocks
- new ability gains

		## Failure States

- Get overwhelmed by enemy pressure.
- Run out of time before the completion condition unlocks.
- Lose health by lingering in active hazard lanes.

		## Visual Identity

- storm-lit arena lanes
- high-contrast enemy silhouettes
- rainy neon reflections
- goal-first readability

		## Controls And Readability

- WASD or Arrow keys move the player through the arena.
- Shift triggers a sprint burst for repositioning.
- Space converts root and petal pressure into crowd control.
- Press Enter to deploy. Use WASD or Arrow keys to move, Shift to dash, and Space to pulse.

		## JSON Data Hooks

- scene layout
- enemy waves
- objective rewards
- goal unlock state
- brainstorm final spec

		## Sprint Builder Branches
		### Root

				- Player promise: The player immediately feels how root improves the route and unlocks Relay the core data to the extraction point before the nebula collapses..
				- Sprint objective: Implement the root slice so the player can reliably feel root under enemy pressure.
				- Change packet scope: game.js, story-structure.json, index.html
				- Simulated checkpoints: Root is driven by canonical brainstorm data rather than ad hoc prompt output., Root is visible in live play within the first minute of a run.

				#### Detail Fractalization
				- Root core slice
  - Implement the root behavior in the main loop.
  - Wire root data into story-structure.json and runtime state.
- Root feedback pass
  - Expose clear HUD and overlay feedback for root.
  - Validate that root stays readable during pressure spikes.

### Petal

				- Player promise: The player immediately feels how petal improves the route and unlocks route unlocks.
				- Sprint objective: Implement the petal slice so the player can reliably feel petal under route hazards.
				- Change packet scope: game.js, story-structure.json, index.html
				- Simulated checkpoints: Petal is driven by canonical brainstorm data rather than ad hoc prompt output., Petal is visible in live play within the first minute of a run.

				#### Detail Fractalization
				- Petal core slice
  - Implement the petal behavior in the main loop.
  - Wire petal data into story-structure.json and runtime state.
- Petal feedback pass
  - Expose clear HUD and overlay feedback for petal.
  - Validate that petal stays readable during pressure spikes.

### Sprint

				- Player promise: The player immediately feels how sprint improves the route and unlocks new ability gains.
				- Sprint objective: Implement the sprint slice so the player can reliably feel sprint under time pressure.
				- Change packet scope: game.js, story-structure.json, index.html
				- Simulated checkpoints: Sprint is driven by canonical brainstorm data rather than ad hoc prompt output., Sprint is visible in live play within the first minute of a run.

				#### Detail Fractalization
				- Sprint core slice
  - Implement the sprint behavior in the main loop.
  - Wire sprint data into story-structure.json and runtime state.
- Sprint feedback pass
  - Expose clear HUD and overlay feedback for sprint.
  - Validate that sprint stays readable during pressure spikes.

		## Delivery Notes

		- Keep this game self-contained inside its own page folder.
		- Keep the HTML entry point and story JSON in the same folder.
		- Preserve a three.js + Rapier prototype structure.
		- Favor game-specific logic over shared systems.
		- Use branch-specific change packets to plan the next sprint in isolated slices.

## Fun Game Assessment

		- Assessment: yes - Ember Shift: Void Relay has a readable arcade core built around root, petal against enemy pressure, route hazards with a clear payoff in Relay the core data to the extraction point before the nebula collapses., route unlocks.

		### Things Needed To Make This Game Fun

- WASD or Arrow keys move the player through the arena.
- Shift triggers a sprint burst for repositioning.
- enemy pressure
- route hazards
- Relay the core data to the extraction point before the nebula collapses.

