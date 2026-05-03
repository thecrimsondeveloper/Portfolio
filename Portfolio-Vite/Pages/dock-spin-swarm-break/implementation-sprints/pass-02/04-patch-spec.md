# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: Enemy and hazard pressure are readable but too generic, so the dock route fantasy is underpowered.
				- Intended behavior: One drone should sweep or hold a lane while one hazard behaves like unstable dock infrastructure that forces pivots and spin timing.
				- Specific change: Give a lead enemy a bridge-blocking movement pattern, give a lead hazard a dock-surge identity with clearer consequence messaging, and connect both to status updates.
				- Invariants: Keep the scene bootstrap, restart flow, and existing input model unchanged.
				- Patch units:

- Select one enemy as the primary lane blocker and tune its pathing or spacing around bridge lanes.
- Reframe one hazard as a dock breaker or frozen surge field with clearer visual and status identity.
- Update collision and status messaging so the player understands when blockers or hazards are shaping the route.

### story-structure.json

				- Problem: The current scene metadata does not name a memorable blocker or dock hazard for the player to read against.
				- Intended behavior: Scene text should prime the player for route blockers, surge pressure, and extraction windows.
				- Specific change: Refresh selected descriptive and rules text to mention bridge lanes, blocker drones, and winter surge hazards.
				- Invariants: Do not alter the JSON schema or discard canonical brainstorm output.
				- Patch units:

- Update hook, objective, and scene rule phrasing toward blockers and bridge pressure.
- Rename one hazard or pressure-facing field to support the specialized enemy pass.

### index.html

				- Problem: The shell still lacks one concise sentence about blockers and bridge hazards.
				- Intended behavior: The player should know before starting that spin bursts are meant to crack blocked lanes and surge zones.
				- Specific change: Tighten the start hint and one visible label to reflect blockers and surge pressure.
				- Invariants: Keep layout, responsiveness, and start behavior unchanged.
				- Patch units:

- Update the visible intro hint with blocker and surge language.
- Retain the existing HUD layout while sharpening terminology.
