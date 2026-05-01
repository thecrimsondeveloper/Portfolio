# Validation Loop 02 Edit Plan

- File: game.js
  Reason: Replace the generic pickup loop with patrol routes, vision cones, alert pressure, crash stuns, and hold-to-secure uplinks.
  Exact change: Patch the runtime loop to play as stealth patrol extraction.
  Invariant: Preserve the locked page identity and self-contained page folder.
  Verification command: `node --check game.js`

- File: story-structure.json
  Reason: Drive the repaired stealth loop from canonical scene data.
  Exact change: Add patrol routes, uplink hold timing, hazard alert values, and extraction timing.
  Invariant: Preserve `runtimeTemplate = stealth_patrol` and the canonical identity.
  Verification command: `node -e "JSON.parse(require('fs').readFileSync('story-structure.json','utf8'))"`

- File: index.html
  Reason: Align overlay copy and instructions with patrol evasion and uplink extraction.
  Exact change: Refresh shell-facing wording only.
  Invariant: Keep the page shell and launch path unchanged.
  Verification command: Load the page over HTTP and confirm the overlay and HUD text match the repaired loop.