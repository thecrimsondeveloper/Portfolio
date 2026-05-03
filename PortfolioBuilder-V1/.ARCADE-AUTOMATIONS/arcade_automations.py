#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import queue
import re
import signal
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
TARGETS_FILE = ROOT / "targets.json"
LATEST_FILE = ROOT / "latest.json"
RUNS_DIR = ROOT / "runs"
LOGS_DIR = ROOT / "logs"
VERSIONS_DIR = ROOT / "versions"
FAILED_BUILDS_DIR = ROOT / "failed-builds"
LOCK_FILE = ROOT / "supervisor.lock"
DEFAULT_VERSION = "v001"
DEFAULT_MAX_CONCURRENT = 1
DEFAULT_HEARTBEAT_SECONDS = 4.0

EventCallback = Callable[[str, dict[str, Any]], None]


def emit_event(name: str, payload: dict[str, Any] | None = None, callbacks: list[EventCallback] | None = None) -> None:
    event = {
        "event": name,
        "at": iso(),
        **(payload or {}),
    }
    line = f"[event] {name} {json.dumps(event, sort_keys=True)}"
    print(line, flush=True)
    for callback in callbacks or []:
        callback(name, event)


def utc_now() -> datetime:
    return datetime.utcnow()


def iso(dt: datetime | None = None) -> str:
    return (dt or utc_now()).replace(microsecond=0).isoformat() + "Z"


def timestamp() -> str:
    return utc_now().strftime("%Y%m%d-%H%M%S")


def ensure_layout() -> None:
    for path in (RUNS_DIR, LOGS_DIR, VERSIONS_DIR, FAILED_BUILDS_DIR):
        path.mkdir(parents=True, exist_ok=True)
    if not TARGETS_FILE.exists():
        atomic_write_json(TARGETS_FILE, {"targets": {}, "updatedAt": iso()})
    if not LATEST_FILE.exists():
        atomic_write_json(
            LATEST_FILE,
            {
                "latestVersion": DEFAULT_VERSION,
                "promotedAt": iso(),
                "reason": "Initial automation baseline.",
            },
        )
    first_version = VERSIONS_DIR / DEFAULT_VERSION
    first_version.mkdir(parents=True, exist_ok=True)
    first_targets = first_version / "targets.json"
    if not first_targets.exists():
        atomic_write_json(first_targets, {"targets": {}, "updatedAt": iso()})


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else default


def load_targets() -> dict[str, Any]:
    ensure_layout()
    data = load_json(TARGETS_FILE, {"targets": {}, "updatedAt": iso()})
    targets = data.get("targets")
    if isinstance(targets, list):
        data["targets"] = {
            str(item["id"]): item for item in targets if isinstance(item, dict) and item.get("id")
        }
    elif not isinstance(targets, dict):
        data["targets"] = {}
    return data


def save_targets(data: dict[str, Any]) -> None:
    data["updatedAt"] = iso()
    atomic_write_json(TARGETS_FILE, data)


def sanitize_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip()).strip("-")
    if not cleaned:
        raise ValueError("id cannot be empty after sanitizing")
    return cleaned


def parse_env(values: list[str] | None) -> dict[str, str]:
    env: dict[str, str] = {}
    for item in values or []:
        if "=" not in item:
            raise ValueError(f"env value must be KEY=VALUE: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("env key cannot be empty")
        env[key] = value
    return env


def parse_command(raw: str) -> list[str]:
    try:
        command = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"--cmd-json must be a JSON array: {exc}") from exc
    if not isinstance(command, list) or not command or not all(isinstance(part, str) for part in command):
        raise ValueError("--cmd-json must be a non-empty JSON array of strings")
    return command


