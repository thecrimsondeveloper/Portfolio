# Sprint Review

		## Thoughts

		Movement is the primary feel; keep edits minimal and scoped to game.js, story-structure.json, and index.html. Expose ember tuning and ensure triggerPulse respects ember.

		## Target Changes


- Expose player.emberMax and player.pulseCost in story-structure.json
- Gate triggerPulse() behind ember and consume ember when pulsed
- Add Ember Charge display to HUD in index.html

		## Risks


- Introducing syntax errors in game.js
- Changing HUD may require CSS tweaks

		## Acceptance Signals


- game.js passes `node --check`
- HUD shows Ember Charge label and updates
- Pulse cannot be triggered when ember < pulseCost

		## Target Files Or Surfaces


- game.js
- story-structure.json
- index.html
