# Arcade Integration Review Pass 02

## Observed Pattern

- Arcade player and library load entries from Pages/arcade-library.json.
- Each entry needs slug, title, section, pagePath, and metadataPath.
- Per-game metadata JSON should describe the live game loop, not a stale prior scaffold.

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

- Keep pagePath rooted at Pages/<slug>/ so the arcade iframe can load the page directly.
- Keep metadataPath in the generated page folder.
- Do not touch unrelated arcade UI code when the existing manifest pattern already works.

## Gaps

- No integration gaps remain after refreshing the per-game metadata copy.