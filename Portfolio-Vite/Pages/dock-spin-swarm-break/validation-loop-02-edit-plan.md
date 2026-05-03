
		# Validation Loop 02 Edit Plan

		### game.js

- Reason: This file contains the unresolved gameplay-specific gaps.
- Exact change: Apply the movement tuning, blocker drone behavior, dock surge hazard identity, and route-focused status plus score messaging already identified in prior loops.
- Invariant: Preserve the current scene bootstrap, controls, and restart flow.
- Verification command: Run a browser smoke test and confirm the game now reads as a dock route-breaker with one blocker enemy and one surge hazard.

### story-structure.json

- Reason: Text should follow the repaired runtime, not lead it.
- Exact change: Update only the selected objective, hook, and rules fields needed to match blocked lanes, extraction charge, and surge pressure.
- Invariant: Preserve the existing JSON schema and canonical brainstorm-derived fields.
- Verification command: Parse the JSON and reload the page to confirm the overlay still resolves.

### index.html

- Reason: The shell needs only terminology alignment after runtime repair.
- Exact change: Tighten the visible HUD labels and intro hint so the opening read matches the repaired route-breaker loop.
- Invariant: Preserve the existing HTML structure and responsive shell.
- Verification command: Open the page and confirm the revised hint and labels still fit cleanly.
