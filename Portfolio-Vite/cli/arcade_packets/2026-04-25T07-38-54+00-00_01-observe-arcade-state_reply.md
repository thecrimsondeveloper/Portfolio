Inspecting repository for arcade runtime, schemas, templates, pages, and portfolio data. Running parallel file-glob searches and reporting intent.

Reading base-game schema and a template to align JSON fields and conventions (parallel views).

restated request
- Produce a single ArcadeBuilder reply packet (simulate full worker chain) for flags: idea=prism, theme=ice, mechanic=reflect, content=beams, mode=auto, tone=auto, depth=full; inspect repo state, plan, produce schema-bound JSON decisions, validation cues, and next commands.

taught decision frame
- Prefer existing shared runtimes/templates. Treat tiny flags as seeds. Do not add runtime code or external assets. Use greybox visuals and JSON-driven content. Preserve user intent (prism+reflect+ice). Validate against base-game.schema.json and use Portfolio-CLI templates.

per-step decisions
01-observe-arcade-state
- Found Portfolio-CLI directory with base-game.schema.json, multiple templates, arcade_builder_cli.py, and Portfolio-Vite/Pages runtime assets (arcade-runtime.js, arcade-bootstrap.js, arcade-assets.json). Good: existing schema and templates support adding a new entry without adding runtime code.

02-expand-seed-flags
- Intent: a puzzle/puzzle-arcade where cold/ice aesthetic + prism that reflects colored beams across rotatable prisms to targets; progressive levels increase prism count, split beams, and time pressure.

03-select-runtime-mode
- Chosen shared runtime mode: "labRift" (puzzle/interaction mode available in schema enum). Matches reflective/puzzle nature better than pulseGrid/runner.

04-plan-game-loop
- Core action: rotate placed prism(s) or toggle reflectors to route beams.
- Player controls: click/tap + drag rotation (discrete snap) or keyboard rotate; limited rotations per stage.
- Scoring: points per target hit, bonus for combos (split/multi-target), time bonus.
- Fail state: time runs out or misrouted beam count exceeds allowed (or too few targets completed).
- Progression: level sequence of increasing grid complexity, new beam colors, prism types (splitter, refractor), and moving hazards.

05-plan-theme-pack
- Palette: "ice-prism" — muted cyan/white gradients, glass-like accents.
- Mood: chilly, crystalline clarity; UI accents use high-contrast cyan and pale violet.
- Labels: title "Prism: Ice Beams", mode label "Lab: Prism".
- Presentation constraints: greybox sprites only (no external images). Use existing sprite keys from visuals template.

06-plan-content-contract
- Reusable objects in content JSON:
  - emitters: {id,x,y,dir,color,intensity}
  - prisms: {id,x,y,type,orientation,rotatable:boolean,split:false}
  - reflectors: {id,x,y,orientation,mirrored:boolean}
  - targets: {id,x,y,color,requiredHits}
  - beams: runtime-generated (described as expected behavior only)
  - level: {id,grid:{cols,rows},timeLimit,parScore,entities:[emitters,prisms,reflectors,targets]}
- Mechanic tags: "reflect","split","refract" to help runtime interpret behavior.

07-plan-schema-fields
- Must satisfy base-game.schema.json required top-level fields: id, slug, title, mode (use "labRift"), palette, instructions, hud, overlay, visuals, settings, help, menu, onboarding, meta, content.
- content must be an object with "levels":[ ... ] and top-level mechanic metadata.

08-fill_json (JSON-ready game object)
- Create a complete JSON object conforming to base-game.schema.json. (Provided below under "JSON-ready decisions".)

09-repair_json
- Ensure required fields exist, "mode" set to allowed enum value ("labRift"), settings.sections.controls include required keys (key,label,type,value). Use only allowed menu actions. No additionalProperties outside schema shape.

10-build-arcade-entry
- Prepare packet using arcade reply contract (arcade_packets/prism-ice_reply.md) containing this artifact; then run reconcile → validate → build using arcade_builder_cli.py.

11-validate-build
- Validation cues below; run schema validator via existing CLI (arcade_builder_cli.py validate or python JSON schema check). Confirm mode enum, required fields, settings control object shapes, content present and levels array non-empty.

