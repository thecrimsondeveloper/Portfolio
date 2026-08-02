# Contributing

## Start Here

Read [AGENTS.md](AGENTS.md), [memory.md](memory.md), the `.agent` workspace, and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) before changing the repository.

## Choose One Surface

- Portfolio content: `Portfolio-Vite/src/data/portfolio/`
- Application routing and state: `Portfolio-Vite/src/app/`
- Interface styling: `Portfolio-Vite/src/styles/`
- Arcade metadata and games: `Portfolio-Vite/Pages/`
- Builder and orchestration tools: `Portfolio-Vite/cli/`
- Prompt-gated agent workflow: `ChatHub-Harness/`

Do not combine unrelated surfaces in one pull request. Preserve Arcade folder
names and public URLs. Do not use the legacy root site as current application
source.

## Validation

Run the canonical build:

```bash
cd Portfolio-Vite
npm run build
```

For visual or interaction changes, start the local app and inspect the affected
routes at desktop and mobile widths. For tooling or ChatHub changes, run the
focused command with local/mock inputs and preserve sanitized evidence.

Do not commit `dist/`, dependency folders, browser profiles, local environment
files, provider credentials, generated run packets, or private paths.
