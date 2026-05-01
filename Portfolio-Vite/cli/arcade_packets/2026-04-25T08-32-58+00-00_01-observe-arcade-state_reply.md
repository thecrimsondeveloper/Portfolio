restated request:
- Seed an ArcadeBuilder reply packet for "Crystal Comet Run" (mode: runner) by inspecting the project, expanding flags into a full game plan, selecting runtime, producing schema-bound JSON decisions, and recommending next build steps.

taught decision frame:
- Prefer existing shared runtimes/templates (use runner.template.json & runner.schema.json).
- Keep output schema-bound JSON; do not add JS runtime.
- Use seed flags as guidance; preserve user intent (momentum racing, maze reconfiguration, temporal phasing).
- Reuse shared assets; avoid external resources.

per-step decisions:
- 01-observe-arcade-state: Found Portfolio-CLI with templates, schemas, arcade_session.json, arcade_run.md, arcade_packets. Relevant files: templates/runner.template.json, schemas/runner.schema.json, base-game.schema.json, arcade_builder_cli.py, arcade_session.json, arcade_run.md.
- 02-expand-seed-flags: Compact intent — high-speed comet runner through shifting prismatic crystal mazes; player manages momentum/boost and phases through temporarily intangible states while the maze reconfigures.
- 03-select-runtime-mode: Chosen runtime: "runner" (match templates/runner.template.json and schemas/runner.schema.json).
- 04-plan-game-loop: Continuous forward run + steering; momentum determines top speed and turning; pick up crystals for score; reconfiguration events change maze layout; temporal phase ability lets player pass through crystals briefly with cooldown; collisions end run.
- 05-plan-theme-pack: Prismatic neon palette, tense neon tone, celestial overlays, UI labels (Speed, Momentum, Phase, Crystals), ambient synth + whoosh SFX placeholders; palette hexs: primary #00E5FF (neon cyan), accent #FF4DFF (magenta), crystal #7CFFB2 (prismatic teal), bg #0A0014 (deep space).
- 06-plan-content-contract: Reusable objects (JSON):
  - game: { id, title, runtime, template }
  - meta: { themeName, palette, tone, tags }
  - mechanics: [momentum, reconfig, phasing]
  - params: numeric gameplay tuning (speedBase, accel, boostMultiplier, momentumDecay, phaseDuration, phaseCooldown, reconfigInterval, reconfigSeverity)
  - content arrays:
    - mazeSegments[]: { id, width, height, seed, reconfigAnchors[] }
    - tiles[]: { type: "path"|"wall"|"crystal"|"gate", pos, properties }
    - powerups[]: { type:"boost"|"phaseCharge", pos, value }
    - entities: { player: { startPos, momentum }, collectibles[] }
  - events[]: { time, type:"reconfig"|"phaseGate", payload }
- 07-plan-schema-fields:
  - Use runner.schema.json as base.
  - Recommend optional additions (non-breaking): phaseConfig (duration, cooldown), reconfigRules (interval, pattern, severity), momentumParams (base, accel, decay), mazeSegments[] structure. These are added as optional fields in game JSON; schema change suggested but not required for runtime if runner.schema.json accepts "metadata"/"params"/"content".
- 08-fill-json (schema-bound game JSON only):
{
  "id": "crystal-comet-run",
  "title": "Crystal Comet Run",
  "runtime": "runner",
  "template": "runner",
  "meta": {
    "themeName": "Prismatic Comet",
    "palette": {
      "bg": "#0A0014",
      "primary": "#00E5FF",
      "accent": "#FF4DFF",
      "crystal": "#7CFFB2"
    },
    "tone": "tense neon",
    "tags": ["momentum","maze-reconfig","temporal-phasing","runner"]
  },
  "mechanics": ["momentum","maze_reconfiguration","temporal_phase"],
  "params": {
    "speedBase": 200,
    "accel": 600,
    "boostMultiplier": 1.6,
    "momentumDecay": 0.6,
    "phaseDuration": 0.9,
    "phaseCooldown": 4.0,
    "reconfigInterval": 6.5,
    "reconfigSeverity": 0.28,
    "segmentLength": 48
  },
  "content": {
    "mazeSegments": [
      { "id":"seg-01","seed":137,"width":12,"height":8,"reconfigAnchors":[{"x":6,"y":4}] }
    ],
    "tiles": [],
    "powerups": [],
    "collectibles": []
  },
  "scoring": {
    "distancePerSecond": 10,
    "crystalValue": 50,
    "phaseGateBonus": 200
  },
  "fail": { "onCollision": true, "onTimeout": false },
  "progression": {
    "difficultyRamp": "increase_reconfig_frequency_and_severity",
    "segmentVariants": 5
  }
}
- 09-repair-json: Ensure all fields are present and types match runner schema: keep unknown/optional fields within top-level "meta"/"params"/"content" so runner schema's base-game fields validate; avoid adding executable code or asset URIs.
- 10-build-arcade-entry: Do not modify files now. Recommended artifacts to write (simulated): arcade_packets/<timestamp>_fill-json_reply.md (contains above JSON), then reconcile into arcade_session.json and arcade_run.md via arcade_builder_cli.py.
- 11-validate-build: Validate with existing CLI: run Portfolio-CLI/arcade_builder_cli.py validate (it checks schema). Also recommend linters/builders already in repo.
- 12-recommend-next: Create a follow-up packet to (A) extend mazeSegments with concrete tile maps for first 3 segments and (B) tune params via playtest session.

