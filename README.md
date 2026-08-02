# Crimson Wheeler Portfolio

![Crimson Wheeler portfolio overview](docs/assets/brand/cover-1280x640.png)

This repository contains Crimson Wheeler's public technical portfolio: systems
architecture, full-stack delivery, automation, game and XR development, and a
browser Arcade of small playable experiments.

**Live site:** [thecrimsondeveloper.github.io/Portfolio](https://thecrimsondeveloper.github.io/Portfolio/)

## Active Surfaces

- `Portfolio-Vite/` is the canonical public application.
- `Portfolio-Vite/Pages/` is the browser Arcade wing and owns the existing game
  route structure.
- `Portfolio-Vite/cli/` contains deterministic portfolio and Arcade tooling.
- `ChatHub-Harness/` is a prompt-gated generation harness whose reviewed output
  is isolated on the `ChatHub-Output` branch.
- `legacy/old-root-site/` preserves the historical root implementation and is
  not the active application.

## Run Locally

```bash
cd Portfolio-Vite
npm install
npm run build
npm run start -- --host 127.0.0.1 --port 4174
```

The production build is written to `Portfolio-Vite/dist/` and is not committed.

## Repository Map

```text
Portfolio
├── Portfolio-Vite
│   ├── src                 canonical portfolio application
│   ├── Pages               public Arcade routes and games
│   ├── public/images       portfolio and Arcade media
│   └── cli                 deterministic builder and orchestration tools
├── ChatHub-Harness         prompt-gated agent workflow source
├── docs                    architecture and maintainer guidance
├── legacy/old-root-site    archived previous implementation
└── .github/workflows       Pages and ChatHub automation
```

## Deployment

The repository's default branch is `development`. The Pages workflow builds
`Portfolio-Vite` and can include reviewed output from `ChatHub-Output` without
turning that generated branch into application source.

The ChatHub harness requires an intentional prompt and configured provider
credentials. Generated results remain review output and should not be treated as
manually authored portfolio source.

## Documentation

- [Documentation index](docs/README.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Arcade boundaries](docs/ARCADE.md)
- [Tooling](docs/TOOLING.md)
- [Small-model development lanes](docs/DEVELOPMENT_FOR_SMALL_MODELS.md)
- [Visual identity](docs/visual-identity.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

No license grant is currently declared at the repository root.
