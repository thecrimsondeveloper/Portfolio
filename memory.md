# Repo Shape
Portfolio is a Vite-first portfolio workspace: `Portfolio-Vite` is the canonical public app, `Portfolio-Vite/Pages` is the stable Kongregate-style Arcade wing, `Portfolio-Vite/cli` owns deterministic generation/orchestration tooling, `legacy/old-root-site` archives the old root site, and root-level docs explain architecture, arcade boundaries, tooling, and small-model edit lanes.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: keep Arcade Builder verbose, keep 30-second local autostart active, and quarantine failed generated folders before they pollute Pages.
- Implemented proof: `.ARCADE-AUTOMATIONS/arcade_automations.py` now emits callback events plus 4-second run heartbeats and supervisor events.
- Verification: observed six PASS runs registered in `arcade-library.json`; failed run `20260502-065710-arcade-builder` was quarantined under `.ARCADE-AUTOMATIONS/failed-builds`.
- Next: monitor the active supervisor for the next failed run and confirm the patched quarantine rule catches it automatically.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: distinguish local build cadence from Codex audit cadence, keep builder reliable, and avoid claiming hourly readiness without checking `targets.json`.
- Current state: local `arcade-builder` supervisor is running, but target interval is `0.5` minutes, not hourly.
- Current audit: Codex app `arcade-automation-audit` is ACTIVE on `gpt-5.5` high with `FREQ=HOURLY;INTERVAL=6`.
- Next: if user wants hourly build cadence, set local target interval to `60`; if user wants hourly improvement audits, update the Codex automation interval from 6 hours to 1 hour.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: give exact runnable commands, set local Arcade Builder to hourly, and preserve the 6-hour Codex improvement cadence.
- Preferred cadence: local builder every 60 minutes so it can create roughly six games before `arcade-automation-audit` improves the system every 6 hours.
- Command shape: replace `arcade-builder` with `--interval-minutes 60`; start supervisor only if no supervisor is already running.
- Next: after command runs, verify `targets.json` shows `intervalMinutes: 60.0` and `status` shows `supervisorRunning: true`.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: answer whether commands had effects from live state, keep hourly cadence clear, and warn when `add-target` resets schedule metadata.
- Verified effect: user's `add-target --interval-minutes 60` changed `targets.json` to `intervalMinutes: 60.0` and supervisor PID `15864` is still running.
- Side effect: replacing the target reset `lastRunAt`, `nextRunAt`, and last status; the active supervisor treated it as due and started run `20260502-103821-arcade-builder`.
- Next: after the current run finishes, confirm `nextRunAt` advances about 60 minutes and avoid re-running `add-target` unless changing cadence or prompt.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: give macOS-safe live monitor commands, show target status plus latest run logs, and avoid relying on unavailable `watch`.
- Preferred monitor: a `while true` terminal loop that prints `status`, `list-targets`, latest run records, and tails the newest arcade-builder log every 5 seconds.
- Current cadence: local builder should stay hourly while `arcade-automation-audit` improves every 6 hours.
- Next: if the monitor is too noisy, add a repo CLI subcommand like `monitor-runs` instead of expanding ad hoc shell snippets.