12-recommend-next
- Create the reply packet in arcade_packets/, then run: reconcile, validate, build. If runtime lacks reflect support, open a small runtime-change ticket.

chosen runtime mode
- labRift (shared puzzle runtime from schema enum)

root game intent
- Prism: Ice Beams — rotate prisms and toggle reflectors to route colored beams from emitters to targets across crystalline (ice) levels. Short puzzle loops with scoring for efficiency and combos.

game loop plan
- Start overlay → Onboarding (3 steps) → Level starts: beams fire from emitters → player rotates prisms/toggles reflectors to direct beams → targets register hits → score updates → level completes when all required targets hit or time expires → progression to next level, difficulty increment.
- Controls: pointer/touch rotate (snap), keyboard rotate keys (←/→), undo last rotation (U).

theme pack
- palette: "ice-prism"
- primary: #DFF7FF (pale glacier)
- accent: #A9F0FF (icy cyan)
- shadow: #9AB3C9 (cold slate)
- sprite keys (greybox): spriteKey: "tile", accentSpriteKey: "prism", hazardSpriteKey: "spike", trailEffectKey: "beamTrail", impactEffectKey: "glassShatter"
- label tone: crisp / clinical

content contract
- content: { "mechanic":"reflect", "beamLifetime":2.5, "snapAngle":45, "levels":[ levelObj ... ] }
- levelObj: {
    "id": "lvl-1",
    "grid": {"cols":6,"rows":6},
    "timeLimit": 45,
    "parScore": 500,
    "emitters":[{id,x,y,dir,color}],
    "prisms":[{id,x,y,type:"standard",orientation:0,rotatable:true}],
    "reflectors":[{...}],
    "targets":[{id,x,y,color,requiredHits:1}],
    "hazards":[...]
  }

schema notes
- base-game.schema.json enforces required top-level fields; mode must be one of ["runner","orbit","pulseGrid","labRift","phaseDrop","harbor","rhythm","echo"] — chosen labRift.
- visuals keys must be strings; settings.sections.controls each must contain key,label,type,value with allowed type in ["select","range"].
- menu.actions.action must be one of {resume,restart,open_help,open_settings}.
- content is free-form object per schema; still adhere to internal templates.

JSON-ready decisions
- Full game JSON (schema-bound) follows (compact but complete):

