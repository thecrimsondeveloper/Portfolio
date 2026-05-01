{
  "restated_request": "Generate the ArcadeBuilder decision packet for a single quick, cozy 'campfire' dodge game (mechanic: dodge, content: lanterns, depth: quick). Provide decision frame, per-step decisions, runtime choice, game intent, loop plan, theme pack, content contract, schema notes, JSON-ready decisions (game JSON fragment), validation cues, downstream command recommendation, and blockers.",
  "taught_decision_frame": "Prefer existing shared greybox runtime; treat flags as seeds; produce schema-bound JSON only; no new JS or external assets; keep presentation minimal and reusable; quick depth => short sessions (~60s).",
  "per_step_decisions": {
    "01-observe-arcade-state": "Assume shared 'greybox' 2D runtime and existing templates for sprite, entity, spawn rules, and palette; no external assets.",
    "02-expand-seed-flags": "Idea: campfire; Theme: cozy; Mechanic: dodge; Content: lanterns (collectibles) vs embers (hazards); Depth: quick => 60s session target.",
    "03-select-runtime-mode": "greybox (2D, top-layer sprite support, deterministic physics-lite).",
    "04-plan-game-loop": "Player moves left/right to avoid falling embers and collect lanterns. Survive until timer ends or until health depletes. Score from lanterns + survival time. Difficulty ramps by spawn rate.",
    "05-plan-theme-pack": "Warm palette, soft UI, cozy labels (Campfire, Lantern), minimal chrome, single-screen layout centered on campfire zone.",
    "06-plan-content-contract": "Entities: player, ember (hazard), lantern (collectible), emberShower (spawn controller). Each entity: id, type, position, velocity, hitbox, value/damage, spriteName (built-in).",
    "07-plan-schema-fields": "Require fields: id,title,runtime,mode,controls,dimensions,entities,spawnRules,scoreRules,failConditions,theme,palette. No asset URLs; use built-in sprite keys.",
    "08-fill-json": "Produce schema-bound JSON object (see json_ready_decisions.game_json).",
    "09-repair-json": "Ensure numeric ranges, required arrays present, no nulls, internal sprite keys used, depth mapped to timing fields.",
    "10-build-arcade-entry": "Packet ready for arcade_builder_cli.py to reconcile into arcade_session.json and build artifacts using existing templates.",
    "11-validate-build": "Validation cues provided; run builder's validate step to ensure schema compliance.",
    "12-recommend-next": "Invoke builder 'build' step and run quick smoke test in headless preview."
  },
  "chosen_runtime_mode": "greybox-2d",
  "root_game_intent": "Quick cozy campfire dodge: dodge falling embers, collect lanterns for score, survive a short session (~60s).",
  "game_loop_plan": {
    "core_action": "Move left/right to dodge hazards and collect lanterns.",
    "scoring": "Lantern = +10 points; +1 point per second survived; combo bonus for consecutive lanterns.",
    "fail_state": "Health reaches 0 (3 ember hits) or explicit 'session_end' after max_time.",
    "progression": "Spawn rates increase gradually every 15s; session ends at max_time (quick)."
  },
  "theme_pack": {
    "palette": {
      "bg": "#2E2B2A",
      "accent": "#FFB86B",
      "lantern": "#FFD27F",
      "ember": "#FF6B6B",
      "text": "#F7F1E1"
    },
    "mood": "warm, calm, cozy",
    "labels": {
      "title": "Campfire Lantern Dodge",
      "start": "Sit By Fire",
      "retry": "Relight"
    },
    "ui_constraints": "Single-screen HUD: timer top-center, score top-left, hearts top-right; no external images"
  },
  "content_contract": {
    "player": {
      "id": "player",
      "type": "player",
      "spriteKey": "camper_basic",
      "controls": ["left","right"],
      "speed": 220,
      "hitbox": {"w":32,"h":32},
      "health": 3
    },
    "lantern": {
      "type": "collectible",
      "spriteKey": "lantern_simple",
      "value": 10,
      "spawn": {"minInterval": 1.5,"maxInterval": 4.0,"xRange":"screenWidthPadding"}
    },
    "ember": {
      "type": "hazard",
      "spriteKey": "ember_small",
      "damage": 1,
      "fallSpeedRange": [120,260],
      "spawn": {"baseRatePerSecond": 0.6,"rampFactor": 1.15,"rampEverySeconds":15}
    }
  },
  "schema_notes": {
    "required_fields": ["id","title","runtime","mode","controls","dimensions","entities","spawnRules","scoreRules","failConditions","theme","palette"],
    "field_types": {"entities":"array","spawnRules":"object","scoreRules":"object","palette":"object"},
    "asset_policy": "spriteKey must reference built-in runtime keys; no external URLs permitted",
    "depth_mapping": {"quick":"max_time_seconds=60","short":"max_time_seconds=120","deep":">=180"}
  },
  "json_ready_decisions": {
    "game_json": {
      "id": "campfire-cozy-dodge-quick",
      "title": "Campfire Lantern Dodge",
      "runtime": "greybox-2d",
      "mode": "quick",
      "theme": "cozy-campfire",
      "dimensions": {"width": 960, "height": 540},
      "controls": {"left":"ArrowLeft","right":"ArrowRight","mobile":"touch-drag"},
      "max_time_seconds": 60,
      "player": {
        "id": "player",
        "spriteKey": "camper_basic",
        "speed": 220,
        "hitbox": {"w":32,"h":32},
        "health": 3
      },
      "entities": [
        {
          "type": "ember",
          "spriteKey": "ember_small",
          "damage": 1,
          "fallSpeedRange": [120,260],
          "spawnRule": {"baseRatePerSecond": 0.6, "rampEverySeconds": 15, "rampMultiplier": 1.15}
        },
        {
          "type": "lantern",
          "spriteKey": "lantern_simple",
          "value": 10,
          "spawnRule": {"minInterval": 1.5, "maxInterval": 4.0}
        }
      ],
      "scoreRules": {"perLantern": 10, "perSecondSurvived": 1, "comboWindowSec": 3, "comboMultiplier": 1.25},
      "failConditions": {"healthDepleted": true, "timeExpiryEndsSession": true},
      "presentation": {"palette":{"bg":"#2E2B2A","accent":"#FFB86B","lantern":"#FFD27F","ember":"#FF6B6B","text":"#F7F1E1"}}
    }
  },
  "validation_cues": [
    "Ensure all required fields exist and are correct types per schema_notes",
    "Confirm spriteKey values map to runtime's built-in keys (no URLs)",
    "Numeric ranges: speeds and spawn intervals must be positive and sensible",
    "Arrays (entities) non-empty",
    "Depth-mapped timing applied (max_time_seconds=60 for quick)"
  ],
  "downstream_arcade_command_recommendation": "Invoke arcade builder reconcile+build: python arcade_builder_cli.py reconcile --packet campfire_cozy && python arcade_builder_cli.py build --session campfire_cozy (then run validate step).",
  "blockers": []
}
