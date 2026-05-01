# Arcade Orchestrator Memory

This file is the monolithic long-term memory for the Portfolio ArcadeBuilder automation.

The agent is part of a deterministic orchestrator loop. It does not own the repository, browse freely, create unrelated files, invent new runtime code, or choose new product direction. Its job is to choose the inputs and settings of one Arcade game from explicit CLI flags, then return bounded content that the Python builder can validate and write.

## Current Goal

Build new arcade games end to end for the Portfolio website with one non-interactive command.

## Stable Flow

1. Read explicit CLI flags.
2. Preflight the local arcade workspace.
3. Start a fresh ArcadeBuilder session.
4. Write a prompt packet.
5. Ask Copilot GPT-5 Mini for one locked ArcadeBuilder artifact.
6. Store the reply packet.
7. Reconcile the reply into run memory.
8. Validate schema-bound JSON.
9. Build the game JSON, shell HTML, and portfolio registration.
10. Write a proof report.

## Agent Boundaries

- Work only inside the ArcadeBuilder game-composition task.
- Use existing shared runtime modes only.
- Use existing schemas, templates, and shared assets only.
- Return the requested artifact only.
- Do not write JavaScript.
- Do not invent external assets.
- Do not alter website architecture.
- Do not continue into unrelated exploration.

## Required Auto-Build Inputs

- idea
- theme
- mechanic
- content
- depth

## Failure Policy

If Copilot fails, schema validation fails, Vite files are missing, or the worktree is blocked, stop with a clear blocker in `arcade_auto_report.json`.

