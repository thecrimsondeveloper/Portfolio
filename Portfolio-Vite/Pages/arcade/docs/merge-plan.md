# Arcade Merge Plan

## Goal
Consolidate the existing arcade library into a smaller set of six deep, identity-rich games. Clean up the `Pages/` folder so every active library entry has its own paired folder, and move all retired legacy game folders into a single archive area.

## Final retained arcade entries

- `Aurora Run` — kept as the core harbor runner experience (from `harbor-auto-sprint`)
- `Lantern Drift` — kept as the echo/memory rhythm experience (from `glow-drift`)
- `Relay Fusion` — kept as the merged relay/run experience (from `clockwork-courier`)
- `Lab Rift` — kept as the top-down shard collection/escape experience (from `riftbound-saga`)
- `Beacon Breaker` — kept as the harbor beacon collection experience (from `beacon-breaker`)
- `Tide Diver` — kept as the tide pool shard collection experience (from `tide-diver`)

## File structure after merge

- `Pages/arcade/aurora-run/`
- `Pages/arcade/lantern-drift/`
- `Pages/arcade/relay-fusion/`
- `Pages/arcade/lab-rift/`
- `Pages/arcade/beacon-breaker/`
- `Pages/arcade/tide-diver/`
- `Pages/arcade/docs/`
- `Pages/arcade/archive/`

## What changed

- Updated `Pages/arcade-library.json` so only the six retained games are present.
- Moved each retained game folder into `Pages/arcade/`.
- Archived all other legacy game folders into `Pages/arcade/archive/`.
- Documented the merge and archival mapping in `Pages/arcade/docs/`.

## Retained mapping rationale

- `Aurora Run` keeps the strongest harbor courier/runner variant with lane bonuses and stage progression.
- `Lantern Drift` preserves the echo/memory-run identity with clear pattern replay.
- `Relay Fusion` preserves the core relay-runner identity and unifies related courier/relay variants.
- `Lab Rift` preserves the strongest non-lane top-down collect-and-escape concept.
- `Beacon Breaker` preserves the simplest harbor collection game with a strong beacon theme.
- `Tide Diver` preserves the tide-pool shard collection game with spatial currents.

## Notes

- No source files outside of `Pages/` were modified.
- Legacy code and game folders are archived instead of deleted to preserve recovery.
- Any new arcade library entry now has a direct paired folder under `Pages/arcade/`.
