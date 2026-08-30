# Portfolio Architecture

Portfolio is a Vite presentation website with externally hosted gameplay media.

```text
Portfolio
├── .github/workflows/static.yml
├── docs
├── legacy/old-root-site
├── Portfolio-Vite
│   ├── src
│   ├── Pages (temporary retained software)
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
- Keep project descriptions, titles, captions, and media URLs in the Vite
  presentation layer.
- Keep gameplay videos outside repository history and configure their public
  origin with `VITE_PORTFOLIO_MEDIA_BASE_URL`.
- Treat `Portfolio-Vite/Pages` as temporary retained software until every game
  has a verified external destination; remove it only in the extraction phase.
