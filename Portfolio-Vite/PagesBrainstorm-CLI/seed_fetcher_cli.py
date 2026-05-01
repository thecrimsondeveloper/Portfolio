#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "PagesInteractive-CLI" / "seed_brainstorming.json"
DEFAULT_OUTPUT = ROOT / "PagesInteractive-CLI" / "seed_brainstorming.json"
DEFAULT_ENDPOINT = "http://10.0.0.137:1234/v1/chat/completions"
DEFAULT_MODEL = "qwen3.5-2b@q8_0"
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_BRAINSTORM_MODE = "auto"
DEFAULT_AUGMENT_ROWS = 1
FALLBACK_SUFFIX_WORDS = [
    "alpha",
    "beta",
    "gamma",
    "delta",
    "ember",
    "signal",
    "vector",
    "relay",
    "lattice",
    "orbit",
    "pulse",
    "matrix",
]

CATEGORY_ORDER = [
    "Environment Seeds",
    "Genre Seeds",
    "Camera Mode Seeds",
    "Arena Shape Seeds",
    "Primary Verb Seeds",
    "Mechanic Seeds",
    "Scoring Model Seeds",
    "Failure Mode Seeds",
    "Enemy Seeds",
    "Enemy Behavior Seeds",
    "Objective Structure Seeds",
    "Resource System Seeds",
    "Progression Seeds",
    "Level Progression Seeds",
    "Twist Constraint Seeds",
]

CATEGORY_INJECTIONS = {
    "Environment Seeds": {
        "harbor": ["dock", "pier", "tide", "channel"],
        "desert": ["dune", "mesa", "basin", "canyon"],
        "frost": ["ice", "glacier", "swell", "shore"],
        "forest": ["grove", "canopy", "moss", "root"],
        "reef": ["coral", "current", "lagoon", "spray"],
    },
    "Mechanic Seeds": {
        "dash": ["sprint", "blink", "slide", "vault"],
        "rewire": ["relay", "signal", "wire", "anchor"],
        "carry": ["haul", "stack", "root", "pivot"],
        "drift": ["glide", "swerve", "skid", "sail"],
        "pulse": ["charge", "burst", "echo", "phase"],
    },
    "Genre Seeds": {
        "chase": ["pursuit", "escape", "pressure", "speed"],
        "stealth": ["sneak", "hide", "patrol", "alarm"],
        "puzzle": ["logic", "switch", "sequence", "solve"],
        "defense": ["hold", "waves", "fortify", "protect"],
        "runner": ["route", "lane", "sprint", "flow"],
    },
    "Camera Mode Seeds": {
        "topdown": ["overhead", "map", "grid", "readable"],
        "sideview": ["platform", "vertical", "jump", "profile"],
        "isometric": ["diagonal", "depth", "tile", "angle"],
        "fixedroom": ["room", "frame", "contained", "scene"],
        "scrolling": ["lane", "forward", "pace", "track"],
    },
    "Arena Shape Seeds": {
        "maze": ["corridor", "junction", "deadend", "route"],
        "lanes": ["tracks", "columns", "switch", "traffic"],
        "loop": ["circuit", "lap", "return", "cycle"],
        "tower": ["climb", "floor", "height", "ascent"],
        "grid": ["cells", "patrol", "zones", "coverage"],
    },
    "Primary Verb Seeds": {
        "dodge": ["sidestep", "avoid", "weave", "evade"],
        "sneak": ["hide", "crawl", "mask", "bypass"],
        "escort": ["guide", "protect", "lead", "deliver"],
        "repair": ["fix", "patch", "restore", "connect"],
        "defend": ["hold", "guard", "block", "shield"],
    },
    "Scoring Model Seeds": {
        "time": ["timer", "split", "rush", "record"],
        "combo": ["chain", "streak", "multiplier", "flow"],
        "survival": ["endure", "seconds", "pressure", "last"],
        "route": ["perfect", "clean", "optimal", "line"],
        "territory": ["hold", "zones", "control", "claim"],
    },
    "Failure Mode Seeds": {
        "caught": ["alarm", "spotted", "capture", "alert"],
        "crushed": ["hazard", "impact", "collapse", "pressure"],
        "timer": ["deadline", "expire", "rush", "countdown"],
        "resource": ["deplete", "empty", "scarcity", "drain"],
        "signal": ["broken", "lost", "disconnect", "static"],
    },
    "Enemy Seeds": {
        "sentry": ["guard", "warden", "fort", "watch"],
        "drone": ["swarm", "stalker", "scout", "night"],
        "marker": ["totem", "beacon", "flag", "signal"],
        "raider": ["hunter", "ambush", "claw", "pack"],
        "warden": ["citadel", "patrol", "shield", "order"],
    },
    "Enemy Behavior Seeds": {
        "patrol": ["route", "sweep", "watch", "loop"],
        "ambush": ["hide", "spring", "trap", "burst"],
        "swarm": ["cluster", "surround", "rush", "crowd"],
        "mirror": ["copy", "reflect", "shadow", "echo"],
        "corrupt": ["infect", "tile", "spread", "decay"],
    },
    "Objective Structure Seeds": {
        "collect": ["set", "pieces", "gather", "complete"],
        "exit": ["escape", "gate", "finish", "route"],
        "escort": ["target", "companion", "guide", "protect"],
        "activate": ["sequence", "switch", "relay", "trigger"],
        "survive": ["waves", "hold", "endure", "timer"],
    },
    "Resource System Seeds": {
        "stamina": ["energy", "burst", "recover", "limit"],
        "light": ["visibility", "glow", "dark", "reveal"],
        "signal": ["range", "static", "relay", "link"],
        "cargo": ["weight", "balance", "carry", "drop"],
        "battery": ["charge", "power", "drain", "cell"],
    },
    "Progression Seeds": {
        "unlock": ["ascend", "evolve", "discover", "reveal"],
        "upgrade": ["enhance", "refine", "advance", "gain"],
        "reveal": ["unfold", "expose", "unveil", "trace"],
        "recover": ["repair", "restore", "stabilize", "renew"],
        "converge": ["merge", "align", "master", "complete"],
    },
    "Level Progression Seeds": {
        "single": ["run", "arcade", "reset", "score"],
        "rooms": ["ladder", "sequence", "chambers", "clear"],
        "branching": ["fork", "choice", "routes", "paths"],
        "waves": ["escalate", "phase", "pressure", "spawn"],
        "finale": ["phase", "climax", "finish", "resolve"],
    },
    "Twist Constraint Seeds": {
        "reverse": ["invert", "zone", "control", "disorient"],
        "onebutton": ["tap", "hold", "release", "timing"],
        "nostop": ["momentum", "forward", "pressure", "flow"],
        "shared": ["health", "linked", "companion", "risk"],
        "decay": ["floor", "collapse", "timer", "vanish"],
    },
}

