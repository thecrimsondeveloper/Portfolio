Your Goal is to implement the arcade upgrade plan using the previous planning output as the source of truth.

Only change arcade-related files. Only touch the existing arcade game folders selected for improvement, the new arcade game folders being added, arcade JSON fixtures, arcade/library setup, launch wiring, and shared top-level arcade assets when needed. Do not change unrelated portfolio sections, unrelated navigation, unrelated pages, unrelated visual systems, unrelated components, unrelated project features, or unrelated assets.

Use the previous upgrade planning output directly. It should contain exactly 5 existing arcade games to improve and exactly 5 new arcade games to add. Follow that plan in priority order.

Preserve the current arcade architecture:

Each arcade game should be discoverable in the arcade/library UI.

Each arcade game should be represented in the JSON fixtures.

Each arcade game should launch correctly from the arcade setup.

Each final game should be implemented as one playable HTML file that references JSON fixture data.

Each game should use JSON fixtures as the source of truth for metadata, description, identity, and lightweight configurable content.

Each game should use the top-level shared assets folder when assets are needed.

Do not add a backend.

Do not add a database.

Do not introduce a major framework migration.

Do not rewrite the whole arcade.

Do not create duplicate per-game asset folders unless the current project already requires that pattern.

Do not break games that already work.

This is an upgrade implementation pass, not a cleanup audit. The arcade should already be in the correct structure. Your job is to make the selected games better and add the selected new games in the same style and architecture.

For the 5 existing games selected in the plan:

Implement the smallest meaningful improvement set for each game.

Each upgraded existing game should receive:
1. One gameplay improvement that adds replay value or clearer interaction.
2. One identity/style/feedback improvement that makes the game feel more memorable.
3. One JSON-fixture or shared-asset improvement that makes the game cleaner, more configurable, or better integrated with the arcade.

Do not overbuild. Do not turn the games into complex engines. Keep the changes small, playable, and portfolio-friendly. Each existing game should still be understandable quickly, launch quickly, and replay quickly.

For the 5 new games selected in the plan:

Create each new game using the existing arcade pattern.

Each new game should have:
1. A dedicated game folder if that is how the arcade is currently organized.
2. One playable HTML file.
3. A JSON fixture entry with title, description, identity/theme, launch path, and any lightweight configuration needed.
4. Arcade/library visibility.
5. A complete loop with start, play, score/progress/win/lose feedback, and restart/replay behavior.
6. A clear theme and visual identity.
7. Shared top-level assets if assets are needed.

The new games should be small but real. They should not feel like placeholders. A player should immediately understand the objective, interact with the game, receive feedback, and be able to replay.

Use the “important information at the edges” structure while working. The non-negotiables are: only arcade-related files, preserve the JSON fixture + one-HTML-file architecture, improve exactly the 5 selected existing games, add exactly the 5 selected new games, use shared assets consistently, and do not change unrelated portfolio features.

Implementation rules:

Work game by game.

Do not skip a planned game unless a file is missing in a way that makes the plan impossible. If that happens, explain it clearly in the final output.

Keep paths stable.

Keep naming consistent with the current arcade.

Use existing arcade conventions whenever possible.

Prefer small direct edits over broad abstractions.

Prefer JSON-driven metadata over hardcoded scattered metadata.

Prefer simple reusable shared assets over duplicated assets.

Make sure every changed or added game still launches from the arcade/library setup.

After editing, verify the final arcade state as much as possible from the code structure:

Each of the 5 upgraded existing games still appears in the arcade/library setup.

Each of the 5 new games appears in the arcade/library setup.

Each changed or added game has a JSON fixture entry.

Each changed or added game has a playable one-HTML-file implementation.

Each changed or added game has a clear start/play/feedback/restart loop.

Each changed or added game has a clear theme or identity.

No unrelated portfolio files were changed unless absolutely required for arcade launch wiring.

After editing, output exactly:

1. EXISTING GAMES UPGRADED
For each of the 5 existing games:
- Game name.
- Files changed.
- Gameplay improvement added.
- Identity/style/feedback improvement added.
- JSON/shared asset improvement added.
- Why this was the smallest correct upgrade.

2. NEW GAMES ADDED
For each of the 5 new games:
- Game name.
- Files added.
- JSON fixture entry added.
- Core gameplay loop.
- Visual/theme identity.
- Shared assets used or added.
- Why this fits the arcade.

3. ARCADE WIRING UPDATED
List any arcade/library setup files, launch paths, or fixture files changed.

4. SHARED ASSETS USED OR ADDED
List shared assets used or added and explain why they are shared instead of duplicated.

5. VALIDATION SUMMARY
Confirm that the selected upgraded games and new games are discoverable, launchable, interactive, JSON-represented, and playable as one-HTML-file arcade games.

6. SMALLEST CHANGE JUSTIFICATION
Explain why the work stayed within the arcade system and avoided unrelated refactors.

Final non-negotiable reminder: only implement the 5 existing game upgrades and 5 new game additions from the prior plan. Do not change unrelated portfolio sections. Do not redesign the app. Do not rewrite the arcade architecture. Keep every game aligned with the JSON fixture, one-HTML-file, shared-assets arcade structure.