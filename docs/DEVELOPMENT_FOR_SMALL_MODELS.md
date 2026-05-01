# Development For Small Models

Use narrow lanes. Pick one lane, edit only its files, then run the matching validation.

```text
Small-model safe lanes
├── Project card
├── Page copy
├── Arcade metadata
├── Project card images
├── CLI/tooling
└── Styling
```

## Safe Lanes

Project cards:

```text
edit: Portfolio-Vite/src/data/portfolio/projects.js
validate: cd Portfolio-Vite && npm run build
```

Page copy and featured slugs:

```text
edit: Portfolio-Vite/src/data/portfolio/pages.js
validate: cd Portfolio-Vite && npm run build
```

Profile, navigation, and design constants:

```text
edit:
├── profile.js
├── nav.js
└── design.js
validate: cd Portfolio-Vite && npm run build
```

Arcade metadata:

```text
edit:
├── Portfolio-Vite/Pages/arcade-library.json
└── Portfolio-Vite/Pages/<game-folder>/<game-slug>.json
validate:
└── open Arcade Library in the browser
```

Project card images:

```text
edit/run:
└── node Portfolio-Vite/scripts/generate-project-card-images.mjs
output:
└── Portfolio-Vite/public/images/projects
```

CLI/tooling:

```text
edit: Portfolio-Vite/cli
avoid: Portfolio-Vite/src/ui and Portfolio-Vite/src/styles
```

Styling:

```text
edit one CSS file at a time:
├── tokens.css
├── themes.css
├── shell.css
├── pages.css
└── components.css
validate with browser screenshot
```

## Never

```text
Never
├── move Arcade game folders
├── rewrite the visual identity accidentally
├── edit generated dist files
├── commit local agent state
├── mix CLI run logs with source edits
├── change deploy workflow and UI in one unverified batch
└── use root legacy files as the active app
```

## Default Validation

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite
npm run build
npm run start -- --host 127.0.0.1 --port 4174
```

Then check:

- landing
- Full Stack
- Game Dev / XR
- Arcade Library
- Arcade player
