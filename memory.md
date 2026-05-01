# Repo Shape
Portfolio is a Vite-first portfolio workspace: `Portfolio-Vite` is the canonical public app, `Portfolio-Vite/Pages` is the stable Kongregate-style Arcade wing, `Portfolio-Vite/cli` owns deterministic generation/orchestration tooling, `legacy/old-root-site` archives the old root site, and root-level docs explain architecture, arcade boundaries, tooling, and small-model edit lanes.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve Vite visual identity, keep Arcade folder URLs stable, and keep CLI/tooling available but separated from generated run state.
- Nav rule now in effect: visible header tabs end with `Arcade Library` then `Arcade`; `Settings` stays separate as the floating button.
- Image overhaul request is active: audit every tab image, replace weak placeholders with stronger art, and shift cards toward thinner, more vertical media with more whitespace.
- Source issue found during audit: `pages['full-stack'].featuredProjectSlugs` includes `a-tiny-rhythm-meter-prototype`, but that slug is missing from `src/data/portfolio/projects.js`.
- Current image truth: section tabs use `projects.js` images; dedicated arcade metadata JSONs still have 0 `image` values across 10 entries, so the arcade player/library metadata surfaces still fall back to text shells.
- Next: if implementing the overhaul, fix the missing slug first, then replace weak SVG project art and tighten card media aspect ratios in section, detail, and arcade card CSS.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve Vite visual identity, keep Arcade folder URLs stable, and keep CLI/tooling available but separated from generated run state.
- Current local run state: `Portfolio-Vite` dev server is running at `http://127.0.0.1:4174/` via `npm run start -- --host 127.0.0.1 --port 4174`.
- Validation for run command: local HTTP probe returned `200 OK`, so the refactored app is serving correctly from the canonical Vite root.
- Next: if the user asks for browser review or screenshots, use the live Vite URL instead of legacy root files.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Main goals: preserve Vite visual identity, keep Arcade folder URLs stable, and keep CLI/tooling available but separated from generated run state.
- Current state: refactor pass is implemented with docs, deploy workflow, split data modules, CLI path cleanup, ignored generated state, and legacy root archive.
- Validation proof remains: Vite build, Python compile, arcade JS syntax checks, image generator, arcade manifest path check, and Playwright page sweep passed after fixing `arcade-runtime.js`.
- Next: if staging/pushing, stage intentional generated-state deletions separately from source changes so the cleanup is easy to review.

## #SELF REMINDERS
- Keep replies short, direct, and action-oriented.
- Vite refactor implemented: root legacy site archived to `legacy/old-root-site`, GitHub Pages now builds `Portfolio-Vite/dist`, and `Portfolio-Vite/src/data/portfolio/` owns split profile/design/nav/pages/projects modules.
- Arcade remains a Kongregate-style wing under `Portfolio-Vite/Pages`; do not move game folders, only harden manifests/runtime/docs around stable paths.
- CLI is self-contained under `Portfolio-Vite/cli`; tracked source stays in command files/schemas/templates/state `arcade_steps.json`, while generated session/report/queue/runs are ignored.
- Validation proof: `npm run build`, Python `py_compile`, `node --check` arcade runtime/bootstrap, image generator, manifest path check, and Playwright page sweep all passed; fixed `content` reference bug in `arcade-runtime.js`.
- Next: if staging/pushing, expect many staged deletions for previously tracked generated CLI packets plus `.DS_Store`; this is intentional cleanup.
