from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CLI_ROOT = Path(__file__).resolve().parent
PORTFOLIO_APP = CLI_ROOT.parent
ROOT = PORTFOLIO_APP.parent
SCHEMAS_DIR = CLI_ROOT / "schemas"
TEMPLATES_DIR = CLI_ROOT / "templates"
PORTFOLIO_DATA = PORTFOLIO_APP / "src" / "data" / "portfolio" / "projects.js"
PORTFOLIO_PAGES = PORTFOLIO_APP / "src" / "data" / "portfolio" / "pages.js"
PAGES_DIR = PORTFOLIO_APP / "Pages"
GAMES_DIR = PAGES_DIR / "games"
ARCADE_ASSETS = PAGES_DIR / "arcade-assets.json"
ORCHESTRATOR_MEMORY_PATH = CLI_ROOT / "arcade_orchestrator_memory.md"
ORCHESTRATOR_SYSTEM_PROMPT_PATH = CLI_ROOT / "arcade_orchestrator_system_prompt.md"

MODE_ORDER = [
    "runner",
    "orbit",
    "pulseGrid",
    "labRift",
    "phaseDrop",
    "harbor",
    "rhythm",
    "echo",
]

MODE_LABELS = {
    "runner": "Endless lane pressure and hazard dodging.",
    "orbit": "Pointer-led popping and target chaining.",
    "pulseGrid": "Beat matching on a reactive grid.",
    "labRift": "Room navigation with pickups and escape.",
    "phaseDrop": "Lane survival with timed phase logic.",
    "harbor": "Cursor steering through drifting collection.",
    "rhythm": "Timing notes against a marker line.",
    "echo": "Pattern memory and input replay.",
}

STAGE_SETTINGS = {
    "idea": {"reasoning": "high", "temperature": 1.0},
    "shape": {"reasoning": "high", "temperature": 0.7},
    "brainstorm": {"reasoning": "high", "temperature": 0.95},
    "expand": {"reasoning": "high", "temperature": 0.8},
    "theme-pack": {"reasoning": "high", "temperature": 0.65},
    "content-plan": {"reasoning": "high", "temperature": 0.55},
    "feature-plan": {"reasoning": "high", "temperature": 0.5},
    "hierarchy-seed": {"reasoning": "high", "temperature": 0.9},
    "hierarchy-expand": {"reasoning": "high", "temperature": 0.85},
    "hierarchy-rank": {"reasoning": "high", "temperature": 0.35},
    "mode-pick": {"reasoning": "high", "temperature": 0.4},
    "json-fill": {"reasoning": "xhigh", "temperature": 0.2},
    "repair-loop": {"reasoning": "xhigh", "temperature": 0.1},
}


@dataclass
class IdeaBrief:
    idea: str = ""
    options: list[str] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)
    brainstorms: list[str] = field(default_factory=list)
    expansions: list[str] = field(default_factory=list)
    theme_pack: dict[str, Any] = field(default_factory=dict)
    content_plan: dict[str, Any] = field(default_factory=dict)
    feature_plan: dict[str, Any] = field(default_factory=dict)
    hierarchy_layers: list[list[str]] = field(default_factory=list)
    hierarchy_survivors: list[str] = field(default_factory=list)
    chosen_section: str | None = None
    chosen_mode: str | None = None
    game_json: dict[str, Any] | None = None


def main() -> None:
    ensure_cli_support_files()
    print("Portfolio Vite CLI")
    print(
        "Type `idea`, `shape`, `brainstorm`, `expand`, `theme-pack`, `content-plan`, `feature-plan`, `hierarchy`, `mode-pick`, `json-fill`, `build`, `validate`, `status`, `help`, or `quit`."
    )

    brief = IdeaBrief()
    while True:
        try:
            line = input("portfolio> ").strip()
        except EOFError:
            print()
            return

        if not line:
            continue

        command, _, tail = line.partition(" ")
        command = command.lower()
        tail = tail.strip()

        if command in {"quit", "exit"}:
            return
        if command == "help":
            print_help()
            continue
        if command == "status":
            print_status(brief)
            continue
        if command == "idea":
            brief = start_idea(tail or brief.idea, brief)
            continue
        if command == "shape":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = shape_idea(brief, tail)
            continue
        if command == "brainstorm":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = brainstorm_idea(brief, tail)
            continue
        if command == "expand":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = expand_idea(brief, tail)
            continue
        if command == "theme-pack":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = build_theme_pack(brief, tail)
            continue
        if command == "content-plan":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = build_content_plan(brief, tail)
            continue
        if command == "feature-plan":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = build_feature_plan(brief, tail)
            continue
        if command == "hierarchy":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = run_hierarchy(brief, tail)
            continue
        if command == "mode-pick":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = prepare_design_stages(brief)
            brief = pick_mode(brief, tail)
            continue
        if command == "json-fill":
            if not brief.idea:
                print("Set an idea first.")
                continue
            brief = fill_game_json(brief, tail)
            continue
        if command == "validate":
            if not brief.game_json:
                print("Generate the game JSON first.")
                continue
            validate_game_json(brief.game_json)
            print("JSON validation passed.")
            continue
        if command == "build":
            if tail and not brief.idea:
                brief = start_idea(tail, brief)
            built = build_game(brief)
            brief.game_json = built
            print(f"Built arcade game: {built['slug']}")
            continue

        brief = start_idea(line, brief)


def print_help() -> None:
    print("Commands:")
    print("  idea       - set or refine the current game idea")
    print("  shape      - expand the idea into options and sections")
    print("  brainstorm - generate distinct game directions")
    print("  expand     - expand promising directions into design sheets")
    print("  theme-pack - generate vibe, palette, and presentation notes")
    print("  content-plan - define content objects and usage")
    print("  feature-plan - define gameplay features before JSON")
    print("  hierarchy  - run layered 5-way ideation, ranking, and survivor selection")
    print("  mode-pick  - choose the runtime mode for the game")
    print("  json-fill  - generate schema-bound game JSON")
    print("  build      - write the game JSON, thin shell, and portfolio entry")
    print("  validate   - validate the current game JSON")
    print("  status     - show the current staged state")
    print("  quit       - exit")


def print_status(brief: IdeaBrief) -> None:
    print(f"Idea: {brief.idea or '(none)'}")
    print(f"Options: {len(brief.options)}")
    print(f"Sections: {', '.join(brief.sections) if brief.sections else '(none)'}")
    print(f"Brainstorms: {len(brief.brainstorms)}")
    print(f"Expansions: {len(brief.expansions)}")
    print(f"Theme pack: {'yes' if brief.theme_pack else 'no'}")
    print(f"Content plan: {'yes' if brief.content_plan else 'no'}")
    print(f"Feature plan: {'yes' if brief.feature_plan else 'no'}")
    print(f"Hierarchy layers: {len(brief.hierarchy_layers)}")
    print(f"Hierarchy survivors: {len(brief.hierarchy_survivors)}")
    print(f"Chosen section: {brief.chosen_section or '(none)'}")
    print(f"Chosen mode: {brief.chosen_mode or '(none)'}")
    print(f"JSON ready: {'yes' if brief.game_json else 'no'}")


def start_idea(idea: str, brief: IdeaBrief) -> IdeaBrief:
    if not idea:
        print("Set an idea first.")
        return brief
    brief.idea = idea
    brief.options = []
    brief.sections = []
    brief.brainstorms = []
    brief.expansions = []
    brief.theme_pack = {}
    brief.content_plan = {}
    brief.feature_plan = {}
    brief.hierarchy_layers = []
    brief.hierarchy_survivors = []
    brief.chosen_section = None
    brief.chosen_mode = None
    brief.game_json = None
    print(f"Idea set: {brief.idea}")
    print("Say `shape` when ready.")
    return brief


