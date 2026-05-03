#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from html import escape as html_escape
from pathlib import Path

# --- CONFIGURATION ---
ROOT = Path(__file__).resolve().parent.parent
PAGES_ROOT = Path("/Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages")
PORTFOLIO_VITE_ROOT = PAGES_ROOT.parent
ARCADE_LIBRARY_FILE = PAGES_ROOT / "arcade-library.json"
SESSIONS_DIR = ROOT / ".ARCADE-SYSTEM" / "sessions"
PLAYWRIGHT_QA_FILE = ROOT / ".ARCADE-CLI" / "engines" / "playwright-qa.py"
DEFAULT_UPGRADE_PASSES = 2
UPGRADE_TARGETS = {"contract.json", "DESIGN.md", "story-structure.json", "index.html", "style.css", "game.js", "VALIDATION.md"}

# --- CHASSIS LOGIC ---

class BuilderChassis:
    def __init__(self, slug: str = None):
        self.slug = slug
        self.target_dir = None
        self.memory = {}

    def get_input(self, prompt: str) -> str:
        print(f"\n[CHASSIS PROMPT]: {prompt}", flush=True)
        print("Enter text below. Finish by typing 'END' on its own line.", flush=True)
        lines = []
        while True:
            line = sys.stdin.readline()
            if line.strip() == "END":
                break
            lines.append(line)
        return "".join(lines).strip()

    def initialize_project(self):
        if not self.slug:
            self.slug = input("Game Slug (lowercase-hyphenated): ").strip()
        
        self.target_dir = PAGES_ROOT / self.slug
        self.target_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n[✔] Workspace initialized at {self.target_dir}", flush=True)

    def run_stage(self, stage_num: int, stage_name: str, file_to_write: str = None):
        print(f"\n--- STAGE {stage_num}: {stage_name} ---", flush=True)
        payload = self.get_input(f"Provide the payload for {stage_name}")
        
        if file_to_write:
            write_path = self.target_dir / file_to_write
            write_path.parent.mkdir(parents=True, exist_ok=True)
            with open(write_path, "w", encoding="utf-8") as f:
                f.write(payload)
            print(f"[✔] File written: {file_to_write}")
        
        return payload

    def append_file(self, filename: str, content: str):
        write_path = self.target_dir / filename
        with open(write_path, "a", encoding="utf-8") as f:
            f.write(content.rstrip() + "\n\n")
        print(f"[✔] File updated: {filename}", flush=True)

    def reset_post_build_reports(self):
        for filename in ("PLAYWRIGHT-QA.md", "UPGRADE-LOOP.md", "FINAL-REPORT.md"):
            path = self.target_dir / filename
            if path.exists():
                path.write_text("", encoding="utf-8")
        qa_dir = self.target_dir / ".qa"
        if qa_dir.exists():
            for screenshot in qa_dir.glob("playwright-pass-*.png"):
                screenshot.unlink()

    def run_playwright_qa(self, pass_index: int) -> dict:
        print(f"\n--- STAGE 8: PLAYWRIGHT QA PASS {pass_index} ---", flush=True)
        self.normalize_canonical_title_assets()
        result = subprocess.run(
            [sys.executable, str(PLAYWRIGHT_QA_FILE), str(self.target_dir), "--pass-index", str(pass_index)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError:
            report = {
                "status": "FAIL",
                "ok": False,
                "passIndex": pass_index,
                "root": str(self.target_dir),
                "syntax": {},
                "browser": {},
                "rawStdout": result.stdout,
                "stderr": result.stderr,
            }
        report["returnCode"] = result.returncode
        if result.stderr.strip():
            report["stderr"] = result.stderr.strip()
        self.write_qa_report(report)
        return report

    def write_qa_report(self, report: dict):
        browser = report.get("browser", {})
        syntax = report.get("syntax", {})
        title_consistency = browser.get("titleConsistency", {})
        external_game_js = browser.get("externalGameJs", {})
        dom_contract = browser.get("domContract", {})
        lines = [
            f"# Playwright QA Pass {report.get('passIndex')}",
            "",
            f"- Status: {report.get('status')}",
            f"- HTTP: {browser.get('httpStatus', 'n/a')}",
            f"- Screenshot: {browser.get('screenshot', '')}",
            f"- Initial state: {browser.get('initialState', 'n/a')}",
            f"- Clicked start: {json.dumps(browser.get('clickedStart', {}))}",
            f"- Canvas nonblack pixels: {browser.get('canvasAfter', {}).get('nonBlackPixels', 0)}",
            f"- Canvas delta nonblack pixels: {browser.get('canvasDeltaNonblack', 0)}",
            f"- Canvas gained pixels: {browser.get('canvasGainedPixels', False)}",
            f"- Playable UI detected: {browser.get('playableUiDetected', False)}",
            f"- Valid start clicked: {browser.get('validStartClicked', False)}",
            f"- External game.js wired: {external_game_js.get('ok', False)}",
            f"- DOM contract: {dom_contract.get('ok', False)}",
            f"- Title consistency: {title_consistency.get('ok', False)}",
            f"- Serious console messages: {len(browser.get('seriousConsoleMessages', []))}",
            f"- Page errors: {len(browser.get('pageErrors', []))}",
            "",
            "## Syntax",
            "",
        ]
        for key, value in syntax.items():
            lines.append(f"- {key}: {'PASS' if value.get('ok') else 'FAIL'}")
            error = value.get("error") or value.get("stderr")
            if error:
                lines.append(f"  - {error[:500]}")
        if browser.get("failureReasons"):
            lines.extend(["", "## Failure Reasons", ""])
            for reason in browser.get("failureReasons", []):
                lines.append(f"- {reason}")
        if title_consistency:
            lines.extend(["", "## Title Consistency", "", f"- Canonical title: {title_consistency.get('canonicalTitle', '')}"])
            for filename, ok in title_consistency.get("files", {}).items():
                lines.append(f"- {filename}: {'PASS' if ok else 'FAIL'}")
        if external_game_js and not external_game_js.get("ok"):
            lines.extend(["", "## Runtime Wiring", "", f"- {external_game_js.get('error', 'game.js wiring failed')}"])
        if dom_contract and not dom_contract.get("ok"):
            lines.extend(["", "## DOM Contract", "", f"- {dom_contract.get('error', 'DOM contract failed')}"])
        if browser.get("seriousConsoleMessages"):
            lines.extend(["", "## Console"])
            for message in browser.get("seriousConsoleMessages", []):
                lines.append(f"- {message.get('type')}: {message.get('text')}")
        if browser.get("browserError"):
            lines.extend(["", "## Browser Error", browser.get("browserError", "")])
        self.append_file("PLAYWRIGHT-QA.md", "\n".join(lines))

    def choose_upgrade_targets(self, qa_report: dict) -> list[str]:
        targets = []
        syntax = qa_report.get("syntax", {})
        browser = qa_report.get("browser", {})
        clicked_start = browser.get("clickedStart", {})
        title_consistency = browser.get("titleConsistency", {})
        external_game_js = browser.get("externalGameJs", {})
        dom_contract = browser.get("domContract", {})
        if not syntax.get("contract", {}).get("ok", True):
            targets.append("contract.json")
        if not syntax.get("story", {}).get("ok", True):
            targets.append("story-structure.json")
        if not syntax.get("gameJs", {}).get("ok", True):
            targets.append("game.js")
        if browser.get("browserError") or browser.get("pageErrors") or browser.get("seriousConsoleMessages"):
            targets.extend(["index.html", "game.js"])
        if browser.get("initialState") == "gameOver" or clicked_start.get("kind") != "valid-start":
            targets.extend(["index.html", "style.css", "game.js"])
        if not browser.get("canvasBecameNonblank"):
            targets.extend(["index.html", "style.css", "game.js"])
        if browser.get("canvasBecameNonblank") and not browser.get("canvasGainedPixels", True):
            targets.extend(["index.html", "style.css", "game.js"])
        if not external_game_js.get("ok", True):
            targets.append("index.html")
        if not dom_contract.get("ok", True):
            targets.extend(["index.html", "game.js"])
        if not title_consistency.get("ok", True):
            title_files = title_consistency.get("files", {})
            title_target_map = {
                "index.html": "index.html",
                "DESIGN.md": "DESIGN.md",
                "VALIDATION.md": "VALIDATION.md",
                "story-structure.json": "story-structure.json",
                "visibleText": "index.html",
            }
            for filename, ok in title_files.items():
                if not ok and filename in title_target_map:
                    targets.append(title_target_map[filename])
        if not targets and not qa_report.get("ok"):
            targets.extend(["index.html", "game.js"])
        ordered = []
        for target in targets:
            if target in UPGRADE_TARGETS and target not in ordered:
                ordered.append(target)
        return ordered

    def run_upgrade_loop(self, initial_report: dict, max_passes: int = DEFAULT_UPGRADE_PASSES) -> dict:
        qa_report = initial_report
        for pass_index in range(1, max_passes + 1):
            if qa_report.get("ok"):
                return qa_report
            print(f"\n--- STAGE 9: UPGRADE LOOP PASS {pass_index} ---", flush=True)
            targets = self.choose_upgrade_targets(qa_report)
            if not targets:
                self.append_file("UPGRADE-LOOP.md", f"# Upgrade Pass {pass_index}\n\nNo safe upgrade targets were identified.")
                return qa_report

            plan_prompt = (
                f"Upgrade Plan Pass {pass_index} (Markdown)\n"
                f"QA report:\n{json.dumps(qa_report, indent=2)}\n"
                f"Target files: {', '.join(targets)}\n"
                "Repair only the QA failures. Do not rename the game, invent a new concept, or replace the canonical title."
            )
            repair_plan = self.get_input(plan_prompt)
            self.append_file("UPGRADE-LOOP.md", f"# Upgrade Pass {pass_index}\n\n## Plan\n\n{repair_plan}\n")

            for target in targets:
                current_text = (self.target_dir / target).read_text(encoding="utf-8", errors="replace")
                replacement_prompt = (
                    f"Upgrade Replacement: {target}\n"
                    f"Canonical title from contract.json: {self.canonical_title()}\n"
                    f"Related files for id/context alignment:\n{self.related_file_context(target)}\n"
                    f"Current {target}:\n{current_text[:20000]}"
                    f"\n\nRepair plan:\n{repair_plan}\n\n"
                    f"QA report:\n{json.dumps(qa_report, indent=2)}\n\n"
                    f"{self.target_upgrade_rules(target)}\n"
                    "Do not rename the game or introduce a different concept.\n"
                    f"Return the complete replacement payload for {target} only."
                )
                replacement = self.get_input(replacement_prompt)
                (self.target_dir / target).write_text(replacement, encoding="utf-8")
                self.append_file("UPGRADE-LOOP.md", f"## Replaced {target}\n\nBytes: {len(replacement.encode('utf-8'))}")

            qa_report = self.run_playwright_qa(pass_index)

        return qa_report

    def canonical_title(self) -> str:
        try:
            data = json.loads((self.target_dir / "contract.json").read_text(encoding="utf-8"))
            title = data.get("title")
            return title if isinstance(title, str) else ""
        except Exception:
            return ""

    def normalize_canonical_title_assets(self) -> None:
        title = self.canonical_title().strip()
        if not title:
            return

        story_path = self.target_dir / "story-structure.json"
        try:
            story = json.loads(story_path.read_text(encoding="utf-8"))
            if isinstance(story, dict) and story.get("title") != title:
                story["title"] = title
                story_path.write_text(json.dumps(story, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                print("[title-normalizer] story-structure.json title aligned", flush=True)
        except Exception:
            pass

        for filename in ("DESIGN.md", "VALIDATION.md"):
            path = self.target_dir / filename
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if title.lower() not in text.lower():
                path.write_text(f"# {title}\n\n{text}", encoding="utf-8")
                print(f"[title-normalizer] {filename} title inserted", flush=True)

        index_path = self.target_dir / "index.html"
        if not index_path.exists():
            return
        html = index_path.read_text(encoding="utf-8", errors="replace")
        updated = html
        if re.search(r"<title\b[^>]*>.*?</title>", updated, flags=re.I | re.S):
            updated = re.sub(r"<title\b[^>]*>.*?</title>", f"<title>{html_escape(title)}</title>", updated, flags=re.I | re.S)
        else:
            updated = re.sub(r"</head>", f"  <title>{html_escape(title)}</title>\n</head>", updated, count=1, flags=re.I)
        if re.search(r"<h1\b[^>]*>.*?</h1>", updated, flags=re.I | re.S):
            updated = re.sub(r"<h1\b[^>]*>.*?</h1>", f"<h1>{html_escape(title)}</h1>", updated, count=1, flags=re.I | re.S)
        else:
            updated = re.sub(r"<body\b([^>]*)>", f"<body\\1>\n  <h1>{html_escape(title)}</h1>", updated, count=1, flags=re.I)
        if re.search(r"(<button\b[^>]*\bid=[\"']startButton[\"'][^>]*>).*?(</button>)", updated, flags=re.I | re.S):
            updated = re.sub(
                r"(<button\b[^>]*\bid=[\"']startButton[\"'][^>]*>).*?(</button>)",
                f"\\1Start {html_escape(title)}\\2",
                updated,
                count=1,
                flags=re.I | re.S,
            )
        if updated != html:
            index_path.write_text(updated, encoding="utf-8")
            print("[title-normalizer] index.html visible title aligned", flush=True)

    def related_file_context(self, target: str) -> str:
        related = []
        for filename in ("index.html", "style.css", "game.js"):
            if filename == target:
                continue
            path = self.target_dir / filename
            if path.exists():
                related.append(f"--- {filename} ---\n{path.read_text(encoding='utf-8', errors='replace')[:6000]}")
        return "\n\n".join(related)

    def target_upgrade_rules(self, target: str) -> str:
        common_title_rule = " Preserve the exact canonical title from contract.json everywhere user-facing."
        if target == "contract.json":
            return "Rules for contract.json: return valid JSON with title, pitch, and seeds; keep title stable unless it is missing."
        if target == "DESIGN.md":
            return "Rules for DESIGN.md: return Markdown only and align the title, game premise, and mechanics to contract.json." + common_title_rule
        if target == "story-structure.json":
            return "Rules for story-structure.json: return valid JSON only; its title must exactly match contract.json.title."
        if target == "VALIDATION.md":
            return "Rules for VALIDATION.md: return Markdown only and validate the actual generated game, not a different concept." + common_title_rule
        if target == "index.html":
            return (
                "Rules for index.html: the page must show visible text or a visible Start/Play button on initial load; "
                "the first-run button label must contain Start, Play, or Begin exactly; labels like Initiate Relay are not accepted; "
                "the Start/Play/Begin button must be clickable by Playwright and must not be Restart/Retry/Play Again on initial load; "
                "use standard ids `<canvas id=\"gameCanvas\">` and `<button id=\"startButton\">`; "
                "do not hide the whole body, canvas, or start screen by default; load ./game.js with a script tag unless "
                "`<!-- arcade-inline-runtime-intentional -->` is present; keep script and element ids coherent." + common_title_rule
            )
        if target == "style.css":
            return (
                "Rules for style.css: never set display:none on body, html, canvas, #game-container, #gameCanvas, "
                "#game-canvas, #startScreen, or #gameUI; keep the game surface visible on initial load."
            )
        if target == "game.js":
            return (
                "Rules for game.js: wire any visible Start/Play button to start gameplay; draw an initial frame before input; "
                "after Start/Play, the canvas must visibly change within one second; use requestAnimationFrame for ongoing gameplay; "
                "implement the same named mechanics promised in contract.json and story-structure.json; use standard DOM ids gameCanvas and startButton." + common_title_rule
            )
        return ""

    def read_json_file(self, filename: str) -> dict:
        path = self.target_dir / filename
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def write_json_file(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def text_list(self, value, fallback: list[str]) -> list[str]:
        if isinstance(value, list):
            cleaned = [str(item).strip() for item in value if str(item).strip()]
            return cleaned or fallback
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return fallback

    def arcade_entry(self, title: str) -> dict:
        return {
            "slug": self.slug,
            "title": title,
            "section": "prototypes",
            "pagePath": f"Pages/{self.slug}/",
            "metadataPath": f"Pages/{self.slug}/{self.slug}.json",
        }

    def arcade_metadata(self, title: str) -> dict:
        contract = self.read_json_file("contract.json")
        story = self.read_json_file("story-structure.json")
        summary = (
            str(contract.get("summary") or "").strip()
            or str(contract.get("pitch") or "").strip()
            or str(story.get("description") or "").strip()
            or f"{title} is a generated playable arcade game."
        )
        instructions = self.text_list(
            contract.get("controls") or contract.get("instructions"),
            ["Use arrow keys or WASD to move.", "Press Space for the core action.", "Use the Start, Play, or Begin button to launch."],
        )
        tags = self.text_list(contract.get("tags"), ["arcade", "generated", "playable"])
        return {
            "id": self.slug,
            "title": title,
            "summary": summary,
            "mode": str(contract.get("arcadeMode") or "arcade-action"),
            "palette": str(contract.get("palette") or self.slug),
            "instructions": " ".join(instructions),
            "tags": tags,
            "hud": {
                "modeLabel": title,
                "objective": summary,
            },
            "overlay": {
                "startTitle": title,
                "startCopy": summary,
                "startAction": "Start Game",
            },
            "content": {
                "hook": summary,
                "actions": instructions[:3],
                "rewards": self.text_list(contract.get("rewards"), tags)[:3],
            },
            "image": "",
        }

    def load_arcade_library(self) -> dict:
        if not ARCADE_LIBRARY_FILE.exists():
            return {"entries": []}
        try:
            data = json.loads(ARCADE_LIBRARY_FILE.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return {"entries": []}
            entries = data.get("entries")
            if not isinstance(entries, list):
                data["entries"] = []
            return data
        except Exception:
            return {"entries": []}

    def register_with_arcade_library(self, final_report: dict) -> dict:
        if not final_report.get("ok"):
            raise RuntimeError("Refusing arcade registration because final QA did not pass.")

        print("\n--- STAGE 10: ARCADE REGISTRATION ---", flush=True)
        title = self.canonical_title() or self.slug.replace("-", " ").title()
        metadata_path = self.target_dir / f"{self.slug}.json"
        metadata = self.arcade_metadata(title)
        self.write_json_file(metadata_path, metadata)

        manifest = self.load_arcade_library()
        entries = [entry for entry in manifest.get("entries", []) if isinstance(entry, dict)]
        entry = self.arcade_entry(title)
        existing_index = next((index for index, item in enumerate(entries) if item.get("slug") == self.slug), None)
        if existing_index is None:
            entries.append(entry)
            change = f"Added {self.slug} to {ARCADE_LIBRARY_FILE}."
        else:
            entries[existing_index] = entry
            change = f"Updated existing {self.slug} entry in {ARCADE_LIBRARY_FILE}."
        manifest["entries"] = sorted(entries, key=lambda item: str(item.get("title") or item.get("slug") or "").lower())
        self.write_json_file(ARCADE_LIBRARY_FILE, manifest)

        integration_report = self.verify_arcade_registration(entry, metadata_path, [f"Wrote arcade metadata to {metadata_path}.", change])
        self.write_arcade_integration_report(integration_report)
        if integration_report.get("remainingGaps"):
            raise RuntimeError(f"Arcade registration failed verification. See {self.target_dir / 'ARCADE-INTEGRATION-SPEC.md'}")
        print(f"[✔] Arcade library registered: {self.slug}", flush=True)
        return integration_report

    def verify_arcade_registration(self, entry: dict, metadata_path: Path, changes: list[str]) -> dict:
        manifest = self.load_arcade_library()
        entries = manifest.get("entries", []) if isinstance(manifest.get("entries"), list) else []
        verified_entry = next((item for item in entries if isinstance(item, dict) and item.get("slug") == self.slug), None)
        checks = {
            "arcadeLibraryEntry": verified_entry == entry,
            "metadataFile": metadata_path.exists(),
            "indexFile": (self.target_dir / "index.html").exists(),
            "storyFile": (self.target_dir / "story-structure.json").exists(),
            "pagePathResolves": (PORTFOLIO_VITE_ROOT / entry["pagePath"]).exists(),
            "metadataPathResolves": (PORTFOLIO_VITE_ROOT / entry["metadataPath"]).exists(),
        }
        remaining_gaps = [name for name, ok in checks.items() if not ok]
        notes = [
            f"{name}: {'PASS' if ok else 'FAIL'}"
            for name, ok in checks.items()
        ]
        return {
            "entry": entry,
            "metadataPath": str(metadata_path),
            "registrationChanges": changes,
            "verificationNotes": notes,
            "remainingGaps": remaining_gaps,
            "continueGate": "Stop" if not remaining_gaps else "Continue",
        }

    def write_arcade_integration_report(self, report: dict):
        lines = [
            "# Arcade Integration Spec",
            "",
            "## Registration Changes",
            "",
        ]
        lines.extend(f"- {item}" for item in report.get("registrationChanges", []))
        lines.extend(["", "## Arcade Entry", "", f"```json\n{json.dumps(report.get('entry', {}), indent=2)}\n```"])
        lines.extend(["", "## Verification Notes", ""])
        lines.extend(f"- {item}" for item in report.get("verificationNotes", []))
        lines.extend(["", "## Open Gaps", ""])
        gaps = report.get("remainingGaps", [])
        lines.extend(f"- {item}" for item in gaps)
        if not gaps:
            lines.append("- No open integration gaps remain.")
        lines.extend(["", "## Continue Gate", "", f"- {report.get('continueGate', 'Stop')}"])
        (self.target_dir / "ARCADE-INTEGRATION-SPEC.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_final_report(self, final_report: dict):
        status = "PASS_AFTER_UPGRADE" if final_report.get("passIndex", 0) > 0 and final_report.get("ok") else final_report.get("status")
        lines = [
            "# Final Arcade Build Report",
            "",
            f"- Final status: {status}",
            f"- QA pass index: {final_report.get('passIndex')}",
            f"- Target folder: {self.target_dir}",
        ]
        self.append_file("FINAL-REPORT.md", "\n".join(lines))
        if not final_report.get("ok"):
            raise RuntimeError(f"Post-build QA failed after upgrade loop. See {self.target_dir / 'PLAYWRIGHT-QA.md'}")

    def build(self):
        self.initialize_project()
        
        # Stage 0: Identity
        self.memory["contract"] = self.run_stage(0, "Contract (Title, Pitch, Seeds)", "contract.json")
        
        # Stage 1: Design
        self.memory["design"] = self.run_stage(1, "Game Design Document (Markdown)", "DESIGN.md")
        
        # Stage 2: Story
        self.memory["story"] = self.run_stage(2, "Story Structure (JSON)", "story-structure.json")
        
        # Stage 3: Core Implementation
        self.memory["html"] = self.run_stage(3, "index.html", "index.html")
        self.memory["css"] = self.run_stage(4, "style.css", "style.css")
        self.memory["js"] = self.run_stage(5, "game.js", "game.js")
        
        # Stage 6: Validation & Polish
        self.run_stage(6, "Validation Review (Markdown)", "VALIDATION.md")
        
        # Stage 7: Final Arcade Integration
        print("\n--- STAGE 7: ARCADE INTEGRATION ---")
        print("Build files complete. Arcade registration will run after browser QA passes.")

        # Stage 8-10: Browser QA, upgrade loop, final report
        self.reset_post_build_reports()
        initial_report = self.run_playwright_qa(0)
        final_report = self.run_upgrade_loop(initial_report)
        self.write_final_report(final_report)
        self.register_with_arcade_library(final_report)
        
        print(f"\n[🏁] {self.slug} materialization finished.")

def main():
    parser = argparse.ArgumentParser(description="Interactive Arcade Build Chassis")
    parser.add_argument("--slug", type=str, help="Override project slug.")
    args = parser.parse_args()
    
    chassis = BuilderChassis(slug=args.slug)
    chassis.build()

if __name__ == "__main__":
    main()
