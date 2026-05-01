# Patch Spec

		## Per-File Patch Units

		### game.js

				- Problem: No ember resource and hazards do not react to pulses
				- Intended behavior: Ember charge is consumed on pulse; hazards and sentries are stunned or paused when pulsed
				- Specific change: Add ember state to the player, wire pulse to consume ember and affect hazards, and add minimal hazard.reaction state to pause damage for stunSeconds.
				- Invariants: Do not change rendering, camera, or global input handling
				- Patch units:

- Add ember variables and HUD binding
- Modify triggerPulse() to consume ember and affect hazards
- Add hazard.reactToPulse() behavior and stun state
