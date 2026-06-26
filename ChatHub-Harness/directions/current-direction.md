# Current Direction

Run the ChatHub-Harness game-build workflow now.

Goal:

- Use only free NVIDIA/build.nvidia.com compatible endpoints.
- Produce a reviewable game-building result.
- Emit a self-contained playable browser game output in the outbox.
- Keep the run linear and bounded.
- Do not modify the public Portfolio-Vite app or Arcade runtime during this run.

Playable output target:

```text
ChatHub-Harness/outbox/latest-game.html
```

Review output target:

```text
ChatHub-Harness/outbox/latest-result.md
ChatHub-Harness/outbox/latest-links.md
```

Game direction:

Create a small arcade prototype called Signal Salvage. The player pilots a bright signal core through a dark grid, collects blue data cores, avoids red corruption fields, and tries to survive a short timer. It should feel like a clean first proof that the harness can generate and publish playable game output.

The result should include:

- what workflow ran
- what free endpoint/model was used or what blocked it
- links to play/review the generated output
- lessons learned for improving the harness
- the next exact direction for the next run
