#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENDPOINT = "http://10.0.0.137:1234/v1/chat/completions"
DEFAULT_EXTENSION_COUNT = 5
DEFAULT_MODEL = "qwen3.5-2b@q8_0"
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_TARGET_ITEMS = 240
BLOCKED_WORDS = {
    "advance",
    "category",
    "develop",
    "enemy",
    "grow",
    "honor",
    "next",
    "planning",
    "progress",
    "progression",
    "seed",
    "seeds",
    "start",
    "strategy",
    "transform",
    "warmth",
}


def clone_data(data):
    return json.loads(json.dumps(data))


def is_valid_dataset_shape(data) -> bool:
    return isinstance(data, list) and all(
        isinstance(category_entry, list)
        and len(category_entry) == 2
        and isinstance(category_entry[0], str)
        and isinstance(category_entry[1], list)
        and all(isinstance(row, list) and len(row) > 0 for row in category_entry[1])
        for category_entry in data
    )


def count_dataset_items(data) -> int:
    if not isinstance(data, list):
        return 0
    return sum(
        len(row)
        for category_entry in data
        if isinstance(category_entry, list) and len(category_entry) == 2 and isinstance(category_entry[1], list)
        for row in category_entry[1]
        if isinstance(row, list)
    )


def build_unique_fallback_word(category: str, row_index: int, seen: set[str]) -> str:
    base = normalize_word(category) or "idea"
    candidate = f"{base}row"
    suffix = row_index
    while candidate in seen:
        suffix += 1
        candidate = f"{base}row{'x' * suffix}"
    return candidate


def remove_duplicate_ideas(data) -> tuple[object, int, list[str]]:
    seen: set[str] = set()
    removed = 0
    summary: list[str] = []

    for category_entry in data:
        if not isinstance(category_entry, list) or len(category_entry) != 2:
            continue
        category, rows = category_entry
        if not isinstance(rows, list):
            continue

        for index, row in enumerate(rows):
            if not isinstance(row, list) or not row:
                continue

            deduped_row: list[str] = []
            for item in row:
                word = normalize_word(str(item).strip())
                if not word:
                    removed += 1
                    continue
                if word in seen:
                    removed += 1
                    summary.append(f"removed duplicate {category}[{index}] -> {word}")
                    continue
                deduped_row.append(word)
                seen.add(word)

            if not deduped_row:
                fallback_word = build_unique_fallback_word(str(category), index, seen)
                deduped_row = [fallback_word]
                seen.add(fallback_word)
            rows[index] = deduped_row

    return data, removed, summary


def build_rewrite_prompt(category: str, seed: str, prior_variant: str = "") -> str:
    anchor = prior_variant.strip() or seed.strip()
    return textwrap.dedent(
        f"""
        category -> {category}
        harbor -> dock
        desert -> dune
        frost -> glacier
        sentry -> guard
        {seed.strip()} -> {anchor}
        {anchor} ->
        """
    ).strip()


def build_smoothing_prompt(category: str, seed: str, previous_word: str, candidate_word: str, used_words: list[str]) -> str:
    banned = ", ".join(used_words[-8:]) if used_words else "none"
    return textwrap.dedent(
        f"""
        category -> {category}
        {seed} -> {previous_word}
        candidate -> {candidate_word}
        used -> {banned}
        next ->
        """
    ).strip()


def build_system_prompt() -> str:
    return "Reply with exactly one lowercase related word. No punctuation. No explanation. No repeats."


