#!/usr/bin/env python3
"""Hierarchical ArcadeBuilder CLI for packet-driven portfolio game builds."""

from __future__ import annotations

import argparse
import cmd
import datetime as dt
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from portfolio_cli import (
    IdeaBrief,
    build_game,
    ensure_cli_support_files,
    fill_game_json,
    pick_fallback_mode,
    validate_game_json,
)


ROOT = Path(__file__).resolve().parents[1]
CLI_ROOT = ROOT / "Portfolio-CLI"
STEPS_PATH = CLI_ROOT / "arcade_steps.json"
SESSION_PATH = CLI_ROOT / "arcade_session.json"
RUN_PATH = CLI_ROOT / "arcade_run.md"
LOCK_PATH = CLI_ROOT / "arcade_run.lock"
PACKETS_DIR = CLI_ROOT / "arcade_packets"
ARCHIVE_DIR = CLI_ROOT / "arcade_run_archive"
COPILOT = Path("/opt/homebrew/bin/copilot")
COPILOT_CONFIG_DIR = ROOT / ".copilot-local"

FLAG_KEYS = ("idea", "theme", "mode", "tone", "mechanic", "content", "depth")
DEFAULT_FLAGS = {
    "idea": "",
    "theme": "",
    "mode": "",
    "tone": "",
    "mechanic": "",
    "content": "",
    "depth": "full",
}


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f"{path.suffix}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def ensure_local_copilot_config() -> Path:
    COPILOT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    source_dir = Path.home() / ".copilot"
    for name in ("config.json", "settings.json"):
        source = source_dir / name
        target = COPILOT_CONFIG_DIR / name
        if source.exists() and not target.exists():
            shutil.copy2(source, target)
    return COPILOT_CONFIG_DIR


def ensure_files() -> None:
    PACKETS_DIR.mkdir(parents=True, exist_ok=True)
    if not RUN_PATH.exists():
        RUN_PATH.write_text(
            "# ArcadeBuilder Run Memory\n\n"
            "Append-only run memory for hierarchical ArcadeBuilder packets.\n\n",
            encoding="utf-8",
        )


def append_run(text: str) -> None:
    ensure_files()
    with RUN_PATH.open("a", encoding="utf-8") as handle:
        handle.write(text.rstrip() + "\n")


def load_steps() -> list[dict[str, str]]:
    return load_json(STEPS_PATH, {"steps": []})["steps"]


def default_session() -> dict[str, Any]:
    return {
        "flags": dict(DEFAULT_FLAGS),
        "active_step": None,
        "active_packet": None,
        "completed_steps": [],
        "blocked_steps": [],
        "decisions": [],
        "reconciled": [],
        "last_result": None,
        "history": [],
    }


def load_session() -> dict[str, Any]:
    session = load_json(SESSION_PATH, default_session())
    session.setdefault("flags", dict(DEFAULT_FLAGS))
    for key, value in DEFAULT_FLAGS.items():
        session["flags"].setdefault(key, value)
    return session


def reset_session(flags: dict[str, str] | None = None, reason: str = "fresh-session") -> dict[str, Any]:
    ensure_files()
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = now_stamp().replace(":", "-")
    for path in (SESSION_PATH, RUN_PATH):
        if path.exists():
            path.rename(ARCHIVE_DIR / f"{stamp}_{path.name}")
    session = default_session()
    if flags:
        apply_flags(session, flags)
    append_history(session, reason, json.dumps(session["flags"], sort_keys=True))
    save_json(SESSION_PATH, session)
    RUN_PATH.write_text(
        "# ArcadeBuilder Run Memory\n\n"
        f"- started: {now_stamp()}\n"
        f"- reason: {reason}\n"
        f"- flags: {json.dumps(session['flags'], sort_keys=True)}\n",
        encoding="utf-8",
    )
    return session


def append_history(session: dict[str, Any], event: str, detail: str) -> None:
    session.setdefault("history", []).append(
        {"time": now_stamp(), "event": event, "detail": detail}
    )
    session["history"] = session["history"][-80:]


def find_step(step_id: str | None) -> dict[str, str] | None:
    if not step_id:
        return None
    for step in load_steps():
        if step["id"] == step_id:
            return step
    return None


def packet_path(step_id: str, kind: str) -> Path:
    safe_time = now_stamp().replace(":", "-")
    return PACKETS_DIR / f"{safe_time}_{step_id}_{kind}.md"


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def lock_info() -> dict[str, str] | None:
    if not LOCK_PATH.exists():
        return None
    try:
        return json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"run_id": "corrupt", "owner": "unknown"}


def git_status() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.stdout.splitlines() if result.returncode == 0 else []


