# Portfolio Architecture

Portfolio is a Vite website with a standalone Arcade wing.

```text
Portfolio
├── .github/workflows/static.yml
├── docs
├── legacy/old-root-site
├── Portfolio-Vite
│   ├── src
│   ├── Pages
│   ├── public/images/projects
│   ├── assets/arcade
│   ├── cli
│   ├── scripts
│   └── workflows
└── memory.md
```

## Canonical App

`Portfolio-Vite` is the active public website. The root legacy site is archived under `legacy/old-root-site` and should not be treated as the current app.

```text
Portfolio-Vite/src
├── app
│   ├── bootstrap.js
│   ├── router.js
│   └── state.js
├── data
│   ├── arcade-projects.js
│   ├── star-store.js
│   └── portfolio
│       ├── index.js
│       ├── profile.js
│       ├── design.js
│       ├── nav.js
│       ├── pages.js
│       └── projects.js
├── ui
└── styles
```

## Deployment

GitHub Pages builds and deploys `Portfolio-Vite/dist`.

```text
push main
└── GitHub Actions
    ├── cd Portfolio-Vite
    ├── npm ci
    ├── npm run build
    └── upload dist
```

## Boundaries

- Keep visual identity in `Portfolio-Vite/src/styles` stable unless the task is explicitly visual.
- Keep route behavior in `Portfolio-Vite/src/app`.
- Edit portfolio content through `Portfolio-Vite/src/data/portfolio`.
- Keep Arcade public files in `Portfolio-Vite/Pages`; do not move existing game folders.
