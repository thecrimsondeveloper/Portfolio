# Portfolio-CLI

Interactive command-line Arcade builder for the portfolio workspace.

## Run

```bash
cd Portfolio-CLI
python3 portfolio_cli.py
```

## ArcadeBuilder Orchestrator

Run the NexusSpace-style hierarchical ArcadeBuilder CLI:

```bash
cd Portfolio-CLI
python3 arcade_builder_cli.py --idea orbit --theme neon --mechanic dodge --depth quick --plan-only
```

The ArcadeBuilder CLI keeps the existing JSON builder intact and adds a packet-driven master workflow around it. The human provides tiny flags, the CLI writes compositional packets, and `copilot-cli-it` style worker calls use `/opt/homebrew/bin/copilot --model gpt-5-mini` when quota is available. If Copilot is unavailable or quota-blocked, the CLI leaves a pending packet for manual or later continuation.

Copilot calls use a workspace-local config mirror at `.copilot-local/` so session-state writes do not depend on `~/.copilot` being writable.

Persistent workflow files:

- `arcade_session.json`
- `arcade_steps.json`
- `arcade_run.md`
- `arcade_packets/`
- `arcade_run.lock`

Interactive commands:

```text
status, flags, steps, safe-next, prompt, copilot, reply, reconcile,
decision, complete-step, block-step, finish-run, validate, build, quit
```

## MiniArcadeOrchestrator

Run one GPT-5 Mini call that teaches the decision frame, simulates the full ArcadeBuilder step chain internally, then writes the result into the existing ArcadeBuilder `reply -> reconcile -> validate -> build` path:

```bash
cd Portfolio-CLI
python3 mini_arcade_orchestrator_cli.py --idea orbit --theme neon --mechanic dodge --depth quick --validate
```

Use `--plan-only` to create the ArcadeBuilder prompt packet without calling Copilot.

Strict end-to-end mode:

```bash
cd Portfolio-CLI
python3 mini_arcade_orchestrator_cli.py \
  --auto-build \
  --idea campfire \
  --theme cozy \
  --mechanic dodge \
  --content lanterns \
  --depth quick
```

`--auto-build` is non-interactive. It implies a fresh session, validation, build, one Copilot retry, preflight checks, locked GPT-5 Mini prompt context, and a final `arcade_auto_report.json`. It requires explicit `--idea`, `--theme`, `--mechanic`, and `--content`, and it forbids `--brainstorm-seeds` and `--idea-loop` so no idea insertion happens during the build.

Mutable orchestration files:

- `arcade_orchestrator_memory.md`
- `arcade_orchestrator_system_prompt.md`
- `arcade_auto_report.json`

## MiniArcade Control Website

Run the local queue UI for repeated MiniArcade orchestrator jobs:

```bash
cd Portfolio-CLI/MiniArcadeControl
npm start
```

The website detects the Portfolio root automatically, stores queue state in `MiniArcadeControl/data/mini_arcade_queue.json`, runs up to five MiniArcade jobs by default, and streams worker updates through `/api/events`.

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

## What it does

- Holds a staged loop: `idea`, `shape`, `brainstorm`, `expand`, `theme-pack`, `content-plan`, `feature-plan`, `mode-pick`, `json-fill`, `build`, `validate`.
- Also supports a hierarchical ideation path with `hierarchy`:
  - seed 5 ideas
  - expand each into 5 child ideas per layer
  - reduce pairwise and merge-rank down to 5 survivors
  - use the top survivor as the build idea
- Prefers a strict JSON-first Arcade flow instead of generating bespoke HTML game logic.
- Adds shared game-framework UI through the runtime:
  - settings panel
  - help overlay
  - pause menu
  - onboarding steps
- Creates per-mode schemas in `Portfolio-CLI/schemas/`.
- Creates per-mode JSON templates in `Portfolio-CLI/templates/`.
- Writes a schema-bound game JSON file under `Portfolio-Vite/Pages/games/`.
- Writes a thin shell page under `Portfolio-Vite/Pages/`.
- Inserts a matching project card into the portfolio Arcade data.
- Validates generated JSON against the base schema and the selected mode schema.
- Validates shared Arcade JavaScript with `node --check` when `node` is available.
- Runs an optional browser playability check using cached Playwright when available.

## Stages

- `idea`
  - Capture the rough game goal.
- `shape`
  - Expand into options and sections.
- `brainstorm`
  - Generate distinct game directions with different mechanics, vibes, and content use.
- `expand`
  - Expand promising directions into compact design sheets.
- `theme-pack`
  - Generate palette direction, vibe words, presentation style, and space type.
- `content-plan`
  - Decide which content objects the game uses and how they are reused.
- `feature-plan`
  - Decide the gameplay features before JSON is filled.
- `hierarchy`
  - Run layered 5-way expansion and reduction before the normal build path.
  - Optional usage: `hierarchy 3` for 3 layers.
- `mode-pick`
  - Choose the shared Arcade runtime mode.
- `json-fill`
  - Generate valid game JSON only.
- `validate`
  - Check the current JSON against the schemas.
- `build`
  - Write the JSON, write the shell, register the game, and run validation.

## Copilot policy

- Creative stages can stay broader:
  - `idea`
  - `shape`
  - `brainstorm`
  - `expand`
  - `theme-pack`
  - `content-plan`
  - `feature-plan`
  - `mode-pick`
- Schema-bound stages should stay strict:
  - `json-fill`
  - `repair-loop`
- The builder is designed so Copilot fills bounded JSON slots only:
  - no new runtime code
  - no external content
  - no external assets
  - shared greybox visuals only
  - shared settings/help/menu/onboarding data only
