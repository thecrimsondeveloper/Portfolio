restated request:
- Produce a full ArcadeBuilder reply packet for "Neon Orbital Courier" (flags provided). Simulate internal ArcadeBuilder worker chain and return a single structured artifact containing per-step decisions, chosen runtime, game intent, loop plan, theme, content contract, schema notes, JSON-ready game object, validation cues, recommended next CLI commands, and blockers.

taught decision frame (condensed):
- Prefer existing shared runtimes/assets; do not add runtime code or external assets.
- Treat short flags as seeds; preserve user intent (urgent neon cyberpunk astro-minimal courier runner).
- Keep game output as schema-bound JSON; minimal schema extensions only if unavoidable.
- Use greybox presentation and shared arcade assets; map new mechanics to parameterized behavior when possible.

per-step decisions:
01-observe-arcade-state
- Assume repo has shared runtime "shared-runner-v1", common palettes, and shared asset keys (icons/sfx). No file edits performed.

02-expand-seed-flags
- seed -> intent: short, urgent high-score courier runs; player dashes through timed windows while orbiting a central body; runs are quick (≈30s) with score for deliveries and distance.

03-select-runtime-mode
- chosen runtime mode: shared-runner-v1 (existing runner mode). Rationale: matches runner flag and shared runtime requirement.

04-plan-game-loop
- Core action: steer courier-on-orbit, perform timed dash windows to hop between orbital lanes and deliver packets.
- Scoring: distance points + delivery bonus + time-multiplier for quick runs; combo for consecutive window hits.
- Fail states: time expired (primary), fatal collision with hazard (secondary).
- Progression: single-run high-score; runs increase obstacle density and shorten dash windows over time.

05-plan-theme-pack
- Palette: neon cyan, magenta, ink black, astro-silver
- Mood: urgent, pulsing; UI minimal: timer prominent, orbital arc HUD, neon glows.
- Labels: title "Neon Orbital Courier"; HUD labels: TIMER, COMBO, SCORE, DELIVER.
- Presentation constraints: no external assets; use shared icons/sfx; mono-weight minimal ship silhouette, neon trail.

06-plan-content-contract
- Reusable objects:
  - run: {seed, duration_ms, difficulty_seed}
  - entity: {type, behavior, radius, damage, spawn_rule}
  - window: {orbit_angle, open_ms, period_ms, reward_multiplier}
  - delivery_point: {orbit_angle, tolerance_deg, bonus}
  - scoring: {distance_per_px, delivery_bonus, combo_multiplier}
- JSON expresses arrays of windows, entity spawn schedule (procedural rules via seeds), and parameters for player dash/orbit.

07-plan-schema-fields
- Use existing fields: id, title, mode, runtime, theme, palette, loop, entities, assets, ui.
- New/validated parameter fields (if absent): movement.behavior = "orbit" (parameterized) and loop.dash_window_ms, dash_cooldown_ms, orbital_radius_px. If runtime lacks explicit "orbit" enum, map to movement.path="circular" + orbit_anchor parameters.

08-fill-json (schema-bound game JSON)
{
  "id": "neon-orbital-courier",
  "title": "Neon Orbital Courier",
  "mode": "runner",
  "runtime": "shared-runner-v1",
  "theme": "neon-cyberpunk-astro-minimal",
  "tone": "urgent",
  "seed_flags": {
    "mechanic": "timed_dash_windows_with_orbit",
    "content": "short_high_score_courier_runs",
    "depth": "full"
  },
  "presentation": {
    "palette": {
      "bg": "#0b0b10",
      "neon_cyan": "#0ff0ff",
      "neon_magenta": "#ff00d6",
      "astro_silver": "#bfc7d6",
      "accent": "#ffd166"
    },
    "ui": {
      "hud": ["timer","score","combo","orbital_indicator"],
      "font": "shared/minimal-sans",
      "logo": "shared/icon-courier"
    }
  },
  "player": {
    "radius_px": 12,
    "movement": {
      "type": "orbit",              /* maps to engine circular path */
      "orbital_anchor": "center",
      "orbital_radius_px": 180,
      "base_angular_speed_deg_per_s": 120
    },
    "dash": {
      "dash_window_ms": 400,
      "dash_duration_ms": 120,
      "dash_cooldown_ms": 900,
      "dash_speed_mult": 2.6
    },
    "health": 1
  },
  "loop": {
    "run_duration_ms": 30000,
    "spawn_seed": 12345,
    "difficulty_curve": "linear",
    "scoring": {
      "distance_per_px": 0.02,
      "delivery_bonus": 750,
      "window_hit_bonus": 150,
      "combo_increment": 0.5,
      "time_remaining_multiplier_per_s": 1.5
    },
    "fail_conditions": ["time_expired","collision"],
    "progression": {
      "increase_spawn_rate_per_10s": 0.12,
      "shrink_dash_window_ms_per_10s": 20
    }
  },
  "content": {
    "windows": [
      {"orbit_angle_deg": 20, "open_ms": 400, "period_ms": 1200, "reward_mult": 1.0},
      {"orbit_angle_deg": 160, "open_ms": 400, "period_ms": 1300, "reward_mult": 1.1}
    ],
    "delivery_points": [
      {"orbit_angle_deg": 90, "tolerance_deg": 18, "bonus": 750}
    ],
    "entities": [
      {"type": "hazard", "behavior": "radial_spike", "radius_px": 14, "spawn_rule": {"every_ms": 1200, "offset_seed": 7}},
      {"type": "drone", "behavior": "patrol_orbit", "radius_px": 10, "spawn_rule": {"every_ms": 2200}}
    ]
  },
  "assets": {
    "use_shared": true,
    "icons": ["shared/ship-minimal","shared/icon-window"],
    "sfx": ["shared/tick","shared/dash","shared/hit","shared/ding"]
  },
  "schema_version": "arcade-game-v1"
}

