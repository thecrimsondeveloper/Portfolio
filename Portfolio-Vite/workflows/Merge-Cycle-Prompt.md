# Arcade Cleanup Cycle

A structured, repeatable prompting loop used to review and improve arcade-style games one game at a time while preserving the existing Portfolio-Vite architecture. Each cycle starts by listing the current games, their features, and their issues, then brainstorms safe improvements, then performs one small game-specific cleanup action. Each game must remain separate, self-contained, and individually editable. Each game should stay as a single HTML entry point that references JSON fixture metadata where applicable. Do not create shared modules, shared engines, shared input systems, shared rendering systems, or shared game logic files.

---

## Universal Rule

Keep every arcade game separate. Do not create shared modules. Do not extract shared systems. Do not centralize game logic. Do not refactor unrelated systems. Do not change non-arcade files. Prefer the smallest useful game-specific improvement. It is okay for games to repeat similar code if that keeps them simple, separate, and easy to edit.

---

## To Use Copy and Paste

### 1.

Goal: Create a read-only inventory of every existing arcade game and describe each one as its own separate player experience, without editing files or running commands.

Thinking chain:
First, identify each arcade game by its entry file and JSON fixture.
Then, describe the actual gameplay: core mechanic, player action, controls, win/fail condition, and visual identity.
Then, judge what makes that game distinct, what feels unfinished, what may be broken, and what is only conceptually duplicated from other games.
Then, estimate current playtime and explain what drives that playtime: score chasing, survival, escalation, collection, replayability, full loop, or story/progression.
Then, choose one smallest safe game-specific improvement for that game only.

Sequential output plan:
1. Read arcade files directly only.
2. Do not run terminal commands, Python snippets, MCP tools, scripts, tests, build tools, package commands, or workspace automation.
3. Keep every arcade game separate.
4. Do not create shared modules, shared systems, shared game logic, or merged frameworks.
5. Use similarity only for comparison, not as a reason to refactor.
6. Output every game with these fields: game name, entry file, JSON fixture, core mechanic, controls, estimated playtime, playtime driver, loop/story assessment, strengths, issues, missing gameplay/polish, and safest next game-specific improvement.
7. If a complete inventory cannot be made from direct file reading, stop and ask for permission before using any execution tool.

### 2.

GOAL: Brainstorm improvements for the existing arcade games without making any changes.

THINK ABOUT: which games feel unfinished, which games need polish, which games need clearer controls, which games need better JSON fixture usage, which games need visual upgrades, and which games would benefit from small isolated improvements.

ACHIEVE BY: choosing the most relevant games from the inventory and listing practical improvement ideas for each one.

RULE: Keep every arcade game separate. Do not create shared modules. Do not extract shared systems. Do not centralize game logic. Do not refactor unrelated systems. Do not change non-arcade files. Prefer the smallest useful game-specific improvement. It is okay for games to repeat similar code if that keeps them simple, separate, and easy to edit.

ENDING RULE: Do not modify files. Output a ranked improvement plan with one section per game, including three possible improvements per selected game.

### 3.

GOAL: Choose one game and plan one small isolated cleanup action.

THINK ABOUT: the current game inventory, the brainstormed improvement list, the safest useful change, the game’s existing structure, and how to improve only that game without affecting any other game.

ACHIEVE BY: selecting one arcade game and describing one specific change that can be made inside that game’s own files.

RULE: Keep every arcade game separate. Do not create shared modules. Do not extract shared systems. Do not centralize game logic. Do not refactor unrelated systems. Do not change non-arcade files. Prefer the smallest useful game-specific improvement. It is okay for games to repeat similar code if that keeps them simple, separate, and easy to edit.

ENDING RULE: Do not modify files. Output the chosen game, the exact issue being targeted, the exact intended change, the files expected to change, and why this is the smallest safe next step.

### 4.

GOAL: Perform one small isolated cleanup action for one arcade game.

THINK ABOUT: the chosen game, the planned change, that game’s single HTML entry point, its JSON fixture metadata if applicable, and preserving all other games exactly as they are.

ACHIEVE BY: editing only the files needed for that one game-specific improvement.

RULE: Keep every arcade game separate. Do not create shared modules. Do not extract shared systems. Do not centralize game logic. Do not refactor unrelated systems. Do not change non-arcade files. Prefer the smallest useful game-specific improvement. It is okay for games to repeat similar code if that keeps them simple, separate, and easy to edit.

ENDING RULE: Report exactly which game changed, which files changed, what issue was improved, what behavior should remain unchanged, and what the next safest game-specific cleanup action is.