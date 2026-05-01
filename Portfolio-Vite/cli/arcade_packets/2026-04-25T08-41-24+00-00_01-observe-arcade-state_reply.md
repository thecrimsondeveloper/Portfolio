restated request
- Create a complete ArcadeBuilder reply packet that simulates the full hierarchical ArcadeBuilder worker chain internally for a compact neon cyberpunk auto-run runner called "Neon Phase Courier" (flags provided). Provide a structured artifact the arcade_builder_cli.py can reconcile.

taught decision frame (short)
- Prefer existing shared runtime templates (runner.template + runner.schema). Keep game output strictly schema-bound JSON. Use greybox assets only; no external assets. Treat short flags as seeds; preserve user intent (auto-run, lane-switch, neon pulse, compact lanes). Don’t invent new runtime code; supply JSON and build instructions that fit existing builder.

per-step decisions
- 01-observe-arcade-state: Use repository templates/schemas. Key files found: Portfolio-CLI/templates/runner.template.json, Portfolio-CLI/schemas/runner.schema.json, Portfolio-CLI/schemas/base-game.schema.json, Portfolio-CLI/arcade_session.json, Portfolio-Vite/Pages/arcade-runtime.js and shell assets.
- 02-expand-seed-flags: Interpret seeds as urgent, short-run courier: auto-run, timed lane-switch mechanic, short lane strips, neon cyberpunk pixel aesthetic, full depth (complete loop+scoring/progression).
- 03-select-runtime-mode: Use existing "runner" shared runtime/template (Portfolio-CLI/templates/runner.template.json).
- 04-plan-game-loop: Auto-forward courier; player issues instant lane-switch inputs (left/right) with a tight timing window; pickups and obstacles spawn on short lane strips; scoring via pickups + combos + near-misses; collision ends run; progression via escalating speed/density across repeated short runs.
- 05-plan-theme-pack: Neon cyberpunk pixel palette, urgent pulse UI, compact HUD, terse text labels, limited greybox tiles, no external art.
- 06-plan-content-contract: Define reusable lane strips, obstacle and pickup objects, speed_profile, runtime flags, presentation block. Keep objects small and repeated.
- 07-plan-schema-fields: Target existing runner.schema.json fields; add/ensure presence of: auto_run (bool), lane_count (int), strip_length (int), lane_strips (array of strip objects), speed_profile, mechanics.input_window & lane_switch_time, scoring object.
- 08-fill-json: Produce schema-bound JSON payload (below) using template "runner".
- 09-repair-json: Keep fields conservative to match runner.schema.json; avoid unknown keys. Validation cues included below.
- 10-build-arcade-entry: Instruct writing reply packet to arcade_packets/neon_phase_courier_reply.md then run arcade_builder_cli.py reconcile -> validate -> build.
- 11-validate-build: Recommend running the repo's validate path against Portfolio-CLI/schemas/runner.schema.json and the arcade_session.json flow.
- 12-recommend-next: After build, iterate with playtest variations (three strip presets: Chill, Pulse, Overclock) and add telemetry and short tutorial strip.

chosen runtime mode
- runner (use Portfolio-CLI/templates/runner.template.json and Portfolio-CLI/schemas/runner.schema.json)

root game intent (single sentence)
- Fast, urgent neon-courier auto-runner: player times rapid lane-swaps on short, repeating lane strips to collect data-chips, avoid drones, and chain combos under an ever-quickening neon pulse.

game loop plan (concise)
- Start run on short lane strip (strip_length ~24 tiles).
- Auto-forward movement at base_speed; player presses left/right to switch lanes.
- Successful pickups add score and build combo; near-miss dodges give small bonus.
- Collision with obstacle immediately ends run.
- Each completed strip advances difficulty: increased speed, slightly higher obstacle density.
- Short-run arc: 3–5 strips per run; optional target_score per run for grading.

theme pack (constraints)
- Palette:
  - bg: #0B0F1A (deep black-blue)
  - neon_cyan: #00F0FF
  - neon_pink: #FF00CC
  - neon_purple: #B400FF
  - accent_yellow: #FFD166 (sparingly)
- Pixel constraints: tile_size 8px, pixel-scale 2 (greybox primitives).
- UI: urgent neon pulse (blink on pickup/near-miss), compact HUD (score, combo, strip counter).
- Labels: "PHASE COURIER", short context strings only.
- Audio cues: "pulse" beep on pickup, low rumble on speed shift (runtime-only placeholders).

content contract (JSON object types)
- metadata: { id, title, author, template, seed, mode }
- presentation: { palette, pixel_scale, ui_theme, tile_size }
- mechanics: { auto_run:bool, lane_count:int, lane_switch_time:float, input_window:float }
- speed_profile: { base_speed:float, acceleration:float, max_speed:float }
- lane_strips: [ { strip_id:int, length:int, obstacles:[{type,pos,lane}], pickups:[{type,pos,lane}], density_hint } ]
- scoring: { pickup_value:int, near_miss_bonus:int, combo_growth:float, time_bonus_factor:int }
- progression: { strips_per_run:int, difficulty_curve:"linear"|"staged", seed }
- runtime_flags: { mode:"runner", compact:true, depth:"full" }

