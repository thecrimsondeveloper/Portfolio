# Repository Agent Guide

## Purpose

Maintain Crimson Wheeler's public portfolio without confusing the canonical
Vite application, the Arcade wing, local tooling, ChatHub generated output, or
the archived legacy site.

## Read Order

1. `memory.md`
2. `.agent/start-here.md`
3. `.agent/intention.md`
4. `.agent/workflow.md`
5. `docs/ARCHITECTURE.md`
6. the documentation for the selected surface

## Boundaries

- Treat `Portfolio-Vite/` as the canonical public application.
- Preserve every existing route under `Portfolio-Vite/Pages/`.
- Keep application data under `Portfolio-Vite/src/data/portfolio/`, route logic
  under `Portfolio-Vite/src/app/`, and automation under `Portfolio-Vite/cli/`.
- Treat `ChatHub-Output` as generated review output, never as source input.
- Do not edit `legacy/old-root-site/` unless a task explicitly targets history.
- Do not commit generated builds, run packets, browser profiles, local agent
  state, provider credentials, or downloaded dependencies.
- Record lasting decisions in `memory.md` and supported operational changes in
  `.agent/change-log.md`.

## Validation

For canonical application changes:

```bash
cd Portfolio-Vite
npm run build
npm run start -- --host 127.0.0.1 --port 4174
```

Inspect the landing page, portfolio sections, Arcade Library, and one playable
Arcade route. Use focused CLI or ChatHub validation when changing those
surfaces. Keep generated and public evidence clearly distinguished.