def shape_idea(brief: IdeaBrief, extra: str) -> IdeaBrief:
    prompt = (
        "Expand this arcade game idea into a list first, then converge by detail section.\n"
        f"Idea: {brief.idea}\n"
        f"Optional note: {extra or '(none)'}\n"
        "Return plain text with two blocks:\n"
        "OPTIONS:\n"
        "- four short game directions\n"
        "SECTIONS:\n"
        "- core loop\n"
        "- controls\n"
        "- visual style\n"
        "- state and feedback\n"
        "- failure and retry\n"
        "Keep it concrete and greyboxed."
    )
    output = run_copilot_stage("shape", prompt)
    brief.options = extract_list_items(output, "OPTIONS") or [
        "Pressure runner loop",
        "Pointer chain loop",
        "Rhythm feedback loop",
        "Room escape loop",
    ]
    brief.sections = extract_list_items(output, "SECTIONS") or [
        "core loop",
        "controls",
        "visual style",
        "state and feedback",
        "failure and retry",
    ]
    print("Options:")
    for item in brief.options:
        print(f"- {item}")
    print("Sections:")
    for item in brief.sections:
        print(f"- {item}")
    return brief


def brainstorm_idea(brief: IdeaBrief, extra: str) -> IdeaBrief:
    prompt = (
        "Brainstorm 6 distinct greyboxed arcade game directions from this idea.\n"
        f"Idea: {brief.idea}\n"
        f"Existing options: {', '.join(brief.options) or '(none)'}\n"
        f"Note: {extra or '(none)'}\n"
        "Vary mechanic, camera feel, pacing, content use, theme, and vibe.\n"
        "Return:\n"
        "BRAINSTORMS:\n"
        "- one short line per direction"
    )
    output = run_copilot_stage("brainstorm", prompt)
    brief.brainstorms = extract_list_items(output, "BRAINSTORMS") or [
        "Neon lane dodger with phase swaps",
        "Harbor rhythm route with drifting beats",
        "Top-down shard sweep under pressure",
        "Orbit chain pop with combo decay",
        "Memory pads in a fake 3D chamber",
        "Sandstorm survival with lane pulses",
    ]
    print("Brainstorms:")
    for item in brief.brainstorms:
        print(f"- {item}")
    return brief


def expand_idea(brief: IdeaBrief, extra: str) -> IdeaBrief:
    if not brief.brainstorms:
        brief = brainstorm_idea(brief, "")
    prompt = (
        "Expand the best 3 brainstorm directions into compact design sheets.\n"
        f"Idea: {brief.idea}\n"
        f"Brainstorms: {', '.join(brief.brainstorms) or '(none)'}\n"
        f"Note: {extra or '(none)'}\n"
        "Each expansion should include core loop, controls, pacing, failure, replay value, and presentation.\n"
        "Return:\n"
        "EXPANSIONS:\n"
        "- one line per expanded direction"
    )
    output = run_copilot_stage("expand", prompt)
    brief.expansions = extract_list_items(output, "EXPANSIONS") or brief.brainstorms[:3]
    print("Expansions:")
    for item in brief.expansions:
        print(f"- {item}")
    return brief


def build_theme_pack(brief: IdeaBrief, extra: str) -> IdeaBrief:
    if not brief.expansions:
        brief = expand_idea(brief, "")
    prompt = (
        "Create a theme pack for this greyboxed arcade game.\n"
        f"Idea: {brief.idea}\n"
        f"Expansions: {', '.join(brief.expansions) or '(none)'}\n"
        f"Note: {extra or '(none)'}\n"
        "Return compact JSON with keys: vibeWords, paletteDirection, surfaceStyle, cameraStyle, spaceType, depthCues, glowLevel, hudTone."
    )
    output = run_copilot_stage("theme-pack", prompt)
    brief.theme_pack = parse_json_or_default(
        output,
        {
            "vibeWords": ["neon", "greybox", "arcade"],
            "paletteDirection": "pulse",
            "surfaceStyle": "flat colored surfaces",
            "cameraStyle": "locked gameplay framing",
            "spaceType": "2.5d",
            "depthCues": "layered glow and spacing",
            "glowLevel": "medium",
            "hudTone": "minimal operator readout",
        },
    )
    print(f"Theme: {brief.theme_pack.get('paletteDirection', '(none)')}")
    return brief


def build_content_plan(brief: IdeaBrief, extra: str) -> IdeaBrief:
    if not brief.theme_pack:
        brief = build_theme_pack(brief, "")
    prompt = (
        "Create a content plan for this arcade game.\n"
        f"Idea: {brief.idea}\n"
        f"Theme pack: {json.dumps(brief.theme_pack)}\n"
        f"Note: {extra or '(none)'}\n"
        "Return compact JSON with keys: contentObjects, usagePattern, challengeFlow, interactionDensity, presentationHooks."
    )
    output = run_copilot_stage("content-plan", prompt)
    brief.content_plan = parse_json_or_default(
        output,
        {
            "contentObjects": ["hazards", "pickups", "targets"],
            "usagePattern": "reused in short repeating waves",
            "challengeFlow": "intro, pressure ramp, dense finish",
            "interactionDensity": "medium",
            "presentationHooks": ["glow lanes", "colored pads", "greyboxed props"],
        },
    )
    print(f"Content: {', '.join(brief.content_plan.get('contentObjects', []))}")
    return brief


def build_feature_plan(brief: IdeaBrief, extra: str) -> IdeaBrief:
    if not brief.content_plan:
        brief = build_content_plan(brief, "")
    prompt = (
        "Create a feature plan for this arcade game before JSON filling.\n"
        f"Idea: {brief.idea}\n"
        f"Theme pack: {json.dumps(brief.theme_pack)}\n"
        f"Content plan: {json.dumps(brief.content_plan)}\n"
        f"Note: {extra or '(none)'}\n"
        "Return compact JSON with keys: coreMechanic, supportMechanics, failState, replayHook, controlStyle."
    )
    output = run_copilot_stage("feature-plan", prompt)
    brief.feature_plan = parse_json_or_default(
        output,
        {
            "coreMechanic": "dodge and route",
            "supportMechanics": ["timed swap", "pickup pressure"],
            "failState": "collision or mistimed move",
            "replayHook": "score chase and pattern variety",
            "controlStyle": "simple styled keyboard or pointer input",
        },
    )
    print(f"Feature: {brief.feature_plan.get('coreMechanic', '(none)')}")
    return brief


def run_hierarchy(brief: IdeaBrief, tail: str) -> IdeaBrief:
    layers = parse_layer_count(tail)
    seeds = hierarchy_seed_ideas(brief.idea)
    all_layers = [seeds]
    current = seeds
    for _ in range(1, layers):
        expanded = []
        for idea in current:
            expanded.extend(hierarchy_expand_idea(brief.idea, idea))
        current = dedupe_keep_order(expanded)
        all_layers.append(current)
    survivors = hierarchy_reduce(current)
    brief.hierarchy_layers = all_layers
    brief.hierarchy_survivors = survivors
    if survivors:
        brief.idea = survivors[0]
        brief.options = []
        brief.sections = []
        brief.brainstorms = []
        brief.expansions = []
        brief.theme_pack = {}
        brief.content_plan = {}
        brief.feature_plan = {}
        brief.chosen_section = None
        brief.chosen_mode = None
        brief.game_json = None
    print("Hierarchy survivors:")
    for item in brief.hierarchy_survivors:
        print(f"- {item}")
    if brief.hierarchy_survivors:
        print(f"Selected build idea: {brief.hierarchy_survivors[0]}")
    return brief


