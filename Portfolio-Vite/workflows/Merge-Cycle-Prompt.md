# Arcade Cleanup Cycle

A structured, repeatable prompting loop used to review and improve arcade-style games one game at a time while preserving the existing Portfolio-Vite architecture. Each cycle starts by listing the current games, their features, and their issues, then brainstorms safe improvements, then performs one small game-specific cleanup action. Each game must remain separate, self-contained, and individually editable. Each game should stay as a single HTML entry point that references JSON fixture metadata where applicable. Do not create shared modules, shared engines, shared input systems, shared rendering systems, or shared game logic files.

---

## Universal Rule

Keep every arcade game separate. Do not create shared modules. Do not extract shared systems. Do not centralize game logic. Do not refactor unrelated systems. Do not change non-arcade files. Prefer the smallest useful game-specific improvement. It is okay for games to repeat similar code if that keeps them simple, separate, and easy to edit.

---

## To Use Copy and Paste

### 1.

GOAL: List all existing arcade games and describe their current state without making any changes.

THINK ABOUT: each game’s name, entry file, JSON fixture usage, core mechanic, controls, visual style, completion level, missing features, bugs, polish issues, and whether it follows the current arcade expectations.

ACHIEVE BY: scanning the arcade-related files and producing a clear inventory of every game, one by one.

RULE: Keep every arcade game separate. Do not create shared modules. Do not extract shared systems. Do not centralize game logic. Do not refactor unrelated systems. Do not change non-arcade files. Prefer the smallest useful game-specific improvement. It is okay for games to repeat similar code if that keeps them simple, separate, and easy to edit.

ENDING RULE: Do not modify files. Output a game-by-game list with features, issues, missing pieces, and the safest next improvement for each game.

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