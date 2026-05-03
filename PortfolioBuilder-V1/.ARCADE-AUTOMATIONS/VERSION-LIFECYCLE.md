# Arcade Builder Version Lifecycle

## Current State

- Active baseline: `arcade-builder` (`v001`)
- Active challenger: `arcade-builder-v002` (`v002`)
- Latest promoted version: `v001`
- Current mode: side-by-side version race

## Rule

Keep the active baseline and newest challenger running together until the challenger is proven better.

## Promotion Gate

Promote the challenger only when its latest comparable run beats the baseline on all required evidence:

- command exit code passes
- final report is `PASS` or `PASS_AFTER_UPGRADE`
- JSON files parse
- `node --check game.js` passes
- strict Playwright proof passes
- Start/Play/Begin interaction is valid
- canvas or HUD visibly changes after Start/Play/Begin
- external `game.js` is loaded unless intentionally inline
- DOM ids `gameCanvas` and `startButton` are coherent
- no initial game-over/restart state
- arcade registration passes
- depth gates pass
- documents and runtime describe the same game

## Decommission Rule

When a challenger is promoted:

1. Update `.ARCADE-AUTOMATIONS/latest.json` to the winning version.
2. Disable the older baseline target in `.ARCADE-AUTOMATIONS/targets.json`.
3. Mark the older target with `lifecycleRole: "decommissioned-baseline"` and `decommissionedBy`.
4. Keep old run records, logs, and version folders as evidence.
5. Do not delete previous versions.

## Next-Version Rule

On the next automation audit after promotion:

1. Copy the promoted builder project into the next incremented folder, for example `versions/v003/PortfolioBuilder-V3`.
2. Apply controlled improvements only inside that new copy.
3. Register a new challenger target, for example `arcade-builder-v003`.
4. Run the promoted baseline and new challenger side by side.
5. Repeat the same promotion gate.

## Current Next Step

Let `arcade-builder` and `arcade-builder-v002` run, then compare their newest outputs before any promotion or decommission action.
