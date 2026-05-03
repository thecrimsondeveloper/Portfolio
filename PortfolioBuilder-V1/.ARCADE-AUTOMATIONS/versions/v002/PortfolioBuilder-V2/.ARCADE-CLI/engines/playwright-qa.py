#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import http.server
import json
import re
import subprocess
import sys
import threading
import time
from pathlib import Path


def run_command(command: list[str], cwd: Path) -> dict:
    started = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        return {
            "command": command,
            "ok": result.returncode == 0,
            "returnCode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "durationSeconds": round(time.time() - started, 3),
        }
    except Exception as e:
        return {
            "command": command,
            "ok": False,
            "returnCode": None,
            "stdout": "",
            "stderr": str(e),
            "durationSeconds": round(time.time() - started, 3),
        }


def check_json_file(path: Path) -> dict:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return {"file": path.name, "ok": True, "error": ""}
    except Exception as e:
        return {"file": path.name, "ok": False, "error": str(e)}


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        return


@contextlib.contextmanager
def local_server(root: Path):
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(root), **kwargs)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/index.html"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def serious_console_messages(messages: list[dict]) -> list[dict]:
    ignored = ("favicon.ico", "willReadFrequently")
    serious = []
    for message in messages:
        text = message.get("text", "")
        if any(token in text for token in ignored):
            continue
        if message.get("type") in {"error", "warning"}:
            serious.append(message)
    return serious


def run_browser_check(root: Path, pass_index: int) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        return {
            "ok": False,
            "setupError": f"Python Playwright is not available: {e}",
            "seriousConsoleMessages": [],
            "consoleMessages": [],
            "pageErrors": [],
        }

    artifacts_dir = root / ".qa"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = artifacts_dir / f"playwright-pass-{pass_index}.png"
    console_messages: list[dict] = []
    page_errors: list[str] = []

    with local_server(root) as url:
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1024, "height": 768})
                page.on("console", lambda msg: console_messages.append({"type": msg.type, "text": msg.text}))
                page.on("pageerror", lambda exc: page_errors.append(str(exc)))
                response = page.goto(url, wait_until="networkidle", timeout=15000)
                status = response.status if response else None
                page.wait_for_timeout(500)
                initial_buttons = button_inventory(page)
                initial_text = page.locator("body").inner_text(timeout=3000)[:500]
                initial_state = classify_initial_state(initial_text, initial_buttons)
                before = canvas_probe(page)
                click_result = click_start_button(page)
                page.wait_for_timeout(1000)
                after = canvas_probe(page)
                visible_text = page.locator("body").inner_text(timeout=3000)[:500]
                buttons_after = button_inventory(page)
                button_labels = [button["text"] for button in buttons_after if button.get("text")]
                page.screenshot(path=str(screenshot_path), full_page=True)
                browser.close()
        except Exception as e:
            return {
                "ok": False,
                "url": url,
                "setupError": "",
                "browserError": str(e),
                "seriousConsoleMessages": serious_console_messages(console_messages),
                "consoleMessages": console_messages,
                "pageErrors": page_errors,
                "screenshot": str(screenshot_path),
            }

    serious = serious_console_messages(console_messages)
    canvas_before_pixels = int(before.get("nonBlackPixels", 0) or 0)
    canvas_after_pixels = int(after.get("nonBlackPixels", 0) or 0)
    canvas_delta_nonblack = canvas_after_pixels - canvas_before_pixels
    canvas_gained_pixels = canvas_delta_nonblack > 100
    canvas_became_nonblank = canvas_after_pixels > 100
    valid_start_clicked = click_result.get("kind") == "valid-start" and click_result.get("clicked")
    playable_ui_detected = bool(visible_text.strip()) and (after.get("canvasPresent") or bool(button_labels))
    external_game_js = check_external_game_js(root)
    dom_contract = check_dom_contract(root)
    title_consistency = check_title_consistency(root, visible_text)
    failure_reasons = browser_failure_reasons(
        status=status,
        serious=serious,
        page_errors=page_errors,
        browser_error="",
        initial_state=initial_state,
        click_result=click_result,
        canvas_after_pixels=canvas_after_pixels,
        canvas_became_nonblank=canvas_became_nonblank,
        canvas_gained_pixels=canvas_gained_pixels,
        external_game_js=external_game_js,
        dom_contract=dom_contract,
        title_consistency=title_consistency,
    )
    ok = not failure_reasons

    return {
        "ok": ok,
        "url": url,
        "httpStatus": status,
        "setupError": "",
        "browserError": "",
        "consoleMessages": console_messages,
        "seriousConsoleMessages": serious,
        "pageErrors": page_errors,
        "initialState": initial_state,
        "initialButtons": initial_buttons,
        "buttonLabels": button_labels,
        "clickedStart": click_result,
        "canvasBefore": before,
        "canvasAfter": after,
        "canvasDeltaNonblack": canvas_delta_nonblack,
        "canvasGainedPixels": canvas_gained_pixels,
        "visibleTextSample": visible_text,
        "playableUiDetected": playable_ui_detected,
        "validStartClicked": valid_start_clicked,
        "canvasBecameNonblank": canvas_became_nonblank,
        "externalGameJs": external_game_js,
        "domContract": dom_contract,
        "titleConsistency": title_consistency,
        "failureReasons": failure_reasons,
        "screenshot": str(screenshot_path),
    }


