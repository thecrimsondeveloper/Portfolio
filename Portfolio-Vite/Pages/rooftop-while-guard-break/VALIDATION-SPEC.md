# Validation Spec

## Gate Checks

- Loop: 2
- HTML rewrite gate: no
- JSON rewrite gate: no
- Review assessment: yes - the runtime now behaves like a stealth patrol extraction page instead of a generic relic arena.
- Continue gate: Stop

## Pass Fail Reasons

- The prior runtime still used floating relic pickups and a generic exit loop, so the patrol-grid contract was not actually satisfied.
- The shell and arcade metadata still described the old loop and needed to be brought back in sync with the repaired page.

## Repair Sequence

- Add patrol routes, vision cones, alert buildup and decay, hold-to-secure uplinks, and extraction hold logic in the runtime.
- Drive the repaired stealth loop from story-structure.json instead of hardcoded arena assumptions.
- Re-validate with JS syntax checks, JSON parsing, and a live browser boot under HTTP.
- Refresh validation and arcade integration artifacts to match the repaired runtime.

## Unresolved Issues

- THREE.Clock emits a non-blocking deprecation warning from the CDN Three.js module, but the page boots and plays normally.

## Next Pass Focus

- No additional validation pass is required for this game page.
