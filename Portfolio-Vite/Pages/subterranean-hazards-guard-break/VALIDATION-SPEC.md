# Validation Spec

## Gate Checks

- Loop: 2
- HTML rewrite gate: no
- JSON rewrite gate: no
- Review assessment: The scaffold is sound. Required changes are focused: add ember resource, make hazards respond to pulses, and expose tuning values. These are small, targeted edits that will make the runtime align with the gameDesignProfile.
- Continue gate: Stop

## Pass Fail Reasons

- No ember resource implemented (pulse is always available without cost).
- Hazards deal damage but do not react to pulses or create safe windows.
- HUD lacks Ember Charge and Companion Status indicators.
- Enemy tuning parameters (visionRange, visionAngle, stunSeconds) are not exposed for quick iteration.

## Repair Sequence

- 1) Add ember fields to story-structure.json (player.emberMax, player.emberRechargeRate, player.pulseCost).
- 2) Edit game.js: add player.ember, show ember in HUD, require ember >= pulseCost to trigger pulse and subtract cost.
- 3) Edit game.js: on triggerPulse set hazard.stun timer and ensure updateHazards skips damage while hazard.stun>0.
- 4) Ensure enemy stun behavior remains compatible and is still triggered by pulse.
- 5) Update index.html overlay hint and HUD copy to include Ember Charge and Companion Status.
- 6) Run syntax checks (`node --check`) and boot the page for a smoke test; adjust tuning values as needed.

## Unresolved Issues

- Pulse currently pushes and stuns enemies; we will gate it behind ember cost to create resource management.
- Hazard stun should be short (0.8-1.5s) to create windows without trivializing danger.
- HUD must show Ember Charge numerically and as a gauge for clarity.

## Next Pass Focus

- Stop after current validation loop.
