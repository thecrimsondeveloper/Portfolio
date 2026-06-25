# ChatHub-Harness

ChatHub-Harness is the root-level linear agent harness for this repository.

Its purpose is to make workflow runs accessible from chat, commits, and GitHub Actions:

```text
user direction
→ direction file
→ workflow JSON
→ Python runner
→ NVIDIA/OpenAI-compatible endpoint when configured
→ outbox result
→ human/agent review
→ lesson update
→ next direction
```

## Design rules

- Keep the harness at the repository root.
- Keep workflows linear and reviewable.
- Treat user directions as the source of intent.
- Treat workflow JSON as the source of process.
- Treat `outbox/` as generated review material.
- Treat `lessons/` as accumulated operating memory.
- Prefer small bounded runs over broad autonomous edits.
- Do not let the harness casually rewrite the portfolio, Arcade runtime, or deployment files.

## Main files

```text
ChatHub-Harness
├── chathub_runner.py
├── directions
│   └── current-direction.md
├── workflows
│   ├── game-build.workflow.json
│   └── nvidia-endpoint-test.workflow.json
├── lessons
│   └── harness-lessons.md
└── outbox
    └── .gitkeep
```

## Local run

```bash
python3 ChatHub-Harness/chathub_runner.py \
  --workflow ChatHub-Harness/workflows/game-build.workflow.json \
  --direction ChatHub-Harness/directions/current-direction.md \
  --out ChatHub-Harness/outbox/latest-result.md \
  --lessons ChatHub-Harness/lessons/harness-lessons.md
```

## NVIDIA setup

Set `NVIDIA_API_KEY` in the environment or as a GitHub Actions secret.

Optional overrides:

```bash
export NVIDIA_API_BASE_URL="https://integrate.api.nvidia.com/v1"
export NVIDIA_MODEL="mistralai/mixtral-8x7b-instruct-v0.1"
```

If no NVIDIA key is present, the runner writes a blocked-but-reviewable result instead of failing by default.

## GitHub Actions

The workflow file is:

```text
.github/workflows/chathub-harness.yml
```

It runs on pushes to `development` that touch `ChatHub-Harness/**`, and it can also be run manually with `workflow_dispatch`.
