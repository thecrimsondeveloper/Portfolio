# ChatHub-Harness Lessons

This file records durable lessons from running ChatHub-Harness.

## Current baseline

- Keep the harness root-level so it can coordinate Portfolio-Vite, Arcade, docs, and future build workflows without being confused for app source.
- Keep each workflow linear: direction → workflow → runner → outbox → review → lesson → next direction.
- Use NVIDIA/OpenAI-compatible endpoints through environment variables instead of hardcoding secrets.
- A missing API key should create a clear blocked result, not a confusing failed workflow.
- Avoid auto-committing generated results until the loop has enough guardrails to prevent recursive push runs.

## Lesson format

```text
- date:
  workflow:
  observation:
  change needed:
  validation:
```
