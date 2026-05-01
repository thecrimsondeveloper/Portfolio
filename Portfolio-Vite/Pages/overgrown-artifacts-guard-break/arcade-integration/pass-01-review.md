# Arcade Integration Review Pass 01

## Observed Pattern

- Arcade player and library load entries from Pages/arcade-library.json.
- Each entry needs slug, title, section, pagePath, and metadataPath.
- Per-game metadata JSON is loaded from metadataPath and supplies title and optional image data for arcade UI surfaces.
- A generated game only needs a live page folder, a metadata JSON file, and a manifest entry to become selectable in the arcade player and library.

## Required Files

- Pages/arcade-library.json
- Pages/overgrown-artifacts-guard-break/overgrown-artifacts-guard-break.json
- Pages/overgrown-artifacts-guard-break/index.html
- Pages/overgrown-artifacts-guard-break/story-structure.json

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

## Gaps

- No integration gaps remain.