chosen runtime mode:
- "runner" (use Portfolio-CLI/templates/runner.template.json and Portfolio-CLI/schemas/runner.schema.json)

root game intent:
- Fast-paced momentum runner through prismatic crystal mazes that periodically reconfigure; player uses boosting and a limited temporal phase to survive and score by collecting crystals and passing phase-gates.

game loop plan:
- Core action: continuous forward thrust + steer (left/right), optional boost consumes momentum charge.
- Secondary action: temporal phase (short intangibility) with cooldown for passing through newly-formed crystals/gates.
- Scoring: distance + crystals + phase-gate bonuses.
- Fail state: collision with wall/crystal when not phased.
- Progression: segmented levels; each segment is a maze template with increasing reconfiguration frequency and pattern complexity.

theme pack:
- Palette: bg #0A0014, primary #00E5FF, accent #FF4DFF, crystal #7CFFB2, hazard #FF9500
- Mood: tense neon, celestial shimmer
- UI labels: Speed, Momentum, Phase, Crystals, Distance
- SFX placeholders: synth-ambient, whoosh-boost, chime-crystal, glitch-reconfig
- Constraints: grayscale readability for UI numbers; minimal text; no external assets.

content contract:
- Define canonical JSON objects:
  - mazeSegment { id, seed, width, height, tileGrid? (optional), reconfigAnchors[] }
  - tile { type, x, y, props }
  - collectible { id, type, x, y, value }
  - powerup { id, type, x, y, amount }
  - event { t, type, payload }
- All coordinates integer grid; times in seconds; values numeric; arrays optional when empty.

schema notes:
- Existing runner.schema.json covers base runner fields. Suggested optional additions (non-breaking):
  - params.phaseConfig: { duration, cooldown }
  - params.reconfigRules: { interval, severity, pattern }
  - content.mazeSegments[].reconfigAnchors
- If validator refuses unknown top-level keys, place additions under "meta" or "params" to remain compatible.

JSON-ready decisions:
- Use id "crystal-comet-run", runtime "runner", template "runner".
- Keep gameplay tunables in params; content arrays initially minimal (empty), to be populated by next packet with concrete tile grids.
- No asset URIs included; use arcade-assets.json placeholders if needed.

validation cues:
- Ensure final JSON passes Portfolio-CLI validator:
  - required top-level keys: id, title, runtime, template, meta, mechanics, params, content
  - types: strings, numbers, arrays as above
  - no functions or code fragments
- Run: python3 Portfolio-CLI/arcade_builder_cli.py validate --file <json>
- Look for schema errors around unknown top-level properties; move them under "meta"/"params" if needed.

downstream ArcadeBuilder command recommendation:
- Reconcile: python3 Portfolio-CLI/arcade_builder_cli.py reconcile --packet ./Portfolio-CLI/arcade_packets/<timestamp>_fill-json_reply.md
- Validate: python3 Portfolio-CLI/arcade_builder_cli.py validate
- Build: python3 Portfolio-CLI/arcade_builder_cli.py build
(Or use CLI wrapper: cd Portfolio-CLI && python3 arcade_builder_cli.py reconcile && python3 arcade_builder_cli.py validate && python3 arcade_builder_cli.py build)

blockers:
- Need concrete maze tile maps for first segments (next packet).
- If runner.schema.json disallows proposed optional fields, a schema change or relocation of fields will be required.
- Playtesting required to tune momentum/phase/reconfig numbers.
- No external assets allowed; rely on shared arcade-assets.json placeholders.