09-repair-json
- Ensured numeric durations are integers (ms), palette hex strings valid, arrays non-empty.
- Mapped "orbit" movement to engine-compatible "movement.type":"orbit" with fallback note in schema_notes.
- No external asset paths used; assets reference shared keys.

10-build-arcade-entry (decision, not executed)
- Output will be stored as reply packet arcade_packets/neon-orbital-courier_reply.md by reply endpoint.
- Reconcile will merge this into arcade_session.json and arcade_run.md.
- Build step will render JSON to final game/portfolio page using existing builder.

11-validate-build (requirements)
- Validate JSON schema: required fields present (id,title,mode,runtime,player,loop,content,presentation,assets).
- Types: strings, ints, arrays matched.
- Runtime compatibility: ensure shared-runner-v1 supports movement.type "orbit" OR content must be remapped to movement.path="circular" + angular params.

12-recommend-next
- Run reconcile, then run validate, then build. Recommended commands (use existing CLI wrapper):
  1) python arcade_builder_cli.py reconcile --reply arcade_packets/neon-orbital-courier_reply.md
  2) python arcade_builder_cli.py validate --session arcade_session.json
  3) python arcade_builder_cli.py build --id neon-orbital-courier
- If validation fails because of "orbit" enum, run small schema reconcile: add mapping OR change player.movement.type to "circular" before build.

chosen runtime mode:
- shared-runner-v1 (runner)

root game intent:
- Short urgent neon-cyberpunk courier runner: perform timed dash windows while orbiting a central anchor to deliver high-score courier runs (30s) with risk/reward dash windows and combo scoring.

game loop plan (condensed):
- Start run (30s). Player orbits center at base angular speed. Dash windows open at fixed orbit angles; dashing during a window grants window_hit bonus and allows delivery. Obstacles and drones spawn progressively. Score adds distance + window hits + delivery bonuses; run ends on time expiry or collision. Aim: high score.

theme pack:
- Palette hex values as in JSON.
- Fonts: minimal shared sans.
- UI: minimal HUD with timer, combo, score, orbital indicator.
- SFX: shared tick/dash/hit/ding. No external assets.

content contract (object definitions):
- run, player.movement, dash, window, delivery_point, entity (type, behavior, spawn_rule), scoring — represented as JSON objects/arrays; all durations in ms integers.

schema notes:
- Required: movement.type supporting "orbit" or fallback to "circular/path" param.
- Ensure loop.run_duration_ms (int), dash fields in ms, palette hex string format, assets.use_shared boolean.
- schema_version: arcade-game-v1 used.

JSON-ready decisions:
- Provided full game JSON (above). Use as arcade_packets/*_reply.md content (wrapped by reply endpoint). No extra runtime code required if runtime supports parameterized orbit behavior.

validation cues:
- Check: id (slug), title (non-empty), mode ∈ {runner,...}, runtime matches available runtimes.
- All *_ms fields integers; palette values /^#[0-9A-Fa-f]{6}$/; assets.use_shared true or false.
- content.windows and entities arrays length ≥1.
- Ensure scoring numbers are finite non-negative.
- If validator errors reference movement.type, map to movement.path="circular" + orbital_anchor parameters.

downstream ArcadeBuilder command recommendation:
- python arcade_builder_cli.py reconcile --reply arcade_packets/neon-orbital-courier_reply.md
- python arcade_builder_cli.py validate --session arcade_session.json
- python arcade_builder_cli.py build --id neon-orbital-courier

blockers:
- If shared-runner-v1 lacks explicit "orbit" movement support, minor schema mapping needed (movement.path:"circular") or engine param addition; this is a schema/runtime capability blocker.
- If required shared assets (icons/sfx keys) missing from asset pack, fallback icon/sfx must be assigned.
- Any strict validator that disallows free-form behavior enums will require schema update prior to build.
