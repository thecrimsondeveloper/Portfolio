# Edit Plan

### game.js

- Reason: This is the only file that can make blockers and hazards mechanically distinct.
- Exact change: Introduce a lead route-blocking enemy behavior, specialize one hazard into a bridge surge field, and revise related status and collision messaging to support the dock-break fantasy.
- Invariant: Preserve the current renderer setup, controls, and overall runtime footprint.
- Verification command: Open the generated page and confirm one enemy sweeps or blocks a route while one hazard clearly reads as a bridge or surge obstacle.

### story-structure.json

- Reason: Runtime-facing text should match the new blocker and hazard behavior.
- Exact change: Revise selected objective, hook, and scene rule text to reference blocked bridge lanes and frozen surge pressure.
- Invariant: Preserve the existing story JSON contract and brainstorm-derived structural fields.
- Verification command: Parse story-structure.json and reload the page to confirm the new text resolves in the overlay and HUD flow.

### index.html

- Reason: The shell should prime the player for blocker and surge counterplay.
- Exact change: Tighten the intro hint or one HUD label so the opening read mentions cracking blocked lanes with spin bursts.
- Invariant: Preserve the current HTML structure and canvas mounting behavior.
- Verification command: Open the page and confirm the new hint is visible and still fits the overlay cleanly.
