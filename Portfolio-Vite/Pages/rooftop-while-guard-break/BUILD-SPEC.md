# Build Spec

## Implementation Chapters

- Movement
- One Enemy Archetype
- One Route Hazard
- Reward Loop
- Full Run Pacing
- Sprint Controls

## Targeted Files

### game.js

- Action: update
- Reason: Replace the generic relic arena loop with a patrol-grid stealth extraction loop.
- Unchanged: Unrelated systems remain unchanged.

### story-structure.json

- Action: update
- Reason: Provide patrol routes, vision tuning, uplink timing, and alert rules from canonical scene data.
- Unchanged: Unrelated systems remain unchanged.

### index.html

- Action: update
- Reason: Align shell copy and player instructions with the repaired stealth runtime.
- Unchanged: Unrelated systems remain unchanged.

## Patch Specs

### game.js

				- Problem: The page still played like a floating relic pickup arena even though the design contract required stealth patrol.
				- Intended behavior: game.js should enforce patrol ownership, vision pressure, stealth uploads, and extraction hold behavior.
				- Specific change: Add patrol routes, vision cones, alert gain and decay, crash stuns, pulse blackout, hold-to-secure uplinks, and extraction hold logic.
				- Invariants: Keep the page self-contained, preserve the locked page identity, and avoid unrelated arcade UI changes.
				- Patch units:

- Inspect game.js
- Replace the generic pickup loop with patrol-grid stealth systems
- Validate runtime syntax and boot behavior

### story-structure.json

				- Problem: story-structure.json did not carry the patrol, uplink, and alert data the repaired loop needed.
				- Intended behavior: story-structure.json should drive patrol routes, uplink hold windows, hazard alert pressure, and extraction timing.
				- Specific change: Update enemy, relic, hazard, and rules payloads for the stealth patrol pass.
				- Invariants: Preserve the canonical identity and runtime template.
				- Patch units:

- Inspect story-structure.json
- Patch patrol-grid scene data

### index.html

				- Problem: index.html still described a generic arena pickup loop.
				- Intended behavior: index.html should explain patrol evasion, uplink holds, and extraction without changing the game identity.
				- Specific change: Refresh overlay copy and instructions.
				- Invariants: Preserve the page shell structure and launch path.
				- Patch units:

- Inspect index.html
- Patch overlay copy and instructions

## Implementation Sequence


- Sprint goal: Repair the generated runtime until Rooftop While: Guard Break actually feels like a stealth patrol page.
		- Pass goal: Replace the generic relic arena loop with a patrol-grid uplink extraction run.
		- Active feature: Movement
		- Plan steps:

- Add patrol-grid scene data and runtime behavior.
- Refresh shell copy to explain the repaired loop.
- Validate syntax, JSON, and live browser boot.

		- Simulated checkpoints:

- game.js compiles cleanly.
- story-structure.json parses cleanly.
- The page boots over HTTP and starts a run without runtime errors.

		- Implementation actions:

- Patched game.js, story-structure.json, and index.html for the stealth patrol repair.
- Validated with node --check, JSON parsing, and a live browser interaction pass.

		- Implementation notes:
		Pass 02 repaired the root-cause runtime mismatch instead of widening scope into a broader refactor.
