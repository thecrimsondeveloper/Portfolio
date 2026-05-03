# v002 Plan

## Run Under Audit

- Run id: `20260502-103953-arcade-builder`
- Target status: `PASS`
- Exit code: `0`
- Generated folder: `/Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages/auto-arcade-20260502-103953`
- Builder run JSON: `/Users/crimsonwheeler/Documents/GitHub/Portfolio/PortfolioBuilder-V1/.ARCADE-SYSTEM/sessions/runs/run-1777718393.json`
- Log path: `/Users/crimsonwheeler/Documents/GitHub/Portfolio/PortfolioBuilder-V1/.ARCADE-AUTOMATIONS/logs/arcade-builder/20260502-103953-arcade-builder.log`
- Latest approved version before audit: `v001`

## Strongest Evidence

- `PLAYWRIGHT-QA.md` reports `Status: PASS`, but also reports `Canvas delta nonblack pixels: 0` and `Canvas gained pixels: False`.
- `FINAL-REPORT.md` reports `Final status: PASS` at QA pass `0`.
- `ARCADE-INTEGRATION-SPEC.md` reports arcade registration checks as `PASS`.
- `node --check game.js` passes.
- `DESIGN.md` describes `Tidebreak: Vortex Drift`, `VALIDATION.md` describes `Bloom Blast: Petal Panic`, while the registered game is `Neon Strata: Resonance Runner`.
- `UPGRADE-LOOP.md` is missing, so no repair loop ran before registration.

## Judgment

- Technical result: `FAIL` under the strict automation gates because canvas growth was false even though the local QA accepted it.
- Depth result: `FAIL` because the shipped game is a basic falling-obstacle dodge loop with score, level, and two powerups, while the contract promises phase shifting, resonance fields, pulse relays, and cascade events.

## Failure Reasons

- QA gate accepts a canvas that was already nonblank before start and does not prove post-start animation growth.
- QA target selection only repairs blank canvas, not zero-growth canvas.
- Design and validation stages are not anchored to the actual generated code, so mismatched concepts can pass title normalization.
- The goal prompt asks for depth, but the chassis does not require a playable mechanic inventory or code-level implementation proof for those mechanics.

## Files That Would Need Change

- `.ARCADE-CLI/engines/playwright-qa.py`: fail when a valid start click does not produce canvas growth, and include that reason in failure output.
- `.ARCADE-CLI/builder-agent.py`: send zero-growth QA failures into the upgrade loop and target `game.js`, `index.html`, and `style.css`.
- `.ARCADE-CLI/builder-orchestrator.py`: strengthen stage prompts so design, story, validation, and game code stay anchored to one canonical title and implemented mechanic checklist.
- `.ARCADE-AUTOMATIONS/targets.json`: future target prompt should require implemented, observable mechanics, not only stated mechanics.

## Why v002 Should Improve Next Runs

- It turns the current false-positive PASS into a repairable FAIL before arcade registration.
- It forces future outputs to prove motion/change after Start, aligning with current Canvas guidance that interactive animation should redraw frames through `requestAnimationFrame`.
- It makes depth auditable by requiring named mechanics to appear in both documents and runtime code.
- It preserves prior versions and does not mutate the active builder until a candidate is tested.

## Runnable V2 Flow

- Copied builder root: `/Users/crimsonwheeler/Documents/GitHub/Portfolio/PortfolioBuilder-V1/.ARCADE-AUTOMATIONS/versions/v002/PortfolioBuilder-V2`
- Copied runtime folders: `.ARCADE-CLI`, `.ARCADE-SYSTEM`, `.ARCADE-TOOLS`
- Copied local runtime files: `.env`, `memory.md`
- Central automation target: `arcade-builder-v002`
- V2 slug prefix: `auto-arcade-v002-{timestamp}`

## Candidate Artifacts

- `AUDIT.md`
- `COMPARISON.md`
- `proposed-targets.json`
- `proposed-playwright-qa.patch`
- `proposed-builder-agent.patch`
- `proposed-builder-orchestrator.patch`

## Promotion Gate

Do not update `.ARCADE-AUTOMATIONS/latest.json` until the separate `arcade-builder-v002` target produces a technically valid, high-depth game that beats V1 on the same evidence gates.

When V2 wins, decommission V1 by disabling `arcade-builder`, mark `arcade-builder-v002` as the active baseline, promote `latest.json` to `v002`, and make the next audit create `v003` from the promoted V2 copy.
