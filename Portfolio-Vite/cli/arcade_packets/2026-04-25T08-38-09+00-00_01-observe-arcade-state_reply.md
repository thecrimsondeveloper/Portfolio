restated request:
- Produce a full ArcadeBuilder reply packet for flag seeds: idea="Ember Harbor Rescue-Drift", theme="Charred industrial docks wit", mode="harbor", tone="urgent heroic", mechanic="Grapple-tether physics with time", content="Fast side-scroll rescue runs tha", depth="full". Inspect repo state first, then produce per-step decisions and JSON-ready design for reconciliation.

taught decision frame:
- Prefer shared runtime modes and existing templates (harbor).  
- Keep output schema-bound JSON; do not add runtime code or external assets.  
- Treat short flags as seeds to expand into concrete, minimal schema fields.  
- Preserve user intent (urgent, heroic, grappling+time) over broad ideation.

per-step decisions:
01-observe-arcade-state:
- Inspected Portfolio-CLI and Portfolio-Vite files: templates/harbor.template.json, schemas/harbor.schema.json, base-game.schema.json, arcade_session.json, arcade_steps.json, arcade_run.md, arcade-assets.json, existing harbor games (drift-harbor.json, drift-beat-harbor.json, sandstorm-memory-harbor.json), arcade runtime (arcade-runtime.js, arcade-bootstrap.js).
- Conclusion: harbor template and harbor.schema.json exist and are the canonical runtime to extend.

02-expand-seed-flags:
- Compact game intent: "Urgent rescue runs through charred industrial docks; player uses a grapple-tether to swing, anchor, and tow survivors to evacuation skiffs while time is scarce—fast side-scrolling segments with time-extensions and physics-based traversal."

03-select-runtime-mode:
- Chosen runtime: harbor (use Portfolio-CLI templates/harbor.template.json and harbor.schema.json).
- Rationale: matches mode flag and existing template, avoids new runtime code.

04-plan-game-loop:
- Core action: grapple-tether attach → swing/anchor → reel/pull → rescue (attach survivor) → deliver to evacuation point.
- Controls: grapple aim + fire, release, reel-in, boost thruster (short), drop/rescue action.
- Scoring: survivors rescued × base points + time-left bonus + chaining multiplier for consecutive quick rescues.
- Fail state: player time meter reaches zero OR player destroyed by hazards (fall into flames, heavy crates) without remaining respawn lives.
- Progression: sequence of short runs (segments) per run; each run is 60–120s segmented into checkpoints with increasing hazard density; "drift" modifier adds moving debris/rafts.
- Meta: runs unlock modifiers (longer tether, faster reel, time-slow pickup).