def unexpected_dirty(lines: list[str]) -> list[str]:
    allowed = (
        " M Portfolio-CLI/",
        "?? Portfolio-CLI/",
        " M Portfolio-Vite/",
        "?? Portfolio-Vite/",
        " M memory.md",
        "?? memory.md",
    )
    ignored = {
        " M .DS_Store",
        "?? .playwright-mcp/",
        "?? .copilot-local/",
        "?? mini-arcade-control-console-cards.png",
        "?? mini-arcade-control.png",
        "?? mini-arcade-single-lane-built.png",
        "?? mini-arcade-single-lane.png",
        " D Pages/dragon.html",
        " D app.js",
        " D index.html",
        " D styles.css",
    }
    return [line for line in lines if line not in ignored and not line.startswith(allowed)]


def parse_flag_pairs(text: str) -> dict[str, str]:
    flags: dict[str, str] = {}
    parts = text.split()
    index = 0
    while index < len(parts):
        token = parts[index]
        if token.startswith("--"):
            key = token[2:].replace("-", "_")
            if key in FLAG_KEYS and index + 1 < len(parts):
                flags[key] = parts[index + 1]
                index += 2
                continue
        index += 1
    return flags


def apply_flags(session: dict[str, Any], flags: dict[str, str]) -> None:
    clean = {
        key: str(value).strip()
        for key, value in flags.items()
        if key in FLAG_KEYS and str(value).strip()
    }
    if "depth" in clean and clean["depth"] not in {"quick", "full", "deep"}:
        clean["depth"] = "full"
    session.setdefault("flags", dict(DEFAULT_FLAGS)).update(clean)


def flags_text(flags: dict[str, str]) -> str:
    return "\n".join(f"- {key}: {flags.get(key) or 'auto'}" for key in FLAG_KEYS)


def compose_worker_prompt(step: dict[str, str], session: dict[str, Any]) -> str:
    flags = session["flags"]
    return f"""Restate this packet literally.

Workspace:
- {ROOT}

Arcade flags:
{flags_text(flags)}

Current step:
- {step["id"]}
- {step["goal"]}

Packet prompt:
{step["prompt"]}

Return only:
- restated packet
- expansion domains
- candidate branches
- assumptions
- blockers
- validation cues
- downstream inputs

Do not edit files.
Do not choose final implementation unless this packet explicitly asks for reconciliation.
Treat Copilot output as candidate material, not truth.
Stay inside this stage. Do not perform extra exploration or unrelated work.
"""


def write_prompt_packet(step: dict[str, str], session: dict[str, Any]) -> Path:
    path = packet_path(step["id"], "prompt")
    content = f"""# ArcadeBuilder Work Packet

packet_kind: prompt
packet_status: pending
time: {now_stamp()}
step: {step["id"]}
module: {step["module"]}
title: {step["title"]}

## Goal

{step["goal"]}

## Worker Prompt

{compose_worker_prompt(step, session)}
"""
    path.write_text(content, encoding="utf-8")
    session["active_packet"] = relative(path)
    append_history(session, "prompt", relative(path))
    save_json(SESSION_PATH, session)
    return path


def write_worker_reply(step: dict[str, str], session: dict[str, Any], text: str) -> Path:
    path = packet_path(step["id"], "reply")
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    session["last_reply"] = relative(path)
    session["last_result"] = f"reply recorded for {step['id']}"
    append_history(session, "reply", relative(path))
    save_json(SESSION_PATH, session)
    return path


def make_brief_from_session(session: dict[str, Any]) -> IdeaBrief:
    flags = session["flags"]
    seed_parts = [
        flags.get("idea") or "arcade",
        flags.get("theme"),
        flags.get("mechanic"),
        flags.get("content"),
        flags.get("tone"),
    ]
    idea = " ".join(part for part in seed_parts if part).strip()
    brief = IdeaBrief(idea=idea)
    if flags.get("mode"):
        brief.chosen_mode = flags["mode"] if flags["mode"] else pick_fallback_mode(idea)
    brief.theme_pack = {
        "vibeWords": [value for value in (flags.get("theme"), flags.get("tone")) if value],
        "paletteDirection": flags.get("theme") or "",
        "surfaceStyle": "flag seeded arcade",
        "spaceType": flags.get("content") or "2d arcade",
    }
    brief.content_plan = {
        "contentObjects": [value for value in (flags.get("content"), flags.get("mechanic")) if value],
        "challengeFlow": f"{flags.get('mechanic') or 'react'} through {flags.get('idea') or 'arcade'}",
    }
    brief.feature_plan = {
        "coreMechanic": flags.get("mechanic") or flags.get("idea") or "arcade reaction",
        "supportMechanics": [value for value in (flags.get("theme"), flags.get("content")) if value],
        "controlStyle": "shared runtime controls",
    }
    return brief