CATEGORY_FALLBACKS = {
    "Environment Seeds": ["harbor", "desert", "frost"],
    "Genre Seeds": ["chase", "stealth", "puzzle"],
    "Camera Mode Seeds": ["topdown", "sideview", "isometric"],
    "Arena Shape Seeds": ["maze", "lanes", "loop"],
    "Primary Verb Seeds": ["dodge", "sneak", "escort"],
    "Mechanic Seeds": ["dash", "rewire", "carry"],
    "Scoring Model Seeds": ["time", "combo", "survival"],
    "Failure Mode Seeds": ["caught", "timer", "resource"],
    "Enemy Seeds": ["sentry", "drone", "marker"],
    "Enemy Behavior Seeds": ["patrol", "ambush", "swarm"],
    "Objective Structure Seeds": ["collect", "exit", "activate"],
    "Resource System Seeds": ["stamina", "signal", "battery"],
    "Progression Seeds": ["unlock", "upgrade", "reveal"],
    "Level Progression Seeds": ["single", "rooms", "branching"],
    "Twist Constraint Seeds": ["reverse", "onebutton", "decay"],
}


def normalize_word(word: str) -> str:
    return re.sub(r"[^a-z]", "", word.lower())


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def probe_lm_studio(endpoint: str, model: str, timeout_seconds: int = 3) -> tuple[bool, str]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Reply with ok."},
            {"role": "user", "content": "ping"},
        ],
        "temperature": 0,
        "max_tokens": 2,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            json.load(response)
        return True, ""
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        return False, str(exc.reason)
    except Exception as exc:
        return False, str(exc)


