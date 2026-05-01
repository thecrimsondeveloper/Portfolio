# Repo Shape
Portfolio is a Vite-first portfolio workspace: `Portfolio-Vite` is the canonical public app, `Portfolio-Vite/Pages` is the stable Kongregate-style Arcade wing, `Portfolio-Vite/cli` owns deterministic generation/orchestration tooling, `legacy/old-root-site` archives the old root site, and root-level docs explain architecture, arcade boundaries, tooling, and small-model edit lanes.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve the 10-stage Arcade Builder flow, keep LM Studio additive/non-blocking, and make seed growth observable.
- Command rule: omit `--raw` when the user needs proof; the brainstorm seed fetcher prints appended rows, source, endpoint, and model only in normal output.
- Required-mode rule: `--brainstorm-mode required` now fails unless LM Studio returns usable unique rows for every category.
- Next: give users the non-raw required command for proof, and `--raw` only for scripts that need just the output path.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve the 10-stage Arcade Builder flow, keep LM Studio additive/non-blocking, and grow 2D brainstorm rows through the 2B model.
- Latest run: `seed_fetcher_cli.py` appended one row per category in place; original four buckets are now 4 rows and expanded categories are now 101 rows.
- Parser rule: model rows split on whitespace and punctuation; low-quality compact rows fall back to deterministic append rows.
- Next: if row quality still feels too compact, improve seed vocabulary normalization rather than resetting the dataset.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve the 10-stage Arcade Builder flow, keep LM Studio additive/non-blocking, and make brainstorm runs grow the seed dataset.
- Seed fetcher rule: preserve existing 2D rows, append one 2B-generated row per category when augmentation is enabled, and fall back deterministically if LM Studio is down.
- 2D shape rule: the 11 expanded categories stay at 100 rows baseline and can grow on each run; do not collapse them back to 3-row samples.
- Next: when running brainstorm CLI directly, use the default auto mode unless you explicitly want deterministic-only output.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve the 10-stage Arcade Builder flow, keep LM Studio additive/non-blocking, and keep seed dimensions mechanically diverse.
- Current seed rule: the 11 uniqueness categories each have 100 unique sampled options in `arcade-seed.json` and 100 matching source rows in `seed_brainstorming.json`.
- Validation rule: prove seed changes with JSON checks, Python compile, exact option counts, and a dead-LM-Studio non-interactive builder run.
- Next: if games still converge, expand runtime templates or final brainstorm synthesis, not just the seed vocabulary.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve the 10-stage Arcade Builder flow, keep LM Studio additive/non-blocking, and push game uniqueness through seed contracts.
- Seed uniqueness rule: `arcade-seed.json`, `seed_brainstorming.json`, and `seed_fetcher_cli.py` must stay aligned when adding category dimensions.
- Contract rule: generated `final-brainstorming.json > gameDesignProfile.seedContract.seed` must include sampled seed categories, not only source samples.
- Next: when validating seed changes, run JSON checks, Python compile, and a dead-LM-Studio non-interactive builder pass.
