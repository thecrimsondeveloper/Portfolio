#!/usr/bin/env python3
"""Prompt-gated ChatHub game harness.

A valid prompt in ChatHub-Harness/ideas/active.prompt.md triggers one bounded
run: ask a free NVIDIA/OpenAI-compatible endpoint for a structured game spec,
render that spec into a self-contained playable browser game, and publish the
outbox through the workflow. Without a real prompt, no endpoint is called.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import textwrap
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from game_spec_renderer import normalize_spec, write_outputs

ROOT = Path(__file__).resolve().parent
DEFAULT_WORKFLOW = ROOT / "workflows" / "game-build.workflow.json"
DEFAULT_PROMPT = ROOT / "ideas" / "active.prompt.md"
DEFAULT_DIRECTION = ROOT / "directions" / "current-direction.md"
DEFAULT_OUT = ROOT / "outbox" / "latest-result.md"
DEFAULT_LESSONS = ROOT / "lessons" / "harness-lessons.md"
DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "mistralai/mixtral-8x7b-instruct-v0.1"
NOOP_SENTINEL = ".chathub-noop"
DEFAULT_FREE_MODEL_ALLOWLIST = {
    DEFAULT_MODEL,
    "nvidia/nemotron-3-ultra-550b-a55b",
    "moonshotai/kimi-k2.6",
    "deepseek-ai/deepseek-v4-pro",
    "zai/glm-5.1",
}


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def env_or_default(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None or not value.strip() else value.strip()


def read_text(path: Path, fallback: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else fallback


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_workflow(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"workflow missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"workflow JSON invalid: {path}: {error}") from error
    if not isinstance(data, dict):
        raise SystemExit(f"workflow root must be an object: {path}")
    return data


def prompt_body(raw_prompt: str) -> str:
    raw_prompt = re.sub(r"<!--.*?-->", "", raw_prompt, flags=re.DOTALL)
    match = re.search(r"(?im)^##\s+Prompt\s*$", raw_prompt)
    if not match:
        return ""
    body = raw_prompt[match.end():]
    next_heading = re.search(r"(?m)^##\s+", body)
    if next_heading:
        body = body[: next_heading.start()]
    return body.strip()


def is_placeholder_prompt(body: str) -> bool:
    normalized = re.sub(r"[\s#`*_>\-:]+", " ", body.lower()).strip()
    return normalized in {"", "todo", "tbd", "none", "no prompt", "no active prompt", "placeholder", "add prompt here", "write prompt here", "empty"} or len(normalized) < 12


def active_prompt_or_none(prompt_path: Path) -> tuple[str | None, str]:
    if not prompt_path.exists():
        return None, f"active prompt file missing: {prompt_path}"
    raw_prompt = read_text(prompt_path)
    body = prompt_body(raw_prompt)
    if is_placeholder_prompt(body):
        return None, "no real content under ## Prompt"
    return raw_prompt.strip(), ""


def endpoint_config(workflow: dict[str, Any]) -> dict[str, Any]:
    endpoint = workflow.get("endpoint") or {}
    base_url_env = endpoint.get("baseUrlEnv", "NVIDIA_API_BASE_URL")
    model_env = endpoint.get("modelEnv", "NVIDIA_MODEL")
    api_key_env = endpoint.get("apiKeyEnv", "NVIDIA_API_KEY")
    return {
        "base_url": env_or_default(base_url_env, endpoint.get("defaultBaseUrl", DEFAULT_BASE_URL)).rstrip("/"),
        "model": env_or_default(model_env, endpoint.get("defaultModel", DEFAULT_MODEL)),
        "api_key_env": api_key_env,
        "api_key": os.getenv(api_key_env, "").strip(),
        "free_only": env_or_default("NVIDIA_FREE_ENDPOINTS_ONLY", "true").lower() not in {"0", "false", "no"},
    }


def configured_free_model_allowlist() -> set[str]:
    raw = os.getenv("NVIDIA_FREE_MODEL_ALLOWLIST", "")
    configured = {item.strip() for item in raw.split(",") if item.strip()}
    return configured or set(DEFAULT_FREE_MODEL_ALLOWLIST)


def free_endpoint_blocker(config: dict[str, Any]) -> str | None:
    if not config.get("free_only"):
        return None
    allowlist = configured_free_model_allowlist()
    if config.get("model") not in allowlist:
        return f"Free-endpoint guard blocked model `{config.get('model')}`. Allowed: {', '.join(sorted(allowlist))}."
    return None


def workflow_steps_text(workflow: dict[str, Any]) -> str:
    steps = workflow.get("linearSteps") or []
    return "\n".join(f"- {s.get('id', 'step')}: {s.get('goal', '').strip()}" for s in steps) or "- no steps declared"


def build_spec_messages(workflow: dict[str, Any], active_prompt: str, direction: str, lessons: str) -> list[dict[str, str]]:
    system = textwrap.dedent(
        """
        You are ChatHub-Harness Game Spec Builder. Return only strict JSON, no markdown.
        Design one small playable browser arcade game for a safe built-in canvas runtime.
        Do not request external assets. Keep it self-contained and playable immediately.
        """
    ).strip()
    schema = {
        "title": "string",
        "tagline": "string",
        "objective": "string",
        "playerName": "string",
        "collectibleName": "string",
        "hazardName": "string",
        "timerSeconds": 45,
        "goalScore": 120,
        "collectibleCount": 10,
        "hazardCount": 7,
        "playerSpeed": 900,
        "hazardSpeed": 95,
        "scorePerCollectible": 10,
        "palette": {"background": "#090b10", "player": "#eef2ff", "collectible": "#8bd3ff", "hazard": "#ff5577", "accent": "#b8ff8b"},
        "backgroundPattern": "grid|stars|rings|cells",
        "winText": "string",
        "loseText": "string",
    }
    user = f"""Active idea prompt:
{active_prompt.strip()}

