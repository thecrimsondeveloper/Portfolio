# Patch Spec

		## Per-File Patch Units

		### story-structure.json

				- Problem: Movement tuning does not yet expose rhythm-step or mirror-walk parameters
				- Intended behavior: Design data defines a step beat window, mirror-walk duration, and dodge cooldown for later runtime use
				- Specific change: Add player movement tuning keys such as beatWindow, mirrorWindow, and dodgeCooldown with starter numeric defaults
				- Invariants: Preserve existing JSON shape and existing player values
				- Patch units:

- Add beatWindow under player movement data
- Add mirrorWindow under player movement data
- Add dodgeCooldown under player movement data

### game.js

				- Problem: Current starter movement likely reads as generic top-down movement instead of rhythm stepping plus mirror walking
				- Intended behavior: Player gains a short movement bonus for on-beat inputs, incurs instability off-beat, and can enter a brief mirrored movement state after a dodge or pulse
				- Specific change: Track step timing timestamps, compute on-beat windows, apply speed modifiers, and expose mirrorWalkActive state that inverts or offsets directional input for a short duration
				- Invariants: Do not rewrite the whole runtime or remove existing input handling
				- Patch units:

- Add movement timing state to player setup
- Update movement handling with beat window check
- Add mirrorWalkActive timer update and HUD-facing values

### index.html

				- Problem: The shell still reads like a generic arena HUD
				- Intended behavior: HUD text reflects the factory run's keys, dawn pressure, and relay progress
				- Specific change: Adjust visible HUD labels or notes to show Keys, Dawn Timer, and Relay progress alongside health
				- Invariants: Keep the existing page scaffold and script hooks intact
				- Patch units:

- Implement Movement
- Validate Movement
