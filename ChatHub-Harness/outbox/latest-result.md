# ChatHub Result

status: blocked
time: 2026-06-26T03:27:14+00:00
workflow: game-build
model: 
base_url: 
free_only: True

## Blocker

Free-endpoint guard blocked model ``. Set NVIDIA_MODEL to an allowlisted free endpoint, or set NVIDIA_FREE_MODEL_ALLOWLIST. Current allowlist: deepseek-ai/deepseek-v4-pro, mistralai/mixtral-8x7b-instruct-v0.1, moonshotai/kimi-k2.6, nvidia/nemotron-3-ultra-550b-a55b, zai/glm-5.1

## Playable Output

A deterministic fallback playable HTML file was still emitted for review:

```text
ChatHub-Harness/outbox/latest-game.html
```

## Next Fix

Set `NVIDIA_API_KEY` as a local environment variable or GitHub Actions secret, then rerun the same workflow. If the blocker is the free-endpoint guard, set `NVIDIA_MODEL` to a known free endpoint or update `NVIDIA_FREE_MODEL_ALLOWLIST`.
