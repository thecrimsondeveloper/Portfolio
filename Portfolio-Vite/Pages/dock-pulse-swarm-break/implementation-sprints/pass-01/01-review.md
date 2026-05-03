# Sprint Review

		## Thoughts

		The current scaffold already renders and handles movement, but its runtime still says collect relics and unlock the exit. The safest first pass is to keep the existing three.js structure and replace relic-goal logic with relay nodes, noise buildup, and route-status HUD text.

		## Target Changes


- Replace relic collection framing with relay repair checkpoints and delivery-route language.
- Add a pulse charge or noise mechanic that changes routing pressure during movement.
- Retheme HUD and objective text around relay count, route stability, and courier pressure.

		## Risks


- A broad rewrite of the main loop could break the currently working render and input path.
- If enemy behavior changes in the same pass, the movement slice may become harder to validate.
- Overlay copy can drift away from live mechanics if HUD strings are not updated together with the runtime state.

		## Acceptance Signals


- The player starts a run whose first objective is to repair relay nodes rather than collect relics.
- Pulse use and movement visibly affect route pressure through a noise or stability meter within the first minute.
- HUD text, objective text, and overlay copy all describe the same relay-repair fantasy.

		## Target Files Or Surfaces


- Keep the existing three.js scene, input manager, and render loop.
- Change only the mechanics and copy needed for the first distinct playable slice.
- Defer deeper commander behavior and finale collapse logic to later passes.
