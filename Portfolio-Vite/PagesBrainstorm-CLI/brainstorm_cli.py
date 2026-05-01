#!/usr/bin/env python3
import argparse
import json
import random
import re
import sys
import textwrap
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "PagesInteractive-CLI" / "summary_brainstorming.json"
DEFAULT_OUTPUT = ROOT / "PagesInteractive-CLI" / "final_brainstorming.json"
DEFAULT_ENDPOINT = "http://10.0.0.137:1234/v1/chat/completions"
DEFAULT_MODEL = "qwen3.5-2b@q8_0"
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_RANDOM_SEED = 17
DEFAULT_EXPLORATION_LOOPS = 4
LM_STUDIO_AVAILABLE = True
LM_STUDIO_UNAVAILABLE_REASON = ""


def normalize_word(word: str) -> str:
    return re.sub(r"[^a-z]", "", word.lower())


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def set_lm_studio_availability(available: bool, reason: str = "") -> None:
    global LM_STUDIO_AVAILABLE, LM_STUDIO_UNAVAILABLE_REASON
    LM_STUDIO_AVAILABLE = available
    LM_STUDIO_UNAVAILABLE_REASON = reason


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


def call_lm_studio(prompt: str, model: str, endpoint: str, system_prompt: str, max_tokens: int = 120, temperature: float = 1.0, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    if not LM_STUDIO_AVAILABLE:
        raise RuntimeError(LM_STUDIO_UNAVAILABLE_REASON or "LM Studio is disabled for this run.")
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


def is_valid_summary_shape(data) -> bool:
    return (
        isinstance(data, dict)
        and isinstance(data.get("categories"), list)
        and isinstance(data.get("gameDesignDoc"), dict)
        and all(
            isinstance(category_entry, dict)
            and isinstance(category_entry.get("category"), str)
            and isinstance(category_entry.get("chainSummaries"), list)
            for category_entry in data.get("categories", [])
        )
    )


def dedupe_words(words: list[str]) -> list[str]:
    deduped = []
    seen: set[str] = set()
    for word in words:
        normalized = normalize_word(str(word))
        if not normalized or normalized in seen:
            continue
        deduped.append(normalized)
        seen.add(normalized)
    return deduped


def pick_words(words: list[str], count: int, rng: random.Random) -> list[str]:
    cleaned = dedupe_words(words)
    if len(cleaned) <= count:
        return cleaned
    return rng.sample(cleaned, count)


def parse_csv_words(text: str, allowed_words: list[str], count: int, fallback_words: list[str]) -> list[str]:
    allowed = set(dedupe_words(allowed_words))
    tokens = re.split(r"[,|/;\n]+", text)
    parsed = []
    seen: set[str] = set()
    for token in tokens:
        normalized = normalize_word(token)
        if not normalized or normalized in seen:
            continue
        if allowed and normalized not in allowed:
            continue
        parsed.append(normalized)
        seen.add(normalized)
        if len(parsed) >= count:
            return parsed
    for fallback in dedupe_words(fallback_words):
        if fallback in seen:
            continue
        parsed.append(fallback)
        seen.add(fallback)
        if len(parsed) >= count:
            break
    return parsed[:count]


def parse_minutes(text: str, fallback_minutes: int) -> str:
    match = re.search(r"\b(8|10|12|15|18)\b", text)
    if match:
        return f"{match.group(1)} minutes"
    return f"{fallback_minutes} minutes"


def slugify_title(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "new-game"


def titleize_identifier(text: str) -> str:
    cleaned = re.sub(r"[_-]+", " ", str(text)).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.title() if cleaned else "Untitled"


def build_objective_text(player_actions: list[str], enemy_types: list[str], progression_goal: list[str]) -> str:
    primary_action = player_actions[0] if player_actions else "move"
    secondary_action = player_actions[1] if len(player_actions) > 1 else primary_action
    primary_enemy = enemy_types[0] if enemy_types else "enemy"
    progression_phrase = ", ".join(progression_goal or ["unlocks"])
    return (
        f"Use {primary_action} and {secondary_action} to survive {primary_enemy} patrols, "
        f"secure relic routes, and turn each run into {progression_phrase} progress."
    )


def choose_runtime_template(summary_data: dict, final_spec: dict) -> tuple[str, str, str]:
    text = json.dumps({"summary": summary_data.get("gameDesignDoc", {}), "finalSpec": final_spec}, ensure_ascii=False).lower()
    if any(word in text for word in ("stealth", "patrol", "infiltration", "crouch", "avoid", "sneak", "caught", "alarm")):
        return "stealth_patrol", "stealth patrol", "patrol grid"
    if any(word in text for word in ("delivery", "sprint", "runner", "wall-running", "zipline", "momentum", "parkour", "scrolling-lane", "route runner")):
        return "route_runner", "route runner", "lane route"
    if any(word in text for word in ("relay", "signal", "reconnect", "chain", "circuit", "network", "repair network")):
        return "relay_chain", "relay chain", "node network"
    if any(word in text for word in ("maze", "map", "library", "cavern", "ruin", "search", "artifact", "vault", "extraction", "reach exit")):
        return "extraction_maze", "extraction maze", "maze"
    return "arena_survival", "arena survival", "arena"


def build_game_design_profile(summary_data: dict, final_document: dict, fallback_source: str) -> dict[str, object]:
    final_spec = final_document.get("finalSpec", {}) if isinstance(final_document.get("finalSpec"), dict) else {}
    world = final_spec.get("world", {}) if isinstance(final_spec.get("world"), dict) else {}
    progression = final_spec.get("progression", {}) if isinstance(final_spec.get("progression"), dict) else {}
    encounter_design = final_spec.get("encounterDesign", {}) if isinstance(final_spec.get("encounterDesign"), dict) else {}
    ui_spec = final_spec.get("ui", {}) if isinstance(final_spec.get("ui"), dict) else {}
    runtime_template, mechanic_family, spatial_structure = choose_runtime_template(summary_data, final_spec)
    seed_contract = {
        "sourceSeed": final_document.get("sourceSeed") or summary_data.get("sourceFile"),
        "sourceSummary": final_document.get("sourceSummary"),
        "sourceSamples": summary_data.get("gameDesignDoc", {}).get("sourceSamples", {}),
    }
    failure_pressure = []
    for item in final_spec.get("enemyTypes", []):
        if isinstance(item, str) and item.strip():
            failure_pressure.append(item.strip())
    for item in encounter_design.get("hazards", []):
        if isinstance(item, str) and item.strip():
            failure_pressure.append(item.strip())
    progression_shape = []
    for key in ("metaGoal", "rewardHooks"):
        for item in progression.get(key, []):
            if isinstance(item, str) and item.strip():
                progression_shape.append(item.strip())
    if progression.get("runToRunGrowth"):
        progression_shape.append(str(progression["runToRunGrowth"]))
    presentation_rules = []
    for item in [world.get("setting"), world.get("visualDirection")]:
        if item:
            presentation_rules.append(str(item))
    for item in ui_spec.get("readabilityGoals", []):
        if isinstance(item, str) and item.strip():
            presentation_rules.append(item.strip())
    def preserve_unique(values: list[str], limit: int = 8) -> list[str]:
        result = []
        seen = set()
        for value in values:
            text = str(value).strip()
            key = text.lower()
            if not text or key in seen:
                continue
            seen.add(key)
            result.append(text)
            if len(result) >= limit:
                break
        return result

    return {
        "seedContract": seed_contract,
        "mechanicFamily": mechanic_family,
        "runtimeTemplate": runtime_template,
        "pacing": final_spec.get("sessionLength", "short readable arcade run"),
        "spatialStructure": spatial_structure,
        "failurePressure": preserve_unique(failure_pressure),
        "progressionShape": progression_shape[:8],
        "presentationRules": presentation_rules[:8],
        "mustPreserve": [
            "Preserve the randomized seed contract through every stage.",
            "Treat final-brainstorming.json as the canonical game specification.",
            "Keep the generated game self-contained in one Pages/<slug>/ folder.",
            "Make runtime behavior match runtimeTemplate instead of defaulting to one arena scaffold.",
        ],
        "fallbackSource": fallback_source,
    }


def build_implementation_chapters(technical_build: dict[str, object], player_actions: list[str], enemy_types: list[str], progression_goal: list[str]) -> list[str]:
    chapters: list[str] = []
    for value in technical_build.get("prototypeOrder", []):
        if isinstance(value, str) and value.strip():
            chapters.append(titleize_identifier(value))

    fallback_chapters = [
        f"{titleize_identifier(player_actions[0]) if player_actions else 'Core'} Controls",
        f"{titleize_identifier(enemy_types[0]) if enemy_types else 'Enemy'} Pressure",
        "Relic Reward Loop",
        f"{titleize_identifier(progression_goal[0]) if progression_goal else 'Progression'} Unlock Flow",
        "Presentation And Polish",
    ]
    for chapter in fallback_chapters:
        if chapter not in chapters:
            chapters.append(chapter)
    return chapters[:6]


def parse_keyed_lines(text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized_key = key.strip().lower()
        normalized_value = value.strip()
        if normalized_key and normalized_value:
            parsed[normalized_key] = normalized_value
    return parsed


def is_placeholder_or_truncated(text: str) -> bool:
    stripped = text.strip().strip('"')
    if not stripped:
        return True
    if stripped.lower() in {"title", "prompt", "injection", "decision", "reply"}:
        return True
    if len(stripped) < 12:
        return True
    if stripped.endswith((" and", " or", " but", " with", " to", " of", " the")):
        return True
    return False


def has_meta_generation_text(text: str) -> bool:
    lowered = text.lower()
    blocked_fragments = [
        "generate no output",
        "does not detect",
        "external dependencies",
        "self-contained",
        "prompt design focuses",
        "the system",
        "strict adherence",
        "required three lines",
        "compliance",
        "maintain strict consistency",
        "game development cycle",
    ]
    return any(fragment in lowered for fragment in blocked_fragments)


def category_lookup(summary_data: dict) -> dict[str, dict]:
    return {str(item.get("category")): item for item in summary_data.get("categories", [])}


def category_words(summary_data: dict, category_name: str) -> list[str]:
    category_entry = category_lookup(summary_data).get(category_name, {})
    words = []
    for key in ("smoothedWords", "sampledWords", "topWords"):
        value = category_entry.get(key, [])
        if isinstance(value, list):
            words.extend(str(item) for item in value)
    for row in category_entry.get("chainSummaries", []):
        if isinstance(row, dict):
            words.extend(str(item) for item in row.get("focusWords", []))
    return dedupe_words(words)


def build_summary_context(summary_data: dict) -> dict[str, object]:
    game_doc = summary_data.get("gameDesignDoc", {})
    return {
        "title": str(game_doc.get("title") or "Untitled Arcade Prototype"),
        "pitch": str(game_doc.get("elevatorPitch") or ""),
        "world": str(game_doc.get("worldConcept") or ""),
        "explorationLevel": str(summary_data.get("explorationLevel") or game_doc.get("explorationLevel") or "broad"),
        "environment": category_words(summary_data, "Environment Seeds"),
        "mechanics": category_words(summary_data, "Mechanic Seeds"),
        "enemies": category_words(summary_data, "Enemy Seeds"),
        "progression": category_words(summary_data, "Progression Seeds"),
    }


def choose_words_with_lm(label: str, pool: list[str], count: int, context: dict[str, object], model: str, endpoint: str, fallback_words: list[str], temperature: float) -> list[str]:
    prompt = textwrap.dedent(
        f"""
        title -> {context['title']}
        pitch -> {context['pitch']}
        world -> {context['world']}
        task -> choose {count} {label}
        pool -> {', '.join(pool[:24])}
        reply ->
        """
    ).strip()
    system_prompt = "Reply only with a short comma-separated list of exact words from the pool. No explanation."
    try:
        text = call_lm_studio(prompt, model=model, endpoint=endpoint, system_prompt=system_prompt, max_tokens=40, temperature=temperature)
        return parse_csv_words(text, pool, count, fallback_words)
    except Exception:
        return parse_csv_words(", ".join(fallback_words), pool, count, fallback_words)


def choose_gameplay_time_with_lm(context: dict[str, object], model: str, endpoint: str, fallback_minutes: int, temperature: float) -> str:
    prompt = textwrap.dedent(
        f"""
        title -> {context['title']}
        pitch -> {context['pitch']}
        exploration -> {context['explorationLevel']}
        choices -> 8 minutes, 10 minutes, 12 minutes, 15 minutes, 18 minutes
        task -> choose one gameplay session length for an arcade run
        reply ->
        """
    ).strip()
    system_prompt = "Reply with one choice only in the format '<number> minutes'. No explanation."
    try:
        text = call_lm_studio(prompt, model=model, endpoint=endpoint, system_prompt=system_prompt, max_tokens=12, temperature=temperature)
        return parse_minutes(text, fallback_minutes)
    except Exception:
        return f"{fallback_minutes} minutes"


def build_step_answers(summary_data: dict, rng: random.Random, model: str, endpoint: str, temperature: float) -> list[dict[str, object]]:
    context = build_summary_context(summary_data)
    fallback_minutes = rng.choice([8, 10, 12, 15, 18] if context["explorationLevel"] != "focused" else [8, 10, 12])
    enemy_fallback = pick_words(context["enemies"], 3, rng) or ["sentry", "swarm", "warden"]
    action_fallback = pick_words(context["mechanics"], 3, rng) or ["dash", "blink", "carry"]
    progression_fallback = pick_words(context["progression"], 2, rng) or ["unlock", "reveal"]
    world_fallback = pick_words(context["environment"], 2, rng) or ["harbor", "pier"]

    gameplay_time = choose_gameplay_time_with_lm(context, model=model, endpoint=endpoint, fallback_minutes=fallback_minutes, temperature=temperature)
    enemy_types = choose_words_with_lm("enemy types", context["enemies"], 3, context, model=model, endpoint=endpoint, fallback_words=enemy_fallback, temperature=temperature)
    verbs = choose_words_with_lm("player actions", context["mechanics"], 3, context, model=model, endpoint=endpoint, fallback_words=action_fallback, temperature=temperature)
    objective_words = choose_words_with_lm("progression goals", context["progression"], 2, context, model=model, endpoint=endpoint, fallback_words=progression_fallback, temperature=temperature)
    world_anchor = choose_words_with_lm("world anchors", context["environment"], 2, context, model=model, endpoint=endpoint, fallback_words=world_fallback, temperature=temperature)

    return [
        {
            "step": "gameplay_time",
            "question": "How long should one run last before it feels complete?",
            "answer": gameplay_time,
            "impact": "Sets encounter density, map size, and upgrade pacing.",
        },
        {
            "step": "enemy_types",
            "question": "Which enemy types define the core pressure of the run?",
            "answer": enemy_types,
            "impact": "Shapes encounter design, telegraphing, and fail-state tension.",
        },
        {
            "step": "player_actions",
            "question": "Which verbs should the player use constantly?",
            "answer": verbs,
            "impact": "Locks the feel of traversal, combat rhythm, and input complexity.",
        },
        {
            "step": "progression_goal",
            "question": "What long-term objective should each run feed into?",
            "answer": objective_words,
            "impact": "Determines meta progression rewards and run-to-run continuity.",
        },
        {
            "step": "world_anchor",
            "question": "Which environmental anchors keep the world readable and memorable?",
            "answer": world_anchor,
            "impact": "Guides art direction, hazard framing, and level landmarks.",
        },
    ]


def build_random_injections(summary_data: dict, rng: random.Random, model: str, endpoint: str, temperature: float) -> list[dict[str, object]]:
    context = build_summary_context(summary_data)
    return [
        {
            "type": "environmental_twist",
            "value": choose_words_with_lm("environmental twist words", context["environment"], 2, context, model=model, endpoint=endpoint, fallback_words=pick_words(context["environment"], 2, rng), temperature=temperature),
            "effect": "Adds a new traversal hazard or alternate route condition.",
        },
        {
            "type": "mechanic_modifier",
            "value": choose_words_with_lm("mechanic modifier words", context["mechanics"], 2, context, model=model, endpoint=endpoint, fallback_words=pick_words(context["mechanics"], 2, rng), temperature=temperature),
            "effect": "Mutates the core verb set for a late-run variant or upgrade branch.",
        },
        {
            "type": "enemy_pressure",
            "value": choose_words_with_lm("enemy pressure words", context["enemies"], 2, context, model=model, endpoint=endpoint, fallback_words=pick_words(context["enemies"], 2, rng), temperature=temperature),
            "effect": "Introduces a new pressure pattern or elite enemy combination.",
        },
        {
            "type": "progression_bonus",
            "value": choose_words_with_lm("progression bonus words", context["progression"], 2, context, model=model, endpoint=endpoint, fallback_words=pick_words(context["progression"], 2, rng), temperature=temperature),
            "effect": "Creates a reward spike that changes long-term routing decisions.",
        },
    ]


def build_exploration_loop_with_lm(context: dict[str, object], env: str, mech: str, enemy: str, prog: str, model: str, endpoint: str, temperature: float) -> dict[str, str]:
    prompt = textwrap.dedent(
        f"""
        title -> {context['title']}
        pitch -> {context['pitch']}
        environment -> {env}
        mechanic -> {mech}
        enemy -> {enemy}
        progression -> {prog}
        format ->
        prompt: ...
        injection: ...
        decision: ...
        reply ->
        """
    ).strip()
    system_prompt = "Reply with exactly three keyed lines: prompt:, injection:, decision:. Keep each line short and concrete."
    fallback = {
        "prompt": f"What happens if {env} traversal meets {mech} play under {enemy} pressure?",
        "injection": f"Resolve the loop by rewarding {prog} instead of raw score.",
        "decision": f"Keep {mech} as a repeatable skill test, escalate with {enemy}, and use {prog} as the reason to push deeper.",
    }
    anchors = [normalize_word(env), normalize_word(mech), normalize_word(enemy), normalize_word(prog)]
    try:
        text = call_lm_studio(prompt, model=model, endpoint=endpoint, system_prompt=system_prompt, max_tokens=120, temperature=temperature)
        parsed = parse_keyed_lines(text)
        prompt_text = parsed.get("prompt", "")
        injection_text = parsed.get("injection", "")
        decision_text = parsed.get("decision", "")
        combined_text = " ".join([prompt_text, injection_text, decision_text]).lower()
        anchor_hits = sum(1 for anchor in anchors if anchor and anchor in combined_text)
        if not any(is_placeholder_or_truncated(value) or has_meta_generation_text(value) for value in (prompt_text, injection_text, decision_text)) and anchor_hits >= 2:
            return {"prompt": prompt_text, "injection": injection_text, "decision": decision_text}
    except Exception:
        pass
    return fallback


def build_exploration_loops(summary_data: dict, rng: random.Random, loop_count: int, model: str, endpoint: str, temperature: float) -> list[dict[str, object]]:
    context = build_summary_context(summary_data)
    loops = []
    for index in range(1, loop_count + 1):
        env = pick_words(context["environment"], 1, rng) or ["harbor"]
        mech = pick_words(context["mechanics"], 1, rng) or ["dash"]
        enemy = pick_words(context["enemies"], 1, rng) or ["sentry"]
        prog = pick_words(context["progression"], 1, rng) or ["unlock"]
        loop_fields = build_exploration_loop_with_lm(context, env[0], mech[0], enemy[0], prog[0], model=model, endpoint=endpoint, temperature=temperature)
        loops.append(
            {
                "loop": index,
                "prompt": loop_fields["prompt"],
                "injection": loop_fields["injection"],
                "decision": loop_fields["decision"],
            }
        )
    return loops


def build_spec_text_with_lm(context: dict[str, object], primary_environment: str, secondary_environment: str, primary_enemy: str, primary_action: str, secondary_action: str, progression_anchor: str, model: str, endpoint: str, temperature: float) -> dict[str, str]:
    prompt = textwrap.dedent(
        f"""
        title -> {context['title']}
        pitch -> {context['pitch']}
        world -> {context['world']}
        environment -> {primary_environment}, {secondary_environment}
        actions -> {primary_action}, {secondary_action}
        enemy -> {primary_enemy}
        progression -> {progression_anchor}
        format ->
        title: ...
        oneLinePitch: ...
        playerFantasy: ...
        worldSetting: ...
        visualDirection: ...
        coreLoop1: ...
        coreLoop2: ...
        coreLoop3: ...
        difficultyRamp: ...
        riskReward: ...
        reply ->
        """
    ).strip()
    system_prompt = "Reply with exactly the requested keyed lines only. No markdown. Keep each value concise."
    try:
        text = call_lm_studio(prompt, model=model, endpoint=endpoint, system_prompt=system_prompt, max_tokens=360, temperature=temperature)
        return parse_keyed_lines(text)
    except Exception:
        return {}


def fallback_core_loop(game_doc: dict, primary_environment: str, primary_enemy: str, primary_action: str, secondary_action: str, progression_anchor: str) -> list[str]:
    existing = game_doc.get("coreLoop", [])
    fallback = [
        f"Scout {primary_environment} routes and read {primary_enemy} pressure.",
        f"Use {primary_action} and {secondary_action} to survive and secure objectives.",
        f"Turn each run into {progression_anchor} growth that unlocks the next challenge band.",
    ]
    merged = []
    for index in range(3):
        if index < len(existing) and isinstance(existing[index], str) and existing[index].strip():
            merged.append(existing[index].strip())
        else:
            merged.append(fallback[index])
    return merged


def build_final_spec(summary_data: dict, source_summary_path: Path, step_answers: list[dict[str, object]], random_injections: list[dict[str, object]], exploration_loops: list[dict[str, object]], model: str, endpoint: str, temperature: float) -> dict[str, object]:
    game_doc = summary_data.get("gameDesignDoc", {})
    context = build_summary_context(summary_data)
    source_samples = game_doc.get("sourceSamples", {})
    environment_words = [normalize_word(word) for word in source_samples.get("environment", []) if normalize_word(word)] or category_words(summary_data, "Environment Seeds")
    mechanic_words = [normalize_word(word) for word in source_samples.get("mechanics", []) if normalize_word(word)] or category_words(summary_data, "Mechanic Seeds")
    enemy_words = [normalize_word(word) for word in source_samples.get("enemies", []) if normalize_word(word)] or category_words(summary_data, "Enemy Seeds")
    progression_words = [normalize_word(word) for word in source_samples.get("progression", []) if normalize_word(word)] or category_words(summary_data, "Progression Seeds")

    gameplay_time = next((item["answer"] for item in step_answers if item["step"] == "gameplay_time"), "12 minutes")
    enemy_types = next((item["answer"] for item in step_answers if item["step"] == "enemy_types"), enemy_words[:3])
    player_actions = next((item["answer"] for item in step_answers if item["step"] == "player_actions"), mechanic_words[:3])
    progression_goal = next((item["answer"] for item in step_answers if item["step"] == "progression_goal"), progression_words[:2])

    primary_environment = environment_words[0] if environment_words else "harbor"
    secondary_environment = environment_words[1] if len(environment_words) > 1 else primary_environment
    primary_enemy = enemy_types[0] if isinstance(enemy_types, list) and enemy_types else "sentry"
    primary_action = player_actions[0] if isinstance(player_actions, list) and player_actions else "dash"
    secondary_action = player_actions[1] if isinstance(player_actions, list) and len(player_actions) > 1 else primary_action
    progression_anchor = progression_goal[0] if isinstance(progression_goal, list) and progression_goal else "unlock"
    spec_text = build_spec_text_with_lm(
        context,
        primary_environment,
        secondary_environment,
        primary_enemy,
        primary_action,
        secondary_action,
        progression_anchor,
        model=model,
        endpoint=endpoint,
        temperature=temperature,
    )
    core_loop = fallback_core_loop(game_doc, primary_environment, primary_enemy, primary_action, secondary_action, progression_anchor)
    one_line_pitch = spec_text.get("onelinepitch")
    player_fantasy = spec_text.get("playerfantasy")
    world_setting = spec_text.get("worldsetting")
    visual_direction = spec_text.get("visualdirection")
    difficulty_ramp = spec_text.get("difficultyramp")
    risk_reward = spec_text.get("riskreward")

    if is_placeholder_or_truncated(one_line_pitch or ""):
        one_line_pitch = None
    if is_placeholder_or_truncated(player_fantasy or ""):
        player_fantasy = None
    if is_placeholder_or_truncated(world_setting or ""):
        world_setting = None
    if is_placeholder_or_truncated(visual_direction or ""):
        visual_direction = None
    if is_placeholder_or_truncated(difficulty_ramp or ""):
        difficulty_ramp = None
    if is_placeholder_or_truncated(risk_reward or ""):
        risk_reward = None

    canonical_title = spec_text.get("title") or str(game_doc.get("title") or f"{primary_environment.capitalize()} {primary_action.capitalize()}")
    canonical_description = one_line_pitch or (
        f"Navigate {primary_environment} and {secondary_environment} spaces with {primary_action} and {secondary_action}, "
        f"survive {primary_enemy}-led pressure, and turn each run into {progression_anchor} progress."
    )
    objective_text = build_objective_text(
        player_actions if isinstance(player_actions, list) else [str(player_actions)],
        enemy_types if isinstance(enemy_types, list) else [str(enemy_types)],
        progression_goal if isinstance(progression_goal, list) else [str(progression_goal)],
    )
    technical_build = {
        "scope": "Small browser-playable prototype",
        "systemsNeeded": ["player controller", "enemy director", "upgrade loop", "hazard routing", "HUD"],
        "prototypeOrder": ["movement", "one enemy archetype", "one route hazard", "reward loop", "full run pacing"],
    }
    core_loop_lines = [
        spec_text.get("coreloop1") or core_loop[0],
        spec_text.get("coreloop2") or core_loop[1],
        spec_text.get("coreloop3") or core_loop[2],
    ]
    implementation_chapters = build_implementation_chapters(
        technical_build,
        player_actions if isinstance(player_actions, list) else [str(player_actions)],
        enemy_types if isinstance(enemy_types, list) else [str(enemy_types)],
        progression_goal if isinstance(progression_goal, list) else [str(progression_goal)],
    )
    feature_roots = [
        titleize_identifier(value)
        for value in (technical_build.get("prototypeOrder", [])[:3] or technical_build.get("systemsNeeded", [])[:3] or player_actions[:3])
    ]

    return {
        "title": canonical_title,
        "sourceSummary": str(source_summary_path),
        "sourceSeed": summary_data.get("sourceFile"),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "explorationLevel": summary_data.get("explorationLevel", "broad"),
        "generation": {
            "mode": "lm_studio_chainstorm_style",
            "endpoint": endpoint,
            "model": model,
            "temperature": temperature,
        },
        "buildReady": True,
        "injectionReady": True,
        "oneLinePitch": canonical_description,
        "pageIdentity": {
            "title": canonical_title,
            "slug": slugify_title(canonical_title),
            "description": canonical_description,
            "objective": objective_text,
            "overlayBriefing": "\n\n".join([canonical_description, *core_loop_lines]),
            "hudObjective": objective_text,
        },
        "buildPacket": {
            "featureRoots": feature_roots,
            "implementationChapters": implementation_chapters,
            "overlay": {
                "introTitle": canonical_title,
                "introBody": canonical_description,
                "introBriefing": "\n\n".join([canonical_description, *core_loop_lines]),
                "startHint": "Press Enter to deploy. Use WASD or Arrow keys to move, Shift to dash, and Space to pulse.",
                "winTitle": "Route Cleared",
                "winBody": "The exit gate is live and the relic chain is stable. Press R to run it again.",
                "lossTitle": "Route Interrupted",
                "lossBody": "The route collapsed under pressure. Press R to run it again.",
            },
            "hud": {
                "objective": objective_text,
                "status": canonical_description,
                "fields": ["objective", "status", "telemetry"],
            },
            "sceneAnchors": {
                "playerActions": player_actions,
                "enemyTypes": enemy_types,
                "hazards": environment_words[:4],
                "progression": progression_goal,
            },
        },
        "steps": step_answers,
        "randomInjections": random_injections,
        "explorationLoops": exploration_loops,
        "finalSpec": {
            "sessionLength": gameplay_time,
            "genre": "arcade action prototype",
            "playerFantasy": player_fantasy or game_doc.get("designDoc", {}).get("playerFantasy") or f"Master {primary_action} movement in a hostile {primary_environment} frontier.",
            "world": {
                "setting": world_setting or f"A stylized world blending {primary_environment}, {secondary_environment}, and shifting threat territory.",
                "visualDirection": visual_direction or game_doc.get("designDoc", {}).get("visualDirection") or f"High-contrast silhouettes shaped by {primary_environment}, {secondary_environment}, and {primary_enemy} motifs.",
                "landmarks": environment_words[:5],
            },
            "coreLoop": core_loop_lines,
            "playerActions": player_actions,
            "enemyTypes": enemy_types,
            "enemyArchetypes": [
                {
                    "name": enemy,
                    "role": role,
                    "behavior": behavior,
                }
                for enemy, role, behavior in zip(
                    enemy_types if isinstance(enemy_types, list) else [primary_enemy],
                    ["pressure chaser", "zone controller", "ambush disruptor"],
                    [
                        "Pushes the player off safe routes and punishes hesitation.",
                        "Locks down key spaces and forces rerouting.",
                        "Breaks steady rhythm and spikes reaction difficulty.",
                    ],
                )
            ],
            "progression": {
                "metaGoal": progression_goal,
                "rewardHooks": progression_words[:4],
                "runToRunGrowth": f"Each run converts performance into {', '.join(progression_goal if isinstance(progression_goal, list) else [str(progression_goal)])} upgrades and route unlocks.",
            },
            "runStructure": {
                "opening": f"Teach {primary_action} movement and introduce {primary_enemy} reads in a low-risk {primary_environment} route.",
                "midgame": f"Layer {secondary_action} interactions, mixed enemy waves, and injection events from the exploration loops.",
                "endgame": f"Force mastery through stacked hazards, elite {primary_enemy} encounters, and a final {progression_anchor} choice.",
            },
            "encounterDesign": {
                "hazards": environment_words[:4],
                "enemyCompositions": [loop["decision"] for loop in exploration_loops[:3]],
                "difficultyRamp": difficulty_ramp or "Ramp through route compression, enemy overlap, and stronger reward bait rather than pure health inflation.",
            },
            "economy": {
                "currencies": progression_words[:3],
                "spenders": [injection["type"] for injection in random_injections],
                "riskReward": risk_reward or "Offer stronger progression currency on routes with denser threat overlap and harder extraction paths.",
            },
            "ui": {
                "hud": ["health", "charge meter", "route objective", "reward tracker"],
                "readabilityGoals": ["fast threat reads", "clear route ownership", "strong reward telegraphing"],
            },
            "audio": {
                "tone": "Punchy arcade percussion with environmental accents tied to route danger.",
                "feedback": ["impact stingers", "threat warning pings", "upgrade reward swells"],
            },
            "technicalBuild": technical_build,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ArcadeBrainstorm-CLI: ingest summary_brainstorming.json and compile final_brainstorming.json using LM Studio."
    )
    parser.add_argument("--file", type=str, default=str(DEFAULT_INPUT), help="Path to summary_brainstorming.json.")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="Path to write final_brainstorming.json.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="LM Studio model id to use for finalization.")
    parser.add_argument("--endpoint", type=str, default=DEFAULT_ENDPOINT, help="LM Studio chat completions endpoint.")
    parser.add_argument("--temperature", type=float, default=1.0, help="Sampling temperature for finalization prompts.")
    parser.add_argument("--random-seed", type=int, default=DEFAULT_RANDOM_SEED, help="Random seed for injections and exploration loops.")
    parser.add_argument("--exploration-loops", type=int, default=DEFAULT_EXPLORATION_LOOPS, help="Number of random exploration loops to run before finalizing the spec.")
    parser.add_argument("--brainstorm-mode", choices=("auto", "required", "skip"), default="auto", help="Use LM Studio additively, require it, or skip it and use deterministic fallbacks.")
    parser.add_argument("--lm-health-timeout", type=int, default=3, help="Seconds to spend on the one-shot LM Studio availability check.")
    parser.add_argument("--raw", action="store_true", help="Print only the output file path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source_path = Path(args.file).expanduser().resolve()
        output_path = Path(args.output).expanduser().resolve()
        summary_data = load_json(source_path)
        if not is_valid_summary_shape(summary_data):
            raise RuntimeError("summary_brainstorming.json does not have the required summary shape.")

        fallback_source = ""
        if args.brainstorm_mode == "skip":
            fallback_source = "brainstorm-mode skip; LM Studio additive generation was not attempted."
            set_lm_studio_availability(False, fallback_source)
        else:
            available, reason = probe_lm_studio(args.endpoint, args.model, timeout_seconds=max(1, args.lm_health_timeout))
            if not available and args.brainstorm_mode == "required":
                raise RuntimeError(f"LM Studio is required but unavailable: {reason}")
            if not available:
                fallback_source = f"LM Studio unavailable during auto preflight: {reason}; deterministic fallback generation was used."
                set_lm_studio_availability(False, fallback_source)
                if not args.raw:
                    print(fallback_source, file=sys.stderr)
            else:
                set_lm_studio_availability(True)

        rng = random.Random(args.random_seed)
        step_answers = build_step_answers(summary_data, rng, model=args.model, endpoint=args.endpoint, temperature=args.temperature)
        random_injections = build_random_injections(summary_data, rng, model=args.model, endpoint=args.endpoint, temperature=args.temperature)
        exploration_loops = build_exploration_loops(summary_data, rng, max(1, args.exploration_loops), model=args.model, endpoint=args.endpoint, temperature=args.temperature)
        final_document = build_final_spec(summary_data, source_path, step_answers, random_injections, exploration_loops, model=args.model, endpoint=args.endpoint, temperature=args.temperature)
        final_document["fallbackSource"] = fallback_source
        final_document["gameDesignProfile"] = build_game_design_profile(summary_data, final_document, fallback_source)
        save_json(output_path, final_document)
        result = str(output_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.raw:
        print(result)
        return 0

    print("\nArcadeBrainstorm-CLI output:\n")
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