def call_lm_studio(prompt: str, model: str, endpoint: str, max_tokens: int = 4, temperature: float = 1.0, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "top_p": 1,
        "max_tokens": max_tokens,
        "stop": ["\n", " "],
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


def parse_variant_response(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            cleaned = "\n".join(lines[1:-1]).strip()
    first_line = cleaned.splitlines()[0].strip()
    variant = first_line.split()[0].strip().strip('"\'.,:;!?()[]{}')
    if not variant:
        raise RuntimeError("Variant response was empty.")
    return variant


def normalize_word(word: str) -> str:
    return re.sub(r"[^a-z]", "", word.lower())


def is_valid_chain_word(word: str, used_words: list[str]) -> bool:
    normalized = normalize_word(word)
    if len(normalized) < 3:
        return False
    if normalized in BLOCKED_WORDS:
        return False
    if normalized in {normalize_word(item) for item in used_words}:
        return False
    return normalized == word.lower()


def load_chain_file(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_chain_file(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def generate_chain_word(category: str, seed: str, anchor: str, model: str, endpoint: str, used_words: list[str] | None = None, temperature: float = 1.0) -> str:
    used_words = used_words or []
    prompt = build_rewrite_prompt(category, seed, anchor)
    last_error = None
    for _ in range(4):
        try:
            candidate = parse_variant_response(call_lm_studio(prompt, model=model, endpoint=endpoint, temperature=temperature))
        except Exception as exc:
            last_error = exc
            continue
        candidate = normalize_word(candidate)
        if is_valid_chain_word(candidate, used_words):
            return candidate
    if last_error:
        raise RuntimeError(f"Unable to generate a valid chain word: {last_error}")
    raise RuntimeError("Unable to generate a valid chain word.")


def smooth_existing_row(category: str, row: list[str], model: str, endpoint: str, temperature: float) -> list[str]:
    if not row:
        return []
    smoothed = [normalize_word(str(row[0]).strip())]
    seed = smoothed[0]
    for candidate in row[1:]:
        candidate_word = normalize_word(str(candidate).strip())
        if not candidate_word:
            continue
        if is_valid_chain_word(candidate_word, smoothed):
            smoothed.append(candidate_word)
            continue
        try:
            next_word = parse_variant_response(
                call_lm_studio(
                    build_smoothing_prompt(category, seed, smoothed[-1], candidate_word, smoothed),
                    model=model,
                    endpoint=endpoint,
                    temperature=temperature,
                )
            )
            next_word = normalize_word(next_word)
        except Exception:
            next_word = candidate_word
        if not is_valid_chain_word(next_word, smoothed):
            next_word = candidate_word
        if is_valid_chain_word(next_word, smoothed):
            smoothed.append(next_word)
    return smoothed


def extend_row(category: str, row: list[str], model: str, endpoint: str, count: int, temperature: float) -> list[str]:
    if not row:
        return row
    seed = row[0]
    extended = list(row)
    attempts = 0
    while len(extended) < len(row) + count and attempts < count * 4:
        attempts += 1
        try:
            next_word = generate_chain_word(category, seed, extended[-1], model=model, endpoint=endpoint, used_words=extended, temperature=temperature)
        except Exception:
            continue
        extended.append(next_word)
    return extended


def smooth_and_extend_dataset(data, model: str, endpoint: str, extension_count: int, temperature: float) -> tuple[object, list[str]]:
    summary = []
    for category_entry in data:
        if not isinstance(category_entry, list) or len(category_entry) != 2:
            continue
        category, rows = category_entry
        if not isinstance(rows, list):
            continue
        for index, row in enumerate(rows):
            if not isinstance(row, list) or not row:
                continue
            cleaned_row = [normalize_word(str(item).strip()) for item in row if normalize_word(str(item).strip())]
            if not cleaned_row:
                continue
            smoothed_row = smooth_existing_row(category, cleaned_row, model=model, endpoint=endpoint, temperature=temperature)
            extended_row = extend_row(category, smoothed_row, model=model, endpoint=endpoint, count=extension_count, temperature=temperature)
            rows[index] = extended_row
            summary.append(f"{category}[{index}] -> {', '.join(extended_row)}")
    return data, summary


def run_dataset_passes(path: Path, model: str, endpoint: str, extension_count: int, temperature: float, passes: int, target_items: int) -> tuple[object, list[str], int]:
    data = load_chain_file(path)
    if not is_valid_dataset_shape(data):
        raise RuntimeError("Brainstorming dataset does not have the required 2D idea array shape.")

    summary: list[str] = []
    completed_passes = 0
    total_duplicates_removed = 0

    while completed_passes < passes and count_dataset_items(data) < target_items:
        snapshot = clone_data(data)
        updated_data, pass_summary = smooth_and_extend_dataset(
            clone_data(data),
            model=model,
            endpoint=endpoint,
            extension_count=max(0, extension_count),
            temperature=temperature,
        )

        if not is_valid_dataset_shape(updated_data):
            save_chain_file(path, snapshot)
            raise RuntimeError("Generated dataset lost the required 2D idea array shape; previous JSON was restored.")

        updated_data, removed_duplicates, dedupe_summary = remove_duplicate_ideas(updated_data)

        if not is_valid_dataset_shape(updated_data):
            save_chain_file(path, snapshot)
            raise RuntimeError("Duplicate removal broke the required 2D idea array shape; previous JSON was restored.")

        data = updated_data
        save_chain_file(path, data)
        completed_passes += 1
        total_duplicates_removed += removed_duplicates
        summary.append(f"pass {completed_passes}: {count_dataset_items(data)} items, duplicates removed {removed_duplicates}")
        summary.extend(pass_summary)
        summary.extend(dedupe_summary)

    summary.append(f"duplicates removed total: {total_duplicates_removed}")
    summary.append(f"ideas needed to refill: {total_duplicates_removed}")
    return data, summary, total_duplicates_removed


def dedupe_and_save_dataset(path: Path, data) -> tuple[object, int]:
    updated_data, removed_duplicates, _ = remove_duplicate_ideas(data)
    if not is_valid_dataset_shape(updated_data):
        raise RuntimeError("Duplicate removal broke the required 2D idea array shape.")
    save_chain_file(path, updated_data)
    return updated_data, removed_duplicates


def extend_seed_chain(data, category_name: str, seed_index: int, model: str, endpoint: str) -> str:
    for category_entry in data:
        if not isinstance(category_entry, list) or len(category_entry) != 2:
            continue
        category, pairs = category_entry
        if category != category_name:
            continue
        if not isinstance(pairs, list):
            raise RuntimeError(f"Category '{category_name}' does not contain a seed pair list.")
        if seed_index < 0 or seed_index >= len(pairs):
            raise RuntimeError(f"Seed index {seed_index} is out of range for category '{category_name}'.")
        pair = pairs[seed_index]
        if not isinstance(pair, list) or len(pair) < 2:
            raise RuntimeError("Each seed pair must contain at least a base seed and one variant seed.")
        base_seed = str(pair[0]).strip()
        anchor = str(pair[-1]).strip()
        variant = generate_chain_word(category_name, base_seed, anchor, model=model, endpoint=endpoint, used_words=pair)
        pair.append(variant)
        return variant
    raise RuntimeError(f"Category '{category_name}' was not found.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chainstorm-CLI: rewrite one seed into the next one-word chain item using an LM Studio-compatible endpoint."
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="2B model id to send to the LM Studio-compatible endpoint.")
    parser.add_argument("--seed", type=str, default="", help="Base seed word to rewrite into the next chain word.")
    parser.add_argument("--anchor", type=str, default="", help="Optional current chain word to rewrite from instead of the base seed.")
    parser.add_argument("--file", type=str, default=str(ROOT / "PagesInteractive-CLI" / "seed_brainstorming.json"),
                        help="Path to the brainstorming JSON file when extending an existing chain.")
    parser.add_argument("--category", type=str, default="", help="Category name inside the brainstorming JSON when extending a chain.")
    parser.add_argument("--seed-index", type=int, default=-1,
                        help="Index of the seed pair inside the selected category to extend from its last entry.")
    parser.add_argument("--endpoint", type=str, default=DEFAULT_ENDPOINT,
                        help="LM Studio-compatible chat completions endpoint.")
    parser.add_argument("--extend-count", type=int, default=DEFAULT_EXTENSION_COUNT,
                        help="Number of new chain items to append to each row during a dataset smoothing pass.")
    parser.add_argument("--temperature", type=float, default=1.0,
                        help="Sampling temperature for chain generation.")
    parser.add_argument("--passes", type=int, default=1,
                        help="Number of full dataset passes to run when extending the brainstorming file.")
    parser.add_argument("--target-items", type=int, default=DEFAULT_TARGET_ITEMS,
                        help="Stop dataset passes once the brainstorming file reaches at least this many total items.")
    parser.add_argument("--raw", action="store_true", help="Print only the raw variant text.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.category and args.seed_index >= 0:
            path = Path(args.file).expanduser().resolve()
            data = load_chain_file(path)
            variant = extend_seed_chain(data, args.category, args.seed_index, model=args.model, endpoint=args.endpoint)
            _, removed_duplicates = dedupe_and_save_dataset(path, data)
            variant = f"{variant}\nduplicates removed total: {removed_duplicates}\nideas needed to refill: {removed_duplicates}"
        elif args.seed.strip():
            variant = generate_chain_word("general", args.seed, args.anchor, model=args.model, endpoint=args.endpoint, used_words=[args.seed, args.anchor] if args.anchor else [args.seed], temperature=args.temperature)
        else:
            path = Path(args.file).expanduser().resolve()
            _, summary, _ = run_dataset_passes(
                path=path,
                model=args.model,
                endpoint=args.endpoint,
                extension_count=max(0, args.extend_count),
                temperature=args.temperature,
                passes=max(1, args.passes),
                target_items=max(1, args.target_items),
            )
            variant = "\n".join(summary)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.raw:
        print(variant)
        return 0

    print("\nChainstorm-CLI variant:\n")
    print(variant)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
