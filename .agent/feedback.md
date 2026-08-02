# Feedback

Status: open

Record review findings as concrete, surface-specific issues. Include the route,
viewport or command, observed behavior, expected behavior, and evidence path.
Keep generated-output review separate from manually authored portfolio source.

## Open Findings

### Arcade base-path resolution

- Surface: production Arcade navigation and metadata loading
- Observed: selecting Arcade from the `/Portfolio/` landing page navigates to
  the domain root and requests `/Pages/arcade-library.json`, which returns 404.
- Expected: navigation and metadata requests preserve the `/Portfolio/` Pages
  base path.
- Evidence: the intended `/Portfolio/Pages/arcade-library.json` URL returns 200;
  this documentation cycle did not modify application source.
