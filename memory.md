# Repo Shape
Portfolio is a two-track workspace: `Portfolio-CLI` for deterministic prototype generation and `Portfolio-Vite` for the live site, with Arcade using shared shells, per-game JSON-driven flow definitions, `arcade_builder_cli.py` as the deterministic packet/build owner, `mini_arcade_orchestrator_cli.py` as the GPT-5 Mini batch/single-run orchestrator, and `Portfolio-CLI/MiniArcadeControl` as the local horizontal queue website with one prompt, Go, optional idea loop, and color-state cards.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Root `.gitignore` now ignores local agent/runtime state, env files, Python/Node build outputs, and non-public screenshot captures.
- Ignored proof checked with `git check-ignore -v` for `.copilot-local`, `.playwright-mcp`, `.codex-screens`, `.nexus-link`, Vite `node_modules/dist/.env`, and root screenshots.
- Tracked `.DS_Store` still appears modified because ignore does not untrack already tracked files; remove from index before push if user approves cleanup.
- Next: decide whether to stage `.gitignore` only or also remove tracked `.DS_Store` and resolve deleted `Pages/dragon.html`.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Current git-tracked repo is still legacy root site only: `.github/workflows/static.yml`, `index.html`, `styles.css`, `app.js`, `.DS_Store`, and `Pages/dragon.html`.
- `Portfolio-Vite/` is the real current app shape but is untracked; clean push needs explicit include/ignore decisions before staging.
- Cleanup priority before push: ignore/remove local state folders, `.DS_Store`, `.env`, build outputs, screenshots, and decide whether deleted `Pages/dragon.html` is intentional.
- Next: if user says clean it, add root `.gitignore`, preserve `Portfolio-Vite` source/public/Pages/cli/workflows, exclude runtime/generated folders, then show a staged diff.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- `Portfolio-Vite/src/data/portfolio.js` uses `project.image` for list cards, detail art, and arcade/prototype card image surfaces.
- Generated card art lives in `Portfolio-Vite/public/images/projects`; rerun `node Portfolio-Vite/scripts/generate-project-card-images.mjs` after adding projects with empty images.
- Build proof for image pass: `npm run build` passes; only existing Vite large chunk warning remains.
- Next: if user wants richer art, replace the generated SVGs with custom bitmap renders while preserving the same `/images/projects/<slug>.*` paths.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Verify the live preview before answering a run request.
- Preserve the explicit-intent gate when small replies leave action unclear.
- Next: keep `127.0.0.1:4173` ready and restart only if the listener drops.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Preserve the explicit-intent gate and ask first when small replies leave action unclear.
- Gemini metallic-water shader port implemented in `star-fishing-scene.js`: render-target refraction, chromatic distortion, FBM normals, Fresnel/specular, click ripples, and star light uniforms.
- Underwater mesh stars are hidden behind water and refracted; surfaced/above stars remain final-pass clear; CDP caught 1 surfaced star after shader port.
- Next: if user wants less intensity, tune shader exposure/specular rather than reverting to simple water.