def format_context(target: dict[str, Any], run_id: str) -> dict[str, str]:
    stamp = timestamp()
    target_id = str(target.get("id", "target"))
    slug_template = str(target.get("slugTemplate") or f"{target_id}-{{timestamp}}")
    goal_template = str(target.get("goalTemplate") or "Run arcade automation target {target_id}. Run id: {run_id}.")
    context = {
        "run_id": run_id,
        "timestamp": stamp,
        "target_id": target_id,
    }
    slug = render_template(slug_template, context)
    context["slug"] = sanitize_id(slug.lower())
    context["goal"] = render_template(goal_template, context)
    return context


def render_template(value: str, context: dict[str, str]) -> str:
    rendered = value
    for key, replacement in context.items():
        rendered = rendered.replace("{" + key + "}", replacement)
    return rendered


def render_command(command: list[str], context: dict[str, str]) -> list[str]:
    return [render_template(part, context) for part in command]


def render_env(target_env: dict[str, Any] | None, context: dict[str, str]) -> dict[str, str]:
    rendered: dict[str, str] = {}
    for key, value in (target_env or {}).items():
        rendered[str(key)] = render_template(str(value), context)
    return rendered


def detect_generated_folder(cwd: Path, context: dict[str, str], log_text: str) -> str | None:
    workspace_match = re.search(r"Workspace initialized at ([^\n\r]+)", log_text)
    if workspace_match:
        return workspace_match.group(1).strip()
    slug = context.get("slug")
    candidate = cwd.parent / "Portfolio-Vite" / "Pages" / slug
    return str(candidate) if candidate.exists() else None


def detect_builder_run_json(log_text: str) -> str | None:
    match = re.search(r"Log saved to ([^\n\r]+\.json)", log_text)
    return match.group(1).strip() if match else None


def quarantine_failed_generated_folder(generated_folder: str | None, run_id: str) -> str | None:
    if not generated_folder:
        return None
    source = Path(generated_folder)
    if not source.exists() or not source.is_dir():
        return None
    destination = FAILED_BUILDS_DIR / f"{run_id}-{source.name}"
    counter = 2
    while destination.exists():
        destination = FAILED_BUILDS_DIR / f"{run_id}-{source.name}-{counter}"
        counter += 1
    shutil.move(str(source), str(destination))
    return str(destination)


def target_due(target: dict[str, Any], now: datetime) -> bool:
    if not target.get("enabled", True):
        return False
    next_run = target.get("nextRunAt")
    if not next_run:
        return True
    try:
        parsed = datetime.fromisoformat(str(next_run).replace("Z", ""))
    except ValueError:
        return True
    return parsed <= now


def next_run_time(target: dict[str, Any], start: datetime | None = None) -> str:
    minutes = float(target.get("intervalMinutes") or 60)
    return iso((start or utc_now()) + timedelta(minutes=minutes))


def set_target_fields(target_id: str, fields: dict[str, Any]) -> None:
    data = load_targets()
    targets = data["targets"]
    target = targets.get(target_id)
    if not target:
        return
    target.update(fields)
    save_targets(data)


