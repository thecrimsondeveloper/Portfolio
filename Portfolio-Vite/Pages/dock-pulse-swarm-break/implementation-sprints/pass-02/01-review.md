# Sprint Review

		## Thoughts

		After the movement pass, the next highest-value change is one enemy archetype that supports the relay fantasy. A commander that projects lane-control pressure is more distinct than adding generic faster swarms, and it can still be built inside the current scene and update loop.

		## Target Changes


- Introduce a commander unit that patrols near relay lanes and creates avoid zones.
- Make pulse bursts briefly interrupt the commander so repairing under pressure is possible.
- Expose commander warnings and lane-lock status through concise HUD or status messaging.

		## Risks


- If the commander is too durable or too fast, the relay loop becomes frustrating before route clarity exists.
- Adding multiple enemy roles in one pass would muddy validation of the commander slice.
- Status copy can become noisy if warnings are not kept brief and state-based.

		## Acceptance Signals


- At least one commander behavior is visible within the first minute of play.
- The commander changes routing decisions by threatening relay lanes or bridge crossings.
- A pulse action can interrupt or soften commander pressure long enough to finish a repair window.

		## Target Files Or Surfaces


- Modify only the existing enemy set and related UI messaging.
- Preserve the main scene boot path and player control model.
- Do not attempt full boss-finale logic in this pass.