Workflow: {workflow.get('title', workflow.get('id', 'game-build'))}
Workflow steps:
{workflow_steps_text(workflow)}

Standing direction:
{direction.strip() or '(empty)'}

Recent lessons:
{lessons[-3000:].strip() or '(none)'}

Return strict JSON matching this shape. Do not include comments or markdown fences:
{json.dumps(schema, indent=2)}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def call_nvidia_chat(config: dict[str, Any], messages: list[dict[str, str]], timeout: int) -> str:
    request = urllib.request.Request(
        f"{config['base_url']}/chat/completions",
        data=json.dumps({"model": config["model"], "messages": messages, "temperature": 0.25, "top_p": 1, "max_tokens": 1600, "stream": False}).encode("utf-8"),
        headers={"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"endpoint HTTP {error.code}: {body[:1200]}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"endpoint connection failed: {error}") from error
    try:
        data = json.loads(raw)
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"endpoint returned unexpected response: {raw[:1200]}") from error
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError(f"endpoint returned empty assistant content: {raw[:1200]}")
    return content.strip()


def parse_json_object(text: str) -> dict[str, Any] | None:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.I).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            try:
                parsed = json.loads(cleaned[start : end + 1])
                return parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                return None
    return None


def no_op_result(workflow: dict[str, Any], prompt_path: Path, reason: str) -> str:
    return f"""# ChatHub No-Op

status: skipped
time: {now_stamp()}
workflow: {workflow.get('id', 'unknown')}
active_prompt: {prompt_path}
endpoint_called: false
output_published: false

## Reason

{reason}

No model endpoint was called. No playable output was generated. The output branch should not be changed by this run.
"""


def blocked_result(workflow: dict[str, Any], config: dict[str, Any], reason: str) -> str:
    return f"""# ChatHub Game Build Result

status: blocked
time: {now_stamp()}
workflow: {workflow.get('id', 'unknown')}
model: {config.get('model', '')}
base_url: {config.get('base_url', '')}
free_only: {config.get('free_only')}

## Blocker

{reason}

The harness still generated a playable fallback game from the active prompt so the website output remains playable.
"""


def clear_noop_sentinel(out_dir: Path) -> None:
    sentinel = out_dir / NOOP_SENTINEL
    if sentinel.exists():
        sentinel.unlink()


def mark_noop(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / NOOP_SENTINEL).write_text("skip output branch publish\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one prompt-gated ChatHub game workflow")
    parser.add_argument("--workflow", type=Path, default=DEFAULT_WORKFLOW)
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    parser.add_argument("--direction", type=Path, default=DEFAULT_DIRECTION)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--lessons", type=Path, default=DEFAULT_LESSONS)
    parser.add_argument("--require-key", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    workflow = load_workflow(args.workflow)
    active_prompt, no_prompt_reason = active_prompt_or_none(args.prompt)
    clear_noop_sentinel(args.out.parent)
    if active_prompt is None:
        write_text(args.out, no_op_result(workflow, args.prompt, no_prompt_reason))
        mark_noop(args.out.parent)
        print(f"ChatHub-Harness skipped: {no_prompt_reason}")
        return 0

    direction = read_text(args.direction)
    lessons = read_text(args.lessons)
    config = endpoint_config(workflow)
    blocker = free_endpoint_blocker(config)
    raw_spec = None
    raw_model_output = ""
    status = "completed"

    if blocker:
        result = blocked_result(workflow, config, blocker)
        status = "blocked-free-endpoint-guard"
    elif not config["api_key"]:
        result = blocked_result(workflow, config, f"Missing `{config['api_key_env']}`.")
        status = "blocked-missing-key"
    else:
        try:
            raw_model_output = call_nvidia_chat(config, build_spec_messages(workflow, active_prompt, direction, lessons), args.timeout)
            raw_spec = parse_json_object(raw_model_output)
            status = "completed" if raw_spec else "completed-with-spec-fallback"
            result = f"""# ChatHub Game Build Result

status: {status}
time: {now_stamp()}
workflow: {workflow.get('id', 'unknown')}
model: {config.get('model', '')}
free_only: {config.get('free_only')}

## Model Game Spec Output

```json
{raw_model_output.strip()[:3000]}
```
"""
        except RuntimeError as error:
            result = blocked_result(workflow, config, str(error))
            status = "blocked-endpoint-error"
            print(f"ChatHub-Harness blocked: {error}")

    spec = normalize_spec(raw_spec, active_prompt)
    if raw_spec is None:
        result += "\n## Spec Fallback\n\nThe model did not provide a parseable spec, so the harness generated a safe playable spec from the active prompt.\n"
    result += f"""
## Playable Output

The harness generated a playable browser game directly from the active prompt/spec.

```text
ChatHub-Harness/outbox/latest-game.html
ChatHub-Harness/outbox/games/{spec['slug']}/index.html
```

## Normalized Game Spec

```json
{json.dumps(spec, indent=2)}
```
"""
    write_text(args.out, result)
    write_outputs(args.out.parent, spec, result, config.get("model", ""), status)
    print(f"ChatHub-Harness wrote playable game: {spec['title']} ({spec['slug']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
