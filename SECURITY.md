# Security Policy

## Scope

This public repository contains a static portfolio, browser games, local
automation tools, and a prompt-gated workflow that can call a configured model
provider and publish generated review output to a separate branch.

## Reporting

Use an existing private contact route for the maintainer before publishing
exploitable details. Do not place credentials, private paths, account data,
provider responses containing sensitive material, or weaponized proof content
in a public issue.

Include the affected commit, repository-relative paths, reproduction steps,
impact, and sanitized evidence.

## Sensitive Boundaries

- Keep model-provider keys in GitHub secrets or local environment variables.
- Require intentional prompt content before ChatHub makes an endpoint call.
- Keep generated ChatHub results isolated on `ChatHub-Output` until reviewed.
- Treat Arcade games and imported media as untrusted browser content until their
  source, license, links, and runtime behavior are reviewed.
- Do not publish `.env` files, browser profiles, local agent state, generated
  run packets, absolute private paths, or deployment credentials.
- Preserve the static site's content-security assumptions when adding external
  scripts, frames, APIs, or media.

Supported-version and response-time commitments are not currently specified.
