Reading repository root and searching for arcade schemas, templates, and session artifacts to observe current Arcade runtime state. Running directory view and glob searches (reports intent + file queries).

restated request:
Simulate the full ArcadeBuilder worker chain for flags (Crystal Maze Sprint; Neon crystalloids meets cosmic aurora; runner; electrifying; Momentum racing in shifting procedural corridors; short high-speed runs with timed maze reconfigurations; depth: full) and emit a single structured reply packet describing decisions, schema needs, JSON-ready parameters, validation cues, and next commands.

taught decision frame:
- Prefer existing shared runtimes and shell assets.
- Output must be schema-bound JSON (no new runtime JS).
- No external assets; reuse portfolio assets.
- Treat flags as seeds; preserve user intent (momentum runner, timed maze reconfigs).
- Don’t invent new runtime code; adapt schemas/templates.

per-step decisions:
01-observe-arcade-state: Found Portfolio-CLI/arcade_session.json, arcade_steps.json, many arcade_packets, Portfolio-Vite/Pages/arcade-runtime.js, arcade-assets.json, arcade-shell.css. Use shared web shell.
02-expand-seed-flags: Compose intent: short, momentum-driven sprint through procedural shifting corridors with timed reconfig events and crystal pickups.
03-select-runtime-mode: Shared web greybox "runner" shell (Portfolio-Vite/Pages/arcade-runtime.js) — browser greybox runner.
04-plan-game-loop: Short runs (30–60s). Player builds momentum, passes corridors, collects crystals, avoids collisions. Maze reconfig occurs on timer; momentum retention across reconfigs; fail on crash/timeout.
05-plan-theme-pack: Neon aurora palette, holographic crystals, particle trails, pulse UI. No external assets; reference existing arcade-assets keys.
06-plan-content-contract: Content objects: game_meta, player_config, corridor_template[], event_schedule[], obstacle[], collectible[], scoring_rules, ui_text.
07-plan-schema-fields: Add/require fields: seed, run_length_seconds, reconfig_interval_seconds, corridor_density, momentum_decay, spawn_rules, difficulty_tiers, asset_keys (must map to arcade-assets.json), validation flags.
08-fill-json: Decide canonical defaults and structure (see JSON-ready decisions below).
09-repair-json: Ensure all required schema fields present, use existing asset keys, sanitize strings, numeric ranges, no URLs.
10-build-arcade-entry: Recommend run: reconcile -> validate -> build using Portfolio-CLI scripts (see commands).
11-validate-build: Validate JSON schema, ensure arcade-assets.json contains referenced asset keys, run local shell page preview in dev server.
12-recommend-next: After build, run playtest packet generation and tune reconfig timings/difficulty.

chosen runtime mode:
"web-greybox-runner" — use Portfolio-Vite/Pages/arcade-runtime.js and arcade-shell.css; run in browser shell.

root game intent:
Neon Crystal Maze Sprint — a short, electrifying momentum-runner where procedural corridors reconfigure on a timer; maintain speed and line-of-sight to collect crystals and beat time.

game loop plan:
- Core action: steer + boost to maintain momentum through narrow corridors.
- Scoring: time survived + crystals collected + momentum combo multiplier.
- Fail state: collision with wall/obstacle or run timer expiry without finishing goal.
- Progression: repeated short runs (30–60s). Each run seeds a corridor sequence; reconfig events every N seconds shift layouts; players chase higher scores/shorter completion times.

