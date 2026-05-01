# Arcade Integration Spec

## Initial Review Gaps

- Arcade library entry is missing from Pages/arcade-library.json.
- Arcade metadata file is missing at ancient-puzzles-guard-break.json.

## Observed Pattern

- Arcade player and library load entries from Pages/arcade-library.json.
- Each entry needs slug, title, section, pagePath, and metadataPath.
- Per-game metadata JSON is loaded from metadataPath and supplies title and optional image data for arcade UI surfaces.
- A generated game only needs a live page folder, a metadata JSON file, and a manifest entry to become selectable in the arcade player and library.

## Required Files

- Pages/arcade-library.json
- Pages/ancient-puzzles-guard-break/ancient-puzzles-guard-break.json
- Pages/ancient-puzzles-guard-break/index.html
- Pages/ancient-puzzles-guard-break/story-structure.json

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

- Wrote arcade metadata to /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages/ancient-puzzles-guard-break/ancient-puzzles-guard-break.json.
- Added ancient-puzzles-guard-break to /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages/arcade-library.json.

## Verification Notes

- Arcade library manifest resolves the ancient-puzzles-guard-break entry.
- Arcade metadata file exists at /Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages/ancient-puzzles-guard-break/ancient-puzzles-guard-break.json.
- Generated page contains index.html and story-structure.json for arcade launch.

## Continue Gate

- Stop
