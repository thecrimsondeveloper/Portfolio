# v002 Comparison

## v001 Observed Behavior

- Generated and registered `auto-arcade-20260502-103953`.
- Marked final status `PASS`.
- Allowed arcade registration after a QA report with `Canvas gained pixels: False`.
- Did not run an upgrade loop.
- Let design, story, validation, and runtime describe different game concepts.

## v002 Candidate Behavior

- Runs from a copied builder root at `.ARCADE-AUTOMATIONS/versions/v002/PortfolioBuilder-V2`.
- Uses a separate central automation target, `arcade-builder-v002`, instead of replacing `arcade-builder`.
- Fail QA when Start is clicked but canvas pixels do not grow/change enough to prove post-start gameplay.
- Route zero-growth canvas failures into the upgrade loop.
- Require stage prompts to keep one canonical title, one implemented mechanic inventory, and code-visible mechanics.
- Require target prompts to demand runtime-visible mechanics rather than only design claims.

## Expected Improvement

- Fewer false-positive PASS reports.
- More repair attempts before registration.
- Better alignment between contract, story, design, validation, and `game.js`.
- More pressure toward high-depth generated games with observable mechanics.

## Risk

- Stricter canvas-growth QA may fail games with a fully drawn static board that changes through non-pixel state only.
- Mitigation: allow explicit evidence of changed canvas pixels, changed HUD text, or animation frame counter in future QA if needed, but do not accept a pure no-change canvas as playable proof.

## Side-By-Side Test Policy

- V1 remains `arcade-builder`.
- V2 runs as `arcade-builder-v002`.
- Compare latest V1 and V2 runs by exit code, final report, strict Playwright evidence, canvas growth, doc/runtime coherence, depth gates, and arcade registration.
- Only promote V2 when its latest evidence is better than V1.
- After V2 wins, disable the V1 target rather than deleting it.
- The next improvement loop must copy the promoted V2 builder into `v003` and register a new `arcade-builder-v003` challenger.

## Promotion Decision

- Current latest: `v001`.
- Runnable candidate created: `v002`.
- Promoted: no.
- Reason: V2 has not yet beaten V1 in a fresh side-by-side automation run.