def call_lm_studio(prompt: str, model: str, endpoint: str, system_prompt: str, max_tokens: int = 64, temperature: float = 0.9, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "top_p": 1,
        "max_tokens": max_tokens,
        "stop": ["\n\n"],
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    last_error = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
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
        raise RuntimeError(f"LM Studio request failed: {last_error}")
    choices = response_data.get("choices", [])
    if not choices:
        raise RuntimeError("LM Studio returned no choices.")
    message = choices[0].get("message", {})
    text = message.get("content") or choices[0].get("text") or message.get("reasoning_content")
    if not text:
        raise RuntimeError("LM Studio returned no usable content.")
    return text.strip()


def is_valid_seed_shape(data) -> bool:
    return isinstance(data, list) and all(
        isinstance(category_entry, list)
        and len(category_entry) == 2
        and isinstance(category_entry[0], str)
        and isinstance(category_entry[1], list)
        and all(isinstance(row, list) and len(row) > 0 for row in category_entry[1])
        for category_entry in data
    )


def parse_seed_words(text: str) -> list[str]:
    parts = [normalize_word(item) for item in text.split(",")]
    return [item for item in parts if item]


def parse_category_map(values: list[str] | None) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    for raw_value in values or []:
        if "=" not in raw_value:
            raise RuntimeError(f"Invalid inject value '{raw_value}'. Use category=word1,word2")
        category_key, raw_words = raw_value.split("=", 1)
        category_name = category_key.strip().lower()
        matching_category = next((item for item in CATEGORY_ORDER if item.lower().startswith(category_name)), None)
        if not matching_category:
            raise RuntimeError(f"Unknown category key '{category_key}'")
        parsed[matching_category] = parse_seed_words(raw_words)
    return parsed


def flatten_unique_words(rows: list[list[str]]) -> list[str]:
    words: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for word in row:
            normalized = normalize_word(word)
            if not normalized or normalized in seen:
                continue
            words.append(normalized)
            seen.add(normalized)
    return words


def normalize_row(row: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for word in row:
        compact = normalize_word(word)
        if not compact or compact in seen:
            continue
        normalized.append(compact)
        seen.add(compact)
    return normalized


def collect_existing_rows(data, category_name: str) -> list[list[str]]:
    for category_entry in data:
        if isinstance(category_entry, list) and len(category_entry) == 2 and category_entry[0] == category_name:
            rows = category_entry[1]
            if not isinstance(rows, list):
                return []
            normalized_rows = []
            for row in rows:
                if isinstance(row, list):
                    normalized = normalize_row(row)
                    if normalized:
                        normalized_rows.append(normalized)
            return normalized_rows
    return []


def collect_existing_words(data, category_name: str) -> list[str]:
    return flatten_unique_words(collect_existing_rows(data, category_name))


def build_row(category_name: str, seed_word: str, existing_words: list[str]) -> list[str]:
    injections = CATEGORY_INJECTIONS.get(category_name, {})
    row: list[str] = []
    seen: set[str] = set()

    def add_word(word: str) -> None:
        normalized = normalize_word(word)
        if not normalized or normalized in seen:
            return
        row.append(normalized)
        seen.add(normalized)

    add_word(seed_word)
    for word in injections.get(seed_word, []):
        add_word(word)
    for word in existing_words:
        if len(row) >= 8:
            break
        if word == seed_word:
            continue
        add_word(word)
    return row or [seed_word]


def build_category_rows(category_name: str, requested_words: list[str], source_data) -> list[list[str]]:
    existing_words = collect_existing_words(source_data, category_name)
    seed_words = requested_words[:] if requested_words else CATEGORY_FALLBACKS[category_name][:]
    for word in existing_words:
        if len(seed_words) >= 3:
            break
        if word not in seed_words:
            seed_words.append(word)

    rows = [build_row(category_name, seed_word, existing_words) for seed_word in seed_words[:3]]
    return rows


def parse_row_words(text: str) -> list[str]:
    tokens = re.split(r"[,|/;\n\s]+", text)
    return [normalize_word(token) for token in tokens if normalize_word(token)]


def row_is_useful(row: list[str]) -> bool:
    if len(row) < 4:
        return False
    if any(len(word) > 18 for word in row):
        return False
    return True


def build_fallback_append_row(category_name: str, source_data) -> list[str]:
    existing_rows = collect_existing_rows(source_data, category_name)
    existing_words = collect_existing_words(source_data, category_name)
    base_words = CATEGORY_FALLBACKS.get(category_name, ["seed", "arcade", "loop"])
    offset = len(existing_rows)
    row = normalize_row(
        [
            base_words[offset % len(base_words)],
            FALLBACK_SUFFIX_WORDS[offset % len(FALLBACK_SUFFIX_WORDS)],
            FALLBACK_SUFFIX_WORDS[(offset + 3) % len(FALLBACK_SUFFIX_WORDS)],
            FALLBACK_SUFFIX_WORDS[(offset + 6) % len(FALLBACK_SUFFIX_WORDS)],
            *existing_words[offset : offset + 4],
        ]
    )
    return None


def build_model_row(category_name: str, source_data, requested_words: list[str], endpoint: str, model: str, brainstorm_mode: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> list[str] | None:
    existing_rows = collect_existing_rows(source_data, category_name)
    existing_words = collect_existing_words(source_data, category_name)
    prompt_seed_words = requested_words[:] if requested_words else CATEGORY_FALLBACKS[category_name][:]
    base_prompt = (
        f"Expand an arcade brainstorming dataset for the category '{category_name}'.\n"
        "Return exactly one comma-separated row of 6 to 8 lowercase seed words.\n"
        "Use commas between every word. Never join multiple words into one token.\n"
        "The first word must be a fresh anchor that is not already one of these existing words:\n"
        f"{', '.join(existing_words[:24])}\n"
        "Keep the row distinct, category-relevant, and usable as a brainstorm chain.\n"
        f"Current seed hints: {', '.join(prompt_seed_words[:8])}\n"
        "Output words only, like: anchor, verb, pressure, route, timer, reward"
    )
    if brainstorm_mode == "skip":
        return None
    if brainstorm_mode == "auto":
        available, reason = probe_lm_studio(endpoint, model, timeout_seconds=max(1, min(3, timeout_seconds)))
        if not available:
            return None
    invalid_rows: list[str] = []
    for attempt in range(1, 4):
        retry_note = ""
        if invalid_rows:
            retry_note = f"\nAvoid these invalid prior outputs: {' | '.join(invalid_rows)}"
        text = call_lm_studio(
            base_prompt + retry_note,
            model=model,
            endpoint=endpoint,
            system_prompt="You expand brainstorming rows for arcade game seeds. Reply with a single comma-separated row only.",
            max_tokens=64,
            temperature=0.7,
            timeout_seconds=timeout_seconds,
        )
        row = normalize_row(parse_row_words(text))
        if row and row_is_useful(row) and row not in existing_rows:
            return row[:8]
        invalid_rows.append(text.strip())
    return row[:8]


def build_dataset(source_data, injected_categories: dict[str, list[str]], endpoint: str, model: str, brainstorm_mode: str, augment_rows: int) -> tuple[list[list[object]], list[dict[str, object]]]:
    dataset = []
    report = []
    for category_name in CATEGORY_ORDER:
        existing_rows = collect_existing_rows(source_data, category_name)
        if existing_rows:
            rows = existing_rows[:]
        else:
            rows = build_category_rows(category_name, injected_categories.get(category_name, []), source_data)
        if augment_rows > 0:
            category_seed_words = injected_categories.get(category_name, []) or CATEGORY_FALLBACKS[category_name][:]
            for _ in range(augment_rows):
                model_row = build_model_row(
                    category_name,
                    source_data,
                    category_seed_words,
                    endpoint=endpoint,
                    model=model,
                    brainstorm_mode=brainstorm_mode,
                )
                if model_row and model_row not in rows:
                    rows.append(model_row)
                    report.append(
                        {
                            "category": category_name,
                            "source": "lm_studio",
                            "row": model_row,
                            "before": len(rows) - 1,
                            "after": len(rows),
                        }
                    )
                else:
                    if brainstorm_mode == "required":
                        raise RuntimeError(f"LM Studio did not return a usable unique row for {category_name}.")
                    fallback_row = build_fallback_append_row(category_name, [[category_name, rows]])
                    if fallback_row and fallback_row not in rows:
                        rows.append(fallback_row)
                        report.append(
                            {
                                "category": category_name,
                                "source": "fallback",
                                "row": fallback_row,
                                "before": len(rows) - 1,
                                "after": len(rows),
                            }
                        )
        dataset.append([category_name, rows])
    return dataset, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SeedFetcher-CLI: inject simple seed parameters and emit a robust summary-ready brainstorming dataset."
    )
    parser.add_argument("--source", type=str, default=str(DEFAULT_SOURCE), help="Source brainstorming dataset to pull fallback vocabulary from.")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="Output brainstorming dataset path.")
    parser.add_argument("--environment", type=str, default="", help="Comma-separated environment seeds.")
    parser.add_argument("--mechanic", type=str, default="", help="Comma-separated mechanic seeds.")
    parser.add_argument("--enemy", type=str, default="", help="Comma-separated enemy seeds.")
    parser.add_argument("--progression", type=str, default="", help="Comma-separated progression seeds.")
    parser.add_argument("--inject", action="append", help="Additional category injections like environment=reef,lagoon")
    parser.add_argument("--brainstorm-mode", choices=("auto", "required", "skip"), default=DEFAULT_BRAINSTORM_MODE, help="Use LM Studio additively, require it, or skip it for deterministic-only output.")
    parser.add_argument("--endpoint", type=str, default=DEFAULT_ENDPOINT, help="LM Studio chat completions endpoint for brainstorm augmentation.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="LM Studio model id for brainstorm augmentation.")
    parser.add_argument("--augment-rows", type=int, default=DEFAULT_AUGMENT_ROWS, help="How many model-generated rows to append per category.")
    parser.add_argument("--lm-health-timeout", type=int, default=3, help="Timeout in seconds for the LM Studio health probe.")
    parser.add_argument("--raw", action="store_true", help="Print only the output dataset path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source_path = Path(args.source).expanduser().resolve()
        output_path = Path(args.output).expanduser().resolve()
        source_data = load_json(source_path)
        if not is_valid_seed_shape(source_data):
            raise RuntimeError("Source brainstorming dataset does not have the required [category, rows] 2D shape.")

        injected_categories = parse_category_map(args.inject)
        direct_injections = {
            "Environment Seeds": parse_seed_words(args.environment),
            "Mechanic Seeds": parse_seed_words(args.mechanic),
            "Enemy Seeds": parse_seed_words(args.enemy),
            "Progression Seeds": parse_seed_words(args.progression),
        }
        for category_name, values in direct_injections.items():
            if values:
                injected_categories[category_name] = values

        available = True
        reason = ""
        if args.brainstorm_mode != "skip":
            available, reason = probe_lm_studio(args.endpoint, args.model, timeout_seconds=max(1, args.lm_health_timeout))
            if not available and args.brainstorm_mode == "required":
                raise RuntimeError(f"LM Studio brainstorm augmentation unavailable: {reason}")

        dataset, report = build_dataset(
            source_data,
            injected_categories,
            endpoint=args.endpoint,
            model=args.model,
            brainstorm_mode=args.brainstorm_mode if available else "skip",
            augment_rows=max(0, args.augment_rows),
        )
        if not is_valid_seed_shape(dataset):
            raise RuntimeError("Generated dataset does not have the required [category, rows] 2D shape.")
        save_json(output_path, dataset)
        result = str(output_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.raw:
        print(result)
        return 0

    print("\nSeedFetcher-CLI output:\n")
    print(result)
    print("\nAugmentation report:")
    print(f"- mode: {args.brainstorm_mode}")
    print(f"- endpoint: {args.endpoint}")
    print(f"- model: {args.model}")
    print(f"- appended rows: {len(report)}")
    for item in report:
        print(f"- {item['category']}: {item['before']} -> {item['after']} via {item['source']} | {', '.join(item['row'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
