#!/usr/bin/env python3
"""Run one ChatHub-Harness workflow from committed direction files.

The runner is intentionally dependency-free so it can run in GitHub Actions with
plain Python. It writes a reviewable outbox artifact whether the NVIDIA endpoint
is configured or blocked.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_WORKFLOW = ROOT / "workflows" / "game-build.workflow.json"
DEFAULT_DIRECTION = ROOT / "directions" / "current-direction.md"
DEFAULT_OUT = ROOT / "outbox" / "latest-result.md"
DEFAULT_LESSONS = ROOT / "lessons" / "harness-lessons.md"


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path, fallback: str = "") -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8")


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


def endpoint_config(workflow: dict[str, Any]) -> dict[str, str]:
    endpoint = workflow.get("endpoint") or {}
    base_url_env = endpoint.get("baseUrlEnv", "NVIDIA_API_BASE_URL")
    model_env = endpoint.get("modelEnv", "NVIDIA_MODEL")
    api_key_env = endpoint.get("apiKeyEnv", "NVIDIA_API_KEY")
    return {
        "base_url": os.getenv(base_url_env, endpoint.get("defaultBaseUrl", "https://integrate.api.nvidia.com/v1")).rstrip("/"),
        "model": os.getenv(model_env, endpoint.get("defaultModel", "mistralai/mixtral-8x7b-instruct-v0.1")),
        "api_key_env": api_key_env,
        "api_key": os.getenv(api_key_env, ""),
    }


def workflow_steps_text(workflow: dict[str, Any]) -> str:
    steps = workflow.get("linearSteps") or []
    lines = []
    for step in steps:
        lines.append(f"- {step.get('id', 'step')}: {step.get('goal', '').strip()}")
    return "\n".join(lines) if lines else "- no steps declared"


def output_contract_text(workflow: dict[str, Any]) -> str:
    contract = workflow.get("outputContract") or []
    return "\n".join(f"- {item}" for item in contract) if contract else "- markdown result"


def constraints_text(workflow: dict[str, Any]) -> str:
    constraints = workflow.get("constraints") or []
    return "\n".join(f"- {item}" for item in constraints) if constraints else "- stay bounded"


def build_prompt(workflow: dict[str, Any], direction: str, lessons: str) -> list[dict[str, str]]:
    system = textwrap.dedent(
        """
        You are ChatHub-Harness, a linear workflow runner for a portfolio and game-building repository.
        Follow the workflow steps in order. Produce a reviewable artifact. Do not claim files were edited.
        Extract durable lessons separately from temporary observations. Keep output concise and operational.
        """
    ).strip()

    user = f"""Workflow: {workflow.get('title', workflow.get('id', 'unnamed workflow'))}
Workflow intent:
{workflow.get('intent', '(none)')}

Linear steps:
{workflow_steps_text(workflow)}

Output contract:
{output_contract_text(workflow)}

Constraints:
{constraints_text(workflow)}

Committed direction:
{direction.strip() or '(empty direction file)'}

Existing lessons:
{lessons[-6000:].strip() or '(no lessons yet)'}

Return the requested markdown artifact only.
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def write_result(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def blocked_result(workflow: dict[str, Any], config: dict[str, str], reason: str) -> str:
    return f"""# ChatHub Result

status: blocked
time: {now_stamp()}
workflow: {workflow.get('id', 'unknown')}
model: {config.get('model', '')}
base_url: {config.get('base_url', '')}

## Blocker

{reason}

## Next Fix

Set `{config.get('api_key_env', 'NVIDIA_API_KEY')}` as a local environment variable or GitHub Actions secret, then rerun the same workflow.
"""


def call_nvidia_chat(config: dict[str, str], messages: list[dict[str, str]], timeout: int) -> str:
    url = f"{config['base_url']}/chat/completions"
    payload = {
        "model": config["model"],
        "messages": messages,
        "temperature": 0.3,
        "top_p": 1,
        "max_tokens": 2048,
        "stream": False,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json",
        },
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
    except json.JSONDecodeError as error:
        raise RuntimeError(f"endpoint returned non-JSON response: {raw[:1200]}") from error

    choices = data.get("choices")
    if not choices:
        raise RuntimeError(f"endpoint returned no choices: {raw[:1200]}")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError(f"endpoint returned empty assistant content: {raw[:1200]}")
    return content.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one ChatHub-Harness workflow")
    parser.add_argument("--workflow", type=Path, default=DEFAULT_WORKFLOW)
    parser.add_argument("--direction", type=Path, default=DEFAULT_DIRECTION)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--lessons", type=Path, default=DEFAULT_LESSONS)
    parser.add_argument("--require-key", action="store_true", help="fail instead of writing a blocked result when the API key is missing")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    workflow = load_workflow(args.workflow)
    direction = read_text(args.direction)
    lessons = read_text(args.lessons)
    config = endpoint_config(workflow)

    if not config["api_key"]:
        result = blocked_result(workflow, config, f"Missing `{config['api_key_env']}`.")
        write_result(args.out, result)
        print(f"ChatHub-Harness blocked: missing {config['api_key_env']}")
        print(f"outbox: {args.out}")
        return 1 if args.require_key else 0

    messages = build_prompt(workflow, direction, lessons)
    try:
        content = call_nvidia_chat(config, messages, args.timeout)
    except RuntimeError as error:
        result = blocked_result(workflow, config, str(error))
        write_result(args.out, result)
        print(f"ChatHub-Harness blocked: {error}")
        print(f"outbox: {args.out}")
        return 0

    result = f"""<!-- generated by ChatHub-Harness at {now_stamp()} -->
<!-- workflow: {workflow.get('id', 'unknown')} -->
<!-- model: {config.get('model', '')} -->

{content}
"""
    write_result(args.out, result)
    print(f"ChatHub-Harness completed: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
