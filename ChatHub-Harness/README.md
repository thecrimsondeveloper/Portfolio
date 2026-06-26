# ChatHub-Harness

ChatHub-Harness is the root-level, prompt-gated, linear agent harness for this repository.

Its purpose is to let GitHub Actions run cloud/offloaded game-building workflows only when there is intentional idea intake:

```text
idea prompt
→ active prompt file
→ workflow JSON
→ Python runner
→ free NVIDIA/OpenAI-compatible endpoint when configured
→ generated outbox result
→ ChatHub-Output review branch
→ GitHub Pages playable output
→ human/agent review
→ lesson update
```

## Core rule

The harness is **not always-on**.

Normal repo changes should not run the agent. The normal push trigger watches only:

```text
ChatHub-Harness/ideas/**
```

Then the runner checks the active prompt again before any endpoint call.

```text
no real prompt
→ no endpoint call
→ no generated game
→ no ChatHub-Output publish

real prompt under ## Prompt
→ run the selected workflow
→ publish output to ChatHub-Output
```

## Main files

```text
ChatHub-Harness
├── chathub_runner.py
├── ideas
│   ├── README.md
│   ├── active.prompt.md
│   ├── queue
│   │   └── .gitkeep
│   ├── archive
│   │   └── .gitkeep
│   └── examples
│       └── game-build.prompt.md
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

## Active prompt

The run switch is:

```text
ChatHub-Harness/ideas/active.prompt.md
```

A valid prompt must include real content under:

```md
## Prompt
```

Example:

```md
# Active Prompt

workflow: game-build
mode: single-game
output: playable

## Prompt

Build a small browser arcade game called Signal Salvage.

The player controls a glowing signal core, collects data shards, avoids corruption fields, and survives for 60 seconds.

Use no external assets. Make it self-contained.
```

Placeholders like `TODO`, empty prompt bodies, or HTML comments are ignored.

## Branch model

```text
development
└── source harness, workflows, active prompt, lessons, app code

ChatHub-Output
└── generated review branch and GitHub Pages branch
```

The agent should normally run from `development` only.

`ChatHub-Output` is output, not input. Generated commits use `[skip chathub]` and the workflow no longer watches `ChatHub-Output` pushes.

## Local run

```bash
python3 ChatHub-Harness/chathub_runner.py \
  --workflow ChatHub-Harness/workflows/game-build.workflow.json \
  --prompt ChatHub-Harness/ideas/active.prompt.md \
  --direction ChatHub-Harness/directions/current-direction.md \
  --out ChatHub-Harness/outbox/latest-result.md \
  --lessons ChatHub-Harness/lessons/harness-lessons.md
```

If no real prompt exists, the runner writes a no-op artifact and marks the run so the workflow skips output-branch publishing.

## NVIDIA setup

Set `NVIDIA_API_KEY` in the environment or as a GitHub Actions secret.

Optional overrides:

```bash
export NVIDIA_API_BASE_URL="https://integrate.api.nvidia.com/v1"
export NVIDIA_MODEL="mistralai/mixtral-8x7b-instruct-v0.1"
export NVIDIA_FREE_ENDPOINTS_ONLY="true"
```

The runner has a free-endpoint guard. If `NVIDIA_MODEL` is not allowlisted while `NVIDIA_FREE_ENDPOINTS_ONLY=true`, the endpoint call is blocked.

## GitHub Actions

The workflow file is:

```text
.github/workflows/chathub-harness.yml
```

Default behavior:

```text
push to development changing ChatHub-Harness/ideas/**
→ run ChatHub-Harness/chathub_runner.py
→ read active.prompt.md
→ if no prompt: skip publish
→ if valid prompt: call endpoint and generate output
→ commit generated output to ChatHub-Output
→ GitHub Pages serves the latest playable result
```

Manual runs can still use `workflow_dispatch`, but the runner will not call an endpoint unless the active prompt is valid.