schema notes (compatibility & minimal changes)
- Use Portfolio-CLI/schemas/runner.schema.json as authoritative. Ensure payload includes only fields expected there; if runner.schema.json already exposes lane_strips/obstacle/pickup concepts, use those exact names. If schema lacks input_window or lane_switch_time, place them under mechanics (likely accepted by base-game.schema.json as metadata) — validation may flag unknown keys; validation cues below advise checks.
- Keep additional keys namespaced under "mechanics" or "presentation" to minimize clash.

JSON-ready decisions (schema-bound payload)
- This payload is intentionally conservative to align with runner schema. Replace array entries with procedurally-generated repeats on reconcile/build if desired.

{
  "id": "neon-phase-courier",
  "title": "Neon Phase Courier",
  "author": "thecrimsondeveloper",
  "template": "runner",
  "mode": "auto-run",
  "seed": "auto-ru",
  "presentation": {
    "palette": {
      "bg": "#0B0F1A",
      "neon_cyan": "#00F0FF",
      "neon_pink": "#FF00CC",
      "neon_purple": "#B400FF",
      "accent_yellow": "#FFD166"
    },
    "tile_size": 8,
    "pixel_scale": 2,
    "ui_theme": "urgent neon pulse"
  },
  "mechanics": {
    "auto_run": true,
    "lane_count": 3,
    "lane_switch_time": 0.18,
    "input_window": 0.28
  },
  "speed_profile": {
    "base_speed": 1.2,
    "acceleration": 0.025,
    "max_speed": 3.0
  },
  "lane_strips": [
    {
      "strip_id": 0,
      "length": 24,
      "obstacles": [
        { "type": "drone", "pos": 10, "lane": 1 }
      ],
      "pickups": [
        { "type": "data_chip", "pos": 6, "lane": 2 },
        { "type": "data_chip", "pos": 18, "lane": 0 }
      ],
      "density_hint": "compact"
    },
    {
      "strip_id": 1,
      "length": 24,
      "obstacles": [
        { "type": "drone", "pos": 8, "lane": 2 },
        { "type": "barrier", "pos": 16, "lane": 1 }
      ],
      "pickups": [
        { "type": "data_chip", "pos": 4, "lane": 0 },
        { "type": "data_chip", "pos": 20, "lane": 2 }
      ],
      "density_hint": "pulse"
    },
    {
      "strip_id": 2,
      "length": 24,
      "obstacles": [
        { "type": "drone", "pos": 12, "lane": 0 }
      ],
      "pickups": [
        { "type": "data_chip", "pos": 5, "lane": 1 },
        { "type": "data_chip", "pos": 14, "lane": 2 }
      ],
      "density_hint": "overclock"
    }
  ],
  "scoring": {
    "pickup_value": 100,
    "near_miss_bonus": 50,
    "combo_growth": 1.15,
    "time_bonus_factor": 10
  },
  "progression": {
    "strips_per_run": 3,
    "difficulty_curve": "linear",
    "run_goal": { "target_score": 2000, "target_distance": 72 }
  },
  "presentation_hints": {
    "title_text": "PHASE COURIER",
    "short_instructions": "TAP L/R — PHASE",
    "tone": "urgent neon pulse"
  }
}

validation cues (what to check & fix)
- Run JSON through Portfolio-CLI/schemas/runner.schema.json validator:
  - Ensure required fields (id,title,template,mechanics,lane_strips) exist.
  - If validator rejects mechanics.input_window or lane_switch_time, move them to metadata or remove and document as runtime hints.
  - Confirm lane_strips elements match obstacle/pickup schemas (fields type,pos,lane).
  - Ensure palette colors are strings and tile_size/pixel_scale numeric.
- Suggested validation commands:
  - python3 Portfolio-CLI/arcade_builder_cli.py validate --session=Portfolio-CLI/arcade_session.json
  - Or run any repository-provided JSON schema validator that the builder uses.

downstream ArcadeBuilder command recommendation
- Save this artifact as Portfolio-CLI/arcade_packets/neon_phase_courier_reply.md (reply file).
- Then run (from repo root):
  - python3 Portfolio-CLI/arcade_builder_cli.py reconcile --reply=Portfolio-CLI/arcade_packets/neon_phase_courier_reply.md
  - python3 Portfolio-CLI/arcade_builder_cli.py validate --session=Portfolio-CLI/arcade_session.json
  - python3 Portfolio-CLI/arcade_builder_cli.py build --session=Portfolio-CLI/arcade_session.json
- After build, open Portfolio-Vite/Pages/arcade-runtime.js test harness to preview greybox run.

blockers (known unknowns)
- Exact required field names in runner.schema.json not inspected line-by-line here — validator may flag unknown or missing keys (mechanics subfields being the most likely).
- If runner.schema.json lacks lane_strips concept, a minimal mapping may be required (e.g., raw event arrays). Validation will reveal mapping fixes.
- No external art allowed; final presentation limited to greybox runtime capabilities in Portfolio-Vite.
- Playtest tuning (input_window, lane_switch_time, speed values) requires iterative validation and feel testing.

end of artifact
