# Gameplay Presentation Boundary

The public portfolio presents browser-game work through reviewed 15-second
videos, poster images, captions, descriptions, and project-detail pages. It no
longer depends on an embedded Arcade player or the stale Arcade registry for
the visitor journey.

## Public presentation

- Project identity and clean display titles live in
  `Portfolio-Vite/src/data/portfolio/presentation.js`.
- Media is loaded from `VITE_PORTFOLIO_MEDIA_BASE_URL`.
- GitHub Pages reads that value from the `PORTFOLIO_MEDIA_BASE_URL` repository
  variable during the build.
- Every media folder contains `gameplay-15s.webm`, `gameplay-15s.mp4`, and
  `poster.webp`.
- Videos are muted, play only near the viewport, and are limited to two
  simultaneous players.
- Reduced-motion and unavailable-media states show the poster or existing
  project artwork.
- Broken `Pages/...` launch links are removed from presented project data.

## Retained software

`Portfolio-Vite/Pages` and the Arcade tooling remain temporarily in this
repository only because extraction has not yet been completed. Do not delete a
game until its source and playable destination have been copied elsewhere and
verified against the capture manifest.

The retained registry is historical implementation data, not the source of
truth for the public gallery.

## Validation

```bash
cd Portfolio-Vite
npm run build
VITE_PORTFOLIO_MEDIA_BASE_URL=https://media.example.com/portfolio-games \
  npm run start -- --host 127.0.0.1 --port 4174
```

Check that the gallery contains the approved capture count, has no local
playable links, never plays more than two videos, preserves project-detail
navigation, and shows posters when reduced motion is enabled.