05-plan-theme-pack:
- Palette: soot black (#0b0b0b), charred steel gray (#2b2f33), ember orange (#ff6a00), ash blue (#6b7c8f), hazard yellow accents.
- Mood cues: flicker particle layers (embers), smoky parallax, silhouette dock cranes.
- Labels/UI: urgent header (bold), timer (left), rescue counter (top-right), tether indicator (cooldown bar).
- Presentation constraint: greybox assets only (use arcade-assets.json symbolic IDs), no external art.

06-plan-content-contract:
- Reusable content objects (JSON shapes):
  - game.meta { id,title,desc,mode,theme,tags,author }
  - physics.params { gravity, tetherRange, tetherCooldown, reelSpeed, swingDamping, timeDrainRate }
  - player { startLives, speed, grappleAimSpeed, tetherParamsRef }
  - survivor { healthState, weight, rescueAttachTime, rescuePoints }
  - hazard { type(enum), damage, pattern (static/moving), collider }
  - segment[] { lengthSecs, spawnList:[{type, x, y, params}], ambient (wind, smokeIntensity), timeBonusCount }
  - pickups { timeExtend, tetherUpgrade, reelBoost }
  - scoring.rules { baseSurvivorPoints, timeMultiplier, comboWindow }
  - ui.config { hudLayoutRef, tutorialHints }
  - progression { runCount, difficultyRamp (per-run) }
- JSON expresses lists of short level segments; each segment uses template-local asset IDs.

07-plan-schema-fields:
- Use harbor.schema.json as base. Required additions/consumable fields (non-breaking):
  - physics.params.tetherRange (number)
  - physics.params.reelSpeed (number)
  - pickups.timeExtend.amount (seconds)
  - segment.spawnList[].role (e.g., "survivor","hazard","obstacle")
  - scoring.comboWindow (ms)
- These are within "game-specific params" field allowed by existing templates — prefer adding under "runtimeParams" or "mechanics" object per harbor.schema.json pattern (no schema file edits here; structure uses template fields allowed by harbor.template.json).

08-fill-json (JSON-ready decisions):
- High-level JSON decisions to produce:
{
  "meta": {
    "id":"ember-harbor-rescue-drift",
    "title":"Ember Harbor Rescue — Drift",
    "author":"thecrimsondeveloper",
    "mode":"harbor",
    "template":"harbor",
    "description":"Urgent side-scroll rescue runs in charred docks; grapple, time, rescue."
  },
  "runtimeParams":{
    "tone":"urgent heroic",
    "theme":"charred-industrial-docks",
    "physics":{
      "gravity":1200,
      "tetherRange":420,
      "tetherCooldown":600,
      "reelSpeed":1.2,
      "swingDamping":0.85,
      "timeDrainRate":1.0
    },
    "player":{
      "startLives":3,
      "speed":420,
      "grappleAimSpeed":900
    },
    "scoring":{
      "baseSurvivorPoints":100,
      "timeMultiplierPerSec":2,
      "comboWindowMs":1500
    },
    "pickups":{
      "timeExtend":{"amount":10,"spawnWeight":0.15},
      "tetherUpgrade":{"level":1,"spawnWeight":0.05}
    },
    "segments":[
      {"id":"seg-01","lengthSecs":60,"spawnList":[{"role":"survivor","x":800,"y":120,"weight":1},{"role":"fire","x":1200,"y":200,"pattern":"moving"}],"ambient":{"smoke":0.4}},
      {"id":"seg-02","lengthSecs":75,"spawnList":[{"role":"survivor","x":600,"y":140},{"role":"crate","x":900,"y":220,"pattern":"falling"}],"ambient":{"smoke":0.6},"drift":true}
    ],
    "progression":{"runsToComplete":8,"difficultyRamp":1.08}
  },
  "assets":["harbor_crane_symbol","evac_skiff_symbol","ember_particle_small"]
}

09-repair-json:
- Ensure all numeric fields use numbers, arrays exist for segments, required meta fields present (id,title,mode,template). Use harbor.template.json conventions: place runtimeParams under "mechanics" if harbor.template expects that — choose "runtimeParams" only if harbor.template.json allows arbitrary mechanics payload. If harbor.template requires specific key (e.g., "params"), map accordingly during reconcile. No schema file edits here.

10-build-arcade-entry:
- Prepare packet file name: arcade_packets/{timestamp}_01-observe-arcade-state_reply.md (builder will save). Packet contains this artifact plus the JSON payload (as above) to be reconciled.
- Do not write files (user forbade editing); recommend builder run to fold into arcade_session.json and write game page.

11-validate-build:
- Validation cues to run (using existing CLI):
  - python Portfolio-CLI/arcade_builder_cli.py validate --payload <packet.json>  (or use relevant validate command in arcade_builder_cli.py). Ensure:
    - meta.id matches filename-safe slug
    - mode === "harbor"
    - template === "harbor"
    - runtimeParams fields match types in Portfolio-CLI/schemas/harbor.schema.json
    - segments[] lengthSecs >0, spawnList entries include valid role strings present in arcade-assets.json
  - If validate reports missing fields, map runtimeParams into the template's expected key (e.g., "mechanics" or "params") and revalidate.

12-recommend-next:
- Produce final packet (this artifact) and then run:
  - python Portfolio-CLI/arcade_builder_cli.py reconcile --packet arcade_packets/<this_packet>.md
  - python Portfolio-CLI/arcade_builder_cli.py validate --id ember-harbor-rescue-drift
  - python Portfolio-CLI/arcade_builder_cli.py build --id ember-harbor-rescue-drift
- After build: playtest tuning pass for tetherRange/reelSpeed and timeDrainRate; iterate.

chosen runtime mode:
- harbor (use templates/harbor.template.json and schemas/harbor.schema.json)

root game intent:
- Fast, urgent heroic side-scroll rescue runs across charred industrial docks. Use grapple-tether swing and reel physics to attach survivors and deliver them to evacuation skiffs before time expires. Drift segments introduce moving obstacles and debris; pickups extend time or improve tether.

game loop plan:
- Start run → navigate segment → use grapple to reach/rescue survivor(s) → chain quick rescues for combo points → drop at skiff checkpoint → short time bonus → next segment (harder) → end-run when runsToComplete achieved; fail if time/lives expire.

theme pack:
- Palette: soot black, charred steel gray, ember orange, ash blue, hazard yellow.
- UI: urgent timer prominent; tether HUD; rescue counter; minimal tutorial overlay first run.
- Presentation: greybox symbols from arcade-assets.json; parallax smoky background; particle embers for danger highlights.

content contract:
- Entities: player, tether, survivor, hazard, pickup, segment, progression, scoring.
- Format: meta + runtimeParams/mechanics + assets[] + segments[].
- Spawn entries: {role, x, y, params}. Roles must align to asset IDs in Portfolio-Vite/Pages/arcade-assets.json.

schema notes:
- Follow Portfolio-CLI/schemas/harbor.schema.json and base-game.schema.json. Place game-specific parameters under the template-allowed mechanics container (e.g., "params" or "mechanics"); validate field names before final commit. Numeric ranges: gravity (200–3000), tetherRange (100–1000), reelSpeed (0.2–3.0), timeExtend.amount integer seconds.

JSON-ready decisions:
- Final JSON will use meta + runtimeParams as in step 08; segments minimal (2 sample segments) for demonstration; queue full content in ArcadeBuilder reconciliation to produce full-level arrays (8 runs). Use asset symbolic IDs only.

validation cues:
- Required meta keys present (id,title,desc,mode,template).  
- runtimeParams fields type-check with harbor.schema.json.  
- segments[] non-empty and spawnList roles exist in arcade-assets.json.  
- IDs slug-safe (lowercase, hyphens).  
- Numeric fields within schema ranges.

downstream ArcadeBuilder command recommendation:
- Run in repo root:
  1) python Portfolio-CLI/arcade_builder_cli.py reconcile --packet <this_packet.md>
  2) python Portfolio-CLI/arcade_builder_cli.py validate --id ember-harbor-rescue-drift
  3) python Portfolio-CLI/arcade_builder_cli.py build --id ember-harbor-rescue-drift
- If CLI differs, use its help: python Portfolio-CLI/arcade_builder_cli.py --help

blockers:
- Must map runtimeParams keys to exact field name expected by harbor.template.json (small ambiguity).  
- No new runtime code allowed — any mechanic not covered by harbor runtime must be expressed as parameters or approximated (e.g., precise swing physics tuning may be limited).  
- Playtesting/tuning required to balance tether physics and time drain—manual iteration after build.
