restated request:
- Simulate the full ArcadeBuilder worker chain and return a single structured ArcadeBuilder reply packet for flags {idea: swarm, theme: acid, mode: auto, tone: auto, mechanic: weave, content: drones, depth: full} — inspect repo state (observed), expand flags, choose runtime, plan loop, theme, contract, produce schema-bound JSON decisions, validation cues, next command, and blockers.

taught decision frame:
- Prefer existing shared runtimes/templates and arcade-assets.json palette/sprites.
- Treat tiny flags as seeds (map "acid" → closest existing palette).
- Keep all behavior expressed in schema-bound JSON; do not add runtime JS.
- Use greybox visuals & existing sprites (sentryDrone).
- Preserve user intent: swarm + weave + drones.

per-step decisions:
01-observe-arcade-state
- Found Portfolio-CLI with arcade_session.json, arcade_steps.json, arcade_run.md, arcade_builder_cli.py; Portfolio-Vite/Pages contains arcade-assets.json, arcade-runtime.js, bootstrap.
- Confirmed shared palettes and sprites; sentryDrone sprite exists.

02-expand-seed-flags
- Compact intent: "Weave through a hostile drone swarm (acid neon), single-screen survival microgame with increasing density and patterned drone paths."

03-select-runtime-mode
- Chosen runtime mode: auto (flag). This maps to shared Arcade greybox runtime (initArcadeGame + JSON config). No new runtime created.

04-plan-game-loop
- Player action: steer avatar to weave through moving drones (continuous 2D movement).
- Feedback: collision flash + score penalty; near-miss particles; HUD score + multiplier.
- Scoring: time-survived + near-miss bonus + weaving through lanes (combo multiplier).
- Fail state: collision with drone -> lose life; 0 lives -> game over.
- Progression: wave-based density growth every 20s, with intermittent "weave corridors" (safe paths) that shift.
- Controls: arrow keys / WASD, single action key none required (weave = movement).

05-plan-theme-pack
- Palette: map "acid" → existing palette "orbit" (closest neon/green accent).
- VibeWords: ["acid","neon","toxic","hazy"]
- SurfaceStyle: "semi-transparent neon surfaces"
- Accent tweak: accentStrong biased toward neon green for UI highlight.
- Labels: title "SWARM: Weave", HUD labels: SCORE, MULT, LIVES, TIME.
- Presentation constraints: greybox shapes, no external images; reuse sentryDrone sprite.

06-plan-content-contract
- Reusable content objects (JSON shapes):
  - player: {id, sprite, radius, speed, lives, startPos}
  - drone: {id, sprite:"sentryDrone", pathType:"weave"|"orbit"|"line", speed, spawnDelay, hp:1, collisionRadius}
  - wave: {timeOffset, dronePatterns: [{type, count, spacing, pathParams}]}
  - spawnRules: {baseRate, densityRamp, maxActive}
  - scoreRules: {survivalRate, nearMissDistance, nearMissBonus, weaveComboWindow}
  - ui: {hudFields: ["score","multiplier","lives","time"]}
  - metadata: {slug, title, description, runtime:"auto", palette:"orbit", seeds: {idea,theme,mechanic,content}}
- Express path patterns as parametric curves (type + amplitude/frequency) in JSON, not JS.

07-plan-schema-fields
- Minimal required fields (align with existing brief/game pattern):
  - slug (string, url-safe)
  - title (string)
  - summary/description (string)
  - runtime.mode (string)
  - theme.palette (string referencing arcade-assets.json palettes)
  - assets.sprites (list of referenced sprite keys present in arcade-assets.json)
  - gameplay: {player, spawnRules, waves, scoring, ui}
  - controls: {movement: "analog"|"digital"}
  - bucket: tags/flags
- Gaps: no new schema fields required; ensure waves/drone path params conform to existing numeric types.