def canvas_probe(page) -> dict:
    return page.evaluate(
        """() => {
            const canvas = document.querySelector('canvas');
            if (!canvas) return { canvasPresent: false, nonBlackPixels: 0, size: null };
            const ctx = canvas.getContext('2d', { willReadFrequently: true });
            let nonBlackPixels = 0;
            try {
                const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
                for (let i = 0; i < data.length; i += 4) {
                    if (data[i] || data[i + 1] || data[i + 2]) nonBlackPixels++;
                }
            } catch (error) {
                return { canvasPresent: true, nonBlackPixels: 0, size: [canvas.width, canvas.height], error: String(error) };
            }
            return { canvasPresent: true, nonBlackPixels, size: [canvas.width, canvas.height] };
        }"""
    )


def button_inventory(page) -> list[dict]:
    return page.locator("button").evaluate_all(
        """(buttons) => buttons.map((button) => {
            const style = window.getComputedStyle(button);
            const rect = button.getBoundingClientRect();
            const text = button.innerText.trim();
            return {
                text,
                id: button.id || "",
                disabled: Boolean(button.disabled),
                visible: Boolean(text) &&
                    style.display !== "none" &&
                    style.visibility !== "hidden" &&
                    Number(style.opacity || "1") > 0 &&
                    rect.width > 0 &&
                    rect.height > 0
            };
        })"""
    )


