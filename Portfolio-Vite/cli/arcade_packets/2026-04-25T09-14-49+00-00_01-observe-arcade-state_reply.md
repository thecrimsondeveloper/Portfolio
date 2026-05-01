restated_request:
- Simulate full internal ArcadeBuilder worker chain and return one structured ArcadeBuilder reply packet for flags {idea: "campfire", theme: "cozy", mode: "runner", tone: "urgent neon pulse", mechanic: "dodge", content: "Compact scope: short lane strips", depth: "quick"} — do not edit files.

taught_decision_frame:
- Prefer existing shared runtimes and assets.
- Keep scope compact and deterministic; seed flags are seeds not complete design.
- Produce schema-bound JSON (no new JS/runtime).
- Use greybox visuals, avoid external assets.
- Preserve user intent: auto-run runner, short lane strips, dodge mechanic, urgent neon pulse flavor over cozy theme.

per-step_decisions:
01-observe-arcade-state:
- Found existing runner motif/palettes (pulse/orbit/signal), runner sprites, runner motif CSS and runtime JS. No new runtime needed.
02-expand-seed-flags:
- Compact auto-run lane runner: "Campfire Dash" — cozy campfire visuals with urgent neon pulse accents; short lane strips, reflex dodge mechanic, 30–60s runs.
03-select-runtime-mode:
- Chosen runtime: "runner" (existing Arcade motif/runner).
04-plan-game-loop:
- Player: auto-forward runner occupying one of 3 lanes; tap to swap lanes (left/right) or hold to slide.
- Core action: dodge obstacles on short lane strips, pick ember pickups to extend score/time.
- Scoring: distance ticks + ember pickups; combos for consecutive pickups without collision.
- Fail state: collision ends run (single life).
- Progression: escalating obstacle spawn rate every 10s; short-run target scores.
05-plan-theme-pack:
- Palette: cozy-warm base + neon pulse accent (use existing "pulse" palette with warmer surface override).
- Mood: cozy campfire warmth + urgent neon pulse accents.
- Labels: Title "Campfire Dash", HUD: TIME, SCORE, COMBO.
- Visual constraints: greybox lane tiles, simple ember pickup, low-poly log obstacles, neon rim glow on obstacles for urgency.
06-plan-content_contract:
- content objects:
  - metadata: id, title, description, runtime="runner", palette
  - layout: lanes_count, lane_width_px, strip_length_tiles
  - player: start_lane, auto_run_speed, lane_switch_cooldown
  - spawn_table: list of obstacle/pickup prototypes with size, hitbox_radius, spawn_chance
  - wave_rules: seed RNG, spawn_rate_base, spawn_rate_increase_per_10s
  - scoring: per_meter, ember_points, combo_multiplier_rules
  - ui: hud_labels, hint_text
  - run: duration_cap_seconds (optional), target_score (optional)
- Runtime uses these to instantiate lanes, spawner, HUD; no new engine code.
07-plan-schema_fields:
- Minimum fields required (prefer existing names):
  - id (string), title (string), runtime (enum: "runner"), palette (string), lanes {count:int, width:int}, player {autoRunSpeed: number, laneSwitchTime: number}, obstacles: [{id,type,size,hitbox,spawnWeight}], pickups: [{id,type,points,durationBonus}], spawnRules {baseRate, escalation: {everySeconds, rateDelta}}, scoring {perMeter, pickupPoints, comboWindow}, fail {collisionEndsRun: bool}, ui {hudLabels}
- Note any gaps: if schema lacks spawn escalation or comboWindow, include them as minimal optional keys (runtime already tolerant).
08-fill-json (JSON-ready decisions):
{
  "id":"campfire-dash",
  "title":"Campfire Dash",
  "runtime":"runner",
  "palette":"pulse",
  "theme":"cozy + urgent neon pulse",
  "metadata":{"author":"automated-packet","depth":"quick"},
  "layout":{"lanes":3,"laneWidth":96,"stripTiles":12},
  "player":{
    "startLane":1,
    "autoRunSpeed":220,
    "laneSwitchTime":160,
    "collisionRadius":20
  },
  "obstacles":[
    {"id":"log","type":"block","size":[60,24],"hitbox":22,"spawnWeight":60,"danger":true},
    {"id":"spark","type":"small","size":[28,28],"hitbox":14,"spawnWeight":30,"danger":true}
  ],
  "pickups":[
    {"id":"ember","type":"score","points":50,"timeBonus":2,"spawnWeight":10}
  ],
  "spawnRules":{
    "baseRatePerSec":0.9,
    "escalation":{"everySeconds":10,"rateDelta":0.18},
    "pattern":"random_lane_weighted"
  },
  "scoring":{
    "perMeter":1,
    "pickupPoints":50,
    "comboWindowMs":1200,
    "comboMultiplierStep":0.2
  },
  "run":{
    "durationCapSeconds":60,
    "targetScore":800
  },
  "fail":{"collisionEndsRun":true,"lives":1},
  "ui":{"hud":["TIME","SCORE","COMBO"],"hint":"Tap to switch lanes — dodge the logs!"}
}
09-repair-json:
- If validation errors flag unknown keys (escalation, comboWindowMs), mark them optional: move under "meta" or tag as "runtimeHints". Minimal repair: ensure unknown keys are placed under "meta" if validator rejects custom keys.

chosen_runtime_mode:
- "runner" (existing page: runner motif in arcade-assets/palettes and arcade-runtime supports lane spawn patterns)

JSON-ready_decisions:
- Provided above; use id "campfire-dash" filename pattern for reply packet.

validation_cues:
- Ensure required fields present: id,title,runtime,layout.player,obstacles/pickups arrays.
- Numeric fields must be numbers (no trailing commas).
- Arrays non-empty for lanes>0.
- If validator rejects spawnRules.pattern string, replace with spawnRules.patternId referencing existing pattern names used by runtime (e.g., "lane-weighted-random").
- If palette "pulse" unavailable, fallback to "signal".

downstream_ArcadeBuilder_command_recommendation:
- Reconcile packet into session and run:
  - python Portfolio-CLI/arcade_builder_cli.py reconcile --packet campfire-dash_reply.md
- Then validate and build:
  - python Portfolio-CLI/arcade_builder_cli.py validate --id campfire-dash
  - python Portfolio-CLI/arcade_builder_cli.py build --id campfire-dash
(If CLI uses different flags, run --help on Portfolio-CLI/arcade_builder_cli.py)

blockers:
- Potential validator rejection of custom keys escalation/comboWindowMs; mitigation: include them under meta or align names to existing schema.
- No bespoke art assets allowed — runtime will greybox with sprites from arcade-assets.json; ensure sprite names match (use generic runnerShip/hazardBlock/padTile).
- Minor: need to confirm exact CLI command flags; run --help if errors.

end.
