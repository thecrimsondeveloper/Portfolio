#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = ROOT / ".ARCADE-SYSTEM" / "sessions"
DEFAULT_INPUT = SESSIONS_DIR / "seed_brainstorming.json"
DEFAULT_OUTPUT = SESSIONS_DIR / "summary_brainstorming.json"
DEFAULT_PASSES = 3
DEFAULT_TOP_K = 12
DEFAULT_ROW_TOP_K = 6
DEFAULT_SAMPLE_SIZE = 3
DEFAULT_RANDOM_SEED = 7
DEFAULT_EXPLORATION_LEVEL = "broad"
DEFAULT_SMOOTH_SAMPLE_SIZE = 6


def normalize_word(word: str) -> str:
    return re.sub(r"[^a-z]", "", word.lower())


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def is_valid_seed_shape(data) -> bool:
    return isinstance(data, list) and all(
        isinstance(category_entry, list)
        and len(category_entry) == 2
        and isinstance(category_entry[0], str)
        and isinstance(category_entry[1], list)
        and all(isinstance(row, list) and len(row) > 0 for row in category_entry[1])
        for category_entry in data
    )


def clean_rows(rows: list[list[str]]) -> list[list[str]]:
    cleaned_rows: list[list[str]] = []
    for row in rows:
        cleaned_row = [normalize_word(item) for item in row if normalize_word(item)]
        if cleaned_row:
            cleaned_rows.append(cleaned_row)
    return cleaned_rows


def collect_word_stats(rows: list[list[str]]) -> tuple[dict[str, float], dict[str, set[str]], dict[str, set[str]]]:
    base_scores: dict[str, float] = defaultdict(float)
    forward_links: dict[str, set[str]] = defaultdict(set)
    backward_links: dict[str, set[str]] = defaultdict(set)

    for row in rows:
        row_seen: set[str] = set()
        row_length = len(row)
        for index, word in enumerate(row):
            position_bonus = max(1.0, row_length - index)
            if word not in row_seen:
                base_scores[word] += 3.0
                row_seen.add(word)
            base_scores[word] += position_bonus
            if index == 0:
                base_scores[word] += 4.0
            if index > 0:
                previous_word = row[index - 1]
                forward_links[previous_word].add(word)
                backward_links[word].add(previous_word)
                base_scores[word] += 1.5
    return dict(base_scores), dict(forward_links), dict(backward_links)


def run_ranked_passes(rows: list[list[str]], passes: int) -> list[dict[str, object]]:
    base_scores, forward_links, backward_links = collect_word_stats(rows)
    current_scores = dict(base_scores)
    pass_results: list[dict[str, object]] = []

    for pass_index in range(1, passes + 1):
        next_scores: dict[str, float] = {}
        for word, base_score in base_scores.items():
            incoming = sum(current_scores.get(link, 0.0) for link in backward_links.get(word, set()))
            outgoing = sum(current_scores.get(link, 0.0) for link in forward_links.get(word, set()))
            next_scores[word] = base_score + (incoming * 0.12) + (outgoing * 0.08)

        ranked_words = sorted(next_scores.items(), key=lambda item: (-item[1], item[0]))
        pass_results.append(
            {
                "pass": pass_index,
                "rankings": [
                    {"word": word, "score": round(score, 3)}
                    for word, score in ranked_words
                ],
            }
        )
        current_scores = next_scores

    return pass_results


def select_top_words(rankings: list[dict[str, object]], top_k: int) -> list[str]:
    return [str(item["word"]) for item in rankings[:top_k]]


def flatten_unique_words(rows: list[list[str]]) -> list[str]:
    unique_words: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for word in row:
            if word in seen:
                continue
            unique_words.append(word)
            seen.add(word)
    return unique_words


def sample_category_words(category: str, rows: list[list[str]], sample_size: int, random_seed: int) -> list[str]:
    candidates = flatten_unique_words(rows)
    if len(candidates) <= sample_size:
        return candidates
    seeded_rng = random.Random(f"{random_seed}:{category}")
    return seeded_rng.sample(candidates, sample_size)