theme pack:
- Palette: Neon Aurora (primary #7CFFEA, #7F3DFF, #FF3D9E; accents #FFD166, #00FFC2); background: subtle aurora gradient; particle: crystal glints (no external images).
- Mood: fast, kinetic, crystalline, cosmic.
- Labels: "Sprint", "Reconfig", "Momentum", "Crystal Combo".
- Presentation constraints: avoid photographic textures; use procedural gradients and CSS/glsl where supported; reference arcade-assets.json keys only.

content contract (JSON objects):
- game_meta {id, title, mode, theme_key, seed, author, depth}
- player_config {speed_base, speed_max, boost_force, momentum_decay, hitbox_radius}
- run_config {run_length_seconds, reconfig_interval_seconds, difficulty_tier}
- corridor_template[] {id, width, turn_density, obstacle_density, theme_mod}
- event_schedule[] {time_offset_seconds, event_type:"reconfig"|"spawn_wave", params}
- obstacles[] {type, position_seed, behavior}
- collectibles[] {type:"crystal", value, spawn_seed, trail:boolean}
- scoring_rules {base_points, momentum_multiplier, combo_window_sec}
- ui_text {strings keys}
All arrays deterministic from seed + corridor_params.

schema notes:
- Required types: integers for seconds, floats for physics params, strings for keys, arrays for templates.
- New/required fields to support game: seed (string/int), reconfig_interval_seconds (int), momentum_decay (float), corridor_templates (array).
- Asset keys must match entries in Portfolio-Vite/Pages/arcade-assets.json; validator must forbid external URLs.
- Ensure max/min ranges: run_length 15–180, reconfig_interval 3–12, momentum_decay 0.0–1.0.

JSON-ready decisions (defaults to include in packet):
- game_meta: {id:"crystal-maze-sprint", title:"Crystal Maze Sprint", mode:"runner", theme_key:"neon-crystal-aurora", seed: 20260425}
- player_config: {speed_base: 320, speed_max: 960, boost_force: 240, momentum_decay: 0.12, hitbox_radius: 12}
- run_config: {run_length_seconds:45, reconfig_interval_seconds:6, difficulty_tier:"normal"}
- corridor_template[0]: {id:"ct-narrow", width:80, turn_density:0.28, obstacle_density:0.12}
- scoring_rules: {base_points:10, momentum_multiplier:0.06, combo_window_sec:2.0}
- event_schedule: [{time_offset_seconds:6,event_type:"reconfig"},{time_offset_seconds:18,event_type:"reconfig"},{time_offset_seconds:30,event_type:"final_reconfig"}]
- collectibles: crystal {value:50, spawn_rate:0.18, trail:true}
- ui_text: concise keys: {start:"Sprint", reconfig:"Maze Reconfigure!", over:"Run Over"}

validation cues:
- Ensure all required fields present and types match.
- run_length_seconds ∈ [15,180]; reconfig_interval_seconds ∈ [3,12].
- seed integer or canonical string.
- asset_key "neon-crystal-aurora" must exist in Portfolio-Vite/Pages/arcade-assets.json.
- No external URLs; only asset_key references.
- Arrays non-empty and event_schedule times increasing.
- Run arcade_builder_cli.py validate (Portfolio-CLI) after reconcile.

downstream ArcadeBuilder command recommendation:
- Reconcile then validate then build:
  1) python Portfolio-CLI/arcade_builder_cli.py reconcile --packet ./Portfolio-CLI/arcade_packets/<this_packet>.md
  2) python Portfolio-CLI/arcade_builder_cli.py validate --session ./Portfolio-CLI/arcade_session.json
  3) python Portfolio-CLI/arcade_builder_cli.py build --session ./Portfolio-CLI/arcade_session.json
(If CLI uses different flags, run help: python Portfolio-CLI/arcade_builder_cli.py --help)

blockers:
- Need to confirm asset_key "neon-crystal-aurora" exists in Portfolio-Vite/Pages/arcade-assets.json (observed arcade-assets.json present; map must be checked during validate).
- Schema extension: if arcade schema lacks fields listed, reconcile step must extend session schema or include optional fields—validator may reject unknown fields.
- No runtime code changes allowed; ensure runtime interprets new fields (momentum, reconfig events) — if runtime lacks support, behavior will be simulated by shell only (visualization may be limited).
