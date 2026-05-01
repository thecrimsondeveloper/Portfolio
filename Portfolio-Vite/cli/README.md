# Portfolio Vite CLI

Automation tooling for the Portfolio Vite app and its Arcade wing.

## Run

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli
python3 portfolio_cli.py
```

## ArcadeBuilder

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli
python3 arcade_builder_cli.py --idea orbit --theme neon --mechanic dodge --depth quick --plan-only
```

The packet-driven builder keeps source commands in this folder, tracked step definitions in `state/`, and generated packet/run history in `runs/`.

```text
cli
├── portfolio_cli.py
├── arcade_builder_cli.py
├── mini_arcade_orchestrator_cli.py
├── MiniArcadeControl
├── schemas
├── templates
├── state
│   ├── arcade_steps.json
│   ├── arcade_session.json
│   ├── arcade_run.md
│   └── arcade_auto_report.json
└── runs
    ├── arcade_packets
    └── arcade_run_archive
```

Interactive commands:

```text
status, flags, steps, safe-next, prompt, copilot, reply, reconcile,
decision, complete-step, block-step, finish-run, validate, build, quit
```

## MiniArcadeOrchestrator

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli
python3 mini_arcade_orchestrator_cli.py --idea orbit --theme neon --mechanic dodge --depth quick --validate
```

Strict end-to-end mode:

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli
python3 mini_arcade_orchestrator_cli.py \
  --auto-build \
  --idea campfire \
  --theme cozy \
  --mechanic dodge \
  --content lanterns \
  --depth quick
```

## MiniArcade Control Website

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli/MiniArcadeControl
npm start
```

The control site detects the repo root, queues MiniArcade jobs, stores queue state in `MiniArcadeControl/data/mini_arcade_queue.json`, and streams worker updates through `/api/events`.

Main local endpoints:

```text
GET  /api/status
GET  /api/events
POST /api/queue
POST /api/queue/batch
POST /api/start
POST /api/stop
POST /api/hard-stop
POST /api/retry
POST /api/settings
```

## Boundaries

- The Vite app lives in `../`.
- The public Arcade wing lives in `../Pages`.
- Shared Arcade assets live in `../assets/arcade` and `../Pages/arcade-assets.json`.
- Do not move existing Arcade game folders.
- `state/arcade_steps.json` is tracked.
- Session, report, queue, and run-history files are generated locally; do not mix them with command source.
