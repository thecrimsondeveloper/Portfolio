# Tooling

Automation lives under `Portfolio-Vite/cli` and should stay separate from app UI code.

```text
Portfolio-Vite/cli
├── portfolio_cli.py
├── arcade_builder_cli.py
├── mini_arcade_orchestrator_cli.py
├── MiniArcadeControl
├── schemas
├── templates
├── state
└── runs
```

## Commands

Interactive portfolio CLI:

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli
python3 portfolio_cli.py
```

Packet-driven ArcadeBuilder:

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli
python3 arcade_builder_cli.py --idea orbit --theme neon --mechanic dodge --depth quick --plan-only
```

MiniArcade orchestrator:

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli
python3 mini_arcade_orchestrator_cli.py --idea orbit --theme neon --mechanic dodge --depth quick --validate
```

Control website:

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/cli/MiniArcadeControl
npm start
```

## State And Runs

```text
cli/state
├── arcade_steps.json
├── arcade_session.json
├── arcade_run.md
└── arcade_auto_report.json

cli/runs
├── arcade_packets
└── arcade_run_archive
```

`arcade_steps.json` is the tracked builder step definition. The other `state` files and everything under `runs` are generated operational output and are ignored for normal git churn.

## Boundaries

- Do not edit app UI files for CLI-only work.
- Do not commit `.copilot-local`, `.playwright-mcp`, `dist`, `node_modules`, or generated run packets.
- Keep command filenames stable unless wrappers are added at the old paths.
