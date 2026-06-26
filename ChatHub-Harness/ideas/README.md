# ChatHub Ideas Intake

This folder is the only normal push-triggered intake surface for ChatHub-Harness.

## Active prompt

Use this file to intentionally run the harness:

```text
ChatHub-Harness/ideas/active.prompt.md
```

The harness only runs the agent when `active.prompt.md` contains real content under a `## Prompt` heading.

No real prompt means:

```text
no endpoint call
no generated game
no ChatHub-Output publish
```

## Valid prompt shape

```md
# Active Prompt

workflow: game-build
mode: single-game
output: playable

## Prompt

Build a small self-contained browser arcade game.
```

## Placeholder prompts are ignored

These do not run the agent:

```md
## Prompt

TODO
```

```md
## Prompt

<!-- Add prompt here. -->
```

## Queue and archive

Future batch mode can use:

```text
ChatHub-Harness/ideas/queue/
ChatHub-Harness/ideas/archive/
```

For now, `active.prompt.md` is the run switch.
