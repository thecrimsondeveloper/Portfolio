Your Goal is to audit and plan the arcade cleanup work, not implement it yet.

Do not edit files. Do not change code. Do not add games. Do not remove games. Do not rewrite the arcade system. This is a planning pass only. Your output should be a massive, detailed cleanup inventory that identifies which arcade games do not currently meet the playable arcade criteria and what each one needs next.

The larger project goal is to make every arcade game in my portfolio discoverable, launchable, interactive, themed, and playable as a complete mini-game loop. The purpose of this prompt is to inspect the current arcade game folders, arcade/library wiring, JSON fixtures, shared assets usage, and game HTML files so the next prompt can use your audit as an implementation checklist.

Only inspect arcade-related files. Focus on the arcade game folders, arcade setup, arcade library entries, arcade JSON fixtures, shared arcade assets, and any one-HTML-file game implementations. Do not spend time auditing unrelated portfolio sections, unrelated pages, unrelated navigation, unrelated styling systems, unrelated components, or unrelated features.

Important current criteria:

Each arcade game should be discoverable in the arcade/library UI.

Each arcade game should be correctly represented in the JSON fixtures.

Each arcade game should launch correctly from the arcade setup.

Each final game should be implemented as one playable HTML file that references the JSON fixture data.

Each game should use JSON fixtures as the source of truth for metadata, description, identity, and lightweight configurable content.

Each game should use the top-level shared assets folder when assets are needed, instead of creating duplicate per-game asset folders.

Each game should have a clear description.

Each game should have a clear theme or visual identity.

Each game should have interactive gameplay, not just a static screen.

Each game should have a complete basic gameplay loop with start, play, score/progress/win/lose feedback, and restart/replay behavior.

Each game should feel intentional enough that a player can understand what it is, what they are trying to do, and why it belongs in the arcade.

The planning goal is to find gaps, not fix them. For every arcade game, inspect whether it meets the criteria above. If a game already meets the criteria, list it under a separate “Likely Complete / Lower Priority” section with a short explanation. If a game does not meet the criteria, list it under “Needs Cleanup” and describe exactly what is missing.

Use the “important information at the edges” structure. Keep the non-negotiable instructions at the beginning and end of your reasoning: this is a planning-only audit, only arcade-related files matter, and the output must become a direct checklist for the next implementation prompt.

In the middle of the audit, be extremely thorough. Go game by game. Look for missing library entries, broken launch paths, missing JSON fixture data, unclear descriptions, unclear themes, duplicated assets, missing shared asset references, static-only screens, no scoring, no start state, no win/lose state, no restart loop, broken controls, confusing instructions, inconsistent naming, or anything else preventing the game from feeling complete.

For each unfinished or incomplete game, output exactly this structure:

GAME: [Game name or folder name]

CURRENT STATUS:
Describe what currently exists. Mention whether the game folder exists, whether there is an HTML file, whether it appears in JSON fixtures, whether it appears in the arcade/library setup, and whether it can likely launch.

MISSING CRITERIA:
List every arcade criterion it currently fails or may fail. Be specific.

CLEANUP PRIORITY:
Choose one: Critical, High, Medium, or Low.
Critical means it is missing from the library, cannot launch, has no playable file, or is basically not a game yet.
High means it launches but lacks a real gameplay loop or core interaction.
Medium means it has some gameplay but needs stronger theme, description, feedback, restart, or fixture cleanup.
Low means it is mostly complete but needs polish or consistency.

THREE GAMEPLAY / IDENTITY IDEAS:
1. Give one practical idea for turning the current concept into a complete small arcade loop.
2. Give a second different idea that uses the same existing identity but creates a clearer interaction or scoring loop.
3. Give a third idea focused on theme, style, player feedback, or replayability.

SMALLEST NEXT IMPLEMENTATION STEP:
Describe the smallest next edit that would move this specific game toward meeting the criteria.

EXPECTED FILE AREAS:
List the likely file areas the next implementation prompt would need to touch, such as the game HTML file, JSON fixture entry, arcade library wiring, launch path, or shared assets folder.

Do not merge games together. List unfinished games one by one. The whole point is to create a clear inventory that the next prompt can consume directly.

Also include a project-level summary with these sections:

ARCADE AUDIT SUMMARY:
Summarize the overall state of the arcade collection.

TOTAL GAMES FOUND:
Give the number of arcade games you found.

LIKELY COMPLETE / LOWER PRIORITY:
List games that seem close to done or already meet the criteria.

NEEDS CLEANUP:
List all games that need cleanup, ordered from most broken to least broken.

COMMON FAILURE PATTERNS:
Identify repeated problems across games, such as missing JSON fixture entries, inconsistent launch paths, static screens, no restart buttons, unclear descriptions, or duplicated assets.

RECOMMENDED IMPLEMENTATION ORDER:
Give the order the next prompt should tackle the games in. Prioritize games that are missing from the library, cannot launch, or lack any playable loop.

DO NOT IMPLEMENT YET:
End by clearly stating that no files were changed and that this audit is ready for the next implementation prompt.

Final non-negotiable reminder: do not edit anything. Do not run broad refactors. Do not change non-arcade files. The only deliverable is a massive, game-by-game planning list of arcade games that do not meet the current criteria, with three ideas per unfinished game so the next prompt can use the audit directly.