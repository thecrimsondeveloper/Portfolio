# Validation Spec

## Gate Checks

- Loop: 1
- HTML rewrite gate: no
- JSON rewrite gate: no
- Review assessment: Scaffold is close to playable but missing resource gating and enemy reaction ties. Applying the editPlan will align runtime with the design intent.
- Continue gate: Stop

## Pass Fail Reasons

- Pulse is not gated by Ember, allowing resource-free spamming
- Enemies lack stun handling and therefore do not react properly to pulses
- HUD is missing an Ember Charge display for player feedback

## Repair Sequence

- Update story-structure.json to add player.emberMax and player.pulseCost and enemy tuning (visionRange, visionAngle, stunSeconds)
- Patch game.js to initialize this.player.ember, check/consume pulseCost in triggerPulse, and add stunTimer logic in updateEnemies
- Add Ember Charge display markup to index.html HUD cluster

## Unresolved Issues

- Movement scaffold exists and feels coherent
- Enemies need stun handling to reward pulse use
- HUD should show Ember so players understand resource state

## Next Pass Focus

- Stop after current validation loop.
