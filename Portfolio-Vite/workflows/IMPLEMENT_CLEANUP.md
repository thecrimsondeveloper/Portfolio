Your Goal is to improve/cleanup only the arcade games in my portfolio project so every arcade game is discoverable, launchable, interactive, and playable as a complete game loop.

Only change the arcade games, the arcade game library entries, the JSON fixtures used by the arcade games, and the minimum arcade setup/wiring required to make those games work. Do not change unrelated portfolio sections, unrelated navigation, unrelated visual systems, unrelated components, unrelated pages, or unrelated project features. Do not redesign the whole app. Do not refactor the whole project. Do not rename folders unless a broken reference absolutely requires it. Do not add backend systems. Do not convert the arcade architecture into something larger than it needs to be.

The arcade games are organized in their own folders. Go through the arcade game folders one by one. For each arcade game, verify that it is properly available in the game library and correctly included in the arcade setup. Every arcade game should have a clear arcade/library description, a coherent visual identity, interactive gameplay, and a complete basic gameplay loop. A complete loop means the player can start or enter the game, understand the objective, interact with the game, receive score/win/lose/progress feedback, and restart/replay without manually refreshing the app.

The arcade games should rely on data fixtures stored in JSON. Treat the JSON fixtures as the shared source of truth for arcade metadata, descriptions, game identity, and any lightweight configurable content the games need. The final playable games should each be implemented as one HTML file that references the JSON fixture data rather than hardcoding all metadata directly into scattered code. Each game’s HTML file should be self-contained enough to run the game UI and gameplay loop, but it should pull its structured identity/configuration from the JSON fixture. The JSON should define the arcade/library-facing information clearly enough that the arcade selection interface can show the game consistently and the game itself can read the data it needs. Keep this architecture simple: HTML game files plus JSON fixture data, with only the minimum supporting JS/CSS needed if the current project already expects that pattern.

There is a top-level assets folder in the project. That assets folder is shared among all arcade games. Do not create isolated duplicate asset folders inside every game unless the current structure already requires it. Use the shared top-level assets folder for common arcade visuals, icons, sprites, textures, sounds, or other reusable materials. If an individual game needs a unique asset, place it in the shared assets system in a clean, organized way and reference it from the game. Avoid duplicating the same asset across multiple game folders. Keep asset paths consistent and stable so games do not break when launched from the arcade/library setup.

Each arcade game should have a stronger game identity. For games where the theme is already obvious, refine and reinforce that theme through the description, UI copy, gameplay feedback, colors, labels, and the core loop. For games where the theme is not obvious, choose a fitting style and build it out enough that the game feels intentional instead of placeholder-like. Do not leave vague names, generic button labels, empty descriptions, or unclear objectives. Hone in on what each game is supposed to be. A player should be able to tell what the game is, why it belongs in the arcade, what they are trying to do, and how the interaction creates a satisfying mini-loop.

Use the “lost in the middle” structure intentionally: keep the non-negotiable requirements at the beginning and end of your work plan, and use the middle to absorb all the detailed context. The highest-priority constraints are that only arcade-related files should change, every arcade game should become available/playable through the library and arcade setup, each game should use JSON fixture data, each final game should be one HTML file referencing that JSON, and the shared top-level assets folder should be used consistently across arcade games.

For each arcade game, inspect the current folder and determine the smallest correct improvement path. Do not invent massive new systems. Do not overbuild. Do not turn simple arcade games into complex engines. Add just enough structure, data, styling, and interaction to make each game feel complete and playable. If a game is currently only a static screen, add real interaction. If a game launches but has no ending or feedback, add score/win/lose/restart behavior. If a game is missing from the library, add it to the fixture/library setup. If a game is in the library but cannot launch, fix the launch path. If a game has no clear description, add one. If a game has no clear theme, choose one and make it visible in the game’s identity and loop.

The expected final state is:
- Every arcade game folder has a playable one-HTML-file game.
- Every arcade game is represented in the JSON fixtures.
- Every arcade game can be discovered from the arcade/library UI.
- Every arcade game can be launched from the arcade setup.
- Every arcade game has a clear description.
- Every arcade game has an intentional theme or style.
- Every arcade game has interactive gameplay.
- Every arcade game has a complete loop with start/play/feedback/restart.
- Shared assets are referenced from the top-level assets folder.
- No unrelated portfolio features are changed.

Do not change anything outside the arcade games, arcade setup, arcade library wiring, shared arcade assets, and arcade JSON fixtures unless it is absolutely required to make the arcade games playable.

After editing, output exactly:
1. Which arcade game folders/files changed.
2. Which JSON fixture entries were added or updated.
3. Which shared assets were used or added.
4. What gameplay loop was completed for each arcade game.
5. How each game’s theme/identity was clarified.
6. Why these were the smallest correct changes to make the arcade collection playable.