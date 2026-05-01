# Arcade Integration Spec

## Initial Review Gaps

- No initial integration gaps were found after the repaired metadata refresh.

## Observed Pattern

- Arcade player and library load entries from Pages/arcade-library.json.
- Each entry needs slug, title, section, pagePath, and metadataPath.
- Per-game metadata JSON is loaded from metadataPath and supplies title and optional image data for arcade UI surfaces.
- A generated game only needs a live page folder, a metadata JSON file, and a manifest entry to become selectable in the arcade player and library.

## Required Files

- Pages/arcade-library.json
- Pages/rooftop-while-guard-break/rooftop-while-guard-break.json
- Pages/rooftop-while-guard-break/index.html
- Pages/rooftop-while-guard-break/story-structure.json

## Required Fields

- slug
- title
- section
- pagePath
- metadataPath
- metadata.title
- metadata.instructions

## Invariants

- Keep pagePath rooted at Pages/<slug>/ so the arcade iframe can load the generated page directly.
- Keep metadataPath inside the generated page folder so the library can resolve game-specific metadata without extra routing.
- Do not require direct edits to arcade UI code when a new entry follows the manifest and metadata pattern.

## Open Gaps

- No open integration gaps remain.

## Registration Changes

- Refreshed /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages/rooftop-while-guard-break/rooftop-while-guard-break.json so arcade instructions and overlay copy match the repaired stealth uplink loop.
- Preserved the existing rooftop-while-guard-break manifest entry in /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages/arcade-library.json.

## Verification Notes

- Arcade library manifest resolves the rooftop-while-guard-break entry.
- Arcade metadata file exists at /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages/rooftop-while-guard-break/rooftop-while-guard-break.json.
- Generated page contains index.html and story-structure.json for arcade launch.
- The page boots over HTTP at Pages/rooftop-while-guard-break/ and clears its intro overlay without runtime errors.

## Continue Gate

- Stop