def sample_ranked_words(category: str, rankings: list[dict[str, object]], sample_size: int, random_seed: int) -> list[str]:
    candidates = [str(item["word"]) for item in rankings]
    if len(candidates) <= sample_size:
        return candidates
    seeded_rng = random.Random(f"ranked:{random_seed}:{category}")
    return seeded_rng.sample(candidates[: max(sample_size * 2, sample_size)], sample_size)


def sample_row_slices(category: str, rows: list[list[str]], sample_size: int, random_seed: int) -> dict[str, list[str]]:
    seeded_rng = random.Random(f"slices:{random_seed}:{category}")
    heads = [row[0] for row in rows if row]
    middles = [row[len(row) // 2] for row in rows if row]
    tails = [row[-1] for row in rows if row]
    focus_pool = flatten_unique_words(rows)

    def choose(values: list[str], label: str) -> list[str]:
        unique_values = []
        seen: set[str] = set()
        for value in values:
            if value in seen:
                continue
            unique_values.append(value)
            seen.add(value)
        if len(unique_values) <= sample_size:
            return unique_values
        return seeded_rng.sample(unique_values, sample_size)

    return {
        "heads": choose(heads, "heads"),
        "middles": choose(middles, "middles"),
        "tails": choose(tails, "tails"),
        "focus": choose(focus_pool, "focus"),
    }


def smooth_sample_parts(primary_words: list[str], piecemeal_parts: dict[str, list[str]], sample_size: int) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for word in primary_words:
        if word not in seen:
            merged.append(word)
            seen.add(word)
    for key in ("heads", "middles", "tails", "focus"):
        for word in piecemeal_parts.get(key, []):
            if word in seen:
                continue
            merged.append(word)
            seen.add(word)
            if len(merged) >= sample_size:
                return merged
    return merged[:sample_size]


def summarize_row(category: str, row: list[str], final_rankings: list[dict[str, object]], row_top_k: int) -> dict[str, object]:
    ranking_lookup = {str(item["word"]): float(item["score"]) for item in final_rankings}
    ranked_row_words = sorted({word for word in row}, key=lambda word: (-ranking_lookup.get(word, 0.0), row.index(word), word))
    focus_words = ranked_row_words[:row_top_k]
    return {
        "category": category,
        "seed": row[0],
        "rowLength": len(row),
        "focusWords": focus_words,
        "chainDigest": " -> ".join(row),
    }


def build_game_title(environment_words: list[str], mechanic_words: list[str], enemy_words: list[str]) -> str:
    lead = environment_words[0] if environment_words else "frontier"
    motion = mechanic_words[0] if mechanic_words else "drift"
    threat = enemy_words[0] if enemy_words else "warden"
    return f"{lead.capitalize()} {motion.capitalize()}: {threat.capitalize()} Break"


def build_game_design_doc(exploration_level: str, category_summaries: list[dict[str, object]]) -> dict[str, object]:
    summary_by_category = {item["category"]: item for item in category_summaries}
    environment_words = summary_by_category.get("Environment Seeds", {}).get("smoothedWords", [])
    mechanic_words = summary_by_category.get("Mechanic Seeds", {}).get("smoothedWords", [])
    enemy_words = summary_by_category.get("Enemy Seeds", {}).get("smoothedWords", [])
    progression_words = summary_by_category.get("Progression Seeds", {}).get("smoothedWords", [])

    title = build_game_title(environment_words, mechanic_words, enemy_words)
    primary_environment = environment_words[0] if environment_words else "harbor"
    secondary_environment = environment_words[1] if len(environment_words) > 1 else primary_environment
    primary_mechanic = mechanic_words[0] if mechanic_words else "dash"
    support_mechanic = mechanic_words[1] if len(mechanic_words) > 1 else primary_mechanic
    threat = enemy_words[0] if enemy_words else "sentry"
    escalation = enemy_words[1] if len(enemy_words) > 1 else threat
    progression_arc = progression_words[0] if progression_words else "unlock"
    late_progression = progression_words[1] if len(progression_words) > 1 else progression_arc

    return {
        "title": title,
        "explorationLevel": exploration_level,
        "sourceSamples": {
            "environment": environment_words,
            "mechanics": mechanic_words,
            "enemies": enemy_words,
            "progression": progression_words,
        },
        "elevatorPitch": (
            f"A {exploration_level} arcade game set between {primary_environment} and {secondary_environment}, "
            f"where the player uses {primary_mechanic} and {support_mechanic} actions to outmaneuver {threat} forces "
            f"and drive a {progression_arc}-to-{late_progression} progression arc."
        ),
        "worldConcept": (
            f"The world blends {', '.join(environment_words[:3]) or primary_environment} into a hostile traversal space "
            f"patrolled by {', '.join(enemy_words[:3]) or threat}, pushing the player through compact but expressive runs."
        ),
        "coreLoop": [
            f"Scout routes through {primary_environment} spaces and identify {threat} pressure points.",
            f"Use {primary_mechanic} and {support_mechanic} interactions to survive, reposition, and secure objectives.",
            f"Convert each run into {progression_arc} gains that unlock stronger options and open the next challenge band.",
        ],
        "mechanics": {
            "primaryActions": mechanic_words[:3],
            "enemyPressure": enemy_words[:3],
            "progressionHooks": progression_words[:3],
        },
        "contentPillars": [
            f"Traversal built around {', '.join(mechanic_words[:3]) or primary_mechanic}.",
            f"Threat reads driven by {', '.join(enemy_words[:3]) or threat}.",
            f"Forward momentum shaped by {', '.join(progression_words[:3]) or progression_arc}.",
        ],
        "aggregatedDocument": {
            "environmentBlend": environment_words[:4],
            "mechanicBlend": mechanic_words[:4],
            "enemyBlend": enemy_words[:4],
            "progressionBlend": progression_words[:4],
            "smootherSummary": (
                f"Merge {', '.join(environment_words[:2]) or primary_environment} spaces with {', '.join(mechanic_words[:2]) or primary_mechanic} verbs, "
                f"then pressure the run with {', '.join(enemy_words[:2]) or threat} threats and resolve it through {', '.join(progression_words[:2]) or progression_arc} growth."
            ),
        },
        "designDoc": {
            "playerFantasy": (
                f"Feel like a fast improviser navigating {primary_environment} hazards while turning {escalation} pressure into opportunities."
            ),
            "sessionStructure": (
                f"Short repeatable runs, escalating from {progression_arc} setup to {late_progression} payoffs, with each success adding a new decision layer."
            ),
            "visualDirection": (
                f"Lean on {primary_environment}, {secondary_environment}, and {threat} motifs for strong silhouettes, readable threat zones, and punchy arcade contrast."
            ),
        },
    }


def build_category_summary(category: str, rows: list[list[str]], passes: int, top_k: int, row_top_k: int, sample_size: int, random_seed: int, smooth_sample_size: int) -> dict[str, object]:
    pass_results = run_ranked_passes(rows, passes)
    final_rankings = pass_results[-1]["rankings"] if pass_results else []
    top_words = select_top_words(final_rankings, top_k)
    sampled_words = sample_category_words(category, rows, sample_size=sample_size, random_seed=random_seed)
    ranked_sample = sample_ranked_words(category, final_rankings, sample_size=sample_size, random_seed=random_seed)
    piecemeal_samples = sample_row_slices(category, rows, sample_size=sample_size, random_seed=random_seed)
    smoothed_words = smooth_sample_parts(sampled_words + ranked_sample, piecemeal_samples, sample_size=smooth_sample_size)
    row_summaries = [summarize_row(category, row, final_rankings, row_top_k) for row in rows]
    return {
        "category": category,
        "rowCount": len(rows),
        "itemCount": sum(len(row) for row in rows),
        "topWords": top_words,
        "sampledWords": sampled_words,
        "rankedSample": ranked_sample,
        "piecemealSamples": piecemeal_samples,
        "smoothedWords": smoothed_words,
        "rankedPasses": [
            {
                "pass": result["pass"],
                "topWords": select_top_words(result["rankings"], top_k),
                "topRankings": result["rankings"][:top_k],
            }
            for result in pass_results
        ],
        "chainSummaries": row_summaries,
    }


def build_summary_document(data, source_path: Path, passes: int, top_k: int, row_top_k: int, sample_size: int, random_seed: int, exploration_level: str, smooth_sample_size: int) -> dict[str, object]:
    categories = []
    total_rows = 0
    total_items = 0

    for category_entry in data:
        category, rows = category_entry
        cleaned_rows = clean_rows(rows)
        category_summary = build_category_summary(
            category,
            cleaned_rows,
            passes=passes,
            top_k=top_k,
            row_top_k=row_top_k,
            sample_size=sample_size,
            random_seed=random_seed,
            smooth_sample_size=smooth_sample_size,
        )
        categories.append(category_summary)
        total_rows += category_summary["rowCount"]
        total_items += category_summary["itemCount"]

    return {
        "sourceFile": str(source_path),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "explorationLevel": exploration_level,
        "method": {
            "name": "chained_inference_aggregation",
            "rankedPassing": True,
            "passCount": passes,
            "topK": top_k,
            "rowTopK": row_top_k,
            "sampleSizePerCategory": sample_size,
            "smoothSampleSize": smooth_sample_size,
            "randomSeed": random_seed,
        },
        "totals": {
            "categoryCount": len(categories),
            "rowCount": total_rows,
            "itemCount": total_items,
        },
        "gameDesignDoc": build_game_design_doc(exploration_level, categories),
        "categories": categories,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ChainSummary-CLI: build summary_brainstorming.json from the chained seed dataset using ranked inference passes."
    )
    parser.add_argument("--file", type=str, default=str(DEFAULT_INPUT), help="Path to seed_brainstorming.json.")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="Path to write summary_brainstorming.json.")
    parser.add_argument("--passes", type=int, default=DEFAULT_PASSES, help="Number of ranked aggregation passes to run per category.")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="Number of ranked words to keep per category pass.")
    parser.add_argument("--row-top-k", type=int, default=DEFAULT_ROW_TOP_K, help="Number of focus words to keep per row summary.")
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE, help="Number of random words to sample per category before game design synthesis.")
    parser.add_argument("--smooth-sample-size", type=int, default=DEFAULT_SMOOTH_SAMPLE_SIZE, help="Number of merged words to keep per category after piecemeal smoothing.")
    parser.add_argument("--random-seed", type=int, default=DEFAULT_RANDOM_SEED, help="Random seed used for per-category sampling.")
    parser.add_argument("--exploration-level", type=str, default=DEFAULT_EXPLORATION_LEVEL, help="Exploration depth label to embed in the generated summary document.")
    parser.add_argument("--raw", action="store_true", help="Print only the raw summary output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        source_path = Path(args.file).expanduser().resolve()
        output_path = Path(args.output).expanduser().resolve()
        data = load_json(source_path)
        if not is_valid_seed_shape(data):
            raise RuntimeError("seed_brainstorming.json does not have the required [category, rows] 2D shape.")

        summary_document = build_summary_document(
            data,
            source_path=source_path,
            passes=max(1, args.passes),
            top_k=max(1, args.top_k),
            row_top_k=max(1, args.row_top_k),
            sample_size=max(1, args.sample_size),
            random_seed=args.random_seed,
            exploration_level=args.exploration_level.strip() or DEFAULT_EXPLORATION_LEVEL,
            smooth_sample_size=max(1, args.smooth_sample_size),
        )
        save_json(output_path, summary_document)
        result = str(output_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.raw:
        print(result)
        return 0

    print("\nChainSummary-CLI output:\n")
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
