# Current Direction

Run the ChatHub-Harness game-build workflow on every development push while keeping the portfolio deployed as the primary static GitHub Pages site.

Goal:

- Always deploy the Portfolio-Vite static site from `development`.
- Always run ChatHub-Harness on `development` pushes.
- Keep the active prompt gate inside the runner so blank prompts still no-op safely.
- Publish generated harness output to `ChatHub-Output`.
- Include the latest ChatHub output inside the static portfolio Pages artifact when available.
- Use only free NVIDIA/build.nvidia.com compatible endpoints.

Playable output target:

```text
ChatHub-Harness/outbox/latest-game.html
```

Review output target:

```text
ChatHub-Harness/outbox/latest-result.md
ChatHub-Harness/outbox/latest-links.md
ChatHub-Harness/outbox/generated-game-spec.json
```

Game direction:

Use the active prompt in `ChatHub-Harness/ideas/active.prompt.md` as the source of game intent. Generate a playable, self-contained browser game directly from the prompt/spec and make it available through the portfolio static site after deploy.

Validation expectation:

- Portfolio root remains the Vite portfolio.
- ChatHub game remains available at `/Portfolio/ChatHub-Harness/outbox/latest-game.html`.
- ChatHub-Output receives the generated review files.
- A later ChatHub-Output push triggers the static portfolio deploy so the latest game is included in the Pages artifact.