def run_target(
    target: dict[str, Any],
    reason: str = "scheduled",
    heartbeat_seconds: float = DEFAULT_HEARTBEAT_SECONDS,
    event_callbacks: list[EventCallback] | None = None,
) -> dict[str, Any]:
    ensure_layout()
    target_id = sanitize_id(str(target["id"]))
    run_id = f"{timestamp()}-{target_id}"
    context = format_context(target, run_id)
    command = render_command(list(target["command"]), context)
    cwd = Path(str(target["cwd"])).expanduser()
    env_overlay = render_env(target.get("env"), context)
    run_dir = RUNS_DIR / target_id
    log_dir = LOGS_DIR / target_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{run_id}.log"
    record_path = run_dir / f"{run_id}.json"
    started = utc_now()
    record: dict[str, Any] = {
        "runId": run_id,
        "targetId": target_id,
        "version": target.get("version", DEFAULT_VERSION),
        "reason": reason,
        "status": "RUNNING",
        "startedAt": iso(started),
        "endedAt": None,
        "cwd": str(cwd),
        "command": command,
        "envKeys": sorted(env_overlay.keys()),
        "logPath": str(log_path),
        "generatedFolder": None,
        "builderRunJson": None,
        "exitCode": None,
    }
    atomic_write_json(record_path, record)
    emit_event(
        "RUN_RECORD_CREATED",
        {"targetId": target_id, "runId": run_id, "recordPath": str(record_path), "reason": reason},
        event_callbacks,
    )

    child_env = os.environ.copy()
    child_env.update(env_overlay)
    output = ""
    exit_code = 127
    last_message = "process launched"
    last_heartbeat = time.monotonic()
    try:
        proc = subprocess.Popen(
            command,
            cwd=str(cwd),
            env=child_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        with log_path.open("w", encoding="utf-8") as log_file:
            assert proc.stdout is not None

            def log_event(_name: str, event: dict[str, Any]) -> None:
                log_file.write(f"[event] {json.dumps(event, sort_keys=True)}\n")
                log_file.flush()

            callbacks = [log_event] + list(event_callbacks or [])
            emit_event(
                "RUN_PROCESS_SPAWNED",
                {"targetId": target_id, "runId": run_id, "pid": proc.pid, "logPath": str(log_path)},
                callbacks,
            )
            print(
                f"[run:{target_id}] {run_id} spawned pid={proc.pid} log={log_path}",
                flush=True,
            )
            line_queue: queue.Queue[str] = queue.Queue()
            line_count = 0

            def read_stdout() -> None:
                assert proc.stdout is not None
                for reader_line in proc.stdout:
                    line_queue.put(reader_line)

            reader = threading.Thread(target=read_stdout, name=f"reader-{run_id}", daemon=True)
            reader.start()

            while proc.poll() is None or reader.is_alive() or not line_queue.empty():
                try:
                    line = line_queue.get(timeout=0.5)
                except queue.Empty:
                    line = ""
                if line:
                    log_file.write(line)
                    log_file.flush()
                    output += line
                    clean_line = line.rstrip()
                    if clean_line:
                        line_count += 1
                        last_message = clean_line[-240:]
                        if line_count == 1 or clean_line.startswith(("--- ", "[✔]", "[🏁", "[ERROR]", "[FALLBACK]")):
                            emit_event(
                                "RUN_OUTPUT_LINE",
                                {
                                    "targetId": target_id,
                                    "runId": run_id,
                                    "line": line_count,
                                    "message": last_message,
                                },
                                callbacks,
                            )
                        print(f"[run:{target_id}] {clean_line}", flush=True)
                    last_heartbeat = time.monotonic()
                    continue

                now = time.monotonic()
                if proc.poll() is None and now - last_heartbeat >= heartbeat_seconds:
                    elapsed = round((utc_now() - started).total_seconds(), 1)
                    heartbeat = (
                        f"[heartbeat:{target_id}] run={run_id} elapsed={elapsed}s "
                        f"last={last_message}\n"
                    )
                    log_file.write(heartbeat)
                    log_file.flush()
                    output += heartbeat
                    emit_event(
                        "RUN_HEARTBEAT",
                        {
                            "targetId": target_id,
                            "runId": run_id,
                            "elapsedSeconds": elapsed,
                            "lastMessage": last_message,
                        },
                        callbacks,
                    )
                    print(heartbeat.rstrip(), flush=True)
                    last_heartbeat = now
        exit_code = proc.wait()
    except Exception as exc:
        output += f"\n[AUTOMATION ERROR] {exc}\n"
        log_path.write_text(output, encoding="utf-8")
        emit_event(
            "RUN_EXCEPTION",
            {"targetId": target_id, "runId": run_id, "error": str(exc), "logPath": str(log_path)},
            event_callbacks,
        )

    ended = utc_now()
    generated_folder = detect_generated_folder(cwd, context, output)
    quarantined_folder = None
    if exit_code != 0:
        quarantined_folder = quarantine_failed_generated_folder(generated_folder, run_id)

    record.update(
        {
            "status": "PASS" if exit_code == 0 else "FAIL",
            "endedAt": iso(ended),
            "durationSeconds": round((ended - started).total_seconds(), 3),
            "exitCode": exit_code,
            "generatedFolder": generated_folder,
            "quarantinedFolder": quarantined_folder,
            "builderRunJson": detect_builder_run_json(output),
            "context": context,
        }
    )
    atomic_write_json(record_path, record)
    emit_event(
        "RUN_RECORD_FINALIZED",
        {
            "targetId": target_id,
            "runId": run_id,
            "status": record["status"],
            "exitCode": exit_code,
            "durationSeconds": record["durationSeconds"],
            "generatedFolder": generated_folder,
            "quarantinedFolder": quarantined_folder,
            "recordPath": str(record_path),
        },
        event_callbacks,
    )
    set_target_fields(
        target_id,
        {
            "lastRunAt": record["endedAt"],
            "lastRunId": run_id,
            "lastStatus": record["status"],
            "lastRecordPath": str(record_path),
            "nextRunAt": next_run_time(target, ended),
        },
    )
    emit_event(
        "TARGET_SCHEDULED",
        {"targetId": target_id, "runId": run_id, "nextRunAt": next_run_time(target, ended)},
        event_callbacks,
    )
    return record


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


class SupervisorLock:
    def __enter__(self) -> "SupervisorLock":
        ensure_layout()
        if LOCK_FILE.exists():
            try:
                pid = int(LOCK_FILE.read_text(encoding="utf-8").strip())
            except ValueError:
                pid = -1
            if pid > 0 and process_alive(pid):
                raise RuntimeError(f"supervisor already running with pid {pid}")
            LOCK_FILE.unlink(missing_ok=True)
        fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        LOCK_FILE.unlink(missing_ok=True)


class Supervisor:
    def __init__(self, poll_seconds: float, max_concurrent: int, heartbeat_seconds: float):
        self.poll_seconds = poll_seconds
        self.max_concurrent = max(1, max_concurrent)
        self.heartbeat_seconds = max(1.0, heartbeat_seconds)
        self.running: dict[str, threading.Thread] = {}
        self.stop_requested = False

    def request_stop(self, *_args: Any) -> None:
        self.stop_requested = True
        emit_event("SUPERVISOR_STOP_REQUESTED", {"activeRuns": sorted(self.running.keys())})

    def prune_finished(self) -> None:
        for target_id, thread in list(self.running.items()):
            if not thread.is_alive():
                self.running.pop(target_id, None)
                emit_event("SUPERVISOR_THREAD_PRUNED", {"targetId": target_id, "activeRuns": sorted(self.running.keys())})

    def start_target(self, target: dict[str, Any]) -> None:
        target_id = str(target["id"])
        snapshot = json.loads(json.dumps(target))
        emit_event(
            "SUPERVISOR_TARGET_DISPATCH",
            {
                "targetId": target_id,
                "nextRunAt": snapshot.get("nextRunAt"),
                "intervalMinutes": snapshot.get("intervalMinutes"),
            },
        )

        def worker() -> None:
            emit_event("SUPERVISOR_WORKER_START", {"targetId": target_id})
            print(f"[run] {target_id} starting", flush=True)
            record = run_target(snapshot, reason="scheduled", heartbeat_seconds=self.heartbeat_seconds)
            emit_event(
                "SUPERVISOR_WORKER_DONE",
                {"targetId": target_id, "status": record["status"], "runId": record["runId"]},
            )
            print(f"[run] {target_id} {record['status']} {record['runId']}", flush=True)

        thread = threading.Thread(target=worker, name=f"arcade-auto-{target_id}", daemon=True)
        self.running[target_id] = thread
        thread.start()

    def run(self) -> None:
        signal.signal(signal.SIGINT, self.request_stop)
        signal.signal(signal.SIGTERM, self.request_stop)
        print(f"[supervisor] watching {TARGETS_FILE}", flush=True)
        emit_event(
            "SUPERVISOR_START",
            {
                "targetsFile": str(TARGETS_FILE),
                "pollSeconds": self.poll_seconds,
                "maxConcurrent": self.max_concurrent,
                "heartbeatSeconds": self.heartbeat_seconds,
            },
        )
        while not self.stop_requested:
            self.prune_finished()
            data = load_targets()
            now = utc_now()
            targets = data.get("targets", {})
            due_targets = [
                target_id
                for target_id, target in targets.items()
                if isinstance(target, dict) and target_due(target, now) and target_id not in self.running
            ]
            emit_event(
                "SUPERVISOR_POLL",
                {
                    "targetCount": len(targets),
                    "dueTargets": due_targets,
                    "activeRuns": sorted(self.running.keys()),
                },
            )
            for target_id, target in list(targets.items()):
                if self.stop_requested:
                    break
                if target_id in self.running:
                    emit_event("SUPERVISOR_TARGET_BUSY", {"targetId": target_id})
                    continue
                if len(self.running) >= self.max_concurrent:
                    emit_event(
                        "SUPERVISOR_MAX_CONCURRENT",
                        {"activeRuns": sorted(self.running.keys()), "maxConcurrent": self.max_concurrent},
                    )
                    break
                if isinstance(target, dict) and target_due(target, now):
                    emit_event("SUPERVISOR_TARGET_DUE", {"targetId": target_id, "now": iso(now)})
                    self.start_target(target)
            time.sleep(self.poll_seconds)
        print("[supervisor] stopping; waiting for active runs", flush=True)
        emit_event("SUPERVISOR_STOPPING", {"activeRuns": sorted(self.running.keys())})
        for thread in list(self.running.values()):
            thread.join()
        emit_event("SUPERVISOR_STOPPED", {"activeRuns": sorted(self.running.keys())})


def add_target(args: argparse.Namespace) -> None:
    data = load_targets()
    target_id = sanitize_id(args.id)
    data["targets"][target_id] = {
        "id": target_id,
        "enabled": not args.paused,
        "intervalMinutes": args.interval_minutes,
        "cwd": str(Path(args.cwd).expanduser()),
        "command": parse_command(args.cmd_json),
        "env": parse_env(args.env),
        "goalTemplate": args.goal_template,
        "slugTemplate": args.slug_template,
        "nextRunAt": None if args.run_immediately else next_run_time({"intervalMinutes": args.interval_minutes}),
        "lastRunAt": None,
        "lastRunId": None,
        "version": args.version,
    }
    save_targets(data)
    print(f"added target {target_id}")


def remove_target(args: argparse.Namespace) -> None:
    data = load_targets()
    target_id = sanitize_id(args.id)
    existed = data["targets"].pop(target_id, None) is not None
    save_targets(data)
    print(("removed" if existed else "missing") + f" target {target_id}")


def set_enabled(args: argparse.Namespace, enabled: bool) -> None:
    data = load_targets()
    target_id = sanitize_id(args.id)
    target = data["targets"].get(target_id)
    if not target:
        raise SystemExit(f"target not found: {target_id}")
    target["enabled"] = enabled
    if enabled and args.run_immediately:
        target["nextRunAt"] = None
    save_targets(data)
    print(("resumed" if enabled else "paused") + f" target {target_id}")


def list_targets(_args: argparse.Namespace) -> None:
    data = load_targets()
    targets = data.get("targets", {})
    if not targets:
        print("no targets")
        return
    for target_id, target in sorted(targets.items()):
        state = "enabled" if target.get("enabled", True) else "paused"
        role = target.get("lifecycleRole") or "unclassified"
        version = target.get("version", DEFAULT_VERSION)
        print(
            f"{target_id} {state} role={role} version={version} every={target.get('intervalMinutes')}m "
            f"next={target.get('nextRunAt')} last={target.get('lastStatus', '-')}/{target.get('lastRunId', '-')}"
        )


def status(_args: argparse.Namespace) -> None:
    data = load_targets()
    latest = load_json(LATEST_FILE, {})
    lock_pid = None
    if LOCK_FILE.exists():
        try:
            lock_pid = int(LOCK_FILE.read_text(encoding="utf-8").strip())
        except ValueError:
            lock_pid = None
    print(json.dumps(
        {
            "targets": len(data.get("targets", {})),
            "latestVersion": latest.get("latestVersion"),
            "lifecyclePolicy": data.get("lifecyclePolicy"),
            "supervisorPid": lock_pid,
            "supervisorRunning": bool(lock_pid and process_alive(lock_pid)),
            "targetsFile": str(TARGETS_FILE),
        },
        indent=2,
    ))


def run_now(args: argparse.Namespace) -> None:
    data = load_targets()
    target_id = sanitize_id(args.id)
    target = data["targets"].get(target_id)
    if not target:
        raise SystemExit(f"target not found: {target_id}")
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text(encoding="utf-8").strip())
        except ValueError:
            pid = -1
        if pid > 0 and process_alive(pid):
            target["nextRunAt"] = None
            target["manualRunRequestedAt"] = iso()
            save_targets(data)
            print(f"queued target {target_id} for running supervisor pid {pid}")
            return
    record = run_target(target, reason="manual", heartbeat_seconds=args.heartbeat_seconds)
    print(json.dumps(record, indent=2))
    if record.get("status") != "PASS":
        raise SystemExit(int(record.get("exitCode") or 1))


