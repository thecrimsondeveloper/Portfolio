#!/usr/bin/env python3
import argparse
import json
import os
import sys
import textwrap
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def build_prompt(theme: str, count: int, audience: str = "arcade game designers") -> str:
    return textwrap.dedent(f"""
    You are a creative arcade game design assistant.
    Generate exactly {count} distinct variant game ideas for the theme: {theme}.
    Each idea should have a short title and a one-sentence summary.
    Keep the ideas playable, arcade-friendly, and easy to implement as small browser games.
    Output a numbered list only, with no extra explanation.
    """)


def call_nvidia_ai(prompt: str) -> str:
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise EnvironmentError("NVIDIA_API_KEY is not set in the environment.")

    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    payload = {
        "model": "mistralai/mixtral-8x7b-instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "top_p": 1,
        "max_tokens": 400,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                response_data = json.load(response)
            break
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}: {exc.reason}"
        except urllib.error.URLError as exc:
            last_error = str(exc.reason)
        except json.JSONDecodeError as exc:
            last_error = f"Invalid JSON response: {exc}"
        if attempt < 3:
            time.sleep(attempt * 2)
            continue
        raise RuntimeError(f"NVIDIA AI request failed: {last_error}")

    choices = response_data.get("choices", [])
    if not choices:
        raise RuntimeError("NVIDIA AI returned no choices.")

    message = choices[0].get("message", {})
    text = message.get("content") or choices[0].get("text")
    return (text or "").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ArcadeBrainstorm-CLI: generate variant arcade game ideas using the NVIDIA endpoint."
    )
    parser.add_argument("--theme", "-t", type=str, default="neon harbor run",
                        help="Theme or starting concept for the variant game ideas.")
    parser.add_argument("--count", "-c", type=int, default=5,
                        help="Number of variant ideas to generate.")
    parser.add_argument("--prompt", "-p", type=str, default="",
                        help="Custom prompt to send to the NVIDIA endpoint instead of the built-in prompt.")
    parser.add_argument("--raw", action="store_true",
                        help="Print only the raw NVIDIA response without extra CLI formatting.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt = args.prompt.strip() or build_prompt(args.theme, args.count)

    try:
        response = call_nvidia_ai(prompt)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.raw:
        print(response)
        return 0

    print("\nArcadeBrainstorm-CLI variants:\n")
    print(response)
    print("\nChoose a game idea from the list and use it to seed your next arcade prototype.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