08-fill-json (JSON-ready game object)
{
  "slug": "swarm-weave-acid",
  "title": "SWARM: Weave",
  "description": "Weave through an acid-neon drone swarm. Survive waves, rack near-miss combos, and outlast escalating density.",
  "runtime": {
    "mode": "auto",
    "canvasSelector": "#game",
    "assetsPath": "./arcade-assets.json"
  },
  "theme": {
    "palette": "orbit",
    "vibeWords": ["acid","neon"],
    "accentOverride": "#7bf1a8"
  },
  "assets": {
    "sprites": ["sentryDrone","runnerShip","orbNode"]
  },
  "gameplay": {
    "player": {
      "id": "pilot",
      "sprite": "runnerShip",
      "radius": 14,
      "speed": 220,
      "lives": 3,
      "startPos": {"x": 0.5, "y": 0.85}
    },
    "spawnRules": {
      "baseRate": 0.9,
      "densityRamp": 0.12,
      "maxActive": 48
    },
    "dronePrototype": {
      "sprite": "sentryDrone",
      "collisionRadius": 12,
      "hp": 1,
      "pathTypes": ["weave","orbit","line"]
    },
    "waves": [
      {"time": 0, "patterns":[{"type":"weave","count":8,"speed":120,"amplitude":0.12,"freq":1.0}]},
      {"time": 20, "patterns":[{"type":"weave","count":12,"speed":150,"amplitude":0.18,"freq":1.2}]},
      {"time": 40, "patterns":[{"type":"orbit","count":10,"speed":140,"radius":0.25}]},
      {"time": 60, "patterns":[{"type":"weave","count":18,"speed":180,"amplitude":0.22,"freq":1.4}]}
    ],
    "scoring": {
      "survivalPerSecond": 1,
      "nearMissDistance": 28,
      "nearMissBonus": 5,
      "weaveComboWindow": 2.5
    },
    "ui": {
      "hudFields": ["score","multiplier","lives","time"],
      "startOverlay": {"title":"SWARM: Weave","copy":"Weave through the drones. Survive as long as possible."}
    },
    "controls": {"movement":"digital"}
  },
  "tags": ["swarm","weave","drones","acid","neon"]
}

09-repair-json
- If validator rejects "accentOverride", fallback: remove accentOverride and rely on palette:"orbit".
- If validator requires numeric ranges, clamp speeds to integers and amplitudes [0,1].
- If sprites referenced but missing, map to available alternatives or remove sprite keys.

validation cues:
- Ensure slug uniqueness (check existing built slugs in Portfolio-CLI session).
- Verify referenced sprites exist in Portfolio-Vite/Pages/arcade-assets.json (sentryDrone exists).
- Confirm palette:"orbit" exists (present).
- Check numeric ranges (speeds, counts, maxActive) acceptable to runtime schema.
- No new JS fields or asset paths introduced.
- Confirm runtime.mode "auto" is accepted by pick_fallback_mode and build pipeline.

chosen runtime mode:
- auto (shared initArcadeGame JSON-driven runtime; no code changes).

JSON-ready decisions:
- Use game JSON above as the build input (file: Portfolio-CLI/game_jsons/swarm-weave-acid.json when building).
- Use assetsPath "./arcade-assets.json" and sprite keys only (no external assets).
- Mark package as ready for validate → build.

downstream ArcadeBuilder command recommendation:
- Plan/preview: python3 Portfolio-CLI/arcade_builder_cli.py --idea swarm --theme acid --mechanic weave --content drones --depth full --plan-only
- Validate JSON: python3 Portfolio-CLI/arcade_builder_cli.py --idea swarm --theme acid --mechanic weave --content drones --depth full --validate
- Build (if validate passes): python3 Portfolio-CLI/arcade_builder_cli.py --idea swarm --theme acid --mechanic weave --content drones --depth full --build

blockers:
- Palette "acid" not present; mapped to "orbit" — confirm acceptance.
- Ensure sprites referenced (runnerShip, sentryDrone) are present in arcade-assets.json; if missing, build will fail.
- File-permission issues or copilot absence are non-blocking for manual build but were observed in run memory; ensure write permissions for Portfolio-CLI and PACKETS_DIR.
- Git dirty worktree will block build (arcade_builder_cli.py checks for unexpected dirty status).
- If schema strictly disallows path paramization, waves/path patterns may need to be simplified to explicit spawn lists.

validation cues (short checklist):
- [ ] slug unique
- [ ] sprites present in arcade-assets.json
- [ ] palette "orbit" exists
- [ ] numeric ranges valid
- [ ] no external assets referenced

end of packet.