def supervisor(args: argparse.Namespace) -> None:
    with SupervisorLock():
        Supervisor(args.poll_seconds, args.max_concurrent, args.heartbeat_seconds).run()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arcade automation target supervisor")
    sub = parser.add_subparsers(dest="command_name", required=True)

    p = sub.add_parser("supervisor", help="Run the hot-reload interval supervisor")
    p.add_argument("--poll-seconds", type=float, default=5.0)
    p.add_argument("--max-concurrent", type=int, default=DEFAULT_MAX_CONCURRENT)
    p.add_argument("--heartbeat-seconds", type=float, default=DEFAULT_HEARTBEAT_SECONDS)
    p.set_defaults(func=supervisor)

    p = sub.add_parser("add-target", help="Add or replace an automation target")
    p.add_argument("--id", required=True)
    p.add_argument("--interval-minutes", type=float, required=True)
    p.add_argument("--cwd", required=True)
    p.add_argument("--cmd-json", required=True)
    p.add_argument("--env", action="append", default=[])
    p.add_argument("--goal-template", default="Run arcade automation target {target_id}. Run id: {run_id}.")
    p.add_argument("--slug-template", default="{target_id}-{timestamp}")
    p.add_argument("--version", default=DEFAULT_VERSION)
    p.add_argument("--paused", action="store_true")
    p.add_argument("--no-run-immediately", dest="run_immediately", action="store_false", default=True)
    p.set_defaults(func=add_target)

    p = sub.add_parser("remove-target", help="Remove an automation target")
    p.add_argument("--id", required=True)
    p.set_defaults(func=remove_target)

    p = sub.add_parser("pause-target", help="Pause an automation target")
    p.add_argument("--id", required=True)
    p.set_defaults(func=lambda args: set_enabled(args, False))

    p = sub.add_parser("resume-target", help="Resume an automation target")
    p.add_argument("--id", required=True)
    p.add_argument("--no-run-immediately", dest="run_immediately", action="store_false", default=True)
    p.set_defaults(func=lambda args: set_enabled(args, True))

    p = sub.add_parser("run-now", help="Run immediately or queue for the active supervisor")
    p.add_argument("--id", required=True)
    p.add_argument("--heartbeat-seconds", type=float, default=DEFAULT_HEARTBEAT_SECONDS)
    p.set_defaults(func=run_now)

    p = sub.add_parser("list-targets", help="List automation targets")
    p.set_defaults(func=list_targets)

    p = sub.add_parser("status", help="Print supervisor and target status")
    p.set_defaults(func=status)

    return parser


def main() -> None:
    ensure_layout()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
