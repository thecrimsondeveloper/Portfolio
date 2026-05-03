#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

# --- CONFIGURATION ---
ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
PAGES_ROOT = Path("/Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages")
NVIDIA_ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_MODEL = "google/gemma-4-31b-it"
NVIDIA_CODE_MODEL = "google/gemma-4-31b-it"
NVIDIA_CODE_FALLBACK_MODEL = "google/gemma-4-31b-it"
NVIDIA_REVIEW_MODEL = "google/gemma-4-31b-it"
RUNS_DIR = ROOT / ".ARCADE-SYSTEM" / "sessions" / "runs"

# --- UTILITIES ---

def load_env():
    if not ENV_FILE.exists():
        return
    with open(ENV_FILE, "r") as f:
        for line in f:
            if "=" in line and line.strip() and not line.lstrip().startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key.strip()] = val.strip()

def call_nvidia(
    messages: list[dict],
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
) -> str:
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError(f"NVIDIA_API_KEY not found in environment or {ENV_FILE}.")

    endpoint = os.environ.get("NVIDIA_ENDPOINT", NVIDIA_ENDPOINT)
    selected_model = model or os.environ.get("NVIDIA_MODEL", NVIDIA_MODEL)
    selected_max_tokens = max_tokens or int(os.environ.get("NVIDIA_MAX_TOKENS", "4096"))
    selected_temperature = temperature if temperature is not None else float(os.environ.get("NVIDIA_TEMPERATURE", "0.35"))

    payload = {
        "model": selected_model,
        "messages": messages,
        "temperature": selected_temperature,
        "top_p": 0.9,
        "max_tokens": selected_max_tokens,
    }
    
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res = json.load(response)
            content = res["choices"][0]["message"]["content"]
            if not content or not content.strip():
                raise RuntimeError("NVIDIA API returned an empty message.")
            return content.strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace").strip()
        detail = f" {body}" if body else ""
        raise RuntimeError(f"NVIDIA API HTTP {e.code} for model {selected_model} at {endpoint}.{detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"NVIDIA API connection failed at {endpoint}: {e.reason}") from e
    except (TimeoutError, socket.timeout) as e:
        raise RuntimeError(f"NVIDIA API timed out for model {selected_model} at {endpoint}: {e}") from e
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise RuntimeError(f"NVIDIA API returned an unexpected response shape: {e}") from e

# --- MONOLITHIC DRIVER ---

class OrchestratorHarness:
    def __init__(self, high_level_goal: str, slug_override: Optional[str] = None):
        self.goal = high_level_goal
        self.slug_override = slug_override
        self.log = {
            "goal": high_level_goal,
            "slugOverride": slug_override,
            "startTime": time.ctime(),
            "events": [],
            "decisions": []
        }
        self.output_buffer = ""
        self.log_path = RUNS_DIR / f"run-{int(time.time())}.json"

    def save_log(self):
        if not RUNS_DIR.exists():
            RUNS_DIR.mkdir(parents=True)
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self.log, f, indent=2)

    def record_event(self, stage: str, action: str, reasoning: str):
        event = {
            "time": time.ctime(),
            "stage": stage,
            "action": action,
            "reasoning": reasoning
        }
        self.log["events"].append(event)
        self.save_log()

    def scan_existing_registry(self) -> str:
        print("\n[🔍 MEMORY GATHERING]: Scanning existing arcade registry...")
        registry = []
        if not PAGES_ROOT.exists():
            return "No existing games found."
            
        for game_dir in PAGES_ROOT.iterdir():
            if game_dir.is_dir():
                manifest_path = game_dir / "story-structure.json"
                if manifest_path.exists():
                    try:
                        with open(manifest_path, "r") as f:
                            data = json.load(f)
                            entry = {"title": data.get("title"), "pitch": data.get("description", "")[:100]}
                            registry.append(entry)
                            print(f"  [+] Found game: {entry['title']}")
                    except:
                        pass
        return json.dumps(registry, indent=2)

    def solve_prompt(self, context: str, registry: str) -> str:
        current_stage = self.current_stage(context)
        model, max_tokens, temperature = self.select_model(current_stage)
        print(f"\n[🧠 REASONING]: Consulting NVIDIA NIM via {model}...")
        prompt = f"""
        You are the PortfolioBuilder Orchestrator. 
        HIGH LEVEL GOAL: {self.goal}
        CURRENT STAGE: {current_stage}
        
        EXISTING GAMES REGISTRY:
        {registry}
        
        CURRENT CHASSIS OUTPUT:
        \"\"\"{context[-16000:]}\"\"\"
        
        TASK:
        The builder chassis is waiting for input at a specific stage.
        Generate the exact payload (JSON, Markdown, or Code) required for this stage.
        {self.stage_payload_rules(current_stage)}
        - Ensure the game is unique.
        - Ensure the code is functional and high-quality.
        - Return ONLY the payload content.
        - Do not return a JSON object with file/code/payload keys unless the current stage explicitly asks for JSON.
        - Do not wrap code in Markdown fences.
        - Do not include the input terminator.
        """
        
        response = self.call_stage_nvidia(current_stage, prompt, model, max_tokens, temperature)
        print("[💡 THOUGHT PROCESS COMPLETED]")
        try:
            return self.normalize_payload(current_stage, response)
        except (RuntimeError, json.JSONDecodeError) as e:
            self.record_event(current_stage, "normalize_retry", str(e))
            repair_prompt = f"""
            The previous payload for stage `{current_stage}` was rejected.
            ERROR: {e}

            Rewrite it as the exact required payload only.
            {self.stage_payload_rules(current_stage)}
            Do not include Markdown fences, explanations, metadata wrappers, or END.

            BROKEN PAYLOAD:
            {response[:10000]}
            """
            retry = self.call_stage_nvidia(current_stage, repair_prompt, model, max_tokens, 0.0)
            try:
                return self.normalize_payload(current_stage, retry)
            except (RuntimeError, json.JSONDecodeError) as retry_error:
                raise RuntimeError(f"NVIDIA returned invalid payload for {current_stage}: {retry_error}") from retry_error

    def call_stage_nvidia(self, stage: str, prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        try:
            return call_nvidia(
                [{"role": "user", "content": prompt}],
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except RuntimeError as e:
            fallback = self.fallback_model(stage, model)
            if not fallback or not self.is_retryable_nvidia_error(str(e)):
                raise
            self.record_event(stage, "model_fallback", f"{model} -> {fallback}: {e}")
            print(f"\n[FALLBACK] NVIDIA model: {model} -> {fallback}")
            return call_nvidia(
                [{"role": "user", "content": prompt}],
                model=fallback,
                max_tokens=max_tokens,
                temperature=temperature,
            )

    def fallback_model(self, stage: str, current_model: str) -> Optional[str]:
        lower_stage = stage.lower()
        if "contract" in lower_stage or "story structure" in lower_stage or "story-structure.json" in lower_stage:
            fallback = os.environ.get("NVIDIA_REVIEW_MODEL", NVIDIA_REVIEW_MODEL)
            return fallback if fallback != current_model else None
        if any(token in lower_stage for token in ("index.html", "style.css", "game.js")):
            fallback = os.environ.get("NVIDIA_CODE_FALLBACK_MODEL", NVIDIA_CODE_FALLBACK_MODEL)
            return fallback if fallback != current_model else None
        if any(token in lower_stage for token in ("design.md", "validation review", "validation.md", "upgrade plan", "upgrade replacement")):
            fallback = os.environ.get("NVIDIA_CODE_FALLBACK_MODEL", NVIDIA_CODE_FALLBACK_MODEL)
            return fallback if fallback != current_model else None
        return None

    def is_retryable_nvidia_error(self, message: str) -> bool:
        return any(token in message for token in ("HTTP 429", "HTTP 404", "HTTP 410", "connection failed", "timed out", "timeout"))

    def current_stage(self, context: str) -> str:
        stage_matches = re.findall(r"Provide the payload for ([^\n]+)", context)
        if stage_matches:
            return stage_matches[-1].strip()
        prompt_matches = re.findall(r"\[CHASSIS PROMPT\]: ([^\n]+)", context)
        return prompt_matches[-1].strip() if prompt_matches else "Unknown"

    def select_model(self, stage: str) -> tuple[str, int, float]:
        current_stage = stage.lower()
        code_model = os.environ.get("NVIDIA_CODE_MODEL", NVIDIA_CODE_MODEL)
        review_model = os.environ.get("NVIDIA_REVIEW_MODEL", NVIDIA_REVIEW_MODEL)
        planning_model = os.environ.get("NVIDIA_MODEL", NVIDIA_MODEL)
        if "contract" in current_stage:
            return code_model, int(os.environ.get("NVIDIA_CODE_MAX_TOKENS", "8192")), float(os.environ.get("NVIDIA_IDEA_TEMPERATURE", "0.1"))
        if "story structure" in current_stage or "story-structure.json" in current_stage:
            return code_model, int(os.environ.get("NVIDIA_CODE_MAX_TOKENS", "8192")), 0.1
        if any(stage in current_stage for stage in ("index.html", "style.css", "game.js")):
            return code_model, int(os.environ.get("NVIDIA_CODE_MAX_TOKENS", "8192")), 0.2
        if any(token in current_stage for token in ("validation review", "validation.md", "design.md", "upgrade plan")):
            return review_model, int(os.environ.get("NVIDIA_REVIEW_MAX_TOKENS", "4096")), 0.2
        return planning_model, int(os.environ.get("NVIDIA_MAX_TOKENS", "4096")), 0.35

    def stage_payload_rules(self, stage: str) -> str:
        lower_stage = stage.lower()
        if "upgrade plan" in lower_stage:
            return "- Return Markdown only. Include concise issues, target files, and exact repair intent. Do not invent a new game concept or rename the canonical title."
        if "contract" in lower_stage:
            return "- Return valid JSON only. First character must be `{`. Include `title`, `pitch`, `summary`, `instructions`, `controls`, `arcadeMode`, `palette`, `tags`, and `seeds`. The `title` is the canonical title for the whole game and arcade registration."
        if "story structure" in lower_stage or "story-structure.json" in lower_stage:
            return "- Return valid JSON only. First character must be `{`. The `title` must exactly match contract.json.title from the prompt."
        if "index.html" in lower_stage:
            return "- Return a complete HTML document only. First line should be `<!DOCTYPE html>`. Keep the body, game surface, and Start/Play/Begin entry visible on initial load. The first-run button label must contain Start, Play, or Begin exactly; labels like Initiate Relay are not accepted. Use standard ids `<canvas id=\"gameCanvas\">` and `<button id=\"startButton\">`. Do not show Restart/Retry/Play Again initially. Load ./game.js with a script tag unless `<!-- arcade-inline-runtime-intentional -->` is present. Preserve the canonical contract title everywhere user-facing."
        if "style.css" in lower_stage:
            return "- Return CSS only. Do not include HTML, JavaScript, or JSON metadata. Never hide body, html, canvas, the game container, or the start screen."
        if "game.js" in lower_stage:
            return "- Return JavaScript only. Do not include HTML, CSS, or JSON metadata. Use standard DOM ids gameCanvas and startButton. Wire Start/Play/Begin controls and draw a visible initial frame plus a nonblank gameplay frame within one second after start. Preserve the canonical contract title where referenced."
        if "design.md" in lower_stage:
            return "- Return Markdown only. It must describe the actual generated game and use contract.json.title as the title."
        if "validation review" in lower_stage or "validation.md" in lower_stage:
            return "- Return Markdown only. It must review the actual generated game and use contract.json.title as the title."
        return ""

    def normalize_payload(self, stage: str, payload: str) -> str:
        cleaned = self.strip_input_terminator(self.strip_markdown_fence(payload))
        lower_stage = stage.lower()
        if "contract" in lower_stage or "story structure" in lower_stage or "story-structure.json" in lower_stage:
            cleaned = self.extract_json_payload(cleaned)
            json.loads(cleaned)
            return cleaned
        if any(name in lower_stage for name in ("index.html", "style.css", "game.js")):
            cleaned = self.extract_code_payload(cleaned)
            if "index.html" in lower_stage and "<html" not in cleaned.lower():
                raise RuntimeError("NVIDIA returned index.html without an <html> document.")
            if "index.html" in lower_stage:
                self.validate_html_payload(cleaned)
            if "style.css" in lower_stage:
                cleaned = self.repair_css_visibility(cleaned)
                self.validate_css_payload(cleaned)
            if "game.js" in lower_stage and cleaned.lstrip().startswith("{"):
                raise RuntimeError("NVIDIA returned JSON metadata instead of JavaScript.")
            if "game.js" in lower_stage:
                self.validate_js_payload(cleaned)
            return cleaned
        if "design.md" in lower_stage or "validation.md" in lower_stage:
            return cleaned
        return cleaned

    def validate_html_payload(self, payload: str) -> None:
        hidden_start_pattern = r"#startScreen\s*(?:,\s*#[^{]+)?\s*\{[^}]*display\s*:\s*none"
        if re.search(hidden_start_pattern, payload, flags=re.I | re.S):
            raise RuntimeError("index.html hides the start screen by default.")
        button_labels = [
            re.sub(r"<[^>]+>", "", match).strip().lower()
            for match in re.findall(r"<button\b[^>]*>(.*?)</button>", payload, flags=re.I | re.S)
        ]
        valid_start_labels = [
            label for label in button_labels
            if not any(token in label for token in ("restart", "retry", "again"))
            and re.search(r"\b(start|play|begin)\b", label)
        ]
        if not valid_start_labels:
            raise RuntimeError("index.html must include a first-run button whose label contains Start, Play, or Begin.")
        if not re.search(r"\bid\s*=\s*['\"]gameCanvas['\"]", payload):
            raise RuntimeError("index.html must include `<canvas id=\"gameCanvas\">`.")
        if not re.search(r"\bid\s*=\s*['\"]startButton['\"]", payload):
            raise RuntimeError("index.html must include `<button id=\"startButton\">`.")
        loads_game_js = re.search(r"<script\b[^>]*\bsrc\s*=\s*['\"](?:\./)?game\.js(?:\?[^'\"]*)?['\"]", payload, flags=re.I)
        inline_marker = "<!-- arcade-inline-runtime-intentional -->" in payload
        if not loads_game_js and not inline_marker:
            raise RuntimeError("index.html must load ./game.js or include the arcade inline-runtime marker.")

    def validate_css_payload(self, payload: str) -> None:
        hidden_selectors = (
            "body",
            "html",
            "canvas",
            "#game-container",
            "#gameCanvas",
            "#game-canvas",
            "#startScreen",
            "#gameUI",
        )
        for selector in hidden_selectors:
            pattern = re.escape(selector) + r"\s*\{[^}]*display\s*:\s*none"
            if re.search(pattern, payload, flags=re.I | re.S):
                raise RuntimeError(f"style.css hides required visible surface: {selector}.")

    def repair_css_visibility(self, payload: str) -> str:
        required_selectors = (
            "body",
            "html",
            "canvas",
            "#game-container",
            "#gameCanvas",
            "#game-canvas",
            "#startScreen",
            "#gameUI",
        )

        def repair_block(match: re.Match) -> str:
            selector = match.group(1)
            body = re.sub(r"display\s*:\s*none\s*;?", "display: block;", match.group(2), flags=re.I)
            return f"{selector} {{{body}}}"

        repaired = payload
        for selector in required_selectors:
            pattern = f"({re.escape(selector)}\\s*)\\{{([^}}]*display\\s*:\\s*none[^}}]*)\\}}"
            repaired = re.sub(pattern, repair_block, repaired, flags=re.I | re.S)
        return repaired

    def validate_js_payload(self, payload: str) -> None:
        if "gameCanvas" not in payload:
            raise RuntimeError("game.js must reference the standard canvas id gameCanvas.")
        if "startButton" not in payload:
            raise RuntimeError("game.js must reference the standard start button id startButton.")

    def strip_markdown_fence(self, payload: str) -> str:
        stripped = payload.strip()
        fence = re.fullmatch(r"```(?:[a-zA-Z0-9_-]+)?\s*\n(.*)\n```", stripped, flags=re.S)
        if fence:
            return fence.group(1).strip()
        if stripped.startswith("```"):
            lines = stripped.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            return "\n".join(lines).strip()
        return stripped

    def extract_json_payload(self, payload: str) -> str:
        try:
            json.loads(payload)
            return payload
        except json.JSONDecodeError:
            start = payload.find("{")
            end = payload.rfind("}")
            if start == -1 or end == -1 or end <= start:
                raise
            candidate = payload[start : end + 1]
            json.loads(candidate)
            return candidate

    def extract_code_payload(self, payload: str) -> str:
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return payload
        if isinstance(data, dict):
            for key in ("code", "payload", "content"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return self.strip_markdown_fence(value)
        return payload

    def strip_input_terminator(self, payload: str) -> str:
        lines = payload.strip().splitlines()
        while lines and lines[-1].strip() == "END":
            lines.pop()
        cleaned = "\n".join(lines).strip()
        if not cleaned:
            raise RuntimeError("NVIDIA returned only an input terminator.")
        return cleaned

    def run_harness(self):
        print(f"🎮 Starting Monolithic Build Harness...")
        print(f"🎯 Goal: {self.goal}")
        
        registry_context = self.scan_existing_registry()

        # Launch the dumb chassis
        cmd = [sys.executable, str(ROOT / ".ARCADE-CLI" / "builder-agent.py")]
        
        process = subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        while process.poll() is None:
            char = process.stdout.read(1)
            if not char:
                break
                
            sys.stdout.write(char)
            sys.stdout.flush()
            self.output_buffer += char
            
            # Detect prompts from the chassis
            if "Game Slug (lowercase-hyphenated):" in self.output_buffer[-50:]:
                slug = self.slug_override or self.goal.lower().replace(" ", "-").replace(":", "")[:30]
                process.stdin.write(slug + "\n")
                process.stdin.flush()
                self.output_buffer = ""
                print(f"\n[📤 INJECTING SLUG]: {slug}")

            if "Enter text below. Finish by typing 'END' on its own line." in self.output_buffer[-100:]:
                print(f"\n[⚡ PROCESSING]: Chassis is waiting for a payload.")
                try:
                    decision = self.solve_prompt(self.output_buffer, registry_context)
                except RuntimeError as e:
                    self.record_event("nvidia", "failed", str(e))
                    process.terminate()
                    process.wait(timeout=5)
                    raise
                print(f"[📤 INJECTING PAYLOAD]")
                
                process.stdin.write(decision + "\nEND\n")
                process.stdin.flush()
                self.output_buffer = ""
                
        return_code = process.wait()
        if return_code != 0:
            self.record_event("builder-agent", "failed", f"builder-agent exited with {return_code}")
            raise RuntimeError(f"builder-agent exited with {return_code}")

        print(f"\n[🏁 HARNESS]: Build complete. Log saved to {self.log_path}")
        self.save_log()

def main():
    load_env()
    parser = argparse.ArgumentParser(description="Monolithic Arcade Build Harness")
    parser.add_argument("--goal", type=str, default="A New Arcade Game", help="The build goal.")
    parser.add_argument("--slug", type=str, default=None, help="Optional generated game slug override.")
    parser.add_argument("--nvidia-preflight", action="store_true", help="Check NVIDIA connectivity and exit.")
    args = parser.parse_args()

    if args.nvidia_preflight:
        checks = {
            "planning": os.environ.get("NVIDIA_MODEL", NVIDIA_MODEL),
            "code": os.environ.get("NVIDIA_CODE_MODEL", NVIDIA_CODE_MODEL),
            "code_fallback": os.environ.get("NVIDIA_CODE_FALLBACK_MODEL", NVIDIA_CODE_FALLBACK_MODEL),
            "review": os.environ.get("NVIDIA_REVIEW_MODEL", NVIDIA_REVIEW_MODEL),
        }
        for label, model in checks.items():
            response = call_nvidia(
                [{"role": "user", "content": "Reply with exactly OK and no other text."}],
                model=model,
                max_tokens=12,
                temperature=0.0,
            )
            print(f"{label}: {model}: {response.strip()}")
        return
    
    harness = OrchestratorHarness(args.goal, slug_override=args.slug)
    try:
        harness.run_harness()
    except RuntimeError as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