def normalized_label(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def is_restart_label(text: str) -> bool:
    label = normalized_label(text)
    return any(token in label for token in ("restart", "retry", "play again", "again"))


def is_valid_start_label(text: str) -> bool:
    label = normalized_label(text)
    if not label or is_restart_label(label):
        return False
    return (
        label in {"start", "play", "begin", "start game", "play game", "begin game"}
        or label.startswith("start ")
        or label.startswith("begin ")
    )


def classify_initial_state(visible_text: str, buttons: list[dict]) -> str:
    text = normalized_label(visible_text)
    visible_buttons = [button for button in buttons if button.get("visible") and not button.get("disabled")]
    if "game over" in text or any(is_restart_label(button.get("text", "")) for button in visible_buttons):
        return "gameOver"
    if any(is_valid_start_label(button.get("text", "")) for button in visible_buttons):
        return "start"
    if visible_buttons:
        return "unknown"
    return "unknown"


def click_start_button(page) -> dict:
    buttons = page.locator("button")
    count = buttons.count()
    restart_candidates: list[str] = []
    for index in range(count):
        button = buttons.nth(index)
        try:
            text = button.inner_text(timeout=1000).strip()
            visible = button.evaluate(
                """(button) => {
                    const style = window.getComputedStyle(button);
                    const rect = button.getBoundingClientRect();
                    return style.display !== "none" &&
                        style.visibility !== "hidden" &&
                        Number(style.opacity || "1") > 0 &&
                        rect.width > 0 &&
                        rect.height > 0 &&
                        !button.disabled;
                }"""
            )
            if not visible:
                continue
            if is_restart_label(text):
                restart_candidates.append(text)
                continue
            if is_valid_start_label(text):
                button.click(timeout=3000)
                return {"attempted": True, "clicked": True, "label": text, "kind": "valid-start"}
        except Exception:
            continue
    if restart_candidates:
        return {
            "attempted": True,
            "clicked": False,
            "label": restart_candidates[0],
            "kind": "restart-state",
            "error": "Only restart/game-over controls were visible.",
        }
    try:
        page.keyboard.press("Space")
        return {"attempted": True, "clicked": False, "label": "", "kind": "keyboard-fallback", "fallback": "Space"}
    except Exception as e:
        return {"attempted": False, "clicked": False, "label": "", "kind": "none", "error": str(e)}


def check_external_game_js(root: Path) -> dict:
    index_path = root / "index.html"
    game_path = root / "game.js"
    result = {
        "gameJsExists": game_path.exists(),
        "indexExists": index_path.exists(),
        "loaded": False,
        "inlineRuntimeIntentional": False,
        "ok": False,
    }
    if not index_path.exists() or not game_path.exists():
        result["error"] = "index.html or game.js is missing."
        return result
    html = index_path.read_text(encoding="utf-8", errors="replace")
    result["loaded"] = bool(re.search(r"<script\b[^>]*\bsrc\s*=\s*['\"](?:\./)?game\.js(?:\?[^'\"]*)?['\"]", html, flags=re.I))
    result["inlineRuntimeIntentional"] = "<!-- arcade-inline-runtime-intentional -->" in html
    result["ok"] = result["loaded"] or result["inlineRuntimeIntentional"]
    if not result["ok"]:
        result["error"] = "index.html does not load generated game.js."
    return result


def check_dom_contract(root: Path) -> dict:
    index_path = root / "index.html"
    game_path = root / "game.js"
    result = {
        "ok": False,
        "indexHasGameCanvas": False,
        "indexHasStartButton": False,
        "gameJsReferencesGameCanvas": False,
        "gameJsReferencesStartButton": False,
    }
    if not index_path.exists() or not game_path.exists():
        result["error"] = "index.html or game.js is missing."
        return result
    html = index_path.read_text(encoding="utf-8", errors="replace")
    js = game_path.read_text(encoding="utf-8", errors="replace")
    result["indexHasGameCanvas"] = bool(re.search(r"\bid\s*=\s*['\"]gameCanvas['\"]", html))
    result["indexHasStartButton"] = bool(re.search(r"\bid\s*=\s*['\"]startButton['\"]", html))
    result["gameJsReferencesGameCanvas"] = "gameCanvas" in js
    result["gameJsReferencesStartButton"] = "startButton" in js
    result["ok"] = (
        result["indexHasGameCanvas"]
        and result["indexHasStartButton"]
        and result["gameJsReferencesGameCanvas"]
        and result["gameJsReferencesStartButton"]
    )
    if not result["ok"]:
        result["error"] = "index.html and game.js must share standard ids gameCanvas and startButton."
    return result


def read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def check_title_consistency(root: Path, visible_text: str) -> dict:
    contract = read_json(root / "contract.json")
    canonical_title = str(contract.get("title") or "").strip()
    result = {
        "canonicalTitle": canonical_title,
        "ok": False,
        "files": {},
    }
    if not canonical_title:
        result["error"] = "contract.json does not define a title."
        return result

    lower_title = canonical_title.lower()
    checks: dict[str, bool] = {}
    for filename in ("index.html", "DESIGN.md", "VALIDATION.md"):
        path = root / filename
        checks[filename] = path.exists() and lower_title in path.read_text(encoding="utf-8", errors="replace").lower()

    story = read_json(root / "story-structure.json")
    story_title = str(story.get("title") or "").strip()
    checks["story-structure.json"] = story_title == canonical_title
    checks["visibleText"] = lower_title in visible_text.lower()
    result["files"] = checks
    result["ok"] = all(checks.values())
    if not result["ok"]:
        result["error"] = "Generated files do not consistently use contract.json.title."
    return result


def browser_failure_reasons(
    *,
    status: int | None,
    serious: list[dict],
    page_errors: list[str],
    browser_error: str,
    initial_state: str,
    click_result: dict,
    canvas_after_pixels: int,
    canvas_became_nonblank: bool,
    canvas_gained_pixels: bool,
    external_game_js: dict,
    dom_contract: dict,
    title_consistency: dict,
) -> list[str]:
    reasons: list[str] = []
    if not status or status >= 400:
        reasons.append(f"index.html returned HTTP {status}.")
    if browser_error:
        reasons.append(f"Browser error: {browser_error}")
    if serious:
        reasons.append(f"{len(serious)} serious console messages were recorded.")
    if page_errors:
        reasons.append(f"{len(page_errors)} page errors were recorded.")
    if initial_state == "gameOver":
        reasons.append("Initial visible state is game-over/restart, not first-run start.")
    if click_result.get("kind") != "valid-start":
        label = click_result.get("label") or "(none)"
        reasons.append(f"No visible valid Start/Play/Begin control was clicked; got {click_result.get('kind')} label {label}.")
    if canvas_after_pixels <= 100:
        reasons.append(f"Canvas stayed blank after interaction ({canvas_after_pixels} nonblack pixels).")
    elif not canvas_became_nonblank:
        reasons.append("Canvas did not show visible gameplay pixels after start.")
    elif not canvas_gained_pixels:
        reasons.append("Canvas did not gain visible gameplay pixels after Start/Play/Begin.")
    if not external_game_js.get("ok"):
        reasons.append(external_game_js.get("error", "Generated game.js is not wired into index.html."))
    if not dom_contract.get("ok"):
        reasons.append(dom_contract.get("error", "Generated DOM ids are not coherent."))
    if not title_consistency.get("ok"):
        reasons.append(title_consistency.get("error", "Generated titles are inconsistent."))
    return reasons


def build_report(root: Path, pass_index: int) -> dict:
    syntax = {
        "contract": check_json_file(root / "contract.json"),
        "story": check_json_file(root / "story-structure.json"),
        "gameJs": run_command(["node", "--check", str(root / "game.js")], root),
    }
    browser = run_browser_check(root, pass_index)
    syntax_ok = all(item.get("ok") for item in syntax.values())
    ok = syntax_ok and browser.get("ok", False)
    return {
        "status": "PASS" if ok else "FAIL",
        "ok": ok,
        "passIndex": pass_index,
        "root": str(root),
        "syntax": syntax,
        "browser": browser,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run browser QA for a generated arcade game.")
    parser.add_argument("target_dir", type=Path)
    parser.add_argument("--pass-index", type=int, default=0)
    args = parser.parse_args()

    report = build_report(args.target_dir.resolve(), args.pass_index)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