def parse_layer_count(tail: str) -> int:
    match = re.search(r"\d+", tail)
    if not match:
        return 2
    return max(1, min(4, int(match.group(0))))


def hierarchy_seed_ideas(root_idea: str) -> list[str]:
    prompt = (
        "Generate exactly 5 distinct arcade game ideas from this root goal.\n"
        f"Root idea: {root_idea}\n"
        "Return:\n"
        "IDEAS:\n"
        "- five idea lines only"
    )
    output = run_copilot_stage("hierarchy-seed", prompt)
    ideas = extract_list_items(output, "IDEAS")
    return normalize_to_five(ideas, [
        f"{root_idea} neon pressure",
        f"{root_idea} salvage loop",
        f"{root_idea} rhythm route",
        f"{root_idea} memory chamber",
        f"{root_idea} survival pulse",
    ])


def hierarchy_expand_idea(root_idea: str, parent_idea: str) -> list[str]:
    prompt = (
        "Generate exactly 5 child game ideas from this parent idea.\n"
        f"Root idea: {root_idea}\n"
        f"Parent idea: {parent_idea}\n"
        "Each child should sharpen or vary the parent by mechanic, content use, vibe, or space.\n"
        "Return:\n"
        "IDEAS:\n"
        "- five child idea lines only"
    )
    output = run_copilot_stage("hierarchy-expand", prompt)
    ideas = extract_list_items(output, "IDEAS")
    return normalize_to_five(ideas, [
        f"{parent_idea} with combo pressure",
        f"{parent_idea} with salvage pickups",
        f"{parent_idea} with rhythm timing",
        f"{parent_idea} with fake 3d depth",
        f"{parent_idea} with hazard waves",
    ])


def hierarchy_reduce(candidates: list[str]) -> list[str]:
    current = dedupe_keep_order(candidates)
    while len(current) > 5:
        next_round = []
        pairs = list(pairwise(current))
        for left, right in pairs:
            next_round.append(rank_pair(left, right))
        if len(current) % 2 == 1:
            next_round.append(current[-1])
        current = dedupe_keep_order(next_round)
        if len(current) > 5:
            current = merge_ranked_set(current)
    return current[:5]


def rank_pair(left: str, right: str) -> str:
    prompt = (
        "Pick the stronger arcade game idea and expand it slightly.\n"
        f"Idea A: {left}\n"
        f"Idea B: {right}\n"
        "Choose the stronger one based on distinctiveness, gameplay depth, and buildability.\n"
        "Return compact JSON with keys: winner, expanded."
    )
    output = run_copilot_stage("hierarchy-rank", prompt)
    match = extract_json_object(output)
    if match:
        try:
            data = json.loads(match)
            winner = data.get("winner")
            expanded = data.get("expanded")
            if winner in {"A", "B"} and isinstance(expanded, str) and expanded.strip():
                return expanded.strip()
        except json.JSONDecodeError:
            pass
    return left if len(left) >= len(right) else right


def merge_ranked_set(candidates: list[str]) -> list[str]:
    prompt = (
        "Reduce this ranked arcade idea set to the best 5 survivors.\n"
        "For each survivor, slightly extend the detail while keeping it concise.\n"
        f"Candidates: {json.dumps(candidates)}\n"
        "Return:\n"
        "SURVIVORS:\n"
        "- five idea lines only"
    )
    output = run_copilot_stage("hierarchy-rank", prompt)
    survivors = extract_list_items(output, "SURVIVORS")
    return normalize_to_five(survivors, candidates[:5])


def pairwise(items: list[str]):
    for index in range(0, len(items) - 1, 2):
        yield items[index], items[index + 1]


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(normalized)
    return result


def normalize_to_five(items: list[str], fallback: list[str]) -> list[str]:
    merged = dedupe_keep_order(items + fallback)
    return merged[:5]


def prepare_design_stages(brief: IdeaBrief) -> IdeaBrief:
    if brief.hierarchy_survivors:
        brief.idea = brief.hierarchy_survivors[0]
    if not brief.sections:
        brief = shape_idea(brief, "")
    if not brief.brainstorms:
        brief = brainstorm_idea(brief, "")
    if not brief.expansions:
        brief = expand_idea(brief, "")
    if not brief.theme_pack:
        brief = build_theme_pack(brief, "")
    if not brief.content_plan:
        brief = build_content_plan(brief, "")
    if not brief.feature_plan:
        brief = build_feature_plan(brief, "")
    return brief


def pick_mode(brief: IdeaBrief, note: str) -> IdeaBrief:
    brief = prepare_design_stages(brief)
    prompt = (
        "Choose the best arcade runtime mode for this game idea.\n"
        f"Idea: {brief.idea}\n"
        f"Options: {', '.join(brief.options) or '(none)'}\n"
        f"Brainstorms: {', '.join(brief.brainstorms) or '(none)'}\n"
        f"Expansions: {', '.join(brief.expansions) or '(none)'}\n"
        f"Theme pack: {json.dumps(brief.theme_pack) or '(none)'}\n"
        f"Content plan: {json.dumps(brief.content_plan) or '(none)'}\n"
        f"Feature plan: {json.dumps(brief.feature_plan) or '(none)'}\n"
        f"Sections: {', '.join(brief.sections) or '(none)'}\n"
        f"Note: {note or '(none)'}\n"
        "Modes:\n"
        + "\n".join(f"- {name}: {description}" for name, description in MODE_LABELS.items())
        + "\nReturn compact JSON with keys: mode, chosenSection, rationale."
    )
    output = run_copilot_stage("mode-pick", prompt)
    mode = None
    chosen_section = None
    match = extract_json_object(output)
    if match:
        try:
            data = json.loads(match)
            mode = data.get("mode")
            chosen_section = data.get("chosenSection")
        except json.JSONDecodeError:
            mode = None
    brief.chosen_mode = mode if mode in MODE_ORDER else pick_fallback_mode(brief.idea)
    if chosen_section and chosen_section in brief.sections:
        brief.chosen_section = chosen_section
    elif not brief.chosen_section and brief.sections:
        brief.chosen_section = brief.sections[0]
    print(f"Mode: {brief.chosen_mode}")
    print(f"Section: {brief.chosen_section or '(none)'}")
    return brief


def fill_game_json(brief: IdeaBrief, note: str) -> IdeaBrief:
    brief = prepare_design_stages(brief)
    ensure_json_ready(brief)
    template = load_mode_template(brief.chosen_mode)
    schema = load_schema_for_mode(brief.chosen_mode)
    asset_manifest = load_asset_manifest()
    prompt = (
        f"{read_orchestrator_control_text()}\n\n"
        "Stage lock: json-fill.\n"
        "Allowed work: fill one existing arcade JSON template for the selected mode.\n"
        "Forbidden work: no repository edits, no runtime code, no external assets, no extra exploration, no broad ideation.\n"
        "Output contract: return one JSON object only.\n\n"
        "Fill this arcade game JSON template.\n"
        "Rules:\n"
        "- Return JSON only.\n"
        "- Do not write JavaScript.\n"
        "- Do not reference external content.\n"
        "- Keep the game greyboxed and use shared assets only.\n"
        "- Use the design stages to vary theme, content use, pacing, and presentation.\n"
        "- Stay inside the existing runtime mode and schema.\n"
        f"Idea: {brief.idea}\n"
        f"Brainstorms: {', '.join(brief.brainstorms) or '(none)'}\n"
        f"Expansions: {', '.join(brief.expansions) or '(none)'}\n"
        f"Theme pack: {json.dumps(brief.theme_pack)}\n"
        f"Content plan: {json.dumps(brief.content_plan)}\n"
        f"Feature plan: {json.dumps(brief.feature_plan)}\n"
        f"Chosen section: {brief.chosen_section or '(none)'}\n"
        f"Mode: {brief.chosen_mode}\n"
        f"Note: {note or '(none)'}\n"
        f"Allowed palettes: {', '.join(asset_manifest['palettes'])}\n"
        f"Allowed sprite keys: {', '.join(asset_manifest['sprites'])}\n"
        f"Allowed effect keys: {', '.join(asset_manifest['effects'])}\n"
        "Template JSON:\n"
        f"{json.dumps(template, indent=2)}\n"
        "Schema summary:\n"
        f"{json.dumps(schema, indent=2)}"
    )
    output = run_copilot_stage("json-fill", prompt)
    game_json = parse_game_json(output) or build_fallback_game_json(brief)
    validate_game_json(game_json)
    brief.game_json = game_json
    print(f"JSON ready: {game_json['slug']}")
    return brief


