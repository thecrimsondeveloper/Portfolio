# Validation Spec

## Gate Checks

- Loop: 1
- HTML rewrite gate: no
- JSON rewrite gate: no
- Review assessment: The scaffold has the right identity and documentation, but the actual playable runtime still needs the planned movement, sentry, and route-hazard mechanics to match the design profile. The build improved at the shell and planning level, but the runtime slice remains incomplete until those focused edits land.
- Continue gate: Stop

## Pass Fail Reasons

- The runtime still risks reading as a generic arena loop because rhythm-step timing and mirror-walk pressure are not yet guaranteed in moment-to-moment movement.
- The factory sentry pressure exists only as a plan unless game.js explicitly supports patrol, alert, and chase state changes.
- The route-building fantasy is incomplete because a concrete collapsing or rotating hazard is still missing from the playable slice.
- The shell now names Keys, Dawn Timer, and Relay progress, but the runtime may not yet update all of those indicators.

## Repair Sequence

- Patch story-structure.json with movement, sentry, and route-hazard tuning values so runtime changes are data-backed.
- Patch game.js in three slices: movement timing, sentry state machine, and a single rotating or locking route hazard tied to the level flow.
- Patch index.html only where needed to expose stable HUD labels for keys, dawn, relay, and alert state.
- Run JSON and JS validation after each focused edit rather than waiting for one large rewrite.

## Unresolved Issues

- Stage 7 copy now expresses the factory stealth run clearly.
- The implementation passes identified the correct narrow slices: movement first, then one sentry archetype.
- Validation still centers on runtime fidelity, not shell polish, because the hazard and live HUD pressure remain under-implemented.

## Next Pass Focus

- Stop after current validation loop.
