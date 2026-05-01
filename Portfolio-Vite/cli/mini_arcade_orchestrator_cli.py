#!/usr/bin/env python3
"""One-call GPT-5 Mini orchestrator for ArcadeBuilder packets."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import socket
import time
import subprocess
from pathlib import Path

import arcade_builder_cli as arcade


COPILOT = Path("/opt/homebrew/bin/copilot")
SEED_KEYS = ("idea", "theme", "mechanic", "content", "tone", "mode", "depth")
VALID_MODES = ("runner", "orbit", "pulseGrid", "labRift", "phaseDrop", "harbor", "rhythm", "echo")
SEED_LIMITS = {"idea": 28, "theme": 28, "mechanic": 32, "content": 32, "tone": 20, "mode": 16, "depth": 8}
DEFAULT_BATCH_PROMPT = (
    "Generate a mixed batch of five portfolio-ready arcade concepts with distinct themes, "
    "clear mechanics, and shared-runtime-safe scope."
)
ORCHESTRATOR_MEMORY_PATH = arcade.CLI_ROOT / "arcade_orchestrator_memory.md"
ORCHESTRATOR_SYSTEM_PROMPT_PATH = arcade.CLI_ROOT / "arcade_orchestrator_system_prompt.md"
AUTO_REPORT_PATH = arcade.STATE_DIR / "arcade_auto_report.json"
REQUIRED_AUTO_FLAGS = ("idea", "theme", "mechanic", "content")


def format_steps() -> str:
    lines = []
    for step in arcade.load_steps():
        lines.append(f"- {step['id']}: {step['goal']}")
    return "\n".join(lines)


def read_control_file(path: Path, fallback: str = "") -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8").strip()


def control_context() -> str:
    system_prompt = read_control_file(
        ORCHESTRATOR_SYSTEM_PROMPT_PATH,
        "You are MiniArcadeOrchestrator, a locked GPT-5 Mini worker.",
    )
    memory = read_control_file(ORCHESTRATOR_MEMORY_PATH)
    return f"""Mutable system prompt:
{system_prompt[-6000:]}

Monolithic orchestrator memory:
{memory[-6000:]}
"""


def compose_orchestrator_prompt(session: dict, active_step: dict) -> str:
    return f"""You are MiniArcadeOrchestrator-CLI, a one-call GPT-5 Mini worker.

{control_context()}

Your job is to simulate the full hierarchical ArcadeBuilder worker chain internally, then return one structured artifact that can be stored as an ArcadeBuilder reply packet and reconciled by arcade_builder_cli.py.

Workspace:
- {arcade.ROOT}

Arcade flags:
{arcade.flags_text(session["flags"])}

Existing ArcadeBuilder endpoint contract:
- reply: stores this output as arcade_packets/*_reply.md
- reconcile: folds this output into arcade_session.json and arcade_run.md
- validate: turns reconciled flags and plan into schema-valid JSON
- build: writes final JSON, shell page, and portfolio registration

Decision frame to teach yourself before deciding:
- Existing shared runtime modes should be preferred.
- Game output must stay schema-bound JSON.
- Do not invent new JavaScript runtime code.
- Do not reference external assets.
- Use shared Arcade assets and greybox presentation.
- Treat tiny flags as seeds, not complete design.
- Preserve user intent over broad brainstorming.

Internal compositional workflow to run inside this one response:
{format_steps()}

Active ArcadeBuilder step:
- {active_step["id"]}: {active_step["goal"]}

Return only this strict artifact:
- restated request
- taught decision frame
- per-step decisions
- chosen runtime mode
- root game intent
- game loop plan
- theme pack
- content contract
- schema notes
- JSON-ready decisions
- validation cues
- downstream ArcadeBuilder command recommendation
- blockers

Stage lock:
- allowed: produce the one ArcadeBuilder artifact above
- forbidden: repository edits, file writes, shell commands, new runtime code, external assets, broad exploration, new idea insertion

Do not edit files.
Do not output prose outside the artifact.
"""


def effective_batch_prompt(flags: dict[str, str]) -> str:
    prompt = (flags.get("prompt") or "").strip()
    if prompt:
        return prompt
    parts = []
    for key in ("idea", "theme", "mechanic", "tone", "content"):
        value = (flags.get(key) or "").strip()
        if value:
            parts.append(f"{key}: {value}")
    if parts:
        return "\n".join(parts)
    return DEFAULT_BATCH_PROMPT


def compose_seed_brainstorm_prompt(flags: dict[str, str], count: int) -> str:
    batch_prompt = effective_batch_prompt(flags)
    return f"""You are step 0 of MiniArcadeOrchestrator-CLI.

Generate exactly {count} distinct arcade seed tuples from this seed prompt.

Workspace:
- {arcade.ROOT}

Seed prompt:
{batch_prompt}

Rules:
- Return JSON only.
- Return an array of exactly {count} objects.
- Each array item must represent exactly one game seed.
- Every field value must be a plain short string, never an array, object, markdown list, or combined bundle.
- Keep every tuple short and production-usable.
- Stay inside shared-runtime arcade ideas.
- If mode is present, it must be one of: {", ".join(VALID_MODES)}.
- If no exact existing mode fits, leave mode as an empty string.
- Prefer materially distinct ideas, themes, and mechanics.
- Do not invent external assets or runtime code.

Each object must include:
- idea
- theme
- mechanic
- content
- depth

Optional:
- tone
- mode

Depth should default to {json.dumps(flags.get("depth") or "full")} when not varied intentionally.
Empty optional fields should be empty strings.
"""


def compose_idea_expansion_prompt(flags: dict[str, str], count: int) -> str:
    return f"""You are step 0A of MiniArcadeOrchestrator-CLI.

Expand this batch prompt into diverse arcade directions before final seed generation.

Workspace:
- {arcade.ROOT}

Batch prompt:
{effective_batch_prompt(flags)}

Known runtime modes:
- {", ".join(VALID_MODES)}

Return only a compact markdown list with:
- {count * 2} candidate directions
- 3 different mechanic families
- 3 different visual themes
- mode fit notes using only known runtime modes

Do not output final JSON in this pass.
Do not invent external assets or new runtime code.
"""


def compose_detail_merge_prompt(flags: dict[str, str], count: int, expansion: str) -> str:
    return f"""You are step 0B of MiniArcadeOrchestrator-CLI.

Merge this expansion into exactly {count} final arcade seed tuples.

Workspace:
- {arcade.ROOT}

Original batch prompt:
{effective_batch_prompt(flags)}

Expansion notes:
{expansion[:6000]}

Rules:
- Return JSON only.
- Return an array of exactly {count} objects.
- Every field value must be a plain short string, never an array, object, markdown list, or combined bundle.
- Each seed must be materially distinct from the others.
- If mode is present, it must be one of: {", ".join(VALID_MODES)}.
- If no exact existing mode fits, leave mode as an empty string.

Each object must include:
- idea
- theme
- mechanic
- content
- depth

Optional:
- tone
- mode

Depth should default to {json.dumps(flags.get("depth") or "full")} when not varied intentionally.
Empty optional fields should be empty strings.
"""


def call_copilot(prompt: str, retries: int = 0) -> tuple[int, str]:
    if not COPILOT.exists():
        return 127, "missing /opt/homebrew/bin/copilot"
    attempts = max(0, retries) + 1
    output = ""
    code = 1
    for attempt in range(attempts):
        result = subprocess.run(
            [
                str(COPILOT),
                "--config-dir",
                str(arcade.ensure_local_copilot_config()),
                "-p",
                prompt,
                "--model",
                "gpt-5-mini",
                "--allow-all",
                "--no-color",
                "--output-format",
                "text",
                "--silent",
                "--add-dir",
                str(arcade.ROOT),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=3600,
        )
        output = (result.stdout or result.stderr or "").strip()
        code = result.returncode
        if code == 0 and output:
            return 0, output
        if attempt + 1 < attempts:
            time.sleep(1.0)
    return code, output or "copilot returned no output"


def port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def ensure_portfolio_vite_server() -> subprocess.Popen | None:
    if port_open(5174):
        return None
    vite_root = arcade.PORTFOLIO_APP
    if not vite_root.exists():
        return None
    process = subprocess.Popen(
        ["npm", "start", "--", "--host", "127.0.0.1", "--port", "5174"],
        cwd=vite_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    for _ in range(80):
        if port_open(5174):
            return process
        if process.poll() is not None:
            return process
        time.sleep(0.25)
    return process


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def write_auto_report(report: dict) -> None:
    report.setdefault("time", now_stamp())
    AUTO_REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def auto_flags(args: argparse.Namespace) -> dict[str, str]:
    return {key: getattr(args, key) for key in arcade.FLAG_KEYS if getattr(args, key, "")}


def preflight_auto_build(args: argparse.Namespace) -> list[str]:
    blockers = []
    flags = auto_flags(args)
    missing = [key for key in REQUIRED_AUTO_FLAGS if not flags.get(key)]
    if missing:
        blockers.append(f"missing required flags: {', '.join(missing)}")
    if args.brainstorm_seeds or args.idea_loop:
        blockers.append("--auto-build does not allow --brainstorm-seeds or --idea-loop")
    if args.plan_only:
        blockers.append("--auto-build cannot be combined with --plan-only")
    if not COPILOT.exists():
        blockers.append("missing /opt/homebrew/bin/copilot")
    required_paths = [
        arcade.STEPS_PATH,
        arcade.PORTFOLIO_APP,
        arcade.PORTFOLIO_APP / "Pages" / "arcade-runtime.js",
        arcade.PORTFOLIO_APP / "Pages" / "arcade-bootstrap.js",
        arcade.PORTFOLIO_APP / "Pages" / "arcade-assets.json",
        arcade.CLI_ROOT / "schemas",
        arcade.CLI_ROOT / "templates",
        ORCHESTRATOR_MEMORY_PATH,
        ORCHESTRATOR_SYSTEM_PROMPT_PATH,
    ]
    for path in required_paths:
        if not path.exists():
            blockers.append(f"missing required path: {path}")
    node = shutil.which("node")
    if node:
        for path in (
            arcade.PORTFOLIO_APP / "Pages" / "arcade-runtime.js",
            arcade.PORTFOLIO_APP / "Pages" / "arcade-bootstrap.js",
        ):
            result = subprocess.run([node, "--check", str(path)], text=True, capture_output=True)
            if result.returncode != 0:
                blockers.append(result.stderr.strip() or result.stdout.strip())
    dirty = arcade.unexpected_dirty(arcade.git_status())
    if dirty:
        blockers.append("unexpected dirty worktree: " + "; ".join(dirty[:8]))
    return blockers


def proof_for_slug(slug: str) -> dict:
    page = arcade.PORTFOLIO_APP / "Pages" / f"{slug}.html"
    game = arcade.PORTFOLIO_APP / "Pages" / "games" / f"{slug}.json"
    portfolio_data = arcade.PORTFOLIO_APP / "src" / "data" / "portfolio" / "projects.js"
    portfolio_text = portfolio_data.read_text(encoding="utf-8") if portfolio_data.exists() else ""
    return {
        "slug": slug,
        "gameJson": str(game),
        "gameJsonExists": game.exists(),
        "shellHtml": str(page),
        "shellHtmlExists": page.exists(),
        "portfolioData": str(portfolio_data),
        "portfolioRegistered": f'"{slug}":' in portfolio_text and f"Pages/{slug}.html" in portfolio_text,
        "websitePath": f"/Pages/{slug}.html",
    }


def print_event(name: str, payload: dict) -> None:
    print(f"{name} {json.dumps(payload, sort_keys=True)}")


def extract_json_array(raw: str) -> list[dict] | None:
    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1 or end < start:
        return None
    try:
        data = json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, list) else None


def normalize_seed_tuple(seed: dict, base_flags: dict[str, str]) -> dict[str, str] | None:
    if not isinstance(seed, dict):
        return None
    normalized = {}
    for key in SEED_KEYS:
        value = seed.get(key, "")
        normalized[key] = str(value).strip() if value is not None else ""
        if normalized[key].startswith(("[", "{")):
            return None
        if len(normalized[key]) > SEED_LIMITS[key]:
            normalized[key] = normalized[key][: SEED_LIMITS[key]].rstrip(" -,.;:")
    required = ("idea", "theme", "mechanic", "content")
    if any(not normalized[key] for key in required):
        return None
    normalized["depth"] = normalized["depth"] or base_flags.get("depth") or "full"
    if normalized["depth"] not in {"quick", "full", "deep"}:
        normalized["depth"] = base_flags.get("depth") or "full"
    if normalized["mode"] not in VALID_MODES:
        normalized["mode"] = base_flags.get("mode") if base_flags.get("mode") in VALID_MODES else ""
    return normalized


def parse_seed_output(output: str, flags: dict[str, str], count: int) -> tuple[int, list[dict[str, str]] | str]:
    array = extract_json_array(output)
    if not array:
        return 1, f"step 0 seed parse failed: {output[:240]}"
    seeds = []
    for item in array:
        normalized = normalize_seed_tuple(item, flags)
        if normalized:
            seeds.append(normalized)
    if len(seeds) != count:
        return 1, f"step 0 seed parse failed: expected {count}, got {len(seeds)}"
    return 0, seeds


def brainstorm_seed_tuples(flags: dict[str, str], count: int, idea_loop: bool = False) -> tuple[int, list[dict[str, str]] | str]:
    if idea_loop:
        code, expansion = call_copilot(compose_idea_expansion_prompt(flags, count))
        if code != 0:
            return code, expansion
        code, output = call_copilot(compose_detail_merge_prompt(flags, count, expansion))
        if code != 0:
            return code, output
        return parse_seed_output(output, flags, count)
    code, output = call_copilot(compose_seed_brainstorm_prompt(flags, count))
    if code != 0:
        return code, output
    return parse_seed_output(output, flags, count)


def make_child_args(args: argparse.Namespace, seed: dict[str, str]) -> argparse.Namespace:
    child = argparse.Namespace(**vars(args))
    for key in arcade.FLAG_KEYS:
        setattr(child, key, seed.get(key, ""))
    child.brainstorm_seeds = False
    child.count = 0
    child.idea_loop = False
    return child


def run_single(args: argparse.Namespace) -> tuple[int, dict]:
    flags = {key: getattr(args, key) for key in arcade.FLAG_KEYS if getattr(args, key, "")}
    if getattr(args, "fresh_session", False):
        arcade.reset_session(flags, "fresh-session")
    shell = arcade.ArcadeBuilderShell(flags)
    shell.onecmd("safe-next")
    step = arcade.find_step(shell.session.get("active_step"))
    if not step:
        print("blocked: no active ArcadeBuilder step")
        return 1, {"status": "failed", "slug": "", "packetPath": ""}

    prompt_path = arcade.write_prompt_packet(step, shell.session)
    prompt = compose_orchestrator_prompt(shell.session, step)
    if args.plan_only:
        print(prompt_path)
        return 0, {"status": "validated", "slug": "", "packetPath": str(prompt_path)}

    code, output = call_copilot(prompt, retries=getattr(args, "retry", 0))
    if code != 0:
        shell.session["last_result"] = f"mini orchestrator blocked: {output[:240]}"
        arcade.append_history(shell.session, "mini-orchestrator-blocked", output[:240])
        arcade.save_json(arcade.SESSION_PATH, shell.session)
        print(f"blocked: {output}")
        print(f"packet pending {prompt_path}")
        return 0, {"status": "blocked", "slug": "", "packetPath": str(prompt_path)}

    reply_path = arcade.write_worker_reply(step, shell.session, output)
    shell.session = arcade.load_session()
    shell.onecmd(f"reconcile {arcade.relative(reply_path)}")
    if args.validate:
        shell.onecmd("validate")
    if args.build:
        vite_process = ensure_portfolio_vite_server()
        shell.onecmd("build")
        if not str(shell.session.get("last_result", "")).startswith("built "):
            print(reply_path)
            return 0, {
                "status": "blocked",
                "slug": shell.session.get("last_result", "").replace("blocked ", ""),
                "packetPath": str(reply_path),
            }
    print(reply_path)
    mode = "build" if args.build else "validate" if args.validate else "plan-only"
    return 0, {
        "status": "built" if mode == "build" else "validated",
        "slug": shell.session.get("last_result", "").replace("built ", "").replace("validated ", ""),
        "packetPath": str(reply_path),
    }


def run_auto_build(args: argparse.Namespace) -> int:
    flags = auto_flags(args)
    report = {
        "status": "started",
        "mode": "auto-build",
        "flags": flags,
        "blockers": [],
        "steps": [],
        "proof": {},
    }
    blockers = preflight_auto_build(args)
    if blockers:
        report["status"] = "blocked"
        report["blockers"] = blockers
        write_auto_report(report)
        print_event("AUTO_BUILD_BLOCKED", {"blockers": blockers, "report": str(AUTO_REPORT_PATH)})
        return 1

    args.validate = True
    args.build = True
    args.fresh_session = True
    args.brainstorm_seeds = False
    args.idea_loop = False
    args.retry = max(args.retry, 1)
    report["steps"].append("preflight")
    report["steps"].append("fresh-session")
    status_code, result = run_single(args)
    report["steps"].extend(["prompt-packet", "gpt-5-mini-reply", "reconcile", "validate", "build"])
    report["result"] = result
    report["status"] = result.get("status", "failed") if status_code == 0 else "failed"
    if report["status"] == "built":
        report["proof"] = proof_for_slug(result.get("slug", ""))
        if not all(
            report["proof"].get(key)
            for key in ("gameJsonExists", "shellHtmlExists", "portfolioRegistered")
        ):
            report["status"] = "blocked"
            report["blockers"].append("build proof failed")
    else:
        report["blockers"].append(result.get("slug") or "auto-build did not produce a built slug")
    write_auto_report(report)
    print_event("AUTO_BUILD_DONE", {"status": report["status"], "slug": result.get("slug", ""), "report": str(AUTO_REPORT_PATH)})
    return 0 if report["status"] == "built" else 1


def run(args: argparse.Namespace) -> int:
    flags = {key: getattr(args, key) for key in arcade.FLAG_KEYS if getattr(args, key, "")}
    if getattr(args, "prompt", "").strip():
        flags["prompt"] = args.prompt.strip()
    if args.auto_build:
        return run_auto_build(args)
    if args.brainstorm_seeds:
        batch_id = f"batch-{time.time_ns()}"
        mode = "build" if args.build else "validate" if args.validate else "plan-only"
        print_event(
            "BATCH_START",
            {
                "batchId": batch_id,
                "count": args.count,
                "mode": mode,
                "prompt": effective_batch_prompt(flags),
                "ideaLoop": bool(args.idea_loop),
            },
        )
        code, result = brainstorm_seed_tuples(flags, args.count, args.idea_loop)
        if code != 0:
            print(f"blocked: {result}")
            print_event("BATCH_DONE", {"batchId": batch_id, "summary": {"failed": 1, "validated": 0, "built": 0, "blocked": 0}})
            return 0
        seeds = result
        print_event("BRAINSTORM_RESULT", {"batchId": batch_id, "seeds": seeds})
        summary = {"validated": 0, "built": 0, "blocked": 0, "failed": 0}
        for index, seed in enumerate(seeds):
            child_job_id = f"{batch_id}-run-{index + 1}"
            print_event("CHILD_START", {"batchId": batch_id, "jobId": child_job_id, "flags": seed})
            child_args = make_child_args(args, seed)
            status_code, child_result = run_single(child_args)
            child_status = child_result["status"] if status_code == 0 else "failed"
            summary[child_status] = summary.get(child_status, 0) + 1
            print_event(
                "CHILD_DONE",
                {
                    "batchId": batch_id,
                    "jobId": child_job_id,
                    "status": child_status,
                    "slug": child_result.get("slug", ""),
                    "packetPath": child_result.get("packetPath", ""),
                },
            )
        print_event("BATCH_DONE", {"batchId": batch_id, "summary": summary})
        return 0
    status, _ = run_single(args)
    return status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="One-call Mini Arcade orchestrator")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--idea", default="")
    parser.add_argument("--theme", default="")
    parser.add_argument("--mode", default="")
    parser.add_argument("--tone", default="")
    parser.add_argument("--mechanic", default="")
    parser.add_argument("--content", default="")
    parser.add_argument("--depth", choices=["quick", "full", "deep"], default="")
    parser.add_argument("--brainstorm-seeds", action="store_true")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--idea-loop", action="store_true")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--auto-build", action="store_true")
    parser.add_argument("--fresh-session", action="store_true")
    parser.add_argument("--retry", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    raise SystemExit(run(parse_args()))


if __name__ == "__main__":
    main()