{
  "id": "prism-ice",
  "slug": "prism-ice-reflect",
  "title": "Prism: Ice Beams",
  "mode": "labRift",
  "palette": "ice-prism",
  "instructions": "Rotate prisms and toggle reflectors to guide cold beams to crystal targets. Use snap rotations to refract and split beams.",
  "hud": { "modeLabel": "Prism Lab" },
  "overlay": {
    "startTitle": "Prism: Ice Beams",
    "startCopy": "Route beams through prisms to charge crystal targets. Rotations snap to angles.",
    "startAction": "Begin Run"
  },
  "visuals": {
    "spriteKey": "tile",
    "accentSpriteKey": "prism",
    "hazardSpriteKey": "spike",
    "trailEffectKey": "beamTrail",
    "impactEffectKey": "glassShatter"
  },
  "settings": {
    "title": "Settings",
    "sections": [
      {
        "title": "Gameplay",
        "controls": [
          { "key": "difficulty", "label": "Difficulty", "type": "select", "value": "normal", "options": ["easy","normal","hard"] },
          { "key": "rotationSnap", "label": "Rotation Snap (degrees)", "type": "range", "value": 45, "min": 15, "max": 90, "step": 15 }
        ]
      }
    ]
  },
  "help": {
    "title": "How to Play",
    "steps": [
      "Rotate prisms (click-drag or arrow keys) to change beam paths.",
      "Use split prisms to send beams to multiple targets.",
      "Complete all crystal targets before time runs out."
    ],
    "tips": [
      "Early rotations are cheap—plan for splits.",
      "Time bonuses grant combo multipliers."
    ]
  },
  "menu": {
    "title": "Pause Menu",
    "actions": [
      { "label": "Resume", "action": "resume" },
      { "label": "Restart", "action": "restart" },
      { "label": "Help", "action": "open_help" },
      { "label": "Settings", "action": "open_settings" }
    ]
  },
  "onboarding": {
    "title": "First Lab",
    "startSteps": [
      "Open Help for controls.",
      "Press Begin to start Level 1.",
      "Rotate the single prism to hit the crystal target."
    ],
    "firstGoal": "Hit the first crystal target"
  },
  "meta": {
    "summary": "A greybox puzzle about rotating prisms to route beams in an ice theme.",
    "goal": "Charge all crystal targets per level.",
    "controls": "Pointer/touch + keyboard rotate",
    "paletteLabel": "Ice Prism",
    "features": ["beam reflection","rotating prisms","splitters","greybox visuals"]
  },
  "content": {
    "mechanic": "reflect",
    "beamLifetime": 2.5,
    "snapAngle": 45,
    "levels": [
      {
        "id": "level-1",
        "grid": { "cols": 6, "rows": 6 },
        "timeLimit": 45,
        "parScore": 500,
        "emitters": [
          { "id": "E1", "x": 0, "y": 2, "dir": "E", "color": "cyan" }
        ],
        "prisms": [
          { "id": "P1", "x": 2, "y": 2, "type": "standard", "orientation": 90, "rotatable": true }
        ],
        "reflectors": [],
        "targets": [
          { "id": "T1", "x": 5, "y": 2, "color": "cyan", "requiredHits": 1 }
        ],
        "hazards": []
      },
      {
        "id": "level-2",
        "grid": { "cols": 7, "rows": 7 },
        "timeLimit": 60,
        "parScore": 1200,
        "emitters": [
          { "id": "E1", "x": 0, "y": 3, "dir": "E", "color": "cyan" },
          { "id": "E2", "x": 0, "y": 1, "dir": "SE", "color": "violet" }
        ],
        "prisms": [
          { "id": "P1", "x": 2, "y": 2, "type": "splitter", "orientation": 45, "rotatable": true },
          { "id": "P2", "x": 3, "y": 4, "type": "standard", "orientation": 0, "rotatable": true }
        ],
        "reflectors": [
          { "id": "R1", "x": 4, "y": 3, "orientation": 135, "mirrored": false }
        ],
        "targets": [
          { "id": "T1", "x": 6, "y": 3, "color": "cyan", "requiredHits": 1 },
          { "id": "T2", "x": 6, "y": 5, "color": "violet", "requiredHits": 1 }
        ],
        "hazards": []
      }
    ]
  }
}

repair-json notes
- Ensured "mode" is "labRift" (allowed enum).
- settings.sections.controls each include required key,label,type,value.
- menu actions limited to allowed enum actions.
- All top-level required fields present.

validation cues
- Run JSON Schema validation against Portfolio-CLI/schemas/base-game.schema.json:
  - Confirm required top-level keys exist.
  - Confirm mode ∈ enum.
  - Confirm settings.sections.controls items include required keys (key,label,type,value).
  - Confirm menu actions length ≥2 and action values valid.
  - Confirm content.levels is non-empty array.
- Spot-check visuals keys are strings.
- If CLI offers: Portfolio-CLI/arcade_builder_cli.py validate --entry prism-ice-reflect (or run reconcile→validate).

downstream ArcadeBuilder command recommendation
1) Write reply packet: arcade_packets/prism-ice_reply.md (store this artifact per contract).
2) Reconcile: python Portfolio-CLI/arcade_builder_cli.py reconcile --reply arcade_packets/prism-ice_reply.md
3) Validate: python Portfolio-CLI/arcade_builder_cli.py validate --session Portfolio-CLI/arcade_session.json
4) Build: python Portfolio-CLI/arcade_builder_cli.py build --entry prism-ice-reflect
(If CLI uses different flags, use equivalent reconcile → validate → build sequence.)

blockers
- Potential runtime blocker: labRift runtime (Portfolio-Vite/Pages/arcade-runtime.js) must support beam-reflect/split mechanics. If not implemented, either:
  - implement small runtime mapping from "reflect" tags to existing labRift behaviors, or
  - constrain levels to emulate reflection via precomputed paths (content-side) — requires runtime extension.
- Visual assets: uses greybox sprite keys assumed present; if missing, visuals will fallback or need simple sprite key mapping in arcade-assets.json.

end.