class ArcadeBuilderShell(cmd.Cmd):
    intro = "ArcadeBuilder CLI attached. Type help or safe-next."
    prompt = "arcadebuilder> "

    def __init__(self, initial_flags: dict[str, str] | None = None):
        super().__init__()
        ensure_files()
        ensure_cli_support_files()
        self.session = load_session()
        if initial_flags:
            apply_flags(self.session, initial_flags)
            append_history(self.session, "flags", json.dumps(initial_flags, sort_keys=True))
            append_run(f"- flags: {json.dumps(self.session['flags'], sort_keys=True)}")
            save_json(SESSION_PATH, self.session)

    def do_status(self, arg: str) -> None:
        print(f"root: {ROOT}")
        print(f"active_step: {self.session.get('active_step')}")
        print(f"active_packet: {self.session.get('active_packet')}")
        print(f"last_result: {self.session.get('last_result')}")
        print(f"completed_steps: {len(self.session.get('completed_steps', []))}")
        print(f"blocked_steps: {len(self.session.get('blocked_steps', []))}")
        print(f"decisions: {len(self.session.get('decisions', []))}")
        info = lock_info()
        print(f"lock: {info['run_id'] if info else 'none'}")

    def do_flags(self, arg: str) -> None:
        updates = parse_flag_pairs(arg)
        if updates:
            apply_flags(self.session, updates)
            append_history(self.session, "flags", json.dumps(updates, sort_keys=True))
            save_json(SESSION_PATH, self.session)
        print(flags_text(self.session["flags"]))

    def do_steps(self, arg: str) -> None:
        for step in load_steps():
            marker = "*" if step["id"] == self.session.get("active_step") else " "
            done = "done" if step["id"] in self.session.get("completed_steps", []) else "open"
            print(f"{marker} {step['id']} [{step['module']}] {done} - {step['title']}")

    def do_safe_next(self, arg: str) -> None:
        completed = set(self.session.get("completed_steps", []))
        blocked = set(self.session.get("blocked_steps", []))
        for step in load_steps():
            if step["id"] in completed or step["id"] in blocked:
                continue
            self.session["active_step"] = step["id"]
            append_history(self.session, "safe-next", step["id"])
            save_json(SESSION_PATH, self.session)
            print(f"{step['id']} [{step['module']}]")
            print(step["goal"])
            return
        print("No safe step available.")

    def do_prompt(self, arg: str) -> None:
        step = find_step(arg.strip()) or find_step(self.session.get("active_step"))
        if not step:
            print("No step selected. Run safe-next or prompt <step_id>.")
            return
        path = write_prompt_packet(step, self.session)
        print(path)

    def do_copilot(self, arg: str) -> None:
        step = find_step(arg.strip()) or find_step(self.session.get("active_step"))
        if not step:
            print("No step selected. Run safe-next first.")
            return
        prompt_path = write_prompt_packet(step, self.session)
        prompt = compose_worker_prompt(step, self.session)
        if not COPILOT.exists():
            self.session["last_result"] = "copilot unavailable; pending packet written"
            append_history(self.session, "copilot-blocked", "missing /opt/homebrew/bin/copilot")
            save_json(SESSION_PATH, self.session)
            print(f"blocked: copilot unavailable; packet pending {prompt_path}")
            return
        result = subprocess.run(
            [
                str(COPILOT),
                "--config-dir",
                str(ensure_local_copilot_config()),
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
                str(ROOT),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=3600,
        )
        output = (result.stdout or result.stderr or "").strip()
        if result.returncode != 0:
            self.session["last_result"] = f"copilot blocked: {output[:240]}"
            append_history(self.session, "copilot-blocked", output[:240])
            save_json(SESSION_PATH, self.session)
            print(f"blocked: {output}")
            print(f"packet pending {prompt_path}")
            return
        path = write_worker_reply(step, self.session, output)
        print(path)

    def do_reply(self, arg: str) -> None:
        step = find_step(arg.strip()) or find_step(self.session.get("active_step"))
        if not step:
            print("No step selected. Run safe-next first.")
            return
        print("Paste worker reply. End with a single line: .")
        lines = []
        while True:
            line = input()
            if line == ".":
                break
            lines.append(line)
        path = write_worker_reply(step, self.session, "\n".join(lines))
        print(path)

    def do_reconcile(self, arg: str) -> None:
        reply_arg = arg.strip() or self.session.get("last_reply")
        if not reply_arg:
            print("No reply to reconcile.")
            return
        path = (ROOT / reply_arg).resolve()
        if not str(path).startswith(str(PACKETS_DIR.resolve())) or not path.exists():
            print("Reply not found or outside arcade_packets.")
            return
        step_id = self.session.get("active_step") or "unknown"
        text = path.read_text(encoding="utf-8")
        artifact = {
            "time": now_stamp(),
            "step": step_id,
            "source": relative(path),
            "summary": "\n".join(line for line in text.splitlines() if line.strip())[:1200],
        }
        self.session.setdefault("reconciled", []).append(artifact)
        self.session["reconciled"] = self.session["reconciled"][-30:]
        self.session["last_result"] = f"reconciled {relative(path)}"
        append_run(f"- reconciled {step_id}: {artifact['summary'][:300]}")
        append_history(self.session, "reconcile", relative(path))
        save_json(SESSION_PATH, self.session)
        print("reconciled")

    def do_decision(self, arg: str) -> None:
        text = arg.strip()
        if not text:
            print("decision text required")
            return
        self.session.setdefault("decisions", []).append({"time": now_stamp(), "text": text})
        self.session["decisions"] = self.session["decisions"][-50:]
        append_history(self.session, "decision", text)
        append_run(f"- decision: {text}")
        save_json(SESSION_PATH, self.session)
        print("recorded")

    def do_complete_step(self, arg: str) -> None:
        step_id = arg.strip() or self.session.get("active_step")
        if not step_id:
            print("step required")
            return
        completed = self.session.setdefault("completed_steps", [])
        if step_id not in completed:
            completed.append(step_id)
        append_history(self.session, "complete-step", step_id)
        append_run(f"- completed: {step_id}")
        save_json(SESSION_PATH, self.session)
        print("recorded")

    def do_block_step(self, arg: str) -> None:
        step_id = arg.strip() or self.session.get("active_step")
        if not step_id:
            print("step required")
            return
        blocked = self.session.setdefault("blocked_steps", [])
        if step_id not in blocked:
            blocked.append(step_id)
        append_history(self.session, "block-step", step_id)
        append_run(f"- blocked: {step_id}")
        save_json(SESSION_PATH, self.session)
        print("recorded")

    def do_finish_run(self, arg: str) -> None:
        summary = arg.strip() or "finished"
        self.session["last_result"] = summary
        append_history(self.session, "finish-run", summary)
        append_run(f"- finished: {summary}")
        save_json(SESSION_PATH, self.session)
        if LOCK_PATH.exists():
            LOCK_PATH.unlink()
        print("finished")

    def do_validate(self, arg: str) -> None:
        brief = make_brief_from_session(self.session)
        brief = fill_game_json(brief, "validate from ArcadeBuilder flags")
        validate_game_json(brief.game_json or {})
        self.session["last_result"] = f"validated {brief.game_json['slug']}"
        append_history(self.session, "validate", brief.game_json["slug"])
        save_json(SESSION_PATH, self.session)
        print(f"validated {brief.game_json['slug']}")

    def do_build(self, arg: str) -> None:
        dirty = unexpected_dirty(git_status())
        if dirty:
            self.session["last_result"] = "blocked unexpected dirty worktree"
            save_json(SESSION_PATH, self.session)
            print("blocked: unexpected dirty worktree")
            for line in dirty:
                print(line)
            return
        brief = make_brief_from_session(self.session)
        game_json = build_game(brief)
        self.session["last_result"] = f"built {game_json['slug']}"
        append_history(self.session, "build", game_json["slug"])
        append_run(f"- built: {game_json['slug']}")
        save_json(SESSION_PATH, self.session)
        print(f"built {game_json['slug']}")

    def do_quit(self, arg: str) -> bool:
        save_json(SESSION_PATH, self.session)
        return True

    def do_exit(self, arg: str) -> bool:
        return self.do_quit(arg)

    def emptyline(self) -> None:
        return None

    def default(self, line: str) -> None:
        command, _, rest = line.partition(" ")
        normalized = command.replace("-", "_")
        if normalized != command and hasattr(self, f"do_{normalized}"):
            return self.onecmd(f"{normalized} {rest}".strip())
        print(f"unknown command: {line}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hierarchical ArcadeBuilder CLI")
    parser.add_argument("--idea", default="")
    parser.add_argument("--theme", default="")
    parser.add_argument("--mode", default="")
    parser.add_argument("--tone", default="")
    parser.add_argument("--mechanic", default="")
    parser.add_argument("--content", default="")
    parser.add_argument("--depth", choices=["quick", "full", "deep"], default="")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    flags = {key: getattr(args, key) for key in FLAG_KEYS if getattr(args, key, "")}
    shell = ArcadeBuilderShell(flags)
    if args.plan_only:
        shell.onecmd("safe-next")
        shell.onecmd("prompt")
        return
    if args.validate:
        shell.onecmd("validate")
        return
    if args.build:
        shell.onecmd("build")
        return
    shell.cmdloop()


if __name__ == "__main__":
    main()
