Your Goal is to audit and plan the next arcade upgrade phase, not implement it yet.

Do not edit files. Do not change code. Do not add games. Do not remove games. Do not rewrite the arcade system. This is a planning pass only. Your output should identify the 5 existing arcade games that would benefit most from upgrades, then propose 5 new arcade games that would fit the existing arcade system.

The previous cleanup phase already made the arcade games structurally playable, discoverable, launchable, interactive, and organized around the correct arcade shape. Now the goal is not to fix broken games. The goal is to improve the strongest opportunities, make the arcade feel richer, and plan a better next implementation pass.

Only inspect arcade-related files. Focus on the arcade game folders, arcade setup, arcade library entries, arcade JSON fixtures, shared arcade assets, and the one-HTML-file arcade game implementations. Do not audit unrelated portfolio sections, unrelated pages, unrelated navigation, unrelated styling systems, unrelated components, or unrelated features.

Important current architecture:

Each arcade game should remain discoverable in the arcade/library UI.

Each arcade game should remain represented in the JSON fixtures.

Each arcade game should remain launchable from the arcade setup.

Each game should continue to be implemented as one playable HTML file that references JSON fixture data.

Each game should continue to use JSON fixtures as the source of truth for metadata, description, identity, and lightweight configurable content.

Each game should continue using the top-level shared assets folder when assets are needed.

Do not propose upgrades that require a backend, database, login system, large framework migration, or project-wide refactor.

Do not propose upgrades that break the one-HTML-file game structure.

Do not propose upgrades that require changing unrelated portfolio features.

This is now an UPGRADE PLANNING PASS. Look for games that are technically working but could become more impressive, more replayable, more polished, more memorable, or more portfolio-worthy.

Use the “important information at the edges” structure. Keep the non-negotiable constraints at the beginning and end of your reasoning: this is planning only, only arcade-related files matter, the existing architecture should be preserved, and the output should become a direct checklist for the next implementation prompt.

In the middle of the audit, be extremely thorough. Go game by game and evaluate which existing games have the best upgrade potential. Look for games that could benefit from better pacing, stronger feedback, clearer identity, improved scoring, combo systems, difficulty scaling, visual polish, stronger instructions, small animation passes, better restart/replay hooks, better sound/juice if existing audio patterns support it, stronger JSON-driven content, or more expressive use of shared assets.

Do not list every game. Select exactly 5 existing arcade games that most deserve improvements.

For each of the 5 existing games that need upgrades, output exactly this structure:

GAME TO UPGRADE: [Game name or folder name]

CURRENT STRENGTH:
Describe what already works well about the game after the cleanup phase.

WHY THIS GAME SHOULD BE UPGRADED:
Explain why this game has strong potential, feels under-polished, or would make the arcade feel better if improved.

UPGRADE PRIORITY:
Choose one: Critical Upgrade, High Upgrade, Medium Upgrade, or Polish Upgrade.
Critical Upgrade means the game technically works but still feels weak compared to the rest of the arcade.
High Upgrade means it has strong potential and should be improved soon.
Medium Upgrade means it would benefit from polish but is not urgent.
Polish Upgrade means it is already solid but could become more impressive.

THREE SPECIFIC IMPROVEMENT IDEAS:
1. Give one gameplay improvement that adds replay value without changing the architecture.
2. Give one identity/style/feedback improvement that makes the game feel more memorable.
3. Give one JSON-fixture or shared-asset improvement that makes the game cleaner, more configurable, or better integrated with the arcade.

SMALLEST NEXT IMPLEMENTATION STEP:
Describe the smallest practical edit the next prompt should make first.

EXPECTED FILE AREAS:
List likely file areas the next implementation prompt would touch, such as the game HTML file, JSON fixture entry, arcade metadata, shared assets, or launch/library wiring.

After listing the 5 existing games to upgrade, propose exactly 5 new arcade games that would fit this portfolio arcade.

The new games should feel feasible inside the current architecture:
- One HTML file per game.
- JSON fixture-driven metadata and lightweight configuration.
- Shared top-level assets folder.
- No backend.
- No unrelated app changes.
- Simple arcade loop.
- Clear start/play/feedback/restart loop.
- Strong visual identity.
- Portfolio-friendly concept.

For each proposed new game, output exactly this structure:

NEW GAME IDEA: [Game title]

WHY IT FITS THIS ARCADE:
Explain why this belongs in the current arcade and how it complements the existing games.

THREE-POINT DESCRIPTION:
1. Core gameplay loop.
2. Visual/theme identity.
3. JSON/shared asset needs.

SMALLEST BUILDABLE VERSION:
Describe the smallest version that would still feel like a real playable arcade game.

EXPECTED FILE AREAS:
List the likely new game folder, HTML file, JSON fixture entry, arcade/library wiring, and any shared assets needed.

Also include a project-level summary with these sections:

ARCADE UPGRADE SUMMARY:
Summarize the overall upgrade opportunity.

5 EXISTING GAMES TO IMPROVE:
List the chosen 5 games in recommended implementation order.

5 NEW GAMES TO ADD:
List the chosen 5 new game ideas in recommended implementation order.

COMMON UPGRADE THEMES:
Identify repeated upgrade opportunities across the arcade, such as better difficulty scaling, stronger score feedback, better animations, clearer themes, richer JSON data, more reusable assets, or improved replay loops.

RECOMMENDED NEXT IMPLEMENTATION ORDER:
Give a direct ordered list combining existing upgrades and new additions. Prioritize existing game improvements first unless a new game would be especially fast and valuable.

DO NOT IMPLEMENT YET:
End by clearly stating that no files were changed and that this upgrade plan is ready for the next implementation prompt.

Final non-negotiable reminder: do not edit anything. Do not run broad refactors. Do not change non-arcade files. Do not break the current arcade structure. The only deliverable is a planning list with exactly 5 existing games to improve, 3 improvement ideas for each, exactly 5 new games to add, and a 3-point description for each new game.