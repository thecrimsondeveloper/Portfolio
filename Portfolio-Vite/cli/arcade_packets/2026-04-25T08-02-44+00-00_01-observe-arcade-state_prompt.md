# ArcadeBuilder Work Packet

packet_kind: prompt
packet_status: pending
time: 2026-04-25T08:02:44+00:00
step: 01-observe-arcade-state
module: arcade
title: Observe Arcade State

## Goal

Inspect existing Arcade runtime, schemas, templates, pages, and portfolio data before choosing work.

## Worker Prompt

Restate this packet literally.

Workspace:
- /Users/crimsonwheeler/Documents/GitHub/Portfolio

Arcade flags:
- idea: ['Neon Courier', 'Clockwork Orchard', 'Echo Drift', 'Rubble Rally', 'Glyph Guard']
- theme: ['Cyberpunk street deliveries, neon city', 'Steampunk automated orchard, clockwork plants', 'Minimalist sonar navigation in misty caverns', 'Post-collapse demolition derby arena', 'Arcane runes defending a ruined keep']
- mode: auto
- tone: auto
- mechanic: ['Timed route with momentum movement, one-button dash and obstacle avoidance', 'Rotate/align tiles to harvest combos; limited moves, cascade scoring', 'Blind top-down navigation using periodic pings; momentum drift and checkpoint racing', 'Short-round physics brawls: bump, stun, pickup upgrades; last-car wins', 'Wave shooter with fast rune-matching to trigger abilities and buffs']
- content: ['Single-screen routes, procedurally placed delivery nodes, small sprite set, 60–120s runs; deterministic RNG', '8×8 grid, 4 tile types, single spritesheet, clear combo rules, no external assets required', 'Top-down polygon obstacles, ping-sound feedback, simple AI obstacles, leaderboards-ready', 'Modular arena templates, 6 vehicle stat tiers, pickup pool, round timer, local multiplayer-ready', 'Finite rune set (3 slots), short enemy wave templates, visual-only glyph UI, paused-power balancing']
- depth: full

Current step:
- 01-observe-arcade-state
- Inspect existing Arcade runtime, schemas, templates, pages, and portfolio data before choosing work.

Packet prompt:
Report what is true now, what is blocked, and the smallest next useful ArcadeBuilder improvement. Do not edit files.

Return only:
- restated packet
- expansion domains
- candidate branches
- assumptions
- blockers
- validation cues
- downstream inputs

Do not edit files.
Do not choose final implementation unless this packet explicitly asks for reconciliation.
Treat Copilot output as candidate material, not truth.