def build_game(brief: IdeaBrief) -> dict[str, Any]:
    brief = prepare_design_stages(brief)
    ensure_json_ready(brief)
    if not brief.game_json:
        brief = fill_game_json(brief, "")
    game_json = brief.game_json or build_fallback_game_json(brief)
    validate_game_json(game_json)
    game_path = GAMES_DIR / f"{game_json['slug']}.json"
    shell_path = PAGES_DIR / f"{game_json['slug']}.html"
    game_path.write_text(json.dumps(game_json, indent=2) + "\n", encoding="utf-8")
    shell_path.write_text(render_arcade_shell(game_json), encoding="utf-8")
    insert_portfolio_project(game_json)
    validate_built_game(game_json, shell_path)
    return game_json


def ensure_json_ready(brief: IdeaBrief) -> None:
    if not brief.sections:
        brief.sections = ["core loop", "controls", "visual style", "state and feedback", "failure and retry"]
    if not brief.chosen_mode:
        brief.chosen_mode = pick_fallback_mode(brief.idea)
    if not brief.chosen_section and brief.sections:
        brief.chosen_section = brief.sections[0]


def run_copilot_stage(stage: str, prompt: str) -> str:
    settings = STAGE_SETTINGS[stage]
    standalone = shutil.which("copilot")
    if standalone:
        result = subprocess.run(
            [
                standalone,
                "--model",
                "gpt-5-mini",
                "--reasoning-effort",
                settings["reasoning"],
                "--temperature",
                str(settings["temperature"]),
                prompt,
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        text = (result.stdout or result.stderr or "").strip()
        if text:
            return text

    gh = shutil.which("gh")
    if not gh:
        return ""

    result = subprocess.run(
        [gh, "copilot", "suggest", "-t", "shell", prompt],
        check=False,
        text=True,
        capture_output=True,
    )
    return (result.stdout or result.stderr or "").strip()


def read_orchestrator_control_text() -> str:
    chunks = []
    for label, path in (
        ("System prompt", ORCHESTRATOR_SYSTEM_PROMPT_PATH),
        ("Memory", ORCHESTRATOR_MEMORY_PATH),
    ):
        if path.exists():
            chunks.append(f"{label}:\n{path.read_text(encoding='utf-8')[-6000:]}")
    return "\n\n".join(chunks)


def extract_list_items(text: str, heading: str) -> list[str]:
    pattern = rf"{heading}\s*:?(.*?)(?:\n[A-Z][A-Z\s/:-]*:|\Z)"
    match = re.search(pattern, text, re.S)
    if not match:
        return []
    block = match.group(1)
    items = []
    for line in block.splitlines():
        line = line.strip().lstrip("-*0123456789. ").strip()
        if line:
            items.append(line)
    return items[:8]


def extract_json_object(text: str) -> str | None:
    match = re.search(r"\{.*\}", text, re.S)
    return match.group(0) if match else None


def parse_game_json(raw: str) -> dict[str, Any] | None:
    match = extract_json_object(raw)
    if not match:
        return None
    try:
        data = json.loads(match)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def parse_json_or_default(raw: str, default: dict[str, Any]) -> dict[str, Any]:
    match = extract_json_object(raw)
    if not match:
        return default
    try:
        data = json.loads(match)
    except json.JSONDecodeError:
        return default
    return data if isinstance(data, dict) else default


def build_fallback_game_json(brief: IdeaBrief) -> dict[str, Any]:
    template = load_mode_template(brief.chosen_mode)
    slug = slugify(brief.idea)
    title = titleize(brief.idea)
    palette = choose_palette_for_mode(brief.chosen_mode, brief.theme_pack)
    instructions = fallback_instructions_for_mode(brief.chosen_mode, brief.feature_plan)
    template["id"] = slug
    template["slug"] = slug
    template["title"] = title
    template["palette"] = palette
    template["instructions"] = instructions
    template["hud"]["modeLabel"] = fallback_mode_label(brief.chosen_mode)
    template["overlay"]["startTitle"] = title
    theme_words = ", ".join(brief.theme_pack.get("vibeWords", []))
    template["overlay"]["startCopy"] = (
        f"Greyboxed arcade game for {brief.idea}. "
        f"Theme: {theme_words or 'arcade greybox'}. "
        f"Play the shared runtime version."
    )
    template["visuals"] = choose_visuals_for_mode(brief.chosen_mode, brief.theme_pack)
    template.update(build_shared_ui_defaults(brief, title, instructions))
    template["meta"] = {
        "summary": f"Greyboxed arcade game generated for {brief.idea}.",
        "goal": brief.idea,
        "controls": instructions,
        "paletteLabel": palette,
        "features": [
            "JSON-driven content",
            *summarize_plan_features(brief),
        ],
    }
    apply_fallback_content(template, brief)
    return template


def validate_game_json(game_json: dict[str, Any]) -> None:
    mode = game_json.get("mode")
    if mode not in MODE_ORDER:
        raise RuntimeError(f"Unsupported mode: {mode}")

    base_schema = load_schema("base-game.schema.json")
    mode_schema = load_schema(f"{mode}.schema.json")
    validate_against_schema(game_json, base_schema, "base-game.schema.json")
    validate_against_schema(game_json, mode_schema, f"{mode}.schema.json")
    validate_asset_keys(game_json)


def validate_against_schema(instance: Any, schema: dict[str, Any], schema_name: str, path: str = "$") -> None:
    expected_type = schema.get("type")
    if expected_type and not matches_type(instance, expected_type):
        raise RuntimeError(f"{schema_name}: {path} expected {expected_type}")

    if expected_type == "object":
        assert isinstance(instance, dict)
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                raise RuntimeError(f"{schema_name}: {path}.{key} is required")

        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in properties:
                validate_against_schema(value, properties[key], schema_name, f"{path}.{key}")
            elif additional is False:
                raise RuntimeError(f"{schema_name}: {path}.{key} is not allowed")

    if expected_type == "array":
        assert isinstance(instance, list)
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            raise RuntimeError(f"{schema_name}: {path} needs at least {min_items} items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(instance):
                validate_against_schema(item, item_schema, schema_name, f"{path}[{index}]")

    if "enum" in schema and instance not in schema["enum"]:
        raise RuntimeError(f"{schema_name}: {path} must be one of {schema['enum']}")


def matches_type(instance: Any, expected: str) -> bool:
    checks = {
        "object": lambda value: isinstance(value, dict),
        "array": lambda value: isinstance(value, list),
        "string": lambda value: isinstance(value, str),
        "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
        "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
        "boolean": lambda value: isinstance(value, bool),
    }
    return checks[expected](instance)


def validate_asset_keys(game_json: dict[str, Any]) -> None:
    manifest = load_asset_manifest()
    palette = game_json.get("palette")
    if palette not in manifest["palettes"]:
        raise RuntimeError(f"Unknown palette key: {palette}")

    visuals = game_json.get("visuals", {})
    for key in ("spriteKey", "accentSpriteKey", "hazardSpriteKey"):
        value = visuals.get(key)
        if value and value not in manifest["sprites"]:
            raise RuntimeError(f"Unknown sprite key: {value}")
    for key in ("trailEffectKey", "impactEffectKey"):
        value = visuals.get(key)
        if value and value not in manifest["effects"]:
            raise RuntimeError(f"Unknown effect key: {value}")


def validate_built_game(game_json: dict[str, Any], shell_path: Path) -> None:
    if not shell_path.exists():
        raise RuntimeError(f"Game shell missing: {shell_path}")
    game_path = GAMES_DIR / f"{game_json['slug']}.json"
    if not game_path.exists():
        raise RuntimeError(f"Game JSON missing: {game_path}")

    shell = shell_path.read_text(encoding="utf-8")
    expected = f'data-arcade-config="./games/{game_json["slug"]}.json"'
    if expected not in shell:
        raise RuntimeError(f"Game shell does not point at {game_json['slug']}.json")

    node = shutil.which("node")
    if node:
        for path in (PAGES_DIR / "arcade-runtime.js", PAGES_DIR / "arcade-bootstrap.js"):
            result = subprocess.run([node, "--check", str(path)], text=True, capture_output=True)
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    validate_game_playability(game_json["slug"])


def validate_game_playability(slug: str) -> None:
    node = shutil.which("node")
    playwright_module = find_playwright_module()
    if not node or not playwright_module:
        return

    script = f"""
const {{ chromium }} = require({json.dumps(str(playwright_module))});
(async () => {{
  const browser = await chromium.launch({{ headless: true }});
  const page = await browser.newPage({{ viewport: {{ width: 1280, height: 800 }} }});
  const errors = [];
  page.on('pageerror', (err) => errors.push(`pageerror:${{err.message}}`));
  page.on('console', (msg) => {{
    if (msg.type() === 'error') errors.push(`console:${{msg.text()}}`);
  }});
  await page.goto('http://127.0.0.1:5174/Pages/{slug}.html', {{ waitUntil: 'networkidle', timeout: 15000 }});
  await page.waitForSelector('#action', {{ timeout: 5000 }});
  await page.click('#action');
  await page.waitForTimeout(500);
  const status = await page.evaluate(() => ({{
    overlayHidden: document.querySelector('#overlay')?.classList.contains('hidden') ?? false,
    canvasWidth: document.querySelector('#game')?.width || 0,
    canvasHeight: document.querySelector('#game')?.height || 0
  }}));
  await browser.close();
  if (errors.length) {{
    throw new Error(errors.join('\\n'));
  }}
  if (!status.overlayHidden || status.canvasWidth < 400 || status.canvasHeight < 300) {{
    throw new Error(`Playability check failed for {slug}: ${{JSON.stringify(status)}}`);
  }}
}})().catch((error) => {{
  console.error(error.message);
  process.exit(1);
}});
"""
    result = subprocess.run([node, "-e", script], text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def find_playwright_module() -> Path | None:
    npx_root = Path.home() / ".npm" / "_npx"
    if not npx_root.exists():
        return None
    candidates = sorted(
        npx_root.glob("*/node_modules/playwright"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def render_arcade_shell(game_json: dict[str, Any]) -> str:
    title = escape_html(game_json["title"])
    slug = escape_html(game_json["slug"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Crimson Wheeler</title>
  <link rel="stylesheet" href="./arcade-shell.css" />
</head>
<body>
  <div class="arcade-hud" id="hud"></div>
  <div class="arcade-overlay" id="overlay">
    <div class="arcade-panel">
      <h2 id="overlay-title"></h2>
      <p id="overlay-copy"></p>
      <button id="action" type="button"></button>
    </div>
  </div>
  <canvas id="game" aria-label="{title}"></canvas>
  <script
    type="module"
    src="./arcade-bootstrap.js"
    data-arcade-config="./games/{slug}.json"
    data-arcade-assets="./arcade-assets.json"
  ></script>
</body>
</html>
"""


def insert_portfolio_project(game_json: dict[str, Any]) -> None:
    text = PORTFOLIO_DATA.read_text(encoding="utf-8")
    slug = game_json["slug"]
    title = js_escape(game_json["title"])
    summary = js_escape(game_json["meta"]["summary"])
    goal = js_escape(game_json["meta"]["goal"])
    controls = js_escape(game_json["meta"]["controls"])
    features = game_json["meta"].get("features", [])
    feature_lines = "\n".join(f'        "{js_escape(item)}",' for item in features[:4])
    entry = f'''    "{slug}": {{
      slug: "{slug}",
      title: "{title}",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "{summary}",
      description:
        "{goal}",
      image: "",
      features: [
{feature_lines}
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {{
          label: "Open Prototype",
          href: "Pages/{slug}.html",
          style: "secondary",
        }},
      ],
    }},\n'''
    marker = '    pillow: {'
    if f'"{slug}": ' in text:
        return
    if marker not in text:
        raise RuntimeError("Could not find insertion point in projects.js")
    text = text.replace(marker, entry + marker, 1)
    text = text.replace(
        '      technologies: ["JSON", "Shared Runtime", "Prototype"],',
        f'      technologies: ["JSON", "Shared Runtime", "Prototype"],',
    )
    PORTFOLIO_DATA.write_text(text, encoding="utf-8")
    append_slug_to_page_featured("prototypes", slug)
    append_slug_to_page_featured("arcade-library", slug)


def append_slug_to_page_featured(page_id: str, slug: str) -> None:
    text = PORTFOLIO_PAGES.read_text(encoding="utf-8")
    pattern = rf'("{page_id}"|{re.escape(page_id)}): \\{{[\\s\\S]*?featuredProjectSlugs:\\s*\\[\\n(?P<body>[\\s\\S]*?)\\n\\s*\\],'
    match = re.search(pattern, text)
    if not match or f'"{slug}"' in match.group("body"):
        return
    insert_at = match.end("body")
    prefix = "" if match.group("body").strip() == "" else "\n"
    text = text[:insert_at] + f'{prefix}        "{slug}",' + text[insert_at:]
    PORTFOLIO_PAGES.write_text(text, encoding="utf-8")


def append_slug_to_featured_slugs(match: re.Match[str], slug: str) -> str:
    body = match.group(2)
    if f'"{slug}"' in body:
        return match.group(0)
    if body.strip():
        body = body.rstrip() + f'\n        "{slug}",'
    else:
        body = f'        "{slug}",'
    return f"{match.group(1)}{body}{match.group(3)}"


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMAS_DIR / name).read_text(encoding="utf-8"))


def load_schema_for_mode(mode: str) -> dict[str, Any]:
    return load_schema(f"{mode}.schema.json")


def load_mode_template(mode: str) -> dict[str, Any]:
    return json.loads((TEMPLATES_DIR / f"{mode}.template.json").read_text(encoding="utf-8"))


def load_asset_manifest() -> dict[str, list[str]]:
    assets = json.loads(ARCADE_ASSETS.read_text(encoding="utf-8"))
    return {
        "palettes": sorted(assets.get("palettes", {}).keys()),
        "sprites": sorted(assets.get("sprites", {}).keys()),
        "effects": sorted(assets.get("effects", {}).keys()),
    }


def choose_palette_for_mode(mode: str, theme_pack: dict[str, Any] | None = None) -> str:
    requested = (theme_pack or {}).get("paletteDirection")
    if requested in {"signal", "orbit", "pulse", "harbor"}:
        return requested
    return {
        "runner": "signal",
        "orbit": "orbit",
        "pulseGrid": "pulse",
        "labRift": "pulse",
        "phaseDrop": "pulse",
        "harbor": "harbor",
        "rhythm": "pulse",
        "echo": "pulse",
    }[mode]


def choose_visuals_for_mode(mode: str, theme_pack: dict[str, Any]) -> dict[str, str]:
    visuals = dict(BASE_VISUALS)
    space_type = str(theme_pack.get("spaceType", "")).lower()
    vibe_words = " ".join(theme_pack.get("vibeWords", [])).lower()
    if mode in {"pulseGrid", "echo", "phaseDrop"}:
        visuals["spriteKey"] = "padTile"
    if mode == "orbit":
        visuals["spriteKey"] = "orbNode"
        visuals["accentSpriteKey"] = "orbNode"
    if mode == "labRift":
        visuals["spriteKey"] = "runnerShip"
        visuals["accentSpriteKey"] = "shardCrystal"
        visuals["hazardSpriteKey"] = "sentryDrone"
    if mode == "harbor":
        visuals["spriteKey"] = "boatSkiff"
        visuals["accentSpriteKey"] = "buoyMarker"
    if "sand" in vibe_words:
        visuals["trailEffectKey"] = "sand"
    if "3d" in space_type or "fake3d" in space_type:
        visuals["accentSpriteKey"] = "orbNode"
    return visuals


def summarize_plan_features(brief: IdeaBrief) -> list[str]:
    features = []
    core = brief.feature_plan.get("coreMechanic")
    if core:
        features.append(str(core).title())
    for item in brief.feature_plan.get("supportMechanics", [])[:2]:
        features.append(str(item).title())
    if brief.theme_pack.get("surfaceStyle"):
        features.append(str(brief.theme_pack["surfaceStyle"]).title())
    return features[:3] or ["Shared runtime mode", "Greyboxed visual treatment"]


def build_shared_ui_defaults(brief: IdeaBrief, title: str, instructions: str) -> dict[str, Any]:
    shared = json.loads(json.dumps(BASE_SHARED_UI))
    shared["help"]["title"] = f"How To Start {title}"
    shared["help"]["steps"] = [
        "Press Start in the center overlay.",
        f"Use the controls: {instructions}",
        f"Follow the first goal: {brief.content_plan.get('challengeFlow', 'learn the opening pattern')}.",
    ]
    shared["help"]["tips"] = [
        f"Theme: {', '.join(brief.theme_pack.get('vibeWords', [])) or 'arcade greybox'}.",
        f"Support mechanics: {', '.join(brief.feature_plan.get('supportMechanics', [])) or 'standard arcade play'}.",
    ]
    shared["onboarding"]["startSteps"] = list(shared["help"]["steps"])
    shared["onboarding"]["firstGoal"] = brief.content_plan.get("challengeFlow", "Learn the opening loop.")
    return shared


def apply_fallback_content(template: dict[str, Any], brief: IdeaBrief) -> None:
    content_objects = [str(item).lower() for item in brief.content_plan.get("contentObjects", [])]
    vibe_words = " ".join(brief.theme_pack.get("vibeWords", [])).lower()
    mode = brief.chosen_mode
    if mode == "runner":
        patterns = template["content"]["patterns"]
        if "pickups" in content_objects:
            patterns.extend([{"lanes": [1, 2]}, {"lanes": [0, 3]}])
        if "sand" in vibe_words:
            template["visuals"]["trailEffectKey"] = "sand"
    elif mode == "orbit":
        if "combo" in vibe_words or "chain" in vibe_words:
            for ring in template["content"]["rings"]:
                ring["velocity"] += 0.15
    elif mode == "pulseGrid":
        if "beats" in content_objects or "targets" in content_objects:
            template["content"]["sequence"].append({"cell": 13, "time": 1.6})
    elif mode == "labRift":
        if "rooms" in content_objects or "pickups" in content_objects:
            template["content"]["shards"].append({"x": 0.82, "y": 0.24})
    elif mode == "phaseDrop":
        if "neon" in vibe_words:
            template["content"]["phases"] = ["#67d5ff", "#b68cff", "#ff7a9e"]
    elif mode == "harbor":
        if "beats" in content_objects or "rhythm" in vibe_words:
            template["content"]["currents"].append({"x": -0.14, "y": 0.04})
        if "markers" in content_objects or "pickups" in content_objects:
            template["content"]["buoys"].append({"x": 0.86, "y": 0.42})
    elif mode == "rhythm":
        if "drift" in vibe_words:
            template["content"]["beats"].append({"time": 3.75})
    elif mode == "echo":
        if "memory" in content_objects or "tokens" in content_objects:
            template["content"]["pattern"].extend([2, 0])


def pick_fallback_mode(idea: str) -> str:
    text = idea.lower()
    if any(term in text for term in ("orbit", "pop", "chain", "click")):
        return "orbit"
    if any(term in text for term in ("beat", "music", "grid", "pulse")):
        return "pulseGrid"
    if any(term in text for term in ("room", "escape", "collect", "maze", "lab")):
        return "labRift"
    if any(term in text for term in ("phase", "lane", "drop")):
        return "phaseDrop"
    if any(term in text for term in ("boat", "harbor", "water", "drift")):
        return "harbor"
    if any(term in text for term in ("rhythm", "track", "notes")):
        return "rhythm"
    if any(term in text for term in ("memory", "pattern", "echo")):
        return "echo"
    return "runner"


def fallback_mode_label(mode: str) -> str:
    return {
        "runner": "Infinite Run",
        "orbit": "Combo Chain",
        "pulseGrid": "Beat Grid",
        "labRift": "Collect Route",
        "phaseDrop": "Phase Shift",
        "harbor": "Drift Route",
        "rhythm": "Hit Beats",
        "echo": "Repeat Pattern",
    }[mode]


def fallback_instructions_for_mode(mode: str, feature_plan: dict[str, Any] | None = None) -> str:
    base = {
        "runner": "Move with arrow keys or A / D.",
        "orbit": "Move the pointer and click targets.",
        "pulseGrid": "Press Space on the active beats.",
        "labRift": "Move with arrows or WASD and collect objects.",
        "phaseDrop": "Use left and right to swap lanes.",
        "harbor": "Steer with the cursor and collect markers.",
        "rhythm": "Press Space as notes hit the marker.",
        "echo": "Repeat the shown pattern with 1, 2, 3, and 4.",
    }[mode]
    control_style = (feature_plan or {}).get("controlStyle")
    return f"{base} Style: {control_style}." if control_style else base


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "prototype"


def titleize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().title() or "Prototype"


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def js_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def ensure_cli_support_files() -> None:
    SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    for name, payload in SCHEMA_FILES.items():
        path = SCHEMAS_DIR / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for name, payload in TEMPLATE_FILES.items():
        path = TEMPLATES_DIR / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


BASE_VISUALS = {
    "spriteKey": "runnerShip",
    "accentSpriteKey": "orbNode",
    "hazardSpriteKey": "hazardBlock",
    "trailEffectKey": "smoke",
    "impactEffectKey": "spark",
}

BASE_META = {
    "summary": "Greyboxed arcade game built from schema-bound JSON.",
    "goal": "",
    "controls": "",
    "paletteLabel": "",
    "features": [
        "JSON-driven content",
        "Shared runtime mode",
        "Greyboxed visual treatment",
    ],
}

BASE_SHARED_UI = {
    "settings": {
        "title": "Settings",
        "sections": [
            {
                "title": "Gameplay",
                "controls": [
                    {"key": "difficulty", "label": "Difficulty", "type": "select", "value": "normal", "options": ["easy", "normal", "hard"]},
                    {"key": "effectIntensity", "label": "Effect Intensity", "type": "range", "value": 0.75, "min": 0, "max": 1, "step": 0.05},
                ],
            }
        ],
    },
    "help": {
        "title": "How To Start",
        "steps": [
            "Press Start in the center overlay.",
            "Use the listed controls to begin the run.",
            "Watch the HUD goal and react to the first pattern.",
        ],
        "tips": [
            "Open Settings before the run if you want a different feel.",
            "Open Menu with Escape to restart or resume.",
        ],
    },
    "menu": {
        "title": "Pause Menu",
        "actions": [
            {"label": "Resume", "action": "resume"},
            {"label": "Restart", "action": "restart"},
            {"label": "Help", "action": "open_help"},
            {"label": "Settings", "action": "open_settings"},
        ],
    },
    "onboarding": {
        "title": "Get Started",
        "startSteps": [
            "Open Help if you need the controls.",
            "Press Start to enter gameplay.",
            "Learn the first rhythm, route, or hazard pattern before chasing score.",
        ],
        "firstGoal": "Learn the opening loop and survive the first pressure ramp.",
    },
}

SCHEMA_FILES: dict[str, dict[str, Any]] = {
    "base-game.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "id",
            "slug",
            "title",
            "mode",
            "palette",
            "instructions",
            "hud",
            "overlay",
            "visuals",
            "settings",
            "help",
            "menu",
            "onboarding",
            "meta",
            "content",
        ],
        "properties": {
            "id": {"type": "string"},
            "slug": {"type": "string"},
            "title": {"type": "string"},
            "mode": {"type": "string", "enum": MODE_ORDER},
            "palette": {"type": "string"},
            "instructions": {"type": "string"},
            "hud": {
                "type": "object",
                "required": ["modeLabel"],
                "properties": {"modeLabel": {"type": "string"}},
                "additionalProperties": False,
            },
            "overlay": {
                "type": "object",
                "required": ["startTitle", "startCopy", "startAction"],
                "properties": {
                    "startTitle": {"type": "string"},
                    "startCopy": {"type": "string"},
                    "startAction": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "visuals": {
                "type": "object",
                "required": [
                    "spriteKey",
                    "accentSpriteKey",
                    "hazardSpriteKey",
                    "trailEffectKey",
                    "impactEffectKey",
                ],
                "properties": {
                    "spriteKey": {"type": "string"},
                    "accentSpriteKey": {"type": "string"},
                    "hazardSpriteKey": {"type": "string"},
                    "trailEffectKey": {"type": "string"},
                    "impactEffectKey": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "settings": {
                "type": "object",
                "required": ["title", "sections"],
                "properties": {
                    "title": {"type": "string"},
                    "sections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["title", "controls"],
                            "properties": {
                                "title": {"type": "string"},
                                "controls": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "required": ["key", "label", "type", "value"],
                                        "properties": {
                                            "key": {"type": "string"},
                                            "label": {"type": "string"},
                                            "type": {"type": "string", "enum": ["select", "range"]},
                                            "value": {},
                                            "options": {"type": "array", "items": {"type": "string"}},
                                            "min": {"type": "number"},
                                            "max": {"type": "number"},
                                            "step": {"type": "number"},
                                        },
                                        "additionalProperties": False,
                                    },
                                    "minItems": 1,
                                },
                            },
                            "additionalProperties": False,
                        },
                        "minItems": 1,
                    },
                },
                "additionalProperties": False,
            },
            "help": {
                "type": "object",
                "required": ["title", "steps"],
                "properties": {
                    "title": {"type": "string"},
                    "steps": {"type": "array", "items": {"type": "string"}, "minItems": 3},
                    "tips": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "menu": {
                "type": "object",
                "required": ["title", "actions"],
                "properties": {
                    "title": {"type": "string"},
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["label", "action"],
                            "properties": {
                                "label": {"type": "string"},
                                "action": {"type": "string", "enum": ["resume", "restart", "open_help", "open_settings"]},
                            },
                            "additionalProperties": False,
                        },
                        "minItems": 2,
                    },
                },
                "additionalProperties": False,
            },
            "onboarding": {
                "type": "object",
                "required": ["title", "startSteps", "firstGoal"],
                "properties": {
                    "title": {"type": "string"},
                    "startSteps": {"type": "array", "items": {"type": "string"}, "minItems": 3},
                    "firstGoal": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "meta": {
                "type": "object",
                "required": ["summary", "goal", "controls", "paletteLabel", "features"],
                "properties": {
                    "summary": {"type": "string"},
                    "goal": {"type": "string"},
                    "controls": {"type": "string"},
                    "paletteLabel": {"type": "string"},
                    "features": {"type": "array", "items": {"type": "string"}, "minItems": 3},
                },
                "additionalProperties": False,
            },
            "content": {"type": "object"},
        },
        "additionalProperties": False,
    },
    "runner.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["runner"]},
            "content": {
                "type": "object",
                "required": ["lanes", "patterns"],
                "properties": {
                    "lanes": {"type": "array", "items": {"type": "number"}, "minItems": 3},
                    "patterns": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["lanes"],
                            "properties": {
                                "lanes": {"type": "array", "items": {"type": "integer"}, "minItems": 1}
                            },
                            "additionalProperties": False,
                        },
                        "minItems": 4,
                    },
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
    "orbit.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["orbit"]},
            "content": {
                "type": "object",
                "required": ["orbitSpeed", "coreRadius", "rings"],
                "properties": {
                    "orbitSpeed": {"type": "number"},
                    "coreRadius": {"type": "number"},
                    "rings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["radiusBand", "radius", "velocity"],
                            "properties": {
                                "radiusBand": {"type": "number"},
                                "radius": {"type": "number"},
                                "velocity": {"type": "number"},
                            },
                            "additionalProperties": False,
                        },
                        "minItems": 3,
                    },
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
    "pulseGrid.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["pulseGrid"]},
            "content": {
                "type": "object",
                "required": ["sequence"],
                "properties": {
                    "sequence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["cell", "time"],
                            "properties": {
                                "cell": {"type": "integer"},
                                "time": {"type": "number"},
                            },
                            "additionalProperties": False,
                        },
                        "minItems": 5,
                    }
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
    "labRift.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["labRift"]},
            "content": {
                "type": "object",
                "required": ["playerSpeed", "shards", "sentries"],
                "properties": {
                    "playerSpeed": {"type": "number"},
                    "shards": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["x", "y"],
                            "properties": {"x": {"type": "number"}, "y": {"type": "number"}},
                            "additionalProperties": False,
                        },
                        "minItems": 4,
                    },
                    "sentries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["x", "y", "rate"],
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "rate": {"type": "number"},
                            },
                            "additionalProperties": False,
                        },
                        "minItems": 2,
                    },
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
    "phaseDrop.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["phaseDrop"]},
            "content": {
                "type": "object",
                "required": ["phases"],
                "properties": {
                    "phases": {"type": "array", "items": {"type": "string"}, "minItems": 3}
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
    "harbor.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["harbor"]},
            "content": {
                "type": "object",
                "required": ["buoys", "currents"],
                "properties": {
                    "buoys": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["x", "y"],
                            "properties": {"x": {"type": "number"}, "y": {"type": "number"}},
                            "additionalProperties": False,
                        },
                        "minItems": 4,
                    },
                    "currents": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["x", "y"],
                            "properties": {"x": {"type": "number"}, "y": {"type": "number"}},
                            "additionalProperties": False,
                        },
                        "minItems": 4,
                    },
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
    "rhythm.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["rhythm"]},
            "content": {
                "type": "object",
                "required": ["loopDuration", "beats"],
                "properties": {
                    "loopDuration": {"type": "number"},
                    "beats": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["time"],
                            "properties": {"time": {"type": "number"}},
                            "additionalProperties": False,
                        },
                        "minItems": 6,
                    },
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
    "echo.schema.json": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["echo"]},
            "content": {
                "type": "object",
                "required": ["pattern", "revealEvery", "inputMap", "padColors"],
                "properties": {
                    "pattern": {"type": "array", "items": {"type": "integer"}, "minItems": 4},
                    "revealEvery": {"type": "number"},
                    "inputMap": {
                        "type": "object",
                        "required": ["1", "2", "3", "4"],
                        "properties": {
                            "1": {"type": "integer"},
                            "2": {"type": "integer"},
                            "3": {"type": "integer"},
                            "4": {"type": "integer"},
                        },
                        "additionalProperties": False,
                    },
                    "padColors": {"type": "array", "items": {"type": "string"}, "minItems": 4},
                },
                "additionalProperties": False,
            },
        },
        "required": ["mode", "content"],
    },
}

TEMPLATE_FILES: dict[str, dict[str, Any]] = {
    "runner.template.json": {
        "id": "new-runner",
        "slug": "new-runner",
        "title": "New Runner",
        "mode": "runner",
        "palette": "signal",
        "instructions": "Move with arrow keys or A / D.",
        "hud": {"modeLabel": "Infinite Run"},
        "overlay": {"startTitle": "New Runner", "startCopy": "Greyboxed runner challenge.", "startAction": "Start Run"},
        "visuals": BASE_VISUALS,
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {
            "lanes": [0.22, 0.4, 0.58, 0.76],
            "patterns": [{"lanes": [0]}, {"lanes": [1]}, {"lanes": [2]}, {"lanes": [3]}, {"lanes": [0, 2]}],
        },
    },
    "orbit.template.json": {
        "id": "new-orbit",
        "slug": "new-orbit",
        "title": "New Orbit",
        "mode": "orbit",
        "palette": "orbit",
        "instructions": "Move the pointer and click targets.",
        "hud": {"modeLabel": "Combo Chain"},
        "overlay": {"startTitle": "New Orbit", "startCopy": "Greyboxed orbit challenge.", "startAction": "Start Chain"},
        "visuals": {**BASE_VISUALS, "spriteKey": "orbNode", "accentSpriteKey": "orbNode"},
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {
            "orbitSpeed": 1.2,
            "coreRadius": 88,
            "rings": [
                {"radiusBand": 0.18, "radius": 18, "velocity": 0.8},
                {"radiusBand": 0.26, "radius": 16, "velocity": 1.1},
                {"radiusBand": 0.34, "radius": 14, "velocity": 1.4},
            ],
        },
    },
    "pulseGrid.template.json": {
        "id": "new-grid",
        "slug": "new-grid",
        "title": "New Grid",
        "mode": "pulseGrid",
        "palette": "pulse",
        "instructions": "Press Space on the pulse beats.",
        "hud": {"modeLabel": "Beat Grid"},
        "overlay": {"startTitle": "New Grid", "startCopy": "Greyboxed pulse grid challenge.", "startAction": "Start Grid"},
        "visuals": {**BASE_VISUALS, "spriteKey": "padTile", "accentSpriteKey": "padTile"},
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {
            "sequence": [
                {"cell": 6, "time": 0.2},
                {"cell": 7, "time": 0.5},
                {"cell": 12, "time": 0.8},
                {"cell": 17, "time": 1.1},
                {"cell": 18, "time": 1.35},
            ]
        },
    },
    "labRift.template.json": {
        "id": "new-lab",
        "slug": "new-lab",
        "title": "New Lab",
        "mode": "labRift",
        "palette": "pulse",
        "instructions": "Move with arrows or WASD and collect objects.",
        "hud": {"modeLabel": "Collect Route"},
        "overlay": {"startTitle": "New Lab", "startCopy": "Greyboxed collection room.", "startAction": "Start Route"},
        "visuals": {**BASE_VISUALS, "spriteKey": "runnerShip", "accentSpriteKey": "shardCrystal", "hazardSpriteKey": "sentryDrone"},
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {
            "playerSpeed": 240,
            "shards": [{"x": 0.24, "y": 0.2}, {"x": 0.36, "y": 0.65}, {"x": 0.58, "y": 0.38}, {"x": 0.72, "y": 0.76}],
            "sentries": [{"x": 0.42, "y": 0.3, "rate": 1.2}, {"x": 0.66, "y": 0.58, "rate": 1.5}],
        },
    },
    "phaseDrop.template.json": {
        "id": "new-phase",
        "slug": "new-phase",
        "title": "New Phase",
        "mode": "phaseDrop",
        "palette": "pulse",
        "instructions": "Use left and right to swap lanes.",
        "hud": {"modeLabel": "Phase Shift"},
        "overlay": {"startTitle": "New Phase", "startCopy": "Greyboxed phase survival run.", "startAction": "Start Drop"},
        "visuals": {**BASE_VISUALS, "spriteKey": "padTile"},
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {"phases": ["#ff7a9e", "#67d5ff", "#b68cff"]},
    },
    "harbor.template.json": {
        "id": "new-harbor",
        "slug": "new-harbor",
        "title": "New Harbor",
        "mode": "harbor",
        "palette": "harbor",
        "instructions": "Steer with the cursor and collect markers.",
        "hud": {"modeLabel": "Drift Route"},
        "overlay": {"startTitle": "New Harbor", "startCopy": "Greyboxed harbor route.", "startAction": "Start Sail"},
        "visuals": {**BASE_VISUALS, "spriteKey": "boatSkiff", "accentSpriteKey": "buoyMarker"},
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {
            "buoys": [{"x": 0.18, "y": 0.24}, {"x": 0.34, "y": 0.56}, {"x": 0.62, "y": 0.34}, {"x": 0.78, "y": 0.68}],
            "currents": [{"x": -0.2, "y": 0.0}, {"x": 0.12, "y": 0.02}, {"x": -0.08, "y": -0.03}, {"x": 0.16, "y": 0.01}],
        },
    },
    "rhythm.template.json": {
        "id": "new-rhythm",
        "slug": "new-rhythm",
        "title": "New Rhythm",
        "mode": "rhythm",
        "palette": "pulse",
        "instructions": "Press Space as notes hit the marker.",
        "hud": {"modeLabel": "Hit Beats"},
        "overlay": {"startTitle": "New Rhythm", "startCopy": "Greyboxed timing line challenge.", "startAction": "Start Track"},
        "visuals": {**BASE_VISUALS, "spriteKey": "orbNode", "accentSpriteKey": "padTile"},
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {
            "loopDuration": 4,
            "beats": [{"time": 0.35}, {"time": 0.9}, {"time": 1.45}, {"time": 2.0}, {"time": 2.75}, {"time": 3.4}],
        },
    },
    "echo.template.json": {
        "id": "new-echo",
        "slug": "new-echo",
        "title": "New Echo",
        "mode": "echo",
        "palette": "pulse",
        "instructions": "Repeat the shown pattern with 1, 2, 3, and 4.",
        "hud": {"modeLabel": "Repeat Pattern"},
        "overlay": {"startTitle": "New Echo", "startCopy": "Greyboxed memory challenge.", "startAction": "Start Loop"},
        "visuals": {**BASE_VISUALS, "spriteKey": "padTile", "accentSpriteKey": "padTile"},
        **BASE_SHARED_UI,
        "meta": BASE_META,
        "content": {
            "pattern": [0, 2, 1, 3],
            "revealEvery": 0.65,
            "inputMap": {"1": 0, "2": 1, "3": 2, "4": 3},
            "padColors": ["#ff7a9e", "#67d5ff", "#b68cff", "#ffd873"],
        },
    },
}


if __name__ == "__main__":
    main()
