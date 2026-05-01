# Arcade Wing

`Portfolio-Vite/Pages` is the portfolio Arcade wing. Treat it like a Kongregate-style games section that belongs to the portfolio but remains separate from the Vite source tree.

```text
Portfolio-Vite/Pages
├── arcade-library.json
├── arcade-assets.json
├── arcade-runtime.js
├── arcade-bootstrap.js
├── arcade-shell.css
├── story-chapter.js
├── arcade
│   ├── docs
│   └── archive
├── lab-rift
├── phase-drop
├── glow-drift
└── other playable game folders
```

## Rules

- Do not move existing Arcade game folders.
- Do not rename game folders without explicit approval.
- Do not move Arcade games into `src`.
- Keep public URLs stable.
- Use `arcade-library.json` as the discoverability manifest.
- Use each game folder's JSON as its metadata/config source.
- Use shared assets from `Portfolio-Vite/assets/arcade` or `Portfolio-Vite/Pages/arcade-assets.json`.

## Game Folder Shape

```text
Pages/<game-folder>
├── index.html
└── <game-slug>.json
```

Some older generated pages may have historical shapes. Preserve paths first, then document or repair wiring without relocating folders.

## Validation

```bash
cd /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite
npm run build
npm run start -- --host 127.0.0.1 --port 4174
```

Check:

- Arcade Library loads.
- Each visible card has a title and image/metadata.
- Launch links resolve under `Pages/...`.
- Arcade player still feels like a standalone game portal.
