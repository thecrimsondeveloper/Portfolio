#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import textwrap
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_ROOT = Path("/Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages")
SEED_FILE = ROOT / ".ARCADE-SYSTEM" / "library" / "arcade-seed.json"
ARCADE_LIBRARY_FILE = PAGES_ROOT / "arcade-library.json"
PROMPT_CONFIG_FILE = ROOT / ".ARCADE-CLI" / "builder-frontier.json"
BRAINSTORM_CLI_FILE = ROOT / ".ARCADE-CLI" / "engines" / "brainstorm-core.py"
CHAINSUMMARY_CLI_FILE = ROOT / ".ARCADE-CLI" / "engines" / "summary-synth.py"
SEED_FETCHER_CLI_FILE = ROOT / ".ARCADE-CLI" / "engines" / "seed-fetcher.py"
ACTIVE_FRONTIER_MEMORY_PATH: Path | None = None
DEFAULT_LAUNCHER_PROMPT = "agent-start"
BRAINSTORM_STOPWORDS = {
	"about",
	"above",
	"across",
	"after",
	"against",
	"arcade",
	"around",
	"because",
	"before",
	"build",
	"complete",
	"dramatic",
	"during",
	"fight",
	"focus",
	"frame",
	"from",
	"game",
	"goal",
	"into",
	"mission",
	"new",
	"objective",
	"page",
	"playable",
	"player",
	"prototype",
	"readable",
	"same",
	"scope",
	"set",
	"small",
	"standalone",
	"story",
	"through",
	"turns",
	"using",
	"vivid",
	"with",
}

BRAINSTORM_SEED_CATEGORY_MAP = {
	"genres": "Genre Seeds",
	"cameraModes": "Camera Mode Seeds",
	"arenaShapes": "Arena Shape Seeds",
	"primaryVerbs": "Primary Verb Seeds",
	"scoringModels": "Scoring Model Seeds",
	"failureModes": "Failure Mode Seeds",
	"enemyBehaviors": "Enemy Behavior Seeds",
	"objectiveStructures": "Objective Structure Seeds",
	"resourceSystems": "Resource System Seeds",
	"levelProgression": "Level Progression Seeds",
	"twistConstraints": "Twist Constraint Seeds",
	"weatherEffects": "Weather Seeds",
	"uiAesthetics": "UI Seeds",
	"movementQuirks": "Movement Seeds",
	"environmentalHazards": "Hazard Seeds",
	"powerSources": "Power Seeds",
	"lightingStyles": "Lighting Seeds",
	"narrativeTone": "Tone Seeds",
	"deathAnimations": "Death Seeds",
	"crowdDynamics": "Crowd Seeds",
	"mapModifiers": "Map Seeds",
	"soundscapes": "Sound Seeds",
	"colorPalettes": "Color Seeds",
	"architecture": "Architecture Seeds",
	"artifactTypes": "Artifact Seeds",
	"gameTempo": "Tempo Seeds",
	"bossMechanics": "Boss Seeds",
	"playerPerks": "Perk Seeds",
	"enemyArchetypes": "Archetype Seeds",
	"narrativeStakes": "Stakes Seeds",
	"postProcessing": "Post-Process Seeds",
}


def slugify(value: str) -> str:
	value = value.lower().strip()
	value = re.sub(r"[^a-z0-9]+", "-", value)
	value = value.strip("-")
	return value or "new-game"


def humanize_identifier(value: str) -> str:
	text = re.sub(r"[_-]+", " ", str(value)).strip()
	text = re.sub(r"\s+", " ", text)
	return text.title() if text else "Untitled"


def load_env_file(env_path: Path) -> None:
	if not env_path.exists():
		return
	for line in env_path.read_text(encoding="utf-8").splitlines():
		line = line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_seed_data() -> dict:
	with open(SEED_FILE, "r", encoding="utf-8") as handle:
		return json.load(handle)


def sample_combination(seed: dict) -> dict:
	options = seed.get("options", {})
	rules = seed.get("randomGenerator", {}).get("sampleRules", {})
	combination = {}

	for key, count in rules.items():
		items = options.get(key, [])
		if not items:
			continue
		if count == 1:
			combination[key] = random.choice(items)
		else:
			combination[key] = random.sample(items, min(count, len(items)))

	return combination


def call_lm_studio_frontier(prompt: str, model: str, endpoint: str, system_prompt: str) -> str:
	payload = {
		"model": model,
		"messages": [
			{"role": "system", "content": system_prompt},
			{"role": "user", "content": prompt},
		],
		"temperature": 1.2,
		"max_tokens": 128,
	}
	request = urllib.request.Request(
		endpoint,
		data=json.dumps(payload).encode("utf-8"),
		headers={"Content-Type": "application/json"},
		method="POST",
	)
	try:
		with urllib.request.urlopen(request, timeout=30) as response:
			response_data = json.load(response)
			choices = response_data.get("choices", [])
			if choices:
				return choices[0].get("message", {}).get("content", "").strip()
	except Exception as e:
		print(f"  [!] LLM Call Error: {e}")
		pass
	return ""


def diversify_seed_library(seed_data: dict, combination: dict, model: str, endpoint: str) -> None:
	"""Asynchronously (conceptually) expand the global seed library with variants of the current sample."""
	print("\nDiversifying arcade-seed.json with new variants...")
	categories = ["themes", "environments", "characterMotivations", "coreLoops", "antagonists", "visualStyles", "weatherEffects", "uiAesthetics", "movementQuirks", "environmentalHazards", "powerSources", "lightingStyles", "narrativeTone", "deathAnimations", "crowdDynamics", "mapModifiers", "soundscapes", "colorPalettes", "architecture", "artifactTypes", "gameTempo", "bossMechanics", "playerPerks", "enemyArchetypes", "narrativeStakes", "postProcessing"]
	
	added_count = 0
	for cat in categories:
		current_options = seed_data.get("options", {}).get(cat, [])
		sampled_value = combination.get(cat)
		if not sampled_value:
			continue
		
		# Sampled value might be a list if count > 1
		sample_str = ", ".join(sampled_value) if isinstance(sampled_value, list) else str(sampled_value)
		
		prompt = (
			f"Given the category '{cat}' and the sampled items '{sample_str}', provide 5 new, wild, and creative variations for this category that are completely different from common tropes. "
			"The goal is high variety. Reply with a comma-separated list of exactly 5 unique items. No explanation."
		)
		print(f"  Requesting variants for {cat}...")
		response = call_lm_studio_frontier(prompt, model, endpoint, "You are a creative game designer pushing for maximum variety. Reply only with a comma-separated list of 5 items.")
		
		if response:
			print(f"  Raw response for {cat}: {response}")
			# Split by comma but also handle potential newlines or bullet points if the LLM ignores instructions
			raw_items = re.split(r"[,;|\n]+", response)
			new_items = [re.sub(r"^[-*0-9.\s]+", "", i).strip().lower() for i in raw_items if i.strip()]
			
			for item in new_items:
				if item and item not in current_options:
					seed_data["options"][cat].append(item)
					print(f"  [+] Added to {cat}: {item}")
					added_count += 1
		else:
			print(f"  [!] No response from LLM for {cat}.")
					
	if added_count > 0:
		write_json_file(SEED_FILE, seed_data)
		print(f"Successfully added {added_count} new options to the global library.")
	else:
		print("No new unique options were added this run.")


def format_combination(combination: dict) -> str:
	lines = ["Generated game seed combination:"]
	for key, value in combination.items():
		label = key.replace("camel", " ").replace("Motivations", " motivations").replace("Loops", " loops")
		label = re.sub(r"([a-z])([A-Z])", r"\1 \2", label).capitalize()
		if isinstance(value, list):
			value = ", ".join(value)
		lines.append(f"- {label}: {value}")
	return "\n".join(lines)


def load_frontier_prompt_config() -> dict:
	with open(PROMPT_CONFIG_FILE, "r", encoding="utf-8") as handle:
		return json.load(handle)


FRONTIER_PROMPT_CONFIG = load_frontier_prompt_config()


def render_prompt_lines(value: str | list[str]) -> str:
	if isinstance(value, list):
		return "\n".join(value).strip()
	return str(value).strip()


def compact_json(value) -> str:
	return json.dumps(value, ensure_ascii=False, indent=2)


def template_value(value) -> str:
	if isinstance(value, (dict, list)):
		return compact_json(value)
	return str(value)


def render_template(text: str, variables: dict) -> str:
	rendered = str(text)
	for key, value in variables.items():
		rendered = rendered.replace("{{" + key + "}}", template_value(value))
	return rendered


def get_stage_prompt(stage_id: str) -> dict:
	return FRONTIER_PROMPT_CONFIG.get("stagePrompts", {}).get(stage_id, {})


def get_launcher_prompt(prompt_name: str) -> dict:
	return FRONTIER_PROMPT_CONFIG.get("launcherPrompts", {}).get(prompt_name, {})


def render_stage_prompt(stage_id: str, variables: dict) -> str:
	stage_prompt = get_stage_prompt(stage_id)
	if not stage_prompt:
		return template_value(variables.get("taskPrompt", ""))
	context_packs = FRONTIER_PROMPT_CONFIG.get("contextPacks", {})
	shared_blocks = FRONTIER_PROMPT_CONFIG.get("sharedPromptBlocks", {})
	blocks = []
	for pack_name in stage_prompt.get("includeContextPacks", []):
		pack = context_packs.get(pack_name, []) or shared_blocks.get(pack_name, [])
		if pack:
			blocks.append(render_prompt_lines(pack))
	prompt_lines = stage_prompt.get("promptText", [])
	if prompt_lines:
		blocks.append(render_prompt_lines([render_template(line, variables) for line in prompt_lines]))
	return "\n\n".join(block for block in blocks if block.strip()).strip()


def render_launcher_prompt(prompt_name: str, variables: dict | None = None) -> str:
	variables = variables or {}
	launcher_prompt = get_launcher_prompt(prompt_name)
	if not launcher_prompt:
		return ""
	context_packs = FRONTIER_PROMPT_CONFIG.get("contextPacks", {})
	shared_blocks = FRONTIER_PROMPT_CONFIG.get("sharedPromptBlocks", {})
	blocks = []
	for pack_name in launcher_prompt.get("includeContextPacks", []):
		pack = context_packs.get(pack_name, []) or shared_blocks.get(pack_name, [])
		if pack:
			blocks.append(render_prompt_lines(pack))
	prompt_lines = launcher_prompt.get("promptText", [])
	if prompt_lines:
		blocks.append(render_prompt_lines([render_template(line, variables) for line in prompt_lines]))
	return "\n\n".join(block for block in blocks if block.strip()).strip()


def prompt_multiline(prompt: str, sentinel: str = "END") -> str:
	print("\n" + prompt)
	print(f"Enter text below. Finish by typing '{sentinel}' on its own line.")
	lines = []
	while True:
		try:
			line = input()
		except EOFError:
			line = sentinel
		if line.strip() == sentinel:
			break
		lines.append(line)
	return "\n".join(lines).strip()


def parse_structured_section(text: str, section_name: str) -> str:
	pattern = re.compile(
		rf"^{re.escape(section_name)}:\s*(.*?)(?=^Goal:|^Reasoning:|^Next Steps:|\Z)",
		re.IGNORECASE | re.MULTILINE | re.DOTALL,
	)
	match = pattern.search(text)
	if not match:
		return ""
	return match.group(1).strip()


def extract_goal_sentence(text: str) -> str:
	goal_text = parse_structured_section(text, "Goal")
	if not goal_text:
		return text.strip()
	first_line = goal_text.splitlines()[0].strip()
	return first_line


def extract_bullets(text: str, section_name: str) -> list[str]:
	section_text = parse_structured_section(text, section_name)
	if not section_text:
		section_text = text
	lines = []
	for line in section_text.splitlines():
		stripped = line.strip()
		if not stripped:
			continue
		if stripped.startswith("-"):
			lines.append(stripped.lstrip("- ").strip())
		else:
			lines.append(stripped)
	return lines


def prompt_short(prompt: str, default: str = "") -> str:
	prompt_text = f"{prompt} [{default}]: " if default else f"{prompt}: "
	try:
		value = input(prompt_text).strip()
	except EOFError:
		value = ""
	if value:
		return value
	if default:
		return default
	return ""


def prompt_yes_no_ai(prompt: str, default: str = "yes") -> str:
	normalized_default = "yes" if default.lower() in {"yes", "y", "1"} else "no"
	default_label = "1" if normalized_default == "yes" else "2"
	option_text = f"{prompt} [1=yes, 2=no] [{default_label}]: "

	def parse_choice(value: str):
		value = value.strip().lower()
		if not value:
			value = default_label
		if value in {"1", "yes", "y"}:
			return "yes"
		if value in {"2", "no", "n"}:
			return "no"
		return None
	try:
		choice = input(option_text).strip().lower()
	except EOFError:
		choice = ""

	normalized = parse_choice(choice)
	if normalized is None:
		print("Invalid choice. Please type 1 or 2.")
		return prompt_yes_no_ai(prompt, default=default)

	return normalized


def prompt_list(prompt: str, minimum_items: int = 0) -> list[str]:
	text = prompt_multiline(prompt)
	lines = [line.strip().lstrip("- ").strip() for line in text.splitlines() if line.strip()]
	if len(lines) >= minimum_items:
		return lines
	return lines


def prompt_csv_list(prompt: str, default: str = "") -> list[str]:
	value = prompt_short(prompt, default=default)
	return [item.strip() for item in value.split(",") if item.strip()]


def strip_markdown_fences(text: str) -> str:
	stripped = text.strip()
	if stripped.startswith("```"):
		lines = stripped.splitlines()
		if len(lines) >= 3 and lines[-1].strip() == "```":
			return "\n".join(lines[1:-1]).strip()
	return stripped


def parse_json_response(text: str):
	return json.loads(strip_markdown_fences(text))


def coerce_bool(value, default: bool = False) -> bool:
	if isinstance(value, bool):
		return value
	if isinstance(value, str):
		normalized = value.strip().lower()
		if normalized in {"true", "yes", "y", "1"}:
			return True
		if normalized in {"false", "no", "n", "2", "0"}:
			return False
	return default


def coerce_text(value, default: str = "") -> str:
	if value is None:
		return default
	text = str(value).strip()
	return text or default


def coerce_list(value, fallback: list[str] | None = None, minimum_items: int = 0) -> list[str]:
	items = []
	if isinstance(value, list):
		for item in value:
			text = coerce_text(item)
			if text:
				items.append(text)
	elif isinstance(value, str):
		for line in value.splitlines():
			text = line.strip().lstrip("- ").strip()
			if text:
				items.append(text)
	if len(items) >= minimum_items:
		return items
	fallback = fallback or []
	return [item for item in fallback if item.strip()]


def prompt_json_bundle(
	prompt: str,
	schema_name: str,
	schema_example: str,
	default,
	stage_id: str | None = None,
	target_dir: Path | None = None,
	extra_variables: dict | None = None,
):
	extra_variables = extra_variables or {}
	stage_prompt = render_stage_prompt(
		stage_id or "",
		{
			"taskPrompt": prompt,
			"schemaExample": schema_example,
			"frontierMemory": summarize_frontier_memory(),
			"repoContext": collect_repo_context(target_dir),
			**extra_variables,
		},
	) if stage_id else prompt
	response = prompt_multiline(
		f"{stage_prompt}\n\nReturn only valid JSON using this shape:\n{schema_example}"
	)
	try:
		payload = parse_json_response(response)
	except json.JSONDecodeError as exc:
		print(f"JSON parse failed for {schema_name}: {exc}. Falling back to defaults.")
		return default
	if isinstance(default, dict) and isinstance(payload, dict):
		merge_frontier_memory_update(stage_id or schema_name, payload.get("memoryUpdate"))
		return payload
	if isinstance(default, list) and isinstance(payload, list):
		return payload
	print(f"JSON payload type mismatch for {schema_name}. Falling back to defaults.")
	return default


def make_safe_filename(text: str) -> str:
	text = re.sub(r"[^a-zA-Z0-9 \-]+", "", text)
	text = text.strip().replace(" ", "-").lower()
	return text[:80] or "chapter"


def ensure_target_directory(folder_name: str, force: bool = False) -> Path:
	target_dir = PAGES_ROOT / folder_name
	if target_dir.exists() and any(target_dir.iterdir()):
		if not force:
			print(f"Warning: target directory '{target_dir}' already exists and is not empty.")
			confirm = input("Type 'yes' to continue and overwrite files inside, or press Enter to cancel: ").strip().lower()
			if confirm != "yes":
				raise SystemExit("Canceled by user.")
	else:
		target_dir.mkdir(parents=True, exist_ok=True)
	return target_dir


def write_text_file(path: Path, content: str) -> None:
	with open(path, "w", encoding="utf-8") as handle:
		handle.write(content)


def write_json_file(path: Path, data: dict) -> None:
	with open(path, "w", encoding="utf-8") as handle:
		json.dump(data, handle, indent=2, ensure_ascii=False)
		handle.write("\n")


def load_json_file(path: Path, default):
	if not path.exists():
		return default
	try:
		with open(path, "r", encoding="utf-8") as handle:
			return json.load(handle)
	except Exception:
		return default


def collect_repo_context(target_dir: Path | None = None) -> dict:
	manifest = load_arcade_library_manifest()
	entries = manifest.get("entries", []) if isinstance(manifest.get("entries"), list) else []
	game_files = []
	if target_dir and target_dir.exists():
		game_files = sorted(path.name for path in target_dir.iterdir() if path.is_file())[:24]
	return {
		"pagesRoot": str(PAGES_ROOT),
		"targetFolder": str(target_dir) if target_dir else "",
		"targetFiles": game_files,
		"arcadeLibraryFile": str(ARCADE_LIBRARY_FILE),
		"arcadeEntryCount": len(entries),
		"recentArcadeEntries": [
			{
				"slug": item.get("slug"),
				"title": item.get("title"),
				"pagePath": item.get("pagePath"),
				"metadataPath": item.get("metadataPath"),
			}
			for item in entries[-8:]
			if isinstance(item, dict)
		],
		"stableConventions": [
			"Generated games live under Portfolio-Vite/Pages/<slug>/.",
			"Each generated game keeps index.html, game.js, story-structure.json, and <slug>.json in its own folder.",
			"Pages/arcade-library.json is the discoverability manifest for the arcade player and library.",
		],
	}


def create_frontier_memory(target_dir: Path, title: str, profile: dict, brainstorm_artifacts: dict, combination: dict) -> Path:
	memory_path = target_dir / "frontier-memory.json"
	if memory_path.exists():
		return memory_path
	memory = {
		"gameTitle": title,
		"profile": profile,
		"canonicalPaths": {
			"targetDir": str(target_dir),
			"brainstormSeed": str(brainstorm_artifacts.get("seed_path", "")),
			"brainstormSummary": str(brainstorm_artifacts.get("summary_path", "")),
			"finalBrainstorm": str(brainstorm_artifacts.get("final_path", "")),
			"story": str(target_dir / "story-structure.json"),
			"gameScript": str(target_dir / "game.js"),
		},
		"seedCombination": combination,
		"stageHistory": [],
		"decisions": [],
		"rejectedIdeas": [],
		"openIssues": [],
		"nextStageNotes": [],
	}
	write_json_file(memory_path, memory)
	return memory_path


def summarize_frontier_memory(memory_path: Path | None = None) -> dict:
	path = memory_path or ACTIVE_FRONTIER_MEMORY_PATH
	memory = load_json_file(path, {}) if path else {}
	return {
		"gameTitle": memory.get("gameTitle"),
		"profile": memory.get("profile", {}),
		"canonicalPaths": memory.get("canonicalPaths", {}),
		"recentStageHistory": memory.get("stageHistory", [])[-6:],
		"decisions": memory.get("decisions", [])[-10:],
		"rejectedIdeas": memory.get("rejectedIdeas", [])[-10:],
		"openIssues": memory.get("openIssues", [])[-10:],
		"nextStageNotes": memory.get("nextStageNotes", [])[-10:],
	}


def extend_unique(existing: list, additions) -> list:
	result = list(existing) if isinstance(existing, list) else []
	items = additions if isinstance(additions, list) else [additions]
	for item in items:
		if item in (None, "", [], {}):
			continue
		if item not in result:
			result.append(item)
	return result


def merge_frontier_memory_update(stage_id: str, update, memory_path: Path | None = None) -> None:
	path = memory_path or ACTIVE_FRONTIER_MEMORY_PATH
	if not path or not isinstance(update, dict):
		return
	memory = load_json_file(path, {})
	if not memory:
		return
	if isinstance(update.get("decisions"), list):
		memory["decisions"] = extend_unique(memory.get("decisions", []), update["decisions"])[-40:]
	if isinstance(update.get("rejectedIdeas"), list):
		memory["rejectedIdeas"] = extend_unique(memory.get("rejectedIdeas", []), update["rejectedIdeas"])[-40:]
	if isinstance(update.get("openIssues"), list):
		memory["openIssues"] = extend_unique(memory.get("openIssues", []), update["openIssues"])[-40:]
	if isinstance(update.get("nextStageNotes"), list):
		memory["nextStageNotes"] = extend_unique(memory.get("nextStageNotes", []), update["nextStageNotes"])[-40:]
	if isinstance(update.get("profilePatch"), dict):
		profile = memory.get("profile", {})
		if isinstance(profile, dict):
			profile.update(update["profilePatch"])
			memory["profile"] = profile
	memory["stageHistory"] = extend_unique(
		memory.get("stageHistory", []),
		[{"stage": stage_id, "event": "memoryUpdate", "summary": update.get("summary", "frontier memory updated")}],
	)[-60:]
	write_json_file(path, memory)


def record_frontier_stage(stage_id: str, summary: str, memory_path: Path | None = None) -> None:
	path = memory_path or ACTIVE_FRONTIER_MEMORY_PATH
	if not path:
		return
	memory = load_json_file(path, {})
	if not memory:
		return
	memory["stageHistory"] = extend_unique(
		memory.get("stageHistory", []),
		[{"stage": stage_id, "event": "stage", "summary": summary}],
	)[-60:]
	write_json_file(path, memory)


def write_markdown_sections(path: Path, title: str, sections: list[tuple[str, str]]) -> None:
	parts = [f"# {title}", ""]
	for heading, body in sections:
		parts.append(f"## {heading}")
		parts.append("")
		parts.append((body or "(No content recorded.)").strip())
		parts.append("")
	write_text_file(path, "\n".join(parts).rstrip() + "\n")


def format_list(items: list[str], fallback: str) -> str:
	clean_items = [item.strip() for item in items if item.strip()]
	if not clean_items:
		return f"- {fallback}"
	return "\n" + "\n".join(f"- {item}" for item in clean_items)


def join_inline(items: list[str], fallback: str) -> str:
	clean_items = [item.strip() for item in items if item.strip()]
	return ", ".join(clean_items) if clean_items else fallback


def create_design_file(target_dir: Path, design_text: str) -> None:
	design_path = target_dir / "DESIGN.md"
	content = textwrap.dedent(
		f"""
		# DESIGN

		{design_text}
		"""
	)
	write_text_file(design_path, content)
	print(f"Saved design spec to {design_path}")


def create_seed_choice_file(target_dir: Path, combination: dict) -> None:
	seed_path = target_dir / "seed-choice.json"
	write_json_file(seed_path, combination)
	print(f"Saved chosen seed payload to {seed_path}")


def create_ideation_file(target_dir: Path, title: str, combination: dict, expansion_text: str) -> None:
	ideation_path = target_dir / "IDEATION.md"
	content = textwrap.dedent(
		f"""
		# IDEATION

		## {title}

		### Seed Summary
		{format_combination(combination)}

		### Expansion Ideas
		{expansion_text}

		Use these expansion ideas as the basis for the fuller design captured in DESIGN.md.
		"""
	)
	write_text_file(ideation_path, content)
	print(f"Saved ideation notes to {ideation_path}")


def create_action_extraction_file(target_dir: Path, title: str, concept: dict) -> None:
	content = textwrap.dedent(
		f"""
		# ACTION EXTRACTION

		## {title}

		### Action Map
		{format_list(concept['action_map'], 'Define the core actions.')}

		### Detail Items
		{format_list(concept['detail_items'], 'Define the prototype details.')}

		### Collapsed Build Summary
		{format_list(concept['collapsed_tasks'], 'Define the build tasks.')}
		"""
	)
	path = target_dir / "ACTION-EXTRACTION.md"
	write_text_file(path, content)
	print(f"Saved action extraction to {path}")


def format_fractal_branches(branches: list[dict]) -> str:
	if not branches:
		return "- No branch slices defined yet."
	sections = []
	for branch in branches:
		branch_name = branch.get("branch", "Unnamed branch")
		tasks = branch.get("tasks", [])
		section = f"- {branch_name}\n" + "\n".join(f"  - {task}" for task in tasks)
		sections.append(section)
	return "\n".join(sections)


def format_feature_packets_for_design(feature_packets: list[dict]) -> str:
	if not feature_packets:
		return "- No sprint branches defined yet."
	sections = []
	for packet in feature_packets:
		sections.append(
			textwrap.dedent(
				f"""
				### {packet['feature']}

				- Player promise: {packet['player_promise']}
				- Sprint objective: {packet['sprint_objective']}
				- Change packet scope: {join_inline(packet['scope'], 'Define packet scope.')}
				- Simulated checkpoints: {join_inline(packet['checkpoints'], 'Define checkpoints.')}

				#### Detail Fractalization
				{format_fractal_branches(packet['branches'])}
				"""
			).strip()
		)
	return "\n\n".join(sections)


def create_feature_branch_files(target_dir: Path, feature_packets: list[dict]) -> None:
	sprint_dir = target_dir / "sprint-builder"
	sprint_dir.mkdir(parents=True, exist_ok=True)

	index_lines = ["# Sprint Builder", "", "Feature branches for the next isolated implementation sprint.", ""]

	for index, packet in enumerate(feature_packets, start=1):
		filename = f"{index:02d}-{make_safe_filename(packet['feature'])}-change-packet.md"
		path = sprint_dir / filename
		content = textwrap.dedent(
			f"""
			# {packet['feature']} Change Packet

			## Sprint Objective

			{packet['sprint_objective']}

			## Player Promise

			{packet['player_promise']}

			## Why This Branch Exists

			{packet['branch_reason']}

			## Detail Fractalization

			{format_fractal_branches(packet['branches'])}

			## Simulated Checkpoints

			{format_list(packet['checkpoints'], 'Define simulated checkpoints.')}

			## Acceptance Signals

			{format_list(packet['acceptance'], 'Define acceptance signals.')}

			## Change Packet Scope

			{format_list(packet['scope'], 'Define packet scope.')}

			## Risks And Unknowns

			{format_list(packet['risks'], 'Define risks and unknowns.')}

			## Implementation Notes

			- Keep this packet isolated to the current game folder.
			- Use the checkpoints as simulated gates before full implementation.
			- Treat each branch slice as a sub-sprint, not as a merged refactor.
			"""
		).strip() + "\n"
		write_text_file(path, content)
		index_lines.append(f"- [{packet['feature']}](./{filename})")
		print(f"Created sprint change packet at {path}")

	write_text_file(sprint_dir / "README.md", "\n".join(index_lines) + "\n")
	print(f"Created sprint builder index at {sprint_dir / 'README.md'}")


def create_implementation_chapters(target_dir: Path, chapters_text: str) -> None:
	implementation_dir = target_dir / "implementation"
	implementation_dir.mkdir(parents=True, exist_ok=True)
	chapter_lines = [line.strip() for line in chapters_text.splitlines() if line.strip()]

	if not chapter_lines:
		chapter_lines = [
			"Game setup and core loop",
			"Movement and player controls",
			"Pressure and fail states",
			"Progression and rewards",
			"Presentation and story framing",
		]
		print("No chapters were entered, so default implementation chapters were created.")

	for index, chapter in enumerate(chapter_lines, start=1):
		filename = f"{index:02d}-{make_safe_filename(chapter)}.md"
		chapter_path = implementation_dir / filename
		write_text_file(chapter_path, f"# {chapter}\n\nWrite the implementation plan for this chapter here.\n")
		print(f"Created implementation chapter {chapter_path}")

	index_path = implementation_dir / "README.md"
	index_content = "# Implementation Chapters\n\n" + "\n".join(
		f"- [{chapter}](./{index:02d}-{make_safe_filename(chapter)}.md)" for index, chapter in enumerate(chapter_lines, start=1)
	)
	write_text_file(index_path, index_content)
	print(f"Created implementation index at {index_path}")


def scan_existing_pages() -> list[dict]:
	pages = []
	for child in PAGES_ROOT.iterdir():
		if not child.is_dir():
			continue
		existing = {"folder": child.name, "title": None, "description": None}
		story_file = child / "story-structure.json"
		if story_file.exists():
			try:
				with open(story_file, "r", encoding="utf-8") as handle:
					data = json.load(handle)
				existing["title"] = data.get("title")
				existing["description"] = data.get("description")
			except Exception:
				pass
		if not existing["title"]:
			design_file = child / "DESIGN.md"
			if design_file.exists():
				try:
					lines = design_file.read_text(encoding="utf-8").splitlines()
					if lines:
						existing["title"] = lines[0].lstrip("# ").strip()
						if len(lines) > 1:
							existing["description"] = lines[1].strip()
				except Exception:
					pass
		if existing["title"] or existing["description"]:
			pages.append(existing)
	return pages


def similarity_score(text_a: str, text_b: str) -> float:
	a_words = set(re.findall(r"[a-z]{4,}", text_a.lower()))
	b_words = set(re.findall(r"[a-z]{4,}", text_b.lower()))
	if not a_words or not b_words:
		return 0.0
	common = a_words & b_words
	return len(common) / max(len(a_words), len(b_words))


def find_similar_pages(title: str, description: str, pages: list[dict]) -> list[dict]:
	candidates = []
	source_text = f"{title} {description}".lower()
	for page in pages:
		existing_text = " ".join(filter(None, [page.get("title", ""), page.get("description", "")]))
		score = similarity_score(source_text, existing_text)
		if score >= 0.15:
			candidates.append(
				{
					"folder": page["folder"],
					"title": page.get("title"),
					"description": page.get("description"),
					"score": score,
				}
			)
	return sorted(candidates, key=lambda item: item["score"], reverse=True)


def confirm_unique_idea(title: str, description: str, pages: list[dict], force: bool = False) -> bool:
	if force:
		print(f"Skipping uniqueness check for '{title}' due to force flag.")
		return True
	similar = find_similar_pages(title, description, pages)
	if not similar:
		return True
	print("\nExisting Pages with potentially similar ideas:")
	for item in similar[:5]:
		print(f"- {item['folder']}: {item['title']} — {item['description']} (similarity {item['score']:.2f})")
	decision = prompt_yes_no_ai(
		"Does this idea look unique enough?",
		default="yes",
	)
	return decision == "yes"


def create_fun_check_file(target_dir: Path, assessment: str, fun_needs: list[str]) -> None:
	fun_path = target_dir / "FUN-CHECK.md"
	content = textwrap.dedent(
		f"""
		# FUN CHECK

		**Is this a fun game?**
		{assessment}

		**Things needed to make this game fun:**
		{format_list(fun_needs, 'Add a clearer fun checklist.')}
		"""
	)
	write_text_file(fun_path, content)
	print(f"Saved fun checklist to {fun_path}")


def append_fun_section_to_design(design_text: str, assessment: str, fun_needs: list[str]) -> str:
	fun_section = textwrap.dedent(
		f"""
		## Fun Game Assessment

		- Assessment: {assessment}

		### Things Needed To Make This Game Fun
		{format_list(fun_needs, 'Add a clearer fun checklist.')}
		"""
	)
	return design_text.rstrip() + "\n\n" + fun_section.strip() + "\n"


def update_game_concept_spec(
	target_dir: Path,
	title: str,
	description: str,
	objective: str,
	combination: dict,
	concept: dict,
	fun_assessment: str = "",
	fun_needs: list[str] | None = None,
) -> None:
	fun_needs = fun_needs or []
	write_markdown_sections(
		target_dir / "GAME-CONCEPT-SPEC.md",
		"Game Concept Spec",
		[
			(
				"Identity",
				textwrap.dedent(
					f"""
					- Title: {title}
					- Description: {description}
					- Objective: {objective}
					- Distinctiveness: {concept['uniqueness']}
					"""
				).strip(),
			),
			("Seed Summary", format_combination(combination)),
			("Core Fantasy", concept["hook"]),
			("Player Actions", format_list(concept["player_actions"], "Define the player actions.")),
			("Core Loop Beats", format_list(concept["loop_beats"], "Define the core loop beats.")),
			("Threats And Pressure", format_list(concept["pressure"], "Define the threats and pressure.")),
			("Rewards And Progression", format_list(concept["rewards"], "Define the rewards and progression.")),
			("Fail States", format_list(concept["fail_states"], "Define the fail states.")),
			("Visual Identity", format_list(concept["visual_identity"], "Define the visual identity.")),
			("Controls And HUD", format_list(concept["controls"], "Define the controls and HUD notes.")),
			("JSON Data Hooks", format_list(concept["data_hooks"], "Define the JSON hooks.")),
			("Story Intro", concept["story_intro"]),
			("HUD Status Message", concept["status_message"]),
			(
				"Fun Check",
				textwrap.dedent(
					f"""
					- Assessment: {fun_assessment or '(Pending fun assessment.)'}
					- Fun needs:
					{format_list(fun_needs, 'Pending fun-needs list.')}
					"""
				).strip(),
			),
		],
	)
	print(f"Updated concept spec at {target_dir / 'GAME-CONCEPT-SPEC.md'}")


def format_feature_packet_markdown(packet: dict) -> str:
	return textwrap.dedent(
		f"""
		### {packet['feature']}

		- Sprint objective: {packet['sprint_objective']}
		- Player promise: {packet['player_promise']}
		- Branch reason: {packet['branch_reason']}

		#### Branch Slices
		{format_fractal_branches(packet['branches'])}

		#### Checkpoints
		{format_list(packet['checkpoints'], 'Define checkpoints.')}

		#### Acceptance Signals
		{format_list(packet['acceptance'], 'Define acceptance signals.')}

		#### Scope
		{format_list(packet['scope'], 'Define scope.')}

		#### Risks
		{format_list(packet['risks'], 'Define risks.')}
		"""
	).strip()


def update_feature_sprint_spec(target_dir: Path, feature_packets: list[dict], active_payload: dict | None = None) -> None:
	active_payload = active_payload or {}
	active_packet = active_payload.get("active_packet") or {}
	packet_sections = "\n\n".join(format_feature_packet_markdown(packet) for packet in feature_packets) or "- No feature packets recorded."
	active_context = textwrap.dedent(
		f"""
		- Active feature: {active_payload.get('active_feature', '(Pending active feature selection.)')}
		- Active packet reason: {active_payload.get('active_packet_reason', '(Pending active packet reasoning.)')}
		- Active sprint objective: {active_packet.get('sprint_objective', '(Pending active sprint objective.)')}
		- Active player promise: {active_packet.get('player_promise', '(Pending active player promise.)')}
		- Current pass goal: {active_payload.get('pass_goal', '(Pending pass goal.)')}
		"""
	).strip()
	write_markdown_sections(
		target_dir / "FEATURE-SPRINT-SPEC.md",
		"Feature Sprint Spec",
		[("All Feature Packets", packet_sections), ("Active Packet Context", active_context)],
	)
	print(f"Updated feature sprint spec at {target_dir / 'FEATURE-SPRINT-SPEC.md'}")


def update_build_spec(target_dir: Path, chapters: list[str], sprint_goal: str = "", payload: dict | None = None) -> None:
	payload = payload or {}
	file_targets = payload.get("file_targets", [])
	patch_specs = payload.get("patch_specs", [])
	file_target_sections = []
	for file_target in file_targets:
		file_target_sections.append(
			textwrap.dedent(
				f"""
				### {file_target['file']}

				- Action: {file_target['action']}
				- Reason: {file_target['reason']}
				- Unchanged: {file_target['unchanged']}
				"""
			).strip()
		)
	patch_sections = []
	for patch_spec in patch_specs:
		patch_sections.append(
			textwrap.dedent(
				f"""
				### {patch_spec['file']}

				- Problem: {patch_spec['problem']}
				- Intended behavior: {patch_spec['intended_behavior']}
				- Specific change: {patch_spec['specific_change']}
				- Invariants: {patch_spec['invariants']}
				- Patch units:
				{format_list(patch_spec['patch_units'], 'No patch units recorded.')}
				"""
			).strip()
		)
	implementation_sequence = textwrap.dedent(
		f"""
		- Sprint goal: {sprint_goal or '(Pending sprint goal.)'}
		- Pass goal: {payload.get('pass_goal', '(Pending pass goal.)')}
		- Active feature: {payload.get('active_feature', '(Pending active feature.)')}
		- Plan steps:
		{format_list(payload.get('plan_steps', []), 'Pending implementation plan.')}

		- Simulated checkpoints:
		{format_list(payload.get('checkpoints', []), 'Pending checkpoints.')}

		- Implementation actions:
		{format_list(payload.get('implementation_actions', []), 'Pending implementation actions.')}

		- Implementation notes:
		{payload.get('implementation_notes', '(Pending implementation notes.)')}
		"""
	).strip()
	write_markdown_sections(
		target_dir / "BUILD-SPEC.md",
		"Build Spec",
		[
			("Implementation Chapters", format_list(chapters, 'Pending implementation chapters.')),
			("Targeted Files", "\n\n".join(file_target_sections) if file_target_sections else "- Pending file targets."),
			("Patch Specs", "\n\n".join(patch_sections) if patch_sections else "- Pending patch specs."),
			("Implementation Sequence", implementation_sequence),
		],
	)
	print(f"Updated build spec at {target_dir / 'BUILD-SPEC.md'}")


def update_validation_spec(target_dir: Path, validation_state: dict) -> None:
	write_markdown_sections(
		target_dir / "VALIDATION-SPEC.md",
		"Validation Spec",
		[
			(
				"Gate Checks",
				textwrap.dedent(
					f"""
					- Loop: {validation_state.get('loop_index', '(Pending loop index.)')}
					- HTML rewrite gate: {validation_state.get('html_rewrite_gate', '(Pending HTML gate.)')}
					- JSON rewrite gate: {validation_state.get('json_rewrite_gate', '(Pending JSON gate.)')}
					- Review assessment: {validation_state.get('review_assessment', '(Pending review assessment.)')}
					- Continue gate: {validation_state.get('continue_gate', '(Pending continue gate.)')}
					"""
				).strip(),
			),
			("Pass Fail Reasons", format_list(validation_state.get('issues', []), 'No validation issues recorded.')),
			("Repair Sequence", format_list(validation_state.get('breakdown', []), 'No repair sequence recorded.')),
			("Unresolved Issues", format_list(validation_state.get('review_notes', []), 'No unresolved issues recorded.')),
			("Next Pass Focus", format_list(validation_state.get('next_focus', []), 'No next-pass focus recorded.')),
		],
	)
	print(f"Updated validation spec at {target_dir / 'VALIDATION-SPEC.md'}")


def load_arcade_library_manifest() -> dict:
	if not ARCADE_LIBRARY_FILE.exists():
		return {"entries": []}
	with open(ARCADE_LIBRARY_FILE, "r", encoding="utf-8") as handle:
		return json.load(handle)


def build_arcade_library_entry(folder_name: str, title: str) -> dict:
	return {
		"slug": folder_name,
		"title": title,
		"section": "prototypes",
		"pagePath": f"Pages/{folder_name}/",
		"metadataPath": f"Pages/{folder_name}/{folder_name}.json",
	}


def build_arcade_metadata(folder_name: str, title: str, description: str, concept: dict) -> dict:
	build_packet = concept.get("build_packet", {}) if isinstance(concept.get("build_packet"), dict) else {}
	overlay = build_packet.get("overlay", {}) if isinstance(build_packet.get("overlay"), dict) else {}
	hud = build_packet.get("hud", {}) if isinstance(build_packet.get("hud"), dict) else {}
	page_identity = concept.get("page_identity", {}) if isinstance(concept.get("page_identity"), dict) else {}
	profile = concept.get("game_design_profile", {}) if isinstance(concept.get("game_design_profile"), dict) else {}
	instructions = join_inline(concept.get("controls", [])[:3], "Use WASD or Arrow keys to move, Shift to dash, and Space to pulse.")
	summary = coerce_text(page_identity.get("description"), description)
	start_copy = coerce_text(overlay.get("introBriefing"), concept.get("story_intro", summary))
	hud_objective = coerce_text(hud.get("objective"), concept.get("status_message", summary))
	return {
		"id": folder_name,
		"title": title,
		"summary": summary,
		"mode": "arcade-action",
		"palette": slugify(title),
		"instructions": instructions,
		"hud": {
			"modeLabel": title,
			"objective": hud_objective,
		},
		"overlay": {
			"startTitle": coerce_text(overlay.get("introTitle"), title),
			"startCopy": start_copy,
			"startAction": "Launch Game",
		},
			"content": {
				"hook": concept.get("hook", summary),
				"actions": concept.get("player_actions", [])[:3],
				"pressure": concept.get("pressure", [])[:3],
				"rewards": concept.get("rewards", [])[:3],
				"runtimeTemplate": profile.get("runtimeTemplate", "arena_survival"),
				"mechanicFamily": profile.get("mechanicFamily", "arena survival"),
			},
		"image": "",
	}


def collect_arcade_integration_review(target_dir: Path, folder_name: str, title: str, description: str, concept: dict) -> dict:
	manifest = load_arcade_library_manifest()
	entries = manifest.get("entries", []) if isinstance(manifest.get("entries"), list) else []
	existing_entry = next((entry for entry in entries if isinstance(entry, dict) and entry.get("slug") == folder_name), None)
	metadata_path = target_dir / f"{folder_name}.json"
	gaps = []
	if existing_entry is None:
		gaps.append("Arcade library entry is missing from Pages/arcade-library.json.")
	if not metadata_path.exists():
		gaps.append(f"Arcade metadata file is missing at {metadata_path.name}.")
	if not (target_dir / "index.html").exists():
		gaps.append("Generated page is missing index.html.")
	if not (target_dir / "story-structure.json").exists():
		gaps.append("Generated page is missing story-structure.json.")

	return {
		"observed_pattern": [
			"Arcade player and library load entries from Pages/arcade-library.json.",
			"Each entry needs slug, title, section, pagePath, and metadataPath.",
			"Per-game metadata JSON is loaded from metadataPath and supplies title and optional image data for arcade UI surfaces.",
			"A generated game only needs a live page folder, a metadata JSON file, and a manifest entry to become selectable in the arcade player and library.",
		],
		"required_files": [
			"Pages/arcade-library.json",
			f"Pages/{folder_name}/{folder_name}.json",
			f"Pages/{folder_name}/index.html",
			f"Pages/{folder_name}/story-structure.json",
		],
		"required_fields": [
			"slug",
			"title",
			"section",
			"pagePath",
			"metadataPath",
			"metadata.title",
			"metadata.instructions",
		],
		"invariants": [
			"Keep pagePath rooted at Pages/<slug>/ so the arcade iframe can load the generated page directly.",
			"Keep metadataPath inside the generated page folder so the library can resolve game-specific metadata without extra routing.",
			"Do not require direct edits to arcade UI code when a new entry follows the manifest and metadata pattern.",
		],
		"gaps": gaps,
		"entry_preview": build_arcade_library_entry(folder_name, title),
		"metadata_preview": build_arcade_metadata(folder_name, title, description, concept),
		"existing_entry": existing_entry,
	}


def create_arcade_integration_pass_files(target_dir: Path, pass_index: int, review_state: dict, ensure_state: dict) -> None:
	arcade_dir = target_dir / "arcade-integration"
	arcade_dir.mkdir(parents=True, exist_ok=True)
	review_path = arcade_dir / f"pass-{pass_index:02d}-review.md"
	ensure_path = arcade_dir / f"pass-{pass_index:02d}-ensure.md"
	remaining_gaps = ensure_state.get("remaining_gaps", review_state.get("gaps", []))
	write_markdown_sections(
		review_path,
		f"Arcade Integration Review Pass {pass_index:02d}",
		[
			("Observed Pattern", format_list(review_state.get("observed_pattern", []), "No pattern recorded.")),
			("Required Files", format_list(review_state.get("required_files", []), "No required files recorded.")),
			("Required Fields", format_list(review_state.get("required_fields", []), "No required fields recorded.")),
			("Invariants", format_list(review_state.get("invariants", []), "No invariants recorded.")),
			("Gaps", format_list(remaining_gaps, "No integration gaps remain.")),
		],
	)
	write_markdown_sections(
		ensure_path,
		f"Arcade Integration Ensure Pass {pass_index:02d}",
		[
			("Registration Changes", format_list(ensure_state.get("registration_changes", []), "No registration changes recorded.")),
			("Verification Notes", format_list(ensure_state.get("verification_notes", []), "No verification notes recorded.")),
			("Continue Gate", f"- {ensure_state.get('continue_gate', 'Stop')}"),
		],
	)
	print(f"Saved arcade integration pass files to {arcade_dir}")


def update_arcade_integration_spec(target_dir: Path, review_state: dict, ensure_state: dict) -> None:
	write_markdown_sections(
		target_dir / "ARCADE-INTEGRATION-SPEC.md",
		"Arcade Integration Spec",
		[
			("Initial Review Gaps", format_list(review_state.get("gaps", []), "No initial integration gaps were found.")),
			("Observed Pattern", format_list(review_state.get("observed_pattern", []), "No arcade pattern recorded.")),
			("Required Files", format_list(review_state.get("required_files", []), "No required files recorded.")),
			("Required Fields", format_list(review_state.get("required_fields", []), "No required fields recorded.")),
			("Invariants", format_list(review_state.get("invariants", []), "No invariants recorded.")),
			("Open Gaps", format_list(ensure_state.get("remaining_gaps", review_state.get("gaps", [])), "No open integration gaps remain.")),
			("Registration Changes", format_list(ensure_state.get("registration_changes", []), "No registration changes recorded.")),
			("Verification Notes", format_list(ensure_state.get("verification_notes", []), "No verification notes recorded.")),
			("Continue Gate", f"- {ensure_state.get('continue_gate', 'Stop')}"),
		],
	)
	print(f"Updated arcade integration spec at {target_dir / 'ARCADE-INTEGRATION-SPEC.md'}")


def ensure_arcade_registration(target_dir: Path, folder_name: str, title: str, description: str, concept: dict, review_state: dict) -> dict:
	manifest = load_arcade_library_manifest()
	entries = manifest.get("entries", []) if isinstance(manifest.get("entries"), list) else []
	metadata = build_arcade_metadata(folder_name, title, description, concept)
	metadata_path = target_dir / f"{folder_name}.json"
	write_json_file(metadata_path, metadata)

	entry = build_arcade_library_entry(folder_name, title)
	entry_index = next((index for index, item in enumerate(entries) if isinstance(item, dict) and item.get("slug") == folder_name), None)
	registration_changes = [f"Wrote arcade metadata to {metadata_path}."]
	if entry_index is None:
		entries.append(entry)
		registration_changes.append(f"Added {folder_name} to {ARCADE_LIBRARY_FILE}.")
	else:
		entries[entry_index] = entry
		registration_changes.append(f"Updated existing {folder_name} entry in {ARCADE_LIBRARY_FILE}.")
	manifest["entries"] = sorted(entries, key=lambda item: coerce_text(item.get("title"), item.get("slug", "")).lower())
	write_json_file(ARCADE_LIBRARY_FILE, manifest)

	reloaded_manifest = load_arcade_library_manifest()
	reloaded_entries = reloaded_manifest.get("entries", []) if isinstance(reloaded_manifest.get("entries"), list) else []
	verified_entry = next((item for item in reloaded_entries if isinstance(item, dict) and item.get("slug") == folder_name), None)
	verification_notes = []
	remaining_gaps = []
	if verified_entry:
		verification_notes.append(f"Arcade library manifest resolves the {folder_name} entry.")
	else:
		verification_notes.append(f"Arcade library manifest is still missing the {folder_name} entry.")
		remaining_gaps.append(f"Arcade library manifest is still missing the {folder_name} entry.")
	if metadata_path.exists():
		verification_notes.append(f"Arcade metadata file exists at {metadata_path}.")
	else:
		verification_notes.append(f"Arcade metadata file is missing at {metadata_path}.")
		remaining_gaps.append(f"Arcade metadata file is missing at {metadata_path}.")
	if (target_dir / "index.html").exists() and (target_dir / "story-structure.json").exists():
		verification_notes.append("Generated page contains index.html and story-structure.json for arcade launch.")
	else:
		remaining_gaps.append("Generated page is missing index.html or story-structure.json for arcade launch.")
	continue_gate = "Continue" if remaining_gaps else "Stop"
	return {
		"registration_changes": registration_changes,
		"verification_notes": verification_notes,
		"remaining_gaps": remaining_gaps,
		"continue_gate": continue_gate,
	}


def run_arcade_integration_loops(target_dir: Path, folder_name: str, title: str, description: str, concept: dict, default_passes: int = 1) -> None:
	if default_passes <= 0:
		update_arcade_integration_spec(
			target_dir,
			{
				"observed_pattern": [],
				"required_files": [],
				"required_fields": [],
				"invariants": [],
				"gaps": ["Arcade integration loop was skipped."],
			},
			{
				"registration_changes": [],
				"verification_notes": ["Arcade integration loop was skipped."],
				"continue_gate": "Stop",
			},
		)
		return

	print("\nSTAGE 10: Run the arcade integration review and ensure loop.")
	for pass_index in range(1, default_passes + 1):
		review_state = collect_arcade_integration_review(target_dir, folder_name, title, description, concept)
		ensure_state = ensure_arcade_registration(target_dir, folder_name, title, description, concept, review_state)
		create_arcade_integration_pass_files(target_dir, pass_index, review_state, ensure_state)
		update_arcade_integration_spec(target_dir, review_state, ensure_state)
		if ensure_state.get("continue_gate") != "Continue":
			print("Arcade integration loop completed successfully.")
			return

	print("Arcade integration loop reached the configured pass limit before the continue gate closed.")


def parse_session_length_minutes(session_length: str, default: int = 8) -> int:
	match = re.search(r"(\d+)", session_length or "")
	if not match:
		return default
	return max(1, int(match.group(1)))


def runtime_template(profile: dict | None) -> str:
	if not isinstance(profile, dict):
		return "arena_survival"
	template = coerce_text(profile.get("runtimeTemplate"), "arena_survival")
	return template if template in {"arena_survival", "route_runner", "stealth_patrol", "relay_chain", "extraction_maze"} else "arena_survival"


def apply_runtime_template_scene(scene: dict, profile: dict | None) -> dict:
	template = runtime_template(profile)
	scene["profile"] = profile or {}
	scene["rules"]["runtimeTemplate"] = template
	scene["rules"]["mechanicFamily"] = coerce_text((profile or {}).get("mechanicFamily"), template.replace("_", " "))
	scene["rules"]["spatialStructure"] = coerce_text((profile or {}).get("spatialStructure"), "arena")
	scene["rules"]["scoreLabel"] = {
		"arena_survival": "Relics",
		"route_runner": "Gates",
		"stealth_patrol": "Intel",
		"relay_chain": "Relays",
		"extraction_maze": "Artifacts",
	}.get(template, "Score")
	if template == "route_runner":
		scene["arena"].update({"width": 30, "depth": 86, "laneColor": "#284d7a", "accentColor": "#ffd166"})
		scene["player"].update({"start": {"x": 0, "y": 0.9, "z": 34}, "speed": 9.6, "dashSpeed": 28.0})
		scene["goal"].update({"position": {"x": 0, "y": 0.4, "z": -36}, "unlockRelics": min(3, len(scene["relics"]))})
		for index, relic in enumerate(scene["relics"]):
			relic["position"] = {"x": [-8, 7, -5, 6, 0][index % 5], "y": 1.2, "z": 22 - index * 13}
		for index, hazard in enumerate(scene["hazards"]):
			hazard["position"] = {"x": [-5, 5, 0][index % 3], "y": 0.05, "z": 12 - index * 18}
			hazard["radius"] = 3.2
		for index, enemy in enumerate(scene["enemies"]):
			enemy["position"] = {"x": [-11, 11, -9, 9][index % 4], "y": 0.9, "z": 16 - index * 14}
			enemy["pursuitRange"] = 12
		scene["camera"]["offset"] = {"x": 0, "y": 22, "z": 18}
		scene["rules"]["statusMessage"] = "Sprint through route gates, grab enough markers, and reach the finish lane."
	elif template == "stealth_patrol":
		scene["arena"].update({"width": 54, "depth": 54, "groundColor": "#08140f", "laneColor": "#23402f", "accentColor": "#9bff6e"})
		scene["player"].update({"speed": 7.2, "dashCooldown": 2.2, "pulseCooldown": 4.2})
		for index, enemy in enumerate(scene["enemies"]):
			enemy["speed"] = round(enemy["speed"] * 0.82, 2)
			enemy["pursuitRange"] = 10 + index * 2
			enemy["role"] = "patrol detector"
		scene["goal"].update({"unlockRelics": min(2, len(scene["relics"]))})
		scene["rules"]["statusMessage"] = "Stay out of patrol vision, collect intel, and slip to the extraction beacon."
	elif template == "relay_chain":
		scene["arena"].update({"width": 60, "depth": 44, "laneColor": "#352d6b", "accentColor": "#ff9ed1"})
		for index, relic in enumerate(scene["relics"]):
			relic["position"] = {"x": -22 + index * 11, "y": 1.2, "z": -8 if index % 2 else 8}
		scene["goal"].update({"position": {"x": 24, "y": 0.4, "z": 0}, "unlockRelics": len(scene["relics"])})
		scene["rules"]["statusMessage"] = "Link every relay node, keep the chain alive, and activate the final signal."
	elif template == "extraction_maze":
		scene["arena"].update({"width": 66, "depth": 66, "groundColor": "#100d18", "laneColor": "#42335f", "accentColor": "#f6ff7d"})
		for index, hazard in enumerate(scene["hazards"]):
			hazard["radius"] = round(4.2 + index * 0.35, 2)
			hazard["damagePerSecond"] = 7 + index * 2
		for index, enemy in enumerate(scene["enemies"]):
			enemy["speed"] = round(enemy["speed"] * 0.9, 2)
			enemy["pursuitRange"] = 14 + index * 2
		scene["goal"].update({"position": {"x": 0, "y": 0.4, "z": -26}, "unlockRelics": min(4, len(scene["relics"]))})
		scene["rules"]["statusMessage"] = "Map the maze, recover artifacts, and extract before the corridors close."
	scene["rules"]["targetRelics"] = scene["goal"]["unlockRelics"]
	return scene


def build_scene_payload(title: str, concept: dict) -> dict:
	final_data = concept.get("brainstorm_final", {}) if isinstance(concept.get("brainstorm_final"), dict) else {}
	final_spec = final_data.get("finalSpec", {}) if isinstance(final_data.get("finalSpec"), dict) else {}
	world = final_spec.get("world", {}) if isinstance(final_spec.get("world"), dict) else {}
	progression = final_spec.get("progression", {}) if isinstance(final_spec.get("progression"), dict) else {}
	encounter_design = final_spec.get("encounterDesign", {}) if isinstance(final_spec.get("encounterDesign"), dict) else {}
	enemy_archetypes = final_spec.get("enemyArchetypes", []) if isinstance(final_spec.get("enemyArchetypes"), list) else []
	enemy_roles = {
		coerce_text(item.get("name")).lower(): coerce_text(item.get("role"), "pressure chaser")
		for item in enemy_archetypes
		if isinstance(item, dict)
	}
	injection_values = []
	for item in final_data.get("randomInjections", []):
		if not isinstance(item, dict):
			continue
		raw_value = item.get("value")
		if isinstance(raw_value, list):
			injection_values.extend(raw_value)
		else:
			injection_values.append(raw_value)

	session_minutes = parse_session_length_minutes(coerce_text(final_spec.get("sessionLength"), "8 minutes"))
	time_limit_seconds = max(90, min(180, session_minutes * 15))
	enemy_types = coerce_list(final_spec.get("enemyTypes"), fallback=concept.get("pressure", []), minimum_items=0)
	if not enemy_types:
		enemy_types = ["guard", "warden", "commander"]
	relic_labels = merge_unique_strings(
		coerce_list(progression.get("rewardHooks"), fallback=[], minimum_items=0),
		coerce_list(progression.get("metaGoal"), fallback=[], minimum_items=0),
		limit=5,
	)
	if not relic_labels:
		relic_labels = ["signal", "mystery", "charge", "route", "bloom"]
	hazard_labels = merge_unique_strings(
		coerce_list(encounter_design.get("hazards"), fallback=[], minimum_items=0),
		injection_values,
		limit=3,
	)
	if not hazard_labels:
		hazard_labels = ["squall", "breaker", "undertow"]

	enemy_positions = [(-16, -10), (14, -14), (-12, 12), (10, 16)]
	enemy_colors = ["#ff8c69", "#ff4f7a", "#ffd166", "#8b6cff"]
	enemies = []
	for index, enemy_name in enumerate(enemy_types[:4]):
		x, z = enemy_positions[index % len(enemy_positions)]
		enemies.append(
			{
				"name": enemy_name.title(),
				"role": enemy_roles.get(enemy_name.lower(), "pressure chaser"),
				"position": {"x": x, "y": 0.9, "z": z},
				"speed": round(1.45 + index * 0.18, 2),
				"radius": round(1.0 + index * 0.08, 2),
				"color": enemy_colors[index % len(enemy_colors)],
				"pursuitRange": 18 + index * 3,
			}
		)

	relic_positions = [(-18, 0), (18, -4), (-6, -16), (14, 12), (-14, 16)]
	relic_colors = ["#7cffc9", "#8bd8ff", "#ffd166", "#ff9ed1", "#f6ff7d"]
	relics = []
	for index, label in enumerate(relic_labels[:5]):
		x, z = relic_positions[index % len(relic_positions)]
		relics.append(
			{
				"label": label.title(),
				"position": {"x": x, "y": 1.2, "z": z},
				"color": relic_colors[index % len(relic_colors)],
			}
		)

	hazard_positions = [(-8, 0), (8, 8), (0, -10)]
	hazards = []
	for index, label in enumerate(hazard_labels[:3]):
		x, z = hazard_positions[index % len(hazard_positions)]
		hazards.append(
			{
				"name": label.title(),
				"position": {"x": x, "y": 0.05, "z": z},
				"radius": round(2.8 + index * 0.45, 2),
				"damagePerSecond": 10 + index * 3,
				"color": ["#4fd1ff", "#ff7a45", "#9bff6e"][index % 3],
			}
		)

	target_relics = max(3, min(len(relics), 4))
	scene = {
		"arena": {
			"width": 56,
			"depth": 56,
			"groundColor": "#08101d",
			"laneColor": "#15345f",
			"accentColor": "#7cffc9",
			"fogColor": "#091120",
			"skyColor": "#050813",
		},
		"player": {
			"start": {"x": 0, "y": 0.9, "z": 18},
			"radius": 0.9,
			"color": "#8bd8ff",
			"speed": 8.5,
			"dashSpeed": 24.0,
			"dashCooldown": 1.35,
			"pulseRadius": 5.5,
			"pulseCooldown": 2.8,
			"maxHealth": 100,
		},
		"goal": {
			"position": {"x": 0, "y": 0.4, "z": -20},
			"radius": 2.6,
			"color": "#7df9ff",
			"unlockRelics": target_relics,
		},
		"relics": relics,
		"enemies": enemies,
		"hazards": hazards,
		"camera": {"offset": {"x": 0, "y": 18, "z": 16}},
		"weather": {"rainDensity": 320},
		"rules": {
			"goalRadius": 2.6,
			"statusMessage": concept.get("status_message") or "Collect relics and unlock the exit.",
			"failStates": concept.get("fail_states", []),
			"progression": concept.get("rewards", []),
			"targetRelics": target_relics,
			"timeLimitSeconds": time_limit_seconds,
		},
		"abilities": {
			"verbs": concept.get("player_actions", [])[:3],
			"summary": concept.get("hook", ""),
		},
			"world": {
				"setting": coerce_text(world.get("setting"), title),
				"visualDirection": coerce_text(world.get("visualDirection"), "High-contrast storm routes with readable silhouettes."),
				"landmarks": coerce_list(world.get("landmarks"), fallback=[], minimum_items=0),
			},
		}
	return apply_runtime_template_scene(scene, concept.get("game_design_profile", {}))


def create_story_json(target_dir: Path, folder_name: str, title: str, description: str, seed_data: dict, concept: dict, design_text: str, chapters: list[str], fun_assessment: str, fun_needs: list[str], feature_packets: list[dict]) -> None:
	story_path = target_dir / "story-structure.json"
	final_data = concept.get("brainstorm_final", {}) if isinstance(concept.get("brainstorm_final"), dict) else {}
	final_spec = final_data.get("finalSpec", {}) if isinstance(final_data.get("finalSpec"), dict) else {}
	scene_payload = build_scene_payload(title, concept)
	exploration_loops = final_data.get("explorationLoops", []) if isinstance(final_data.get("explorationLoops"), list) else []
	story_nodes = [
		{
			"id": "intro",
			"title": "Introduction",
			"text": concept["story_intro"],
			"choices": [],
		}
	]
	for index, loop in enumerate(exploration_loops[:3], start=1):
		if not isinstance(loop, dict):
			continue
		story_nodes.append(
			{
				"id": f"exploration-loop-{index}",
				"title": f"Exploration Loop {index}",
				"text": f"{coerce_text(loop.get('prompt'))} {coerce_text(loop.get('decision'))}".strip(),
				"choices": [],
			}
		)

	story_template = {
		"id": folder_name,
		"title": title,
		"description": description,
		"objective": seed_data.get("objective", ""),
		"seed": seed_data.get("seed", {}),
		"hook": concept["hook"],
		"uniqueness": concept["uniqueness"],
		"controls": concept["controls"],
		"fun": {
			"assessment": fun_assessment,
			"needs": fun_needs,
		},
		"design": {
			"summary": concept["hook"],
			"details": design_text,
			"chapters": chapters,
		},
			"brainstorm": {
				"seedFile": Path(concept.get("brainstorm_seed_file", "brainstorm-seed.json")).name,
				"summaryFile": Path(concept.get("brainstorm_summary_file", "brainstorm-summary.json")).name,
				"finalFile": Path(concept.get("brainstorm_final_file", "final-brainstorming.json")).name,
			"oneLinePitch": coerce_text(final_data.get("oneLinePitch"), concept["hook"]),
			"steps": final_data.get("steps", []),
			"randomInjections": final_data.get("randomInjections", []),
			"explorationLoops": exploration_loops,
				"finalSpec": final_spec,
			},
			"gameDesignProfile": concept.get("game_design_profile", {}),
			"sprintBuilder": {
			"mode": "branching feature design loop",
			"detailFractalization": True,
			"featureBranches": [
				{
					"feature": packet["feature"],
					"sprintObjective": packet["sprint_objective"],
					"playerPromise": packet["player_promise"],
					"checkpoints": packet["checkpoints"],
					"acceptance": packet["acceptance"],
					"scope": packet["scope"],
					"risks": packet["risks"],
					"branches": packet["branches"],
				}
				for packet in feature_packets
			],
		},
		"scene": scene_payload,
		"story": {
			"start": "intro",
			"nodes": story_nodes,
		},
		"delivery": {
			"format": "story-driven JSON nodes",
			"note": join_inline(concept["data_hooks"], "Add more delivery hooks."),
			"prototypeScope": coerce_text(final_spec.get("technicalBuild", {}).get("scope"), "Small browser-playable prototype"),
		},
	}
	write_json_file(story_path, story_template)
	print(f"Created story structure JSON at {story_path}")


def create_html_file(target_dir: Path, title: str, description: str, story_intro: str, ui_notes: list[str]) -> None:
	html_path = target_dir / "index.html"
	ui_detail = join_inline(ui_notes, "WASD / Arrow keys")
	content = textwrap.dedent(
		f"""
		<!DOCTYPE html>
		<html lang="en">
		  <head>
			<meta charset="UTF-8" />
			<meta name="viewport" content="width=device-width, initial-scale=1.0" />
			<title>{title}</title>
			<style>
			  :root {{
				--bg: #050813;
				--panel: rgba(10, 17, 31, 0.86);
				--panel-border: rgba(123, 255, 214, 0.18);
				--text: #eff7ff;
				--muted: #8eabc8;
				--accent: #7cffc9;
			  }}
			  * {{ box-sizing: border-box; }}
			  body {{
				margin: 0;
				font-family: "Trebuchet MS", "Segoe UI", sans-serif;
				background:
				  radial-gradient(circle at top, rgba(125, 249, 255, 0.14), transparent 32%),
				  radial-gradient(circle at 80% 20%, rgba(124, 255, 201, 0.12), transparent 26%),
				  linear-gradient(180deg, #07101d, var(--bg));
				color: var(--text);
				min-height: 100vh;
				overflow: hidden;
			  }}
			  #game-stage {{ width: 100vw; height: 100vh; padding: 1rem; }}
			  #game-container {{
				position: relative;
				width: 100%;
				height: 100%;
				overflow: hidden;
				border-radius: 24px;
				border: 1px solid rgba(125, 249, 255, 0.18);
				background: linear-gradient(180deg, #06101e, #03060d);
				box-shadow: 0 22px 60px rgba(0, 0, 0, 0.36);
			  }}
			  #game-canvas {{ width: 100%; height: 100%; display: block; }}
			  #game-ui {{
				position: absolute;
				inset: 0;
				display: flex;
				justify-content: space-between;
				align-items: flex-start;
				padding: 1rem;
				pointer-events: none;
				gap: 1rem;
			  }}
			  .hud-cluster {{ display: grid; gap: 0.75rem; max-width: min(34rem, 48vw); }}
			  .hud-card {{ padding: 0.8rem 0.95rem; border-radius: 18px; background: rgba(6, 12, 24, 0.82); border: 1px solid rgba(124, 255, 201, 0.12); backdrop-filter: blur(16px); }}
			  .hud-label {{ display: block; font-size: 0.78rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.45rem; }}
			  .hud-value {{ margin: 0; color: var(--text); line-height: 1.45; }}
			  #game-overlay {{ position: absolute; inset: 0; display: none; place-items: center; background: rgba(2, 6, 12, 0.66); z-index: 5; padding: 1rem; }}
			  #game-overlay.visible {{ display: grid; }}
			  .overlay-card {{ width: min(38rem, 100%); padding: 1.35rem 1.4rem; border-radius: 24px; background: rgba(5, 9, 18, 0.92); border: 1px solid rgba(125, 249, 255, 0.2); box-shadow: 0 28px 64px rgba(0, 0, 0, 0.4); }}
			  .overlay-kicker {{ margin: 0 0 0.5rem; color: var(--accent); letter-spacing: 0.18em; text-transform: uppercase; font-size: 0.8rem; }}
			  .overlay-card h1, .overlay-card h2 {{ margin: 0 0 0.65rem; font-size: clamp(2rem, 5vw, 3.5rem); text-transform: uppercase; letter-spacing: 0.08em; }}
			  .overlay-card p {{ margin: 0.35rem 0; color: var(--muted); line-height: 1.5; }}
			  #story-text {{ white-space: pre-wrap; color: #d4e5ff; margin: 1rem 0 0; font-family: inherit; line-height: 1.55; }}
			  #overlay-hint {{ margin-top: 1rem; color: #eff7ff; }}
			  @media (max-width: 900px) {{
				#game-stage {{ padding: 0; }}
				#game-container {{ border-radius: 0; }}
				#game-ui {{ flex-direction: column; align-items: stretch; }}
				.hud-cluster {{ max-width: none; }}
			  }}
			</style>
		  </head>
		  <body>
			<div id="game-stage">
			  <div id="game-container">
				<canvas id="game-canvas"></canvas>
				<div id="game-ui">
				  <div class="hud-cluster">
					<div class="hud-card">
					  <span class="hud-label">Objective</span>
					  <p class="hud-value" id="game-objective">Loading objective...</p>
					</div>
					<div class="hud-card">
					  <span class="hud-label">Status</span>
					  <p class="hud-value" id="game-status">Loading game...</p>
					</div>
				  </div>
				  <div class="hud-cluster">
					<div class="hud-card">
					  <span class="hud-label">Telemetry</span>
					  <p class="hud-value" id="game-metrics">Awaiting scene data...</p>
					</div>
				  </div>
				</div>
				<div id="game-overlay" class="visible">
				  <div class="overlay-card">
					<p class="overlay-kicker">Playable Demo</p>
					<h1 id="overlay-title">{title}</h1>
					<p id="overlay-body">{description}</p>
					<pre id="story-text">{story_intro}</pre>
					<p id="overlay-hint">Press Enter to deploy. {ui_detail}. Press R to restart after a wipe.</p>
				  </div>
				</div>
			  </div>
			</div>
			<script type="module" src="./game.js"></script>
		  </body>
		</html>
		"""
	)
	write_text_file(html_path, content)
	print(f"Created HTML page at {html_path}")


def create_game_script(target_dir: Path) -> None:
	game_js_path = target_dir / "game.js"
	content = textwrap.dedent(
		"""
		import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';

		const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
		const dampFactor = (delta, sharpness) => 1 - Math.exp(-delta * sharpness);

		class InputManager {
		  constructor() {
			this.keys = { forward: false, backward: false, left: false, right: false };
			this.dashRequested = false;
			this.pulseRequested = false;
			window.addEventListener('keydown', (event) => this.onKeyDown(event));
			window.addEventListener('keyup', (event) => this.onKeyUp(event));
		  }

		  onKeyDown(event) {
			if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = true;
			if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = true;
			if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = true;
			if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = true;
			if (event.key === 'Shift' && !event.repeat) this.dashRequested = true;
			if (event.key === ' ' && !event.repeat) {
			  this.pulseRequested = true;
			  event.preventDefault();
			}
		  }

		  onKeyUp(event) {
			if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = false;
			if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = false;
			if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = false;
			if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = false;
		  }

		  consumeDash() {
			const requested = this.dashRequested;
			this.dashRequested = false;
			return requested;
		  }

		  consumePulse() {
			const requested = this.pulseRequested;
			this.pulseRequested = false;
			return requested;
		  }
		}

		class ArenaGame {
		  constructor() {
			this.canvas = document.getElementById('game-canvas');
			this.status = document.getElementById('game-status');
			this.metrics = document.getElementById('game-metrics');
			this.objective = document.getElementById('game-objective');
			this.storyText = document.getElementById('story-text');
			this.overlay = document.getElementById('game-overlay');
			this.overlayTitle = document.getElementById('overlay-title');
			this.overlayBody = document.getElementById('overlay-body');
			this.overlayHint = document.getElementById('overlay-hint');
			this.scene = new THREE.Scene();
			this.camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 220);
			this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
			this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
			this.renderer.outputColorSpace = THREE.SRGBColorSpace;
			this.renderer.shadowMap.enabled = true;
			this.clock = new THREE.Clock();
			this.input = new InputManager();
			this.story = null;
			this.config = null;
			this.elapsed = 0;
			this.state = 'loading';
			this.player = null;
			this.goal = null;
			this.relics = [];
			this.enemies = [];
			this.hazards = [];
			this.rain = null;
			this.timeRemaining = 0;
			this.relicCount = 0;
				this.goalUnlocked = false;
				this.eventMessage = '';
				this.eventTimer = 0;
				this.template = 'arena_survival';
				this.score = 0;
			  }

		  async init() {
			await this.loadStory();
			this.applyVisualTheme();
			this.createArena();
			this.createPlayer();
			this.createGoal();
			this.createRelics();
			this.createHazards();
			this.createEnemies();
			this.createRain();
			this.resetRun();
			this.showIntroOverlay();
			this.onResize();
			window.addEventListener('resize', () => this.onResize());
			window.addEventListener('keydown', (event) => {
			  const key = event.key.toLowerCase();
			  if (key === 'enter' && this.state === 'menu') {
				this.startRun();
			  }
			  if (key === 'r' && this.state !== 'running') {
				this.resetRun();
			  }
			});
			this.animate();
		  }

		  async loadStory() {
			const response = await fetch('./story-structure.json');
			if (!response.ok) {
			  throw new Error('Could not load story-structure.json');
			}
				this.story = await response.json();
				this.config = this.story.scene;
				this.template = this.config?.rules?.runtimeTemplate || this.story?.gameDesignProfile?.runtimeTemplate || 'arena_survival';
				const pitch = this.story?.brainstorm?.oneLinePitch || this.story?.hook || 'Arcade run loaded.';
			const coreLoop = this.story?.brainstorm?.finalSpec?.coreLoop || [];
			this.overlayTitle.textContent = this.story?.title || 'Arcade Run';
			this.overlayBody.textContent = this.story?.description || pitch;
			this.storyText.textContent = [pitch, '', ...coreLoop.slice(0, 3)].join('\\n');
			this.objective.textContent = this.story.objective || pitch;
			if (this.overlayHint) {
			  this.overlayHint.textContent = 'Press Enter to deploy. Use WASD or Arrow keys to move, Shift to dash, Space to pulse. Press R to restart after a wipe.';
			}
		  }

		  showIntroOverlay() {
			this.state = 'menu';
			this.overlay.classList.add('visible');
		  }

		  startRun() {
			this.overlay.classList.remove('visible');
			this.state = 'running';
			this.setStatus(this.config.rules.statusMessage || 'Collect relics and unlock the exit.', 2.2);
		  }

		  applyVisualTheme() {
			const arena = this.config.arena;
			this.scene.background = new THREE.Color(arena.skyColor || '#050813');
			this.scene.fog = new THREE.Fog(arena.fogColor || '#091120', 24, 92);

			const hemi = new THREE.HemisphereLight(0x93cfff, 0x071120, 1.15);
			this.scene.add(hemi);

			const keyLight = new THREE.DirectionalLight(0xe6fbff, 1.4);
			keyLight.position.set(14, 24, 12);
			keyLight.castShadow = true;
			keyLight.shadow.mapSize.set(2048, 2048);
			this.scene.add(keyLight);

			const rimLight = new THREE.PointLight(0x7df9ff, 7, 70, 2.1);
			rimLight.position.set(-18, 14, -8);
			this.scene.add(rimLight);
		  }

		  createArena() {
			const arena = this.config.arena;
			const floor = new THREE.Mesh(
			  new THREE.PlaneGeometry(arena.width, arena.depth),
			  new THREE.MeshStandardMaterial({ color: arena.groundColor, metalness: 0.15, roughness: 0.88 })
			);
			floor.rotation.x = -Math.PI / 2;
			floor.receiveShadow = true;
			this.scene.add(floor);

			const water = new THREE.Mesh(
			  new THREE.CircleGeometry(Math.max(arena.width, arena.depth) * 0.72, 64),
			  new THREE.MeshBasicMaterial({ color: 0x06101d, transparent: true, opacity: 0.85 })
			);
			water.rotation.x = -Math.PI / 2;
			water.position.y = -0.03;
			this.scene.add(water);

			const grid = new THREE.GridHelper(arena.width, 18, arena.accentColor, arena.laneColor);
			grid.position.y = 0.02;
			this.scene.add(grid);

			const boundary = new THREE.Mesh(
			  new THREE.RingGeometry(arena.width * 0.46, arena.width * 0.49, 64),
			  new THREE.MeshBasicMaterial({ color: arena.accentColor, transparent: true, opacity: 0.16, side: THREE.DoubleSide })
			);
			boundary.rotation.x = -Math.PI / 2;
			boundary.position.y = 0.03;
			this.scene.add(boundary);
		  }

		  createPlayer() {
			const playerConfig = this.config.player;
			const group = new THREE.Group();
			const body = new THREE.Mesh(
			  new THREE.IcosahedronGeometry(playerConfig.radius, 3),
			  new THREE.MeshStandardMaterial({ color: playerConfig.color, emissive: 0x164865, emissiveIntensity: 0.4, roughness: 0.25 })
			);
			body.castShadow = true;
			group.add(body);

			const ring = new THREE.Mesh(
			  new THREE.TorusGeometry(playerConfig.radius + 0.26, 0.08, 12, 32),
			  new THREE.MeshBasicMaterial({ color: 0x7df9ff, transparent: true, opacity: 0.65 })
			);
			ring.rotation.x = Math.PI / 2;
			ring.position.y = -playerConfig.radius * 0.5;
			group.add(ring);

			group.position.set(playerConfig.start.x, playerConfig.start.y, playerConfig.start.z);
			this.scene.add(group);
			this.player = {
			  mesh: group,
			  body,
			  ring,
			  radius: playerConfig.radius,
			  velocity: new THREE.Vector3(),
			  dashCooldown: 0,
			  pulseCooldown: 0,
			  invulnerability: 0,
			  maxHealth: playerConfig.maxHealth,
			  health: playerConfig.maxHealth,
			};
		  }

		  createGoal() {
			const goalConfig = this.config.goal;
			const group = new THREE.Group();
			const ring = new THREE.Mesh(
			  new THREE.TorusGeometry(goalConfig.radius, 0.18, 16, 40),
			  new THREE.MeshStandardMaterial({ color: 0x24415f, emissive: 0x112235, emissiveIntensity: 0.45 })
			);
			ring.rotation.x = Math.PI / 2;
			group.add(ring);

			const beacon = new THREE.Mesh(
			  new THREE.CylinderGeometry(0.38, 0.38, 4.5, 12),
			  new THREE.MeshStandardMaterial({ color: goalConfig.color, emissive: 0x1a3840, emissiveIntensity: 0.8 })
			);
			beacon.position.y = 2.2;
			beacon.castShadow = true;
			group.add(beacon);

			group.position.set(goalConfig.position.x, goalConfig.position.y, goalConfig.position.z);
			this.scene.add(group);
			this.goal = { mesh: group, ring, beacon, radius: goalConfig.radius, unlockRelics: goalConfig.unlockRelics };
		  }

		  createRelics() {
			this.relics = this.config.relics.map((config, index) => {
			  const mesh = new THREE.Mesh(
				new THREE.OctahedronGeometry(0.7 + (index % 2) * 0.1, 0),
				new THREE.MeshStandardMaterial({ color: config.color, emissive: 0x19304a, emissiveIntensity: 0.75, roughness: 0.2 })
			  );
			  mesh.position.set(config.position.x, config.position.y, config.position.z);
			  mesh.castShadow = true;
			  this.scene.add(mesh);
			  return { mesh, label: config.label, baseY: config.position.y, collected: false };
			});
		  }

		  createHazards() {
			this.hazards = this.config.hazards.map((config) => {
			  const mesh = new THREE.Mesh(
				new THREE.CylinderGeometry(config.radius, config.radius, 0.14, 32),
				new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.22 })
			  );
			  mesh.position.set(config.position.x, config.position.y, config.position.z);
			  this.scene.add(mesh);
			  const outline = new THREE.Mesh(
				new THREE.TorusGeometry(config.radius, 0.08, 12, 32),
				new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.42 })
			  );
			  outline.rotation.x = Math.PI / 2;
			  outline.position.copy(mesh.position);
			  outline.position.y += 0.08;
			  this.scene.add(outline);
			  return { ...config, mesh, outline };
			});
		  }

		  createEnemies() {
			this.enemies = this.config.enemies.map((config, index) => {
			  const group = new THREE.Group();
			  const body = new THREE.Mesh(
				new THREE.DodecahedronGeometry(config.radius, 0),
				new THREE.MeshStandardMaterial({ color: config.color, emissive: 0x21111b, emissiveIntensity: 0.4, roughness: 0.35 })
			  );
			  body.castShadow = true;
			  group.add(body);
			  const fin = new THREE.Mesh(
				new THREE.ConeGeometry(config.radius * 0.55, config.radius * 1.45, 8),
				new THREE.MeshStandardMaterial({ color: 0xfff2d8, emissive: 0x281a12, emissiveIntensity: 0.22 })
			  );
			  fin.rotation.x = Math.PI;
			  fin.position.y = config.radius * 0.95;
			  group.add(fin);
			  group.position.set(config.position.x, config.position.y, config.position.z);
			  this.scene.add(group);
			  return {
				mesh: group,
				name: config.name,
				role: config.role,
				speed: config.speed,
				radius: config.radius,
				pursuitRange: config.pursuitRange,
				anchor: new THREE.Vector3(config.position.x, config.position.y, config.position.z),
				velocity: new THREE.Vector3(),
				stun: 0,
				hitCooldown: 0,
				phase: index * 0.7,
			  };
			});
		  }

		  createRain() {
			const density = this.config.weather?.rainDensity || 220;
			const positions = new Float32Array(density * 3);
			const halfWidth = this.config.arena.width * 0.5;
			const halfDepth = this.config.arena.depth * 0.5;
			for (let index = 0; index < density; index += 1) {
			  positions[index * 3] = (Math.random() - 0.5) * this.config.arena.width;
			  positions[index * 3 + 1] = Math.random() * 18 + 3;
			  positions[index * 3 + 2] = (Math.random() - 0.5) * this.config.arena.depth;
			}
			const geometry = new THREE.BufferGeometry();
			geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
			const material = new THREE.PointsMaterial({ color: 0x8bd8ff, size: 0.12, transparent: true, opacity: 0.75 });
			this.rain = {
			  points: new THREE.Points(geometry, material),
			  halfWidth,
			  halfDepth,
			};
			this.scene.add(this.rain.points);
		  }

		  resetRun() {
			const playerConfig = this.config.player;
			this.player.mesh.position.set(playerConfig.start.x, playerConfig.start.y, playerConfig.start.z);
			this.player.velocity.set(0, 0, 0);
			this.player.health = this.player.maxHealth;
			this.player.dashCooldown = 0;
			this.player.pulseCooldown = 0;
			this.player.invulnerability = 0;
				this.goalUnlocked = false;
				this.relicCount = 0;
				this.score = 0;
				this.timeRemaining = this.config.rules.timeLimitSeconds;
			this.state = 'running';
			this.elapsed = 0;
			this.overlay.classList.remove('visible');
			this.setStatus(this.config.rules.statusMessage || 'Collect relics and unlock the exit.', 2.2);

			this.relics.forEach((relic) => {
			  relic.collected = false;
			  relic.mesh.visible = true;
			});

			this.enemies.forEach((enemy) => {
			  enemy.mesh.position.copy(enemy.anchor);
			  enemy.velocity.set(0, 0, 0);
			  enemy.stun = 0;
			  enemy.hitCooldown = 0;
			});
			this.updateHud(0);
		  }

		  setStatus(message, ttl = 1.2) {
			this.eventMessage = message;
			this.eventTimer = ttl;
		  }

		  finishRun(title, body) {
			this.state = 'complete';
			this.overlayTitle.textContent = title;
			this.overlayBody.textContent = body;
			if (this.overlayHint) {
			  this.overlayHint.textContent = 'Press R to restart the run.';
			}
			this.overlay.classList.add('visible');
		  }

		  applyDamage(amount, reason) {
			if (this.player.invulnerability > 0 || this.state !== 'running') return;
			this.player.health = Math.max(0, this.player.health - amount);
			this.player.invulnerability = 0.7;
			this.setStatus(reason, 0.8);
			if (this.player.health <= 0) {
			  this.finishRun('Route Interrupted', 'The route collapsed under pressure. Press R to run it again.');
			}
		  }

		  triggerPulse() {
			if (this.player.pulseCooldown > 0 || this.state !== 'running') return;
			const radius = this.config.player.pulseRadius;
			this.player.pulseCooldown = this.config.player.pulseCooldown;
			this.player.ring.scale.setScalar(1.7);
			this.enemies.forEach((enemy) => {
			  const offset = enemy.mesh.position.clone().sub(this.player.mesh.position);
			  offset.y = 0;
			  const distance = offset.length();
			  if (distance < radius) {
				const direction = offset.normalize();
				enemy.velocity.add(direction.multiplyScalar(9));
				enemy.stun = 1.3;
			  }
			});
			this.setStatus('Pulse burst cleared breathing room.', 1.0);
		  }

		  updatePlayer(delta) {
			const move = new THREE.Vector3(
			  (this.input.keys.right ? 1 : 0) - (this.input.keys.left ? 1 : 0),
			  0,
			  (this.input.keys.backward ? 1 : 0) - (this.input.keys.forward ? 1 : 0)
			);
			if (move.lengthSq() > 0) move.normalize();

			if (this.input.consumeDash() && this.player.dashCooldown <= 0) {
			  const dashDirection = move.lengthSq() > 0 ? move.clone() : new THREE.Vector3(0, 0, -1);
			  this.player.velocity.add(dashDirection.multiplyScalar(this.config.player.dashSpeed));
			  this.player.dashCooldown = this.config.player.dashCooldown;
			  this.setStatus('Dash burst engaged.', 0.8);
			}

			if (this.input.consumePulse()) {
			  this.triggerPulse();
			}

				const desiredVelocity = move.multiplyScalar(this.config.player.speed);
				this.player.velocity.lerp(desiredVelocity, dampFactor(delta, 12));
				if (this.template === 'route_runner' && this.state === 'running') {
				  this.player.velocity.z -= 1.6;
				}
				this.player.mesh.position.addScaledVector(this.player.velocity, delta);
			this.player.velocity.multiplyScalar(0.92);

			const halfWidth = this.config.arena.width * 0.5 - 1.8;
			const halfDepth = this.config.arena.depth * 0.5 - 1.8;
			this.player.mesh.position.x = clamp(this.player.mesh.position.x, -halfWidth, halfWidth);
			this.player.mesh.position.z = clamp(this.player.mesh.position.z, -halfDepth, halfDepth);
			this.player.mesh.rotation.y = Math.atan2(this.player.velocity.x || move.x, this.player.velocity.z || move.z);
		  }

		  updateEnemies(delta) {
			this.enemies.forEach((enemy) => {
			  enemy.hitCooldown = Math.max(0, enemy.hitCooldown - delta);
			  if (enemy.stun > 0) {
				enemy.stun = Math.max(0, enemy.stun - delta);
				enemy.mesh.rotation.y += delta * 6;
				enemy.velocity.multiplyScalar(0.94);
			  } else {
				const chase = this.player.mesh.position.clone().sub(enemy.mesh.position);
				chase.y = 0;
				const distance = chase.length();
				let desiredVelocity = new THREE.Vector3();
					if (this.template === 'stealth_patrol') {
					  const patrol = new THREE.Vector3(Math.sin(this.elapsed * 0.8 + enemy.phase), 0, Math.cos(this.elapsed * 0.6 + enemy.phase));
					  desiredVelocity = distance < enemy.pursuitRange ? chase.normalize().multiplyScalar(enemy.speed * 3.2) : patrol.multiplyScalar(enemy.speed * 1.45);
					} else if (this.template === 'route_runner') {
					  desiredVelocity.set(Math.sin(this.elapsed * 1.6 + enemy.phase), 0, Math.cos(this.elapsed * 0.4 + enemy.phase) * 0.35).multiplyScalar(enemy.speed * 2.4);
					  if (distance < enemy.pursuitRange) desiredVelocity.add(chase.normalize().multiplyScalar(enemy.speed * 1.7));
					} else if (this.template === 'relay_chain') {
					  desiredVelocity = distance < enemy.pursuitRange ? chase.normalize().multiplyScalar(enemy.speed * 3.5) : enemy.anchor.clone().sub(enemy.mesh.position).setY(0).multiplyScalar(0.25);
					} else {
					  if (distance < enemy.pursuitRange) {
						desiredVelocity = chase.normalize().multiplyScalar(enemy.speed * 4.3);
					  } else {
						desiredVelocity.set(Math.sin(this.elapsed + enemy.phase), 0, Math.cos(this.elapsed * 0.8 + enemy.phase)).multiplyScalar(enemy.speed * 1.8);
					  }
					}
				enemy.velocity.lerp(desiredVelocity, dampFactor(delta, 4.8));
			  }

			  enemy.mesh.position.addScaledVector(enemy.velocity, delta);
			  enemy.mesh.position.x = clamp(enemy.mesh.position.x, -24, 24);
			  enemy.mesh.position.z = clamp(enemy.mesh.position.z, -24, 24);
			  enemy.mesh.lookAt(this.player.mesh.position.x, enemy.mesh.position.y, this.player.mesh.position.z);

			  const distanceToPlayer = enemy.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
			  if (distanceToPlayer < enemy.radius + this.player.radius && enemy.hitCooldown <= 0) {
				enemy.hitCooldown = 1.1;
				this.applyDamage(12, `${enemy.name} broke through the route.`);
			  }
			});
		  }

		  updateRelics(delta) {
			this.relics.forEach((relic, index) => {
			  if (relic.collected) return;
			  relic.mesh.rotation.y += delta * (1.5 + index * 0.15);
			  relic.mesh.position.y = relic.baseY + Math.sin(this.elapsed * 2 + index) * 0.18;
			  const distance = relic.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
				  if (distance < 1.65) {
					relic.collected = true;
					relic.mesh.visible = false;
					this.relicCount += 1;
					const scoreGain = this.template === 'relay_chain' ? 150 : this.template === 'stealth_patrol' ? 125 : 100;
					this.score += scoreGain;
					const scoreLabel = this.config.rules.scoreLabel || 'Relic';
					this.setStatus(`${scoreLabel} ${relic.label} secured. Exit charge increased.`, 1.0);
				if (!this.goalUnlocked && this.relicCount >= this.goal.unlockRelics) {
				  this.goalUnlocked = true;
				  this.goal.ring.material.color.set(0x7df9ff);
				  this.goal.ring.material.emissive?.set?.(0x0f3340);
				  this.goal.beacon.material.emissiveIntensity = 1.35;
				  this.setStatus('Exit gate unlocked. Reach the beacon.', 1.4);
				}
			  }
			});
		  }

		  updateHazards(delta) {
			this.hazards.forEach((hazard, index) => {
			  const pulse = 1 + Math.sin(this.elapsed * 2.2 + index) * 0.08;
			  hazard.outline.scale.setScalar(pulse);
			  const distance = hazard.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
			  if (distance < hazard.radius) {
				this.applyDamage(hazard.damagePerSecond * delta, `${hazard.name} chewed through the route.`);
			  }
			});
		  }

		  updateGoal() {
			const bob = Math.sin(this.elapsed * 2.8) * 0.16;
			this.goal.beacon.position.y = 2.2 + bob;
			this.goal.ring.rotation.z += 0.01;
			if (!this.goalUnlocked) return;
				const distance = this.goal.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
				if (distance < this.goal.radius) {
				  const winCopy = {
					arena_survival: ['Route Cleared', 'The exit gate is live and the relic chain is stable. Press R to run it again.'],
					route_runner: ['Finish Lane Cleared', 'The route gates are behind you and the sprint line is open. Press R to run it again.'],
					stealth_patrol: ['Extraction Quiet', 'The patrol grid never fully locked on and the intel is secure. Press R to run it again.'],
					relay_chain: ['Signal Chain Live', 'Every relay is linked and the final beacon is transmitting. Press R to run it again.'],
					extraction_maze: ['Maze Extracted', 'The artifact route is mapped and the exit is open. Press R to run it again.'],
				  }[this.template] || ['Route Cleared', 'The exit gate is live. Press R to run it again.'];
				  this.finishRun(winCopy[0], winCopy[1]);
				}
		  }

		  updateRain(delta) {
			if (!this.rain) return;
			const attribute = this.rain.points.geometry.getAttribute('position');
			for (let index = 0; index < attribute.count; index += 1) {
			  attribute.array[index * 3 + 1] -= delta * 18;
			  attribute.array[index * 3] += delta * 0.7;
			  if (attribute.array[index * 3 + 1] < 0) {
				attribute.array[index * 3] = (Math.random() - 0.5) * this.config.arena.width;
				attribute.array[index * 3 + 1] = Math.random() * 18 + 6;
				attribute.array[index * 3 + 2] = (Math.random() - 0.5) * this.config.arena.depth;
			  }
			}
			attribute.needsUpdate = true;
		  }

		  updateCamera(delta) {
			const offset = this.config.camera.offset;
			const targetPosition = new THREE.Vector3(
			  this.player.mesh.position.x + offset.x,
			  offset.y,
			  this.player.mesh.position.z + offset.z
			);
			this.camera.position.lerp(targetPosition, dampFactor(delta, 3.5));
			this.camera.lookAt(this.player.mesh.position.x, 0.8, this.player.mesh.position.z - 2);
		  }

		  updateHud(delta) {
			this.timeRemaining = Math.max(0, this.timeRemaining - delta);
			this.player.dashCooldown = Math.max(0, this.player.dashCooldown - delta);
			this.player.pulseCooldown = Math.max(0, this.player.pulseCooldown - delta);
			this.player.invulnerability = Math.max(0, this.player.invulnerability - delta);
			this.player.ring.scale.lerp(new THREE.Vector3(1, 1, 1), dampFactor(delta, 6));

			if (this.timeRemaining <= 0 && this.state === 'running') {
			  this.finishRun('Window Closed', 'The storm sealed the route before extraction. Press R to try again.');
			}

			if (this.eventTimer > 0) {
			  this.eventTimer = Math.max(0, this.eventTimer - delta);
				}
				const activeMessage = this.eventTimer > 0 ? this.eventMessage : this.config.rules.statusMessage;
				this.status.textContent = activeMessage;
				const templateLabel = (this.config.rules.mechanicFamily || this.template).replace(/_/g, ' ');
				const scoreLabel = this.config.rules.scoreLabel || 'Relics';
				this.metrics.textContent = `${templateLabel} | Health ${Math.ceil(this.player.health)} | ${scoreLabel} ${this.relicCount}/${this.goal.unlockRelics} | Score ${this.score} | Time ${Math.ceil(this.timeRemaining)}s | Dash ${this.player.dashCooldown > 0 ? this.player.dashCooldown.toFixed(1) + 's' : 'ready'} | Pulse ${this.player.pulseCooldown > 0 ? this.player.pulseCooldown.toFixed(1) + 's' : 'ready'}`;
			  }

		  update(delta) {
			if (this.state !== 'running') {
			  this.updateRain(delta);
			  this.updateCamera(delta);
			  return;
			}
			this.elapsed += delta;
			this.updatePlayer(delta);
			this.updateEnemies(delta);
			this.updateRelics(delta);
			this.updateHazards(delta);
			this.updateGoal();
			this.updateRain(delta);
			this.updateCamera(delta);
			this.updateHud(delta);
		  }

		  animate() {
			requestAnimationFrame(() => this.animate());
			const delta = Math.min(this.clock.getDelta(), 0.05);
			this.update(delta);
			this.renderer.render(this.scene, this.camera);
		  }

		  onResize() {
			const width = this.canvas.clientWidth || window.innerWidth;
			const height = this.canvas.clientHeight || window.innerHeight * 0.68;
			this.camera.aspect = width / height;
			this.camera.updateProjectionMatrix();
			this.renderer.setSize(width, height, false);
		  }
		}

		const game = new ArenaGame();
		game.init().catch((error) => {
		  const storyText = document.getElementById('story-text');
		  const status = document.getElementById('game-status');
		  if (storyText) storyText.textContent = error.message;
		  if (status) status.textContent = 'Game bootstrap failed.';
		  console.error(error);
		});
		"""
	)
	write_text_file(game_js_path, content)
	print(f"Created game script at {game_js_path}")


def create_validation_file(target_dir: Path, loop_index: int, kind: str, content: str) -> None:
	filename = f"validation-loop-{loop_index:02d}-{kind}.md"
	path = target_dir / filename
	text = textwrap.dedent(
		f"""
		# Validation Loop {loop_index:02d} {kind.replace('-', ' ').title()}

		{content}
		"""
	)
	write_text_file(path, text)
	print(f"Created validation file at {path}")


def create_continue_gate_file(target_dir: Path, loop_index: int, status: str, next_steps: list[str]) -> None:
	filename = f"continue-gate-{loop_index:02d}.md"
	path = target_dir / filename
	content = textwrap.dedent(
		f"""
		# Continue Gate {loop_index:02d}

		**Status:** {status}

		**Next steps:**
		{format_list(next_steps, 'No remaining issues recorded.')}
		"""
	)
	write_text_file(path, content)
	print(f"Created continue gate file at {path}")


def collect_bootstrap_identity(default_title: str, default_description: str, default_objective: str, combination: dict, existing_pages: list[dict]) -> dict:
	existing_summary = "\n".join(
		f"- {page['folder']}: {page.get('title') or '(No title)'} -- {page.get('description') or '(No description)'}"
		for page in existing_pages[:12]
	) or "- No comparable existing pages were found."
	schema_example = textwrap.dedent(
		"""
		{
		  "title": "string",
		  "description": "string",
		  "objective": "string"
		}
		"""
	).strip()
	prompt = textwrap.dedent(
		f"""
		Create the identity payload for a new standalone arcade page. Use the seed combination, avoid obvious overlap with existing pages, and optimize for a distinct but buildable concept.
		Preserve a tight arcade scope and make the title, description, and objective line up with the same playable core.

		Seed combination:
		{format_combination(combination)}

		Default anchors:
		- Title: {default_title}
		- Description: {default_description}
		- Objective: {default_objective}

		Existing pages to avoid overlapping with:
		{existing_summary}
		"""
	).strip()
	bundle = prompt_json_bundle(
		prompt,
		"bootstrap_identity",
		schema_example,
		default={
			"title": default_title,
			"description": default_description,
			"objective": default_objective,
		},
		stage_id="bootstrap_identity",
	)
	return {
		"title": coerce_text(bundle.get("title"), default_title),
		"description": coerce_text(bundle.get("description"), default_description),
		"objective": coerce_text(bundle.get("objective"), default_objective),
	}


def create_execution_sprint_index(sprint_root: Path, sprint_goal: str, title: str) -> None:
	pass_dirs = sorted(
		[child.name for child in sprint_root.iterdir() if child.is_dir() and child.name.startswith("pass-")]
	)
	content = textwrap.dedent(
		f"""
		# Implementation Sprints

		**Goal:** {sprint_goal}

		**Game:** {title}

		## Passes
		{format_list(pass_dirs, 'No sprint passes recorded yet.')}
		"""
	).strip() + "\n"
	write_text_file(sprint_root / "README.md", content)
	print(f"Updated implementation sprint index at {sprint_root / 'README.md'}")


def summarize_feature_packets(feature_packets: list[dict]) -> str:
	if not feature_packets:
		return "- No feature packets available."
	return "\n".join(
		f"- {packet['feature']}: {packet['sprint_objective']}" for packet in feature_packets
	)


def find_feature_packet(feature_packets: list[dict], feature_name: str) -> dict | None:
	feature_name = feature_name.strip().lower()
	for packet in feature_packets:
		if packet["feature"].strip().lower() == feature_name:
			return packet
	return None


def create_execution_sprint_pass_files(pass_dir: Path, payload: dict) -> None:
	active_packet = payload.get("active_packet") or {}
	active_packet_content = textwrap.dedent(
		f"""
		# Active Packet

		## Selected Feature

		{payload['active_feature']}

		## Sprint Objective

		{active_packet.get('sprint_objective', '(No sprint objective recorded.)')}

		## Player Promise

		{active_packet.get('player_promise', '(No player promise recorded.)')}

		## Why This Packet Is Active

		{payload['active_packet_reason'] or '(No active-packet reason recorded.)'}

		## Candidate Packets Seen During Selection

		{format_list(payload['candidate_packets'], 'No candidate packets recorded.')}
		"""
	).strip() + "\n"
	write_text_file(pass_dir / "00-active-packet.md", active_packet_content)

	review_content = textwrap.dedent(
		f"""
		# Sprint Review

		## Thoughts

		{payload['thoughts'] or '(No thoughts recorded.)'}

		## Target Changes

		{format_list(payload['target_changes'], 'No target changes recorded.')}

		## Risks

		{format_list(payload['risks'], 'No risks recorded.')}

		## Acceptance Signals

		{format_list(payload['acceptance'], 'No acceptance signals recorded.')}

		## Target Files Or Surfaces

		{format_list(payload['scope'], 'No files or surfaces recorded.')}
		"""
	).strip() + "\n"
	write_text_file(pass_dir / "01-review.md", review_content)

	file_targets_sections = []
	for file_target in payload["file_targets"]:
		file_targets_sections.append(
			textwrap.dedent(
				f"""
				### {file_target['file']}

				- Action: {file_target['action']}
				- Reason: {file_target['reason']}
				- Expected unchanged: {file_target['unchanged']}
				"""
			).strip()
		)
	file_targets_body = "\n\n".join(file_targets_sections) if file_targets_sections else "- No file targets recorded."
	file_targets_content = textwrap.dedent(
		f"""
		# File Targets

		## Targeted Surfaces

		{file_targets_body}
		"""
	).strip() + "\n"
	write_text_file(pass_dir / "02-file-targets.md", file_targets_content)

	plan_content = textwrap.dedent(
		f"""
		# Change Pack Plan

		## Sprint Objective

		{payload['pass_goal']}

		## Implementation Plan

		{format_list(payload['plan_steps'], 'No plan steps recorded.')}

		## Simulated Checkpoints

		{format_list(payload['checkpoints'], 'No checkpoints recorded.')}
		"""
	).strip() + "\n"
	write_text_file(pass_dir / "03-change-pack-plan.md", plan_content)

	patch_spec_sections = []
	for patch_spec in payload["patch_specs"]:
		patch_spec_sections.append(
			textwrap.dedent(
				f"""
				### {patch_spec['file']}

				- Problem: {patch_spec['problem']}
				- Intended behavior: {patch_spec['intended_behavior']}
				- Specific change: {patch_spec['specific_change']}
				- Invariants: {patch_spec['invariants']}
				- Patch units:
				{format_list(patch_spec['patch_units'], 'No patch units recorded.')}
				"""
			).strip()
		)
	patch_spec_body = "\n\n".join(patch_spec_sections) if patch_spec_sections else "- No patch specs recorded."
	patch_spec_content = textwrap.dedent(
		f"""
		# Patch Spec

		## Per-File Patch Units

		{patch_spec_body}
		"""
	).strip() + "\n"
	write_text_file(pass_dir / "04-patch-spec.md", patch_spec_content)

	implementation_content = textwrap.dedent(
		f"""
		# Implementation Notes

		## Actions

		{format_list(payload['implementation_actions'], 'No implementation actions recorded.')}

		## Notes

		{payload['implementation_notes'] or '(No implementation notes recorded.)'}
		"""
	).strip() + "\n"
	write_text_file(pass_dir / "05-implementation.md", implementation_content)

	edit_plan_sections = []
	for item in payload.get("edit_plan", []):
		edit_plan_sections.append(
			textwrap.dedent(
				f"""
				### {item['file']}

				- Reason: {item['reason']}
				- Exact change: {item['exact_change']}
				- Invariant: {item['invariant']}
				- Verification command: {item['verification_command']}
				"""
			).strip()
		)
	write_text_file(
		pass_dir / "05-edit-plan.md",
		"# Edit Plan\n\n" + ("\n\n".join(edit_plan_sections) if edit_plan_sections else "- No edit plan recorded.") + "\n",
	)

	gate_content = textwrap.dedent(
		f"""
		# Completion Gate

		**Goal complete:** {'yes' if payload['goal_complete'] else 'no'}

		## Remaining Work

		{format_list(payload['remaining_work'], 'No remaining work recorded.')}
		"""
	).strip() + "\n"
	write_text_file(pass_dir / "06-completion-gate.md", gate_content)


def collect_file_targets(active_feature: str, active_packet: dict | None, target_dir: Path) -> list[dict]:
	default_scope = active_packet.get("scope", []) if active_packet else []
	if not default_scope:
		default_scope = ["game.js", "index.html", "story-structure.json"]

	file_targets = []
	for suggested_target in default_scope:
		file_name = prompt_short(
			f"Enter the concrete file or surface to target for '{active_feature}'",
			suggested_target,
		)
		action = prompt_short(
			f"For '{file_name}', enter the intended action (update/append/replace/no-op)",
			"update",
		)
		reason = prompt_short(
			f"Explain why '{file_name}' must change for '{active_feature}'",
		)
		unchanged = prompt_short(
			f"State one thing in '{file_name}' that should remain unchanged",
			"core movement and unrelated systems remain unchanged",
		)
		file_targets.append(
			{
				"file": file_name,
				"action": action,
				"reason": reason,
				"unchanged": unchanged,
			}
		)

	additional_targets = prompt_list(
		f"List any additional files or surfaces that should be targeted for '{active_feature}', one per line. If none, type END immediately.",
	)
	for extra_target in additional_targets:
		file_targets.append(
			{
				"file": extra_target,
				"action": prompt_short(f"Enter the intended action for '{extra_target}'", "update"),
				"reason": prompt_short(f"Explain why '{extra_target}' must change"),
				"unchanged": prompt_short(
					f"State one thing in '{extra_target}' that should remain unchanged",
					"unrelated systems remain unchanged",
				),
			}
		)

	print(f"\nFile targets for {target_dir.name}:")
	print("\n".join(f"- {item['file']} ({item['action']})" for item in file_targets) or "- (No file targets recorded.)")
	return file_targets


def collect_patch_specs(file_targets: list[dict], active_feature: str) -> list[dict]:
	patch_specs = []
	for file_target in file_targets:
		problem = prompt_short(
			f"For '{file_target['file']}', state the current problem that blocks '{active_feature}'",
		)
		intended_behavior = prompt_short(
			f"For '{file_target['file']}', state the intended behavior after the change",
		)
		specific_change = prompt_short(
			f"For '{file_target['file']}', describe the specific code or content change",
		)
		invariants = prompt_short(
			f"For '{file_target['file']}', state the invariants that must remain unchanged",
			file_target['unchanged'],
		)
		patch_units = prompt_list(
			f"For '{file_target['file']}', list 2 to 4 patch units, one per line.",
			minimum_items=2,
		)
		patch_specs.append(
			{
				"file": file_target["file"],
				"problem": problem,
				"intended_behavior": intended_behavior,
				"specific_change": specific_change,
				"invariants": invariants,
				"patch_units": patch_units,
			}
		)
	return patch_specs


def collect_execution_sprint_payload(pass_index: int, sprint_goal: str, target_dir: Path, feature_packets: list[dict]) -> dict:
	default_feature = feature_packets[0]["feature"] if feature_packets else "core loop"
	default_scope = feature_packets[0].get("scope", ["game.js", "index.html", "story-structure.json"]) if feature_packets else ["game.js", "index.html", "story-structure.json"]
	schema_example = textwrap.dedent(
		"""
		{
		  "passGoal": "string",
		  "thoughts": "string",
		  "activeFeature": "string",
		  "activePacketReason": "string",
		  "targetChanges": ["string"],
		  "risks": ["string"],
		  "acceptance": ["string"],
		  "scope": ["string"],
		  "fileTargets": [
		    {"file": "string", "action": "string", "reason": "string", "unchanged": "string"}
		  ],
			  "patchSpecs": [
			    {"file": "string", "problem": "string", "intendedBehavior": "string", "specificChange": "string", "invariants": "string", "patchUnits": ["string"]}
			  ],
			  "editPlan": [
			    {"file": "string", "reason": "string", "exactChange": "string", "invariant": "string", "verificationCommand": "string"}
			  ],
			  "planSteps": ["string"],
			  "checkpoints": ["string"],
			  "implementationActions": ["string"],
			  "implementationNotes": "string",
			  "goalComplete": false,
			  "remainingWork": ["string"],
			  "memoryUpdate": {
			    "summary": "string",
			    "decisions": ["string"],
			    "rejectedIdeas": ["string"],
			    "openIssues": ["string"],
			    "nextStageNotes": ["string"]
			  }
			}
			"""
		).strip()
	prompt = textwrap.dedent(
		f"""
		Prepare the full implementation pass payload for one execution sprint pass. This should cover review, active packet selection, file targeting, patch planning, execution checklist, and the completion gate in a single response.
		Bias toward narrow, concrete edits that preserve unrelated behavior.

		Game folder: {target_dir.name}
		Pass index: {pass_index:02d}
		Overall sprint goal: {sprint_goal}
		Available feature packets:
		{summarize_feature_packets(feature_packets)}

		Default active feature if nothing stronger emerges: {default_feature}
		Default file scope if missing: {join_inline(default_scope, 'game.js, index.html, story-structure.json')}
		"""
	).strip()
	bundle = prompt_json_bundle(
		prompt,
		"implementation_pass",
		schema_example,
		default={},
		stage_id="implementation_pass",
		target_dir=target_dir,
	)
	active_feature = coerce_text(bundle.get("activeFeature"), default_feature)
	active_packet = find_feature_packet(feature_packets, active_feature) or (feature_packets[0] if feature_packets else {})
	file_targets = bundle.get("fileTargets", []) if isinstance(bundle.get("fileTargets"), list) else []
	normalized_targets = []
	if not file_targets:
		for item in default_scope:
			normalized_targets.append(
				{
					"file": item,
					"action": "update",
					"reason": f"Advance {active_feature}.",
					"unchanged": "Unrelated systems remain unchanged.",
				}
			)
	else:
		for item in file_targets:
			if not isinstance(item, dict):
				continue
			normalized_targets.append(
				{
					"file": coerce_text(item.get("file"), "game.js"),
					"action": coerce_text(item.get("action"), "update"),
					"reason": coerce_text(item.get("reason"), f"Advance {active_feature}."),
					"unchanged": coerce_text(item.get("unchanged"), "Unrelated systems remain unchanged."),
				}
			)
	patch_specs_raw = bundle.get("patchSpecs", []) if isinstance(bundle.get("patchSpecs"), list) else []
	normalized_patch_specs = []
	for item in patch_specs_raw:
		if not isinstance(item, dict):
			continue
		normalized_patch_specs.append(
			{
				"file": coerce_text(item.get("file"), normalized_targets[0]["file"] if normalized_targets else "game.js"),
				"problem": coerce_text(item.get("problem"), f"{active_feature} is not fully implemented."),
				"intended_behavior": coerce_text(item.get("intendedBehavior"), f"{active_feature} behaves correctly and readably."),
				"specific_change": coerce_text(item.get("specificChange"), f"Implement the next slice of {active_feature}."),
				"invariants": coerce_text(item.get("invariants"), "Preserve unrelated systems and existing core controls."),
				"patch_units": coerce_list(item.get("patchUnits"), fallback=[f"Implement {active_feature}", f"Validate {active_feature}"], minimum_items=2),
			}
		)
	if not normalized_patch_specs:
		for target in normalized_targets:
			normalized_patch_specs.append(
				{
					"file": target["file"],
					"problem": f"{active_feature} is blocked in {target['file']}.",
					"intended_behavior": f"{target['file']} supports the next slice of {active_feature}.",
					"specific_change": f"Update {target['file']} to support {active_feature}.",
					"invariants": target["unchanged"],
					"patch_units": [f"Inspect {target['file']}", f"Patch {target['file']} for {active_feature}"],
				}
			)

	edit_plan_raw = bundle.get("editPlan", []) if isinstance(bundle.get("editPlan"), list) else []
	edit_plan = []
	for item in edit_plan_raw:
		if not isinstance(item, dict):
			continue
		edit_plan.append(
			{
				"file": coerce_text(item.get("file"), normalized_targets[0]["file"] if normalized_targets else "game.js"),
				"reason": coerce_text(item.get("reason"), f"Advance {active_feature}."),
				"exact_change": coerce_text(item.get("exactChange"), f"Implement the planned {active_feature} slice."),
				"invariant": coerce_text(item.get("invariant"), "Preserve unrelated generated game behavior."),
				"verification_command": coerce_text(item.get("verificationCommand"), "python3 -m py_compile Portfolio-Vite/PagesInteractive-CLI/interactive_builder_frontier.py"),
			}
		)
	if not edit_plan:
		for spec in normalized_patch_specs:
			edit_plan.append(
				{
					"file": spec["file"],
					"reason": spec["problem"],
					"exact_change": spec["specific_change"],
					"invariant": spec["invariants"],
					"verification_command": "Open the generated index.html and confirm the planned behavior manually.",
				}
			)

	pass_goal = coerce_text(bundle.get("passGoal"), sprint_goal)
	thoughts = coerce_text(bundle.get("thoughts"), f"Focus pass {pass_index:02d} on {active_feature}.")
	active_packet_reason = coerce_text(bundle.get("activePacketReason"), f"{active_feature} is the best current packet for this pass.")
	target_changes = coerce_list(bundle.get("targetChanges"), fallback=[f"Advance {active_feature}."], minimum_items=1)
	risks = coerce_list(bundle.get("risks"), fallback=[f"{active_feature} could widen scope if not constrained."], minimum_items=1)
	acceptance = coerce_list(bundle.get("acceptance"), fallback=[f"{active_feature} becomes testable and readable."], minimum_items=1)
	scope = coerce_list(bundle.get("scope"), fallback=default_scope, minimum_items=1)
	plan_steps = coerce_list(bundle.get("planSteps"), fallback=[f"Implement the next slice of {active_feature}.", f"Validate the change for {active_feature}."], minimum_items=2)
	checkpoints = coerce_list(bundle.get("checkpoints"), fallback=[f"{active_feature} compiles cleanly.", f"{active_feature} behaves as intended."], minimum_items=2)
	implementation_actions = coerce_list(bundle.get("implementationActions"), fallback=plan_steps, minimum_items=1)
	implementation_notes = coerce_text(bundle.get("implementationNotes"), f"Pass {pass_index:02d} notes are pending.")
	goal_complete = coerce_bool(bundle.get("goalComplete"), default=False)
	remaining_work = coerce_list(bundle.get("remainingWork"), fallback=[])

	return {
		"pass_goal": pass_goal,
		"active_feature": active_feature,
		"active_packet": active_packet or {},
		"active_packet_reason": active_packet_reason,
		"candidate_packets": [packet["feature"] for packet in feature_packets],
		"thoughts": thoughts,
		"target_changes": target_changes,
		"risks": risks,
			"acceptance": acceptance,
			"scope": scope,
			"file_targets": normalized_targets,
			"plan_steps": plan_steps,
			"checkpoints": checkpoints,
			"patch_specs": normalized_patch_specs,
			"edit_plan": edit_plan,
			"implementation_actions": implementation_actions,
			"implementation_notes": implementation_notes,
			"goal_complete": goal_complete,
			"remaining_work": remaining_work,
		}


def run_execution_sprint_loops(target_dir: Path, title: str, feature_packets: list[dict], default_passes: int = 2) -> None:
	if default_passes <= 0:
		return

	sprint_root = target_dir / "implementation-sprints"
	sprint_root.mkdir(parents=True, exist_ok=True)
	default_goal = f"Build the first playable implementation passes for {title}."
	sprint_goal = default_goal
	chapters = []
	implementation_dir = target_dir / "implementation"
	if implementation_dir.exists():
		chapters = [path.stem.split("-", 1)[1].replace("-", " ").title() for path in sorted(implementation_dir.glob("[0-9][0-9]-*.md"))]
	update_build_spec(target_dir, chapters, sprint_goal=sprint_goal)
	print("\nSTAGE 8: Run the bundled implementation sprint loop.")
	print("Each pass now uses one large payload prompt covering review, file targets, patch units, execution sequence, and the completion gate.")

	for pass_index in range(1, default_passes + 1):
		pass_dir = sprint_root / f"pass-{pass_index:02d}"
		pass_dir.mkdir(parents=True, exist_ok=True)
		payload = collect_execution_sprint_payload(pass_index, sprint_goal, target_dir, feature_packets)
		create_execution_sprint_pass_files(pass_dir, payload)
		create_execution_sprint_index(sprint_root, sprint_goal, title)
		update_feature_sprint_spec(target_dir, feature_packets, active_payload=payload)
		update_build_spec(target_dir, chapters, sprint_goal=sprint_goal, payload=payload)
		print(f"\nSaved implementation sprint folder: {pass_dir}")
		if payload["goal_complete"]:
			print("Implementation sprint goal marked complete. Stopping loop.")
			return

	print("Implementation sprint loop reached the configured pass limit before the goal was marked complete.")


def collect_feature_branch_packets(title: str, concept: dict) -> list[dict]:
	final_data = concept.get("brainstorm_final", {}) if isinstance(concept.get("brainstorm_final"), dict) else {}
	final_spec = final_data.get("finalSpec", {}) if isinstance(final_data.get("finalSpec"), dict) else {}
	build_packet = final_data.get("buildPacket", {}) if isinstance(final_data.get("buildPacket"), dict) else {}
	technical_build = final_spec.get("technicalBuild", {}) if isinstance(final_spec.get("technicalBuild"), dict) else {}
	default_features = concept["player_actions"][:3] or ["movement", "feedback", "hazards"]
	feature_roots = coerce_list(build_packet.get("featureRoots"), fallback=[], minimum_items=0)
	if not feature_roots:
		feature_roots = coerce_list(technical_build.get("prototypeOrder"), fallback=default_features, minimum_items=1)
	systems_needed = coerce_list(technical_build.get("systemsNeeded"), fallback=["player controller", "enemy director", "HUD"], minimum_items=0)
	prototype_order = coerce_list(technical_build.get("prototypeOrder"), fallback=feature_roots, minimum_items=0)

	packets = []
	for index, raw_feature in enumerate(feature_roots[:3], start=1):
		feature = humanize_identifier(raw_feature)
		action = concept["player_actions"][min(index - 1, len(concept["player_actions"]) - 1)] if concept["player_actions"] else "move"
		pressure = concept["pressure"][min(index - 1, len(concept["pressure"]) - 1)] if concept["pressure"] else "enemy pressure"
		reward = concept["rewards"][min(index - 1, len(concept["rewards"]) - 1)] if concept["rewards"] else "run progression"
		system = humanize_identifier(systems_needed[min(index - 1, len(systems_needed) - 1)]) if systems_needed else feature
		branch_anchor = humanize_identifier(prototype_order[min(index - 1, len(prototype_order) - 1)]) if prototype_order else feature
		packets.append(
			{
				"feature": feature,
				"sprint_objective": f"Implement the {feature.lower()} slice so the player can reliably feel {action} under {pressure}.",
				"player_promise": f"The player immediately feels how {feature.lower()} improves the route and unlocks {reward}.",
				"branch_reason": f"{feature} is a distinct, testable slice backed by the canonical brainstorm packet and should land without widening scope.",
				"branches": [
					{
						"branch": f"{feature} core slice",
						"tasks": [
							f"Implement the {branch_anchor.lower()} behavior in the main loop.",
							f"Wire {system.lower()} data into story-structure.json and runtime state.",
						],
					},
					{
						"branch": f"{feature} feedback pass",
						"tasks": [
							f"Expose clear HUD and overlay feedback for {feature.lower()}.",
							f"Validate that {feature.lower()} stays readable during pressure spikes.",
						],
					},
				],
				"checkpoints": [
					f"{feature} is driven by canonical brainstorm data rather than ad hoc prompt output.",
					f"{feature} is visible in live play within the first minute of a run.",
				],
				"acceptance": [
					f"The player can describe what {feature.lower()} does after one run.",
					f"{feature} remains readable without breaking the current arena loop.",
				],
				"scope": ["game.js", "story-structure.json", "index.html"],
				"risks": [
					f"{feature} could sprawl beyond the canonical build packet if extra systems are added.",
					f"{feature} could reduce readability if feedback does not stay compact.",
				],
			}
		)
	return packets


def review_html_loop(target_dir: Path, title: str, description: str, concept: dict, force: bool = False) -> None:
	if force:
		print("Skipping manual HTML shell review due to force flag.")
		create_html_file(target_dir, title, description, concept["story_intro"], concept["controls"])
		return
	create_html_file(target_dir, title, description, concept["story_intro"], concept["controls"])
	schema_example = textwrap.dedent(
		"""
		{
		  "reviseHtmlShell": false,
		  "storyIntro": "string",
		  "description": "string",
		  "uiNotes": ["string"]
		}
		"""
	).strip()
	prompt = textwrap.dedent(
		f"""
		Review the generated starter shell for the arcade page and decide whether a rewrite is needed. If a rewrite is needed, return the revised story intro, revised short description, and revised UI notes in the same payload.

		Game title: {title}
		Current description: {description}
		Current story intro: {concept['story_intro']}
		Current controls and HUD notes: {join_inline(concept['controls'], 'WASD / Arrow keys')}
		"""
	).strip()
	bundle = prompt_json_bundle(
		prompt,
		"html_review",
		schema_example,
		default={},
		stage_id="html_review",
		target_dir=target_dir,
	)
	if not coerce_bool(bundle.get("reviseHtmlShell"), default=False):
		return
	concept["story_intro"] = coerce_text(bundle.get("storyIntro"), concept["story_intro"])
	updated_description = coerce_text(bundle.get("description"), description)
	ui_notes = coerce_list(bundle.get("uiNotes"), fallback=concept["controls"], minimum_items=2)
	if ui_notes:
		concept["controls"] = ui_notes
	create_html_file(target_dir, title, updated_description, concept["story_intro"], concept["controls"])


def run_validation_loops(target_dir: Path, default_loops: int = 3) -> None:
	if default_loops <= 0:
		write_text_file(
			target_dir / "completion-gate.md",
			"# Validation Completion\n\nValidation loops were skipped. Review the generated files manually.\n",
		)
		update_validation_spec(
			target_dir,
			{
				"loop_index": "skipped",
				"html_rewrite_gate": "skipped",
				"json_rewrite_gate": "skipped",
				"review_assessment": "Validation loops were skipped.",
				"continue_gate": "stopped",
				"issues": [],
				"breakdown": [],
				"review_notes": [],
				"next_focus": ["Review generated files manually."],
			},
		)
		return

	print("\nSTAGE 9: Run Plan -> Action -> Review -> Continue Gate loops.")
	completed_loops = 0

	for loop_index in range(1, default_loops + 1):
		completed_loops = loop_index
		schema_example = textwrap.dedent(
			"""
			{
			  "issues": ["string"],
			  "fixes": ["string"],
			  "breakdown": ["string"],
			  "goals": ["string"],
			  "htmlRewriteGate": false,
			  "replacementHtml": "string",
			  "jsonRewriteGate": false,
			  "replacementJson": "string",
			  "editPlan": [
			    {"file": "string", "reason": "string", "exactChange": "string", "invariant": "string", "verificationCommand": "string"}
			  ],
			  "reviewAssessment": "string",
			  "reviewNotes": ["string"],
			  "continueGate": true,
			  "memoryUpdate": {
			    "summary": "string",
			    "decisions": ["string"],
			    "rejectedIdeas": ["string"],
			    "openIssues": ["string"],
			    "nextStageNotes": ["string"]
			  }
			}
			"""
		).strip()
		prompt = textwrap.dedent(
			f"""
			Run one full validation loop for the generated game folder. In one payload, identify the concrete issues, isolate the most important fixes, break the work into executable steps, decide whether HTML or JSON rewrites are needed, assess whether the build improved, and decide whether another validation loop should run.

			Game folder: {target_dir.name}
			Loop index: {loop_index:02d}
			Canonical specs available: GAME-CONCEPT-SPEC.md, FEATURE-SPRINT-SPEC.md, BUILD-SPEC.md, VALIDATION-SPEC.md
			"""
		).strip()
		bundle = prompt_json_bundle(
			prompt,
			"validation_loop",
			schema_example,
			default={},
			stage_id="validation_loop",
			target_dir=target_dir,
		)
		issues = coerce_list(bundle.get("issues"), fallback=["Review current game build for the next concrete issue."], minimum_items=1)
		create_validation_file(target_dir, loop_index, "issues", format_list(issues, "No issues recorded."))

		fixes = coerce_list(bundle.get("fixes"), fallback=issues[:3], minimum_items=1)
		create_validation_file(target_dir, loop_index, "plan", format_list(fixes, "No action plan recorded."))

		breakdown = coerce_list(bundle.get("breakdown"), fallback=fixes, minimum_items=1)
		create_validation_file(target_dir, loop_index, "breakdown", format_list(breakdown, "No implementation breakdown recorded."))

		goals = coerce_list(bundle.get("goals"), fallback=fixes, minimum_items=1)
		create_validation_file(target_dir, loop_index, "goal-spec", format_list(goals, "No goal spec recorded."))
		edit_plan_raw = bundle.get("editPlan", []) if isinstance(bundle.get("editPlan"), list) else []
		edit_plan = []
		for item in edit_plan_raw:
			if not isinstance(item, dict):
				continue
			edit_plan.append(
				{
					"file": coerce_text(item.get("file"), "game.js"),
					"reason": coerce_text(item.get("reason"), "Repair validation issue."),
					"exact_change": coerce_text(item.get("exactChange"), "Apply the narrow validation repair."),
					"invariant": coerce_text(item.get("invariant"), "Preserve unrelated generated game behavior."),
					"verification_command": coerce_text(item.get("verificationCommand"), "Open the generated index.html and confirm the repair manually."),
				}
			)
		if not edit_plan:
			edit_plan = [
				{
					"file": "game.js",
					"reason": "Validation loop requires a planned repair before rewrites.",
					"exact_change": fixes[0] if fixes else "Inspect the generated runtime.",
					"invariant": "Do not rewrite generated HTML or JSON without a concrete plan.",
					"verification_command": "Open the generated index.html and confirm the repair manually.",
				}
			]
		edit_plan_content = "\n\n".join(
			textwrap.dedent(
				f"""
				### {item['file']}

				- Reason: {item['reason']}
				- Exact change: {item['exact_change']}
				- Invariant: {item['invariant']}
				- Verification command: {item['verification_command']}
				"""
			).strip()
			for item in edit_plan
		)
		create_validation_file(target_dir, loop_index, "edit-plan", edit_plan_content)

		rebuild_choice = "yes" if coerce_bool(bundle.get("htmlRewriteGate"), default=False) else "no"
		replacement_html = coerce_text(bundle.get("replacementHtml"), "")
		if rebuild_choice == "yes" and replacement_html.strip():
			write_text_file(target_dir / "index.html", replacement_html)
			print(f"Updated HTML page at {target_dir / 'index.html'}")

		json_choice = "yes" if coerce_bool(bundle.get("jsonRewriteGate"), default=False) else "no"
		replacement_json = coerce_text(bundle.get("replacementJson"), "")
		if json_choice == "yes" and replacement_json.strip():
			try:
				parsed = parse_json_response(replacement_json)
				write_json_file(target_dir / "story-structure.json", parsed)
				print(f"Updated JSON file at {target_dir / 'story-structure.json'}")
			except json.JSONDecodeError as exc:
				print(f"JSON was invalid: {exc}. The file was not updated.")

		review_assessment = coerce_text(bundle.get("reviewAssessment"), "yes - the build is moving in the right direction.")
		review_notes = coerce_list(bundle.get("reviewNotes"), fallback=[], minimum_items=0)
		review_content = textwrap.dedent(
			f"""
			**Review assessment:**
			{review_assessment}

			**Remaining issues or observations:**
			{format_list(review_notes, 'No remaining issues recorded.')}
			"""
		)
		create_validation_file(target_dir, loop_index, "review", review_content)

		continue_choice = "yes" if coerce_bool(bundle.get("continueGate"), default=True) else "no"
		gate_status = "Continue" if continue_choice == "yes" else "Stop"
		create_continue_gate_file(target_dir, loop_index, gate_status, review_notes)
		update_validation_spec(
			target_dir,
			{
				"loop_index": loop_index,
				"html_rewrite_gate": "yes" if rebuild_choice == "yes" else "no",
				"json_rewrite_gate": "yes" if json_choice == "yes" else "no",
				"review_assessment": review_assessment,
				"continue_gate": gate_status,
				"issues": issues,
				"breakdown": breakdown,
				"review_notes": review_notes,
				"next_focus": review_notes if continue_choice == "yes" else ["Stop after current validation loop."],
			},
		)
		if continue_choice != "yes":
			print("Stopping early based on the continue gate.")
			break

	completion_content = textwrap.dedent(
		f"""
		# Validation Completion

		Completed {completed_loops} Plan -> Action -> Review -> Continue Gate loop(s).

		Review the generated files and confirm that the build is ready for the next manual pass.
		"""
	)
	write_text_file(target_dir / "completion-gate.md", completion_content)
	print(f"Created completion gate file at {target_dir / 'completion-gate.md'}")


def get_seed_value(combination: dict, singular: str, plural: str, default: str) -> str:
	value = combination.get(singular)
	if not value:
		value = combination.get(plural)
	if isinstance(value, list):
		return ", ".join(value)
	return str(value) if value else default


def extract_brainstorm_terms(text: str, limit: int = 3) -> list[str]:
	terms = []
	seen = set()
	for raw_word in re.findall(r"[a-zA-Z]{4,}", text.lower()):
		if raw_word in BRAINSTORM_STOPWORDS or raw_word in seen:
			continue
		seen.add(raw_word)
		terms.append(raw_word)
		if len(terms) >= limit:
			break
	return terms


def merge_unique_strings(*collections, limit: int | None = None) -> list[str]:
	merged = []
	seen = set()
	for collection in collections:
		for item in collection:
			text = coerce_text(item)
			if not text:
				continue
			key = text.lower()
			if key in seen:
				continue
			seen.add(key)
			merged.append(text)
			if limit is not None and len(merged) >= limit:
				return merged
	return merged


def choose_runtime_template_from_spec(combination: dict, final_data: dict) -> tuple[str, str, str]:
	text = json.dumps({"seed": combination, "final": final_data}, ensure_ascii=False).lower()
	if any(word in text for word in ("route runner", "runner", "delivery", "checkpoint", "finish line", "lane", "sprint", "momentum", "parkour", "chase", "scrolling")):
		return "route_runner", "route runner", "lane route"
	if any(word in text for word in ("relay", "signal", "reconnect", "circuit", "network", "node", "link", "sequence", "chain reaction")):
		return "relay_chain", "relay chain", "node network"
	if any(word in text for word in ("maze", "map", "library", "cavern", "ruin", "search", "artifact", "vault", "extraction", "key", "escape route")):
		return "extraction_maze", "extraction maze", "maze"
	if any(word in text for word in ("stealth", "infiltration", "crouch", "avoid", "sneak", "caught", "alarm", "visibility", "shadow")):
		return "stealth_patrol", "stealth patrol", "patrol grid"
	return "arena_survival", "arena survival", "arena"


def derive_game_design_profile(combination: dict, final_data: dict, summary_data: dict | None = None) -> dict:
	summary_data = summary_data or {}
	final_spec = final_data.get("finalSpec", {}) if isinstance(final_data.get("finalSpec"), dict) else {}
	world = final_spec.get("world", {}) if isinstance(final_spec.get("world"), dict) else {}
	progression = final_spec.get("progression", {}) if isinstance(final_spec.get("progression"), dict) else {}
	encounter_design = final_spec.get("encounterDesign", {}) if isinstance(final_spec.get("encounterDesign"), dict) else {}
	ui_spec = final_spec.get("ui", {}) if isinstance(final_spec.get("ui"), dict) else {}
	runtime_template, mechanic_family, spatial_structure = choose_runtime_template_from_spec(combination, final_data)
	failure_pressure = merge_unique_strings(
		coerce_list(final_spec.get("enemyTypes"), fallback=[], minimum_items=0),
		coerce_list(encounter_design.get("hazards"), fallback=[], minimum_items=0),
		limit=8,
	)
	progression_shape = merge_unique_strings(
		coerce_list(progression.get("metaGoal"), fallback=[], minimum_items=0),
		coerce_list(progression.get("rewardHooks"), fallback=[], minimum_items=0),
		[progression.get("runToRunGrowth")],
		limit=8,
	)
	presentation_rules = merge_unique_strings(
		[world.get("setting"), world.get("visualDirection")],
		coerce_list(ui_spec.get("readabilityGoals"), fallback=[], minimum_items=0),
		limit=8,
	)
	return {
		"seedContract": {
			"seed": combination,
			"sourceSeed": final_data.get("sourceSeed") or summary_data.get("sourceFile"),
			"sourceSummary": final_data.get("sourceSummary"),
			"sourceSamples": summary_data.get("gameDesignDoc", {}).get("sourceSamples", {}),
		},
		"mechanicFamily": mechanic_family,
		"runtimeTemplate": runtime_template,
		"pacing": final_spec.get("sessionLength", "short readable arcade run"),
		"spatialStructure": spatial_structure,
		"failurePressure": failure_pressure,
		"progressionShape": progression_shape,
		"presentationRules": presentation_rules,
		"mustPreserve": [
			"Preserve the randomized seed contract through every stage.",
			"Treat final-brainstorming.json as the canonical game specification.",
			"Keep the generated game self-contained in one Pages/<slug>/ folder.",
			"Make runtime behavior match runtimeTemplate instead of defaulting to one arena scaffold.",
		],
		"fallbackSource": final_data.get("fallbackSource", ""),
	}


def ensure_game_design_profile(combination: dict, final_data: dict, summary_data: dict | None = None) -> dict:
	if not isinstance(final_data, dict):
		return derive_game_design_profile(combination, {}, summary_data)
	profile = final_data.get("gameDesignProfile")
	if not isinstance(profile, dict) or not profile.get("runtimeTemplate"):
		profile = derive_game_design_profile(combination, final_data, summary_data)
		final_data["gameDesignProfile"] = profile
	seed_contract = profile.get("seedContract")
	if not isinstance(seed_contract, dict):
		seed_contract = {}
	seed_contract["seed"] = combination
	if summary_data and not seed_contract.get("sourceSamples"):
		seed_contract["sourceSamples"] = summary_data.get("gameDesignDoc", {}).get("sourceSamples", {})
	if not seed_contract.get("sourceSeed"):
		seed_contract["sourceSeed"] = final_data.get("sourceSeed") or (summary_data or {}).get("sourceFile")
	if not seed_contract.get("sourceSummary"):
		seed_contract["sourceSummary"] = final_data.get("sourceSummary")
	profile["seedContract"] = seed_contract
	final_data["gameDesignProfile"] = profile
	return profile


def infer_brainstorm_seed_inputs(title: str, description: str, objective: str, combination: dict) -> dict:
	theme_text = get_seed_value(combination, "theme", "themes", "")
	environment_text = get_seed_value(combination, "environment", "environments", "")
	setting_text = get_seed_value(combination, "setting", "settings", "")
	loop_text = get_seed_value(combination, "coreLoop", "coreLoops", "")
	motivation_text = get_seed_value(combination, "characterMotivation", "characterMotivations", "")
	return {
		"environment": extract_brainstorm_terms(f"{environment_text} {setting_text} {title} {description}"),
		"mechanic": extract_brainstorm_terms(f"{loop_text} {objective} {title}"),
		"enemy": extract_brainstorm_terms(f"{theme_text} {description}"),
		"progression": extract_brainstorm_terms(f"{motivation_text} {objective} {description}"),
	}


def build_brainstorm_seed_injections(combination: dict) -> dict[str, list[str]]:
	injections: dict[str, list[str]] = {}
	for seed_key, category_name in BRAINSTORM_SEED_CATEGORY_MAP.items():
		value = combination.get(seed_key)
		if isinstance(value, list):
			raw_values = [str(item) for item in value]
		else:
			raw_values = [str(value or "")]
		terms: list[str] = []
		for raw_value in raw_values:
			compact = re.sub(r"[^a-zA-Z]+", "", raw_value.lower())
			if len(compact) >= 4:
				terms.append(compact)
			terms.extend(extract_brainstorm_terms(raw_value, limit=3))
		terms = merge_unique_strings(terms, limit=3)
		if terms:
			injections[category_name] = terms
	return injections


def run_brainstorm_cli(script_path: Path, cli_args: list[str], label: str) -> str:
	command = [sys.executable, str(script_path), *cli_args]
	completed = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True)
	if completed.returncode != 0:
		failure_output = (completed.stderr or completed.stdout or "Unknown error").strip()
		raise RuntimeError(f"{label} failed: {failure_output}")
	stdout_lines = [line.strip() for line in (completed.stdout or "").splitlines() if line.strip()]
	if not stdout_lines:
		raise RuntimeError(f"{label} did not report an output path.")
	return stdout_lines[-1]


def run_brainstorm_pipeline(
	target_dir: Path,
	title: str,
	description: str,
	objective: str,
	combination: dict,
	brainstorm_mode: str = "auto",
	brainstorm_endpoint: str | None = None,
	brainstorm_model: str | None = None,
) -> dict:
	seed_inputs = infer_brainstorm_seed_inputs(title, description, objective, combination)
	seed_output = target_dir / "brainstorm-seed.json"
	summary_output = target_dir / "brainstorm-summary.json"
	final_output = target_dir / "final-brainstorming.json"
	seed_source = ROOT / "PagesInteractive-CLI" / "seed_brainstorming.json"

	seed_args = ["--source", str(seed_source), "--output", str(seed_output), "--raw"]
	for category in ("environment", "mechanic", "enemy", "progression"):
		if seed_inputs[category]:
			seed_args.extend([f"--{category}", ",".join(seed_inputs[category])])
	for category_name, terms in build_brainstorm_seed_injections(combination).items():
		seed_args.extend(["--inject", f"{category_name}={','.join(terms)}"])

	print("Running brainstorm seed expansion...")
	run_brainstorm_cli(SEED_FETCHER_CLI_FILE, seed_args, "seed fetcher")
	print("Running brainstorm summary synthesis...")
	run_brainstorm_cli(
		CHAINSUMMARY_CLI_FILE,
		[
			"--file",
			str(seed_output),
			"--output",
			str(summary_output),
			"--exploration-level",
			"expansive",
			"--sample-size",
			"3",
			"--smooth-sample-size",
			"6",
			"--raw",
		],
		"chain summary",
	)
	print("Running final brainstorm synthesis...")
	run_brainstorm_cli(
		BRAINSTORM_CLI_FILE,
		[
			"--file",
			str(summary_output),
			"--output",
			str(final_output),
			"--exploration-loops",
			"4",
			"--brainstorm-mode",
			brainstorm_mode,
			"--endpoint",
			brainstorm_endpoint or "http://10.0.0.137:1234/v1/chat/completions",
			"--model",
			brainstorm_model or "qwen3.5-2b@q8_0",
			"--random-seed",
			str(random.randint(1, 1000000)),
			"--raw",
		],
		"brainstorm finalizer",
	)

	with open(seed_output, "r", encoding="utf-8") as handle:
		seed_data = json.load(handle)
	with open(summary_output, "r", encoding="utf-8") as handle:
		summary_data = json.load(handle)
	with open(final_output, "r", encoding="utf-8") as handle:
		final_data = json.load(handle)

	return {
		"seed_path": seed_output,
		"summary_path": summary_output,
		"final_path": final_output,
		"seed_data": seed_data,
		"summary_data": summary_data,
		"final_data": final_data,
	}


def materialize_brainstorm_artifacts(target_dir: Path, brainstorm_artifacts: dict, combination: dict | None = None) -> dict:
	seed_path = target_dir / "brainstorm-seed.json"
	summary_path = target_dir / "brainstorm-summary.json"
	final_path = target_dir / "final-brainstorming.json"

	seed_data = json.loads(json.dumps(brainstorm_artifacts.get("seed_data", {})))
	summary_data = json.loads(json.dumps(brainstorm_artifacts.get("summary_data", {})))
	final_data = json.loads(json.dumps(brainstorm_artifacts.get("final_data", {})))

	if isinstance(summary_data, dict):
		summary_data["sourceFile"] = str(seed_path)
	if isinstance(final_data, dict):
		final_data["sourceSummary"] = str(summary_path)
		final_data["sourceSeed"] = str(seed_path)
		ensure_game_design_profile(combination or {}, final_data, summary_data if isinstance(summary_data, dict) else {})

	write_json_file(seed_path, seed_data)
	write_json_file(summary_path, summary_data)
	write_json_file(final_path, final_data)

	return {
		"seed_path": seed_path,
		"summary_path": summary_path,
		"final_path": final_path,
		"seed_data": seed_data,
		"summary_data": summary_data,
		"final_data": final_data,
	}


def derive_canonical_brainstorm_identity(brainstorm_artifacts: dict, fallback_title: str, fallback_description: str, fallback_objective: str) -> dict:
	final_data = brainstorm_artifacts.get("final_data", {}) if isinstance(brainstorm_artifacts, dict) else {}
	page_identity = final_data.get("pageIdentity", {}) if isinstance(final_data.get("pageIdentity"), dict) else {}
	build_packet = final_data.get("buildPacket", {}) if isinstance(final_data.get("buildPacket"), dict) else {}
	overlay = build_packet.get("overlay", {}) if isinstance(build_packet.get("overlay"), dict) else {}
	hud = build_packet.get("hud", {}) if isinstance(build_packet.get("hud"), dict) else {}

	title = coerce_text(page_identity.get("title"), coerce_text(final_data.get("title"), fallback_title))
	description = coerce_text(page_identity.get("description"), coerce_text(final_data.get("oneLinePitch"), fallback_description))
	objective = coerce_text(page_identity.get("objective"), coerce_text(hud.get("objective"), fallback_objective))
	briefing = coerce_text(page_identity.get("overlayBriefing"), coerce_text(overlay.get("introBriefing"), description))
	hud_objective = coerce_text(page_identity.get("hudObjective"), objective)

	return {
		"title": title,
		"slug": slugify(coerce_text(page_identity.get("slug"), title)),
		"description": description,
		"objective": objective,
		"overlay_briefing": briefing,
		"hud_objective": hud_objective,
	}


def convert_final_brainstorm_to_concept(title: str, description: str, objective: str, combination: dict, brainstorm_artifacts: dict) -> dict:
	final_data = brainstorm_artifacts.get("final_data", {}) if isinstance(brainstorm_artifacts, dict) else {}
	summary_data = brainstorm_artifacts.get("summary_data", {}) if isinstance(brainstorm_artifacts, dict) else {}
	game_design_profile = ensure_game_design_profile(combination, final_data, summary_data)
	final_spec = final_data.get("finalSpec", {}) if isinstance(final_data, dict) else {}
	page_identity = final_data.get("pageIdentity", {}) if isinstance(final_data.get("pageIdentity"), dict) else {}
	build_packet = final_data.get("buildPacket", {}) if isinstance(final_data.get("buildPacket"), dict) else {}
	overlay = build_packet.get("overlay", {}) if isinstance(build_packet.get("overlay"), dict) else {}
	hud = build_packet.get("hud", {}) if isinstance(build_packet.get("hud"), dict) else {}
	summary_doc = summary_data.get("gameDesignDoc", {}) if isinstance(summary_data, dict) else {}
	world = final_spec.get("world", {}) if isinstance(final_spec.get("world"), dict) else {}
	progression = final_spec.get("progression", {}) if isinstance(final_spec.get("progression"), dict) else {}
	run_structure = final_spec.get("runStructure", {}) if isinstance(final_spec.get("runStructure"), dict) else {}
	encounter_design = final_spec.get("encounterDesign", {}) if isinstance(final_spec.get("encounterDesign"), dict) else {}
	technical_build = final_spec.get("technicalBuild", {}) if isinstance(final_spec.get("technicalBuild"), dict) else {}
	ui_spec = final_spec.get("ui", {}) if isinstance(final_spec.get("ui"), dict) else {}

	player_actions = coerce_list(
		final_spec.get("playerActions"),
		fallback=summary_doc.get("mechanics", {}).get("primaryActions", []),
		minimum_items=3,
	)
	if len(player_actions) < 3:
		player_actions = merge_unique_strings(player_actions, ["root", "petal", "sprint"], limit=3)

	loop_beats = merge_unique_strings(
		coerce_list(final_spec.get("coreLoop"), fallback=[], minimum_items=0),
		[run_structure.get("opening"), run_structure.get("midgame"), run_structure.get("endgame")],
		coerce_list(summary_doc.get("coreLoop"), fallback=[], minimum_items=0),
		limit=6,
	)
	if len(loop_beats) < 4:
		loop_beats = merge_unique_strings(
			loop_beats,
			[
				"Enter the route and read the first threat.",
				"Use the core verb set to resolve the active pressure.",
				"Convert the current room into progression gain.",
				"Trigger the completion condition and finish the playfield.",
			],
			limit=6,
		)

	random_injections = final_data.get("randomInjections", []) if isinstance(final_data.get("randomInjections"), list) else []
	random_effects = [item.get("effect") for item in random_injections if isinstance(item, dict)]
	pressure = merge_unique_strings(
		coerce_list(final_spec.get("enemyTypes"), fallback=[], minimum_items=0),
		coerce_list(encounter_design.get("hazards"), fallback=[], minimum_items=0),
		random_effects,
		limit=6,
	)
	if len(pressure) < 3:
		pressure = merge_unique_strings(pressure, ["enemy pressure", "route hazards", "time pressure"], limit=6)

	rewards = merge_unique_strings(
		coerce_list(progression.get("metaGoal"), fallback=[], minimum_items=0),
		coerce_list(progression.get("rewardHooks"), fallback=[], minimum_items=0),
		[progression.get("runToRunGrowth")],
		limit=6,
	)
	if len(rewards) < 3:
		rewards = merge_unique_strings(rewards, [objective, "route unlocks", "new ability gains"], limit=6)

	fail_states = merge_unique_strings(
		[
			f"Get overwhelmed by {pressure[0]}." if pressure else "Get overwhelmed by enemy pressure.",
			"Run out of time before the completion condition unlocks.",
			"Lose health by lingering in active hazard lanes.",
		],
		limit=4,
	)

	visual_identity = merge_unique_strings(
		[world.get("setting"), world.get("visualDirection")],
		coerce_list(world.get("landmarks"), fallback=[], minimum_items=0),
		limit=6,
	)
	if len(visual_identity) < 4:
		visual_identity = merge_unique_strings(
			visual_identity,
			["storm-lit arena lanes", "high-contrast enemy silhouettes", "rainy neon reflections", "goal-first readability"],
			limit=6,
		)

	controls = merge_unique_strings(
		[
			"WASD or Arrow keys move the player through the arena.",
			f"Shift triggers a {player_actions[2]} burst for repositioning." if len(player_actions) > 2 else "Shift triggers a burst dash.",
			f"Space converts {player_actions[0]} and {player_actions[1]} pressure into crowd control." if len(player_actions) > 1 else "Space triggers the arena-control ability.",
			coerce_text(overlay.get("startHint"), "Press Enter to deploy. Use WASD or Arrow keys to move, Shift to dash, and Space to pulse."),
		],
		coerce_list(ui_spec.get("hud"), fallback=[], minimum_items=0),
		limit=6,
	)

	data_hooks = merge_unique_strings(
		[
			"scene layout",
			"enemy waves",
			"objective rewards",
			"goal unlock state",
			"brainstorm final spec",
		],
		coerce_list(technical_build.get("systemsNeeded"), fallback=[], minimum_items=0),
		limit=6,
	)

	hook = coerce_text(
		page_identity.get("description"),
		coerce_text(
			final_data.get("oneLinePitch"),
			coerce_text(summary_doc.get("elevatorPitch"), f"{title} turns the current seed into a readable arcade challenge."),
		),
	)
	uniqueness = coerce_text(
		final_spec.get("playerFantasy"),
		f"{title} uses {join_inline(player_actions[:3], 'arcade verbs')} inside {join_inline(visual_identity[:3], 'a readable world')}.",
	)
	story_intro = coerce_text(page_identity.get("overlayBriefing"), coerce_text(overlay.get("introBriefing"), coerce_text(final_data.get("oneLinePitch"), hook)))
	status_message = coerce_text(
		page_identity.get("hudObjective"),
		coerce_text(hud.get("objective"), f"Complete objectives, resolve {join_inline(pressure[:2], 'enemy pressure')}, and trigger the finish condition."),
	)
	action_map = merge_unique_strings(player_actions, loop_beats, limit=6)
	detail_items = merge_unique_strings(pressure, rewards, limit=6)
	collapsed_tasks = [
		f"Implement player actions: {join_inline(player_actions[:3], 'movement verbs')}.",
		f"Build the run beats: {join_inline(loop_beats[:4], 'opening, escalation, mastery, extraction')}.",
		f"Support pressure sources: {join_inline(pressure[:3], 'enemy lanes and hazards')}.",
		f"Expose JSON hooks: {join_inline(data_hooks[:4], 'scene, enemies, rewards, goal')}.",
	]

	return {
		"hook": hook,
		"player_actions": player_actions,
		"loop_beats": loop_beats,
		"pressure": pressure,
		"rewards": rewards,
		"fail_states": fail_states,
		"uniqueness": uniqueness,
		"visual_identity": visual_identity,
		"controls": controls,
		"data_hooks": data_hooks,
		"story_intro": story_intro,
		"status_message": status_message,
		"action_map": action_map[:6],
		"detail_items": detail_items[:6],
		"collapsed_tasks": collapsed_tasks,
		"brainstorm_seed_file": str(brainstorm_artifacts["seed_path"]),
		"brainstorm_summary_file": str(brainstorm_artifacts["summary_path"]),
		"brainstorm_final_file": str(brainstorm_artifacts["final_path"]),
		"brainstorm_summary": summary_data,
			"brainstorm_final": final_data,
			"game_design_profile": game_design_profile,
			"page_identity": page_identity,
		"build_packet": build_packet,
	}


def collect_frontier_concept(title: str, description: str, objective: str, combination: dict, target_dir: Path) -> dict:
	print("Running the brainstorm pipeline for the concept stage...")
	brainstorm_artifacts = run_brainstorm_pipeline(target_dir, title, description, objective, combination)
	concept = convert_final_brainstorm_to_concept(title, description, objective, combination, brainstorm_artifacts)
	print(f"Saved brainstorm seed to {brainstorm_artifacts['seed_path']}")
	print(f"Saved brainstorm summary to {brainstorm_artifacts['summary_path']}")
	print(f"Saved final brainstorm spec to {brainstorm_artifacts['final_path']}")
	return concept


def compose_expansion_text(title: str, objective: str, concept: dict) -> str:
	return textwrap.dedent(
		f"""
		- Core hook: {concept['hook']}
		- Objective frame: {objective}
		- Distinct angle: {concept['uniqueness']}
		- Player actions: {join_inline(concept['player_actions'], 'move and react')}
		- Pressure sources: {join_inline(concept['pressure'], 'obstacles and timers')}
		- Rewards and escalation: {join_inline(concept['rewards'], 'survival and score growth')}
		- Visual identity: {join_inline(concept['visual_identity'], 'strong readable shapes')}
		- Data hooks: {join_inline(concept['data_hooks'], 'scene, rules, goals, events')}
		- Title anchor: {title}
		"""
	).strip()


def collect_build_planning_bundle(title: str, description: str, objective: str, concept: dict, feature_packets: list[dict]) -> dict:
	final_data = concept.get("brainstorm_final", {}) if isinstance(concept.get("brainstorm_final"), dict) else {}
	final_spec = final_data.get("finalSpec", {}) if isinstance(final_data.get("finalSpec"), dict) else {}
	build_packet = final_data.get("buildPacket", {}) if isinstance(final_data.get("buildPacket"), dict) else {}
	technical_build = final_spec.get("technicalBuild", {}) if isinstance(final_spec.get("technicalBuild"), dict) else {}
	ui_spec = final_spec.get("ui", {}) if isinstance(final_spec.get("ui"), dict) else {}

	implementation_chapters = coerce_list(build_packet.get("implementationChapters"), fallback=[], minimum_items=0)
	if not implementation_chapters:
		implementation_chapters = [humanize_identifier(item) for item in coerce_list(technical_build.get("prototypeOrder"), fallback=[], minimum_items=0)]
	if not implementation_chapters:
		implementation_chapters = [
			"Core Movement Loop",
			"Threat Pressure Pass",
			"Reward And Goal Flow",
			"Presentation And Overlay Polish",
		]

	fun_needs = merge_unique_strings(
		coerce_list(ui_spec.get("readabilityGoals"), fallback=[], minimum_items=0),
		concept.get("controls", [])[:2],
		concept.get("pressure", [])[:2],
		concept.get("rewards", [])[:2],
		limit=5,
	)
	if len(fun_needs) < 3:
		fun_needs = merge_unique_strings(
			fun_needs,
			[
				"Immediate readable feedback",
				"Escalation that stays fair",
				"A clear exit condition",
			],
			limit=5,
		)

	return {
		"fun_assessment": (
			f"yes - {title} has a readable arcade core built around "
			f"{join_inline(concept['player_actions'][:2], 'core verbs')} against {join_inline(concept['pressure'][:2], 'active pressure')} "
			f"with a clear payoff in {join_inline(concept['rewards'][:2], 'run progression')}."
		),
		"fun_needs": fun_needs,
		"implementation_chapters": implementation_chapters,
	}


def compose_design_text(title: str, description: str, objective: str, combination: dict, concept: dict, feature_packets: list[dict]) -> str:
	return textwrap.dedent(
		f"""
		## {title}

		**Description:** {description}

		**Objective:** {objective}

		**Seed Summary:**
		{format_combination(combination)}

		## Core Fantasy

		{concept['hook']}

		## Why This Game Is Distinct

		{concept['uniqueness']}

		## Player Actions
		{format_list(concept['player_actions'], 'Define the player actions.')}

		## Core Loop
		{format_list(concept['loop_beats'], 'Define the gameplay loop.')}

		## Pressure And Opposition
		{format_list(concept['pressure'], 'Define the pressure sources.')}

		## Rewards And Progression
		{format_list(concept['rewards'], 'Define the rewards and escalation.')}

		## Failure States
		{format_list(concept['fail_states'], 'Define the fail states.')}

		## Visual Identity
		{format_list(concept['visual_identity'], 'Define the visual identity.')}

		## Controls And Readability
		{format_list(concept['controls'], 'Define the controls and HUD.')}

		## JSON Data Hooks
		{format_list(concept['data_hooks'], 'Define the JSON hooks.')}

		## Sprint Builder Branches
		{format_feature_packets_for_design(feature_packets)}

		## Delivery Notes

		- Keep this game self-contained inside its own page folder.
		- Keep the HTML entry point and story JSON in the same folder.
		- Preserve a three.js + Rapier prototype structure.
		- Favor game-specific logic over shared systems.
		- Use branch-specific change packets to plan the next sprint in isolated slices.
		"""
	).strip()


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Interactive arcade page builder tuned for smaller frontier prompts")
	parser.add_argument("--force", action="store_true", help="Overwrite existing target directories without prompting.")
	parser.add_argument("--title", type=str, help="Use this title as a brainstorm hint instead of the seed-generated default.")
	parser.add_argument("--description", type=str, help="Use this description as a brainstorm hint instead of the seed-generated default.")
	parser.add_argument("--objective", type=str, help="Use this objective as a brainstorm hint instead of the seed-generated default.")
	parser.add_argument("--implementation-sprints", type=int, default=2, help="Number of implementation sprint passes to run.")
	parser.add_argument("--validation-loops", type=int, default=3, help="Number of validation loops to run.")
	parser.add_argument("--arcade-integration-passes", type=int, default=1, help="Number of arcade integration review and ensure passes to run.")
	parser.add_argument("--brainstorm-mode", choices=("auto", "required", "skip"), default="auto", help="Use LM Studio additively, require it, or skip it for deterministic brainstorm fallbacks.")
	parser.add_argument("--brainstorm-endpoint", type=str, default="http://10.0.0.137:1234/v1/chat/completions", help="LM Studio chat completions endpoint for brainstorm finalization.")
	parser.add_argument("--brainstorm-model", type=str, default="qwen3.5-2b@q8_0", help="LM Studio model id for brainstorm finalization.")
	parser.add_argument("--resume", type=str, help="Path to frontier-memory.json to resume a build.")
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	global ACTIVE_FRONTIER_MEMORY_PATH
	
	resuming = False
	start_stage = 1
	
	if args.resume:
		ACTIVE_FRONTIER_MEMORY_PATH = Path(args.resume)
		if ACTIVE_FRONTIER_MEMORY_PATH.exists():
			memory = load_json_file(ACTIVE_FRONTIER_MEMORY_PATH, {})
			resuming = True
			start_stage = int(memory.get("nextStage", 1))
			game_title = memory.get("gameTitle", "Resumed Game")
			target_dir = ACTIVE_FRONTIER_MEMORY_PATH.parent
			folder_name = target_dir.name
			combination = memory.get("seedCombination", {})
			# We need to reconstruct some variables that would have been set in earlier stages
			game_description = memory.get("profile", {}).get("oneLinePitch", "")
			game_objective = memory.get("profile", {}).get("objective", "")
			print(f"Resuming build for '{game_title}' at Stage {start_stage}...")
		else:
			print(f"Error: Resume file {args.resume} not found.")
			sys.exit(1)

	if not resuming:
		launcher_prompt = render_launcher_prompt(DEFAULT_LAUNCHER_PROMPT)
		if launcher_prompt:
			print("AGENT-START PROMPT")
			print(launcher_prompt)
			print()

	print("Interactive arcade game builder for smaller frontier prompts")
	print("This script runs the brainstorm chain first, then creates a new Page folder from the canonical brainstorm packet, saves DESIGN.md, builds implementation chapters, and scaffolds a story JSON shape.\n")

	load_env_file(ROOT / ".env")
	seed = load_seed_data()
	combination = sample_combination(seed)
	
	# Diversify the global seed library with new variants based on this sample
	if args.brainstorm_mode != "skip":
		diversify_seed_library(seed, combination, args.brainstorm_model, args.brainstorm_endpoint)
		
	print(format_combination(combination))

	default_title = get_seed_value(combination, "theme", "themes", "New Arcade Game").title()
	default_description = (
		f"A {get_seed_value(combination, 'theme', 'themes', 'new game')} set in "
		f"{get_seed_value(combination, 'environment', 'environments', 'a vivid location')} at "
		f"{get_seed_value(combination, 'setting', 'settings', 'a dramatic time')}."
	)
	default_objective = (
		f"{get_seed_value(combination, 'characterMotivations', 'characterMotivations', 'Complete the mission').capitalize()} "
		f"through {get_seed_value(combination, 'coreLoops', 'coreLoops', 'a readable gameplay loop')}."
	)
	title_hint = args.title or default_title
	description_hint = args.description or default_description
	objective_hint = args.objective or default_objective
	brainstorm_artifacts = {}
	brainstorm_identity = {}
	brainstorm_attempt = 0

	if start_stage <= 1:
		while True:
			brainstorm_attempt += 1
			existing_pages = scan_existing_pages()
			print(f"\nSTAGE 1: Run the brainstorm pipeline first and lock the canonical build packet. (Attempt {brainstorm_attempt})")
			with tempfile.TemporaryDirectory(prefix="frontier-brainstorm-") as staging_dir:
				brainstorm_artifacts = run_brainstorm_pipeline(
					Path(staging_dir),
					title_hint,
					description_hint,
					objective_hint,
					combination,
					brainstorm_mode=args.brainstorm_mode,
					brainstorm_endpoint=args.brainstorm_endpoint,
					brainstorm_model=args.brainstorm_model,
				)
			brainstorm_identity = derive_canonical_brainstorm_identity(brainstorm_artifacts, title_hint, description_hint, objective_hint)
			game_title = brainstorm_identity["title"]
			game_description = brainstorm_identity["description"]
			game_objective = brainstorm_identity["objective"]
			if confirm_unique_idea(game_title, game_description, existing_pages, force=args.force):
				break
			title_hint = f"{game_title} Variant"
			description_hint = game_description
			objective_hint = game_objective
			print("\nThe brainstorm identity was too close to an existing page. Rerunning the brainstorm chain with a stronger uniqueness hint.")

		folder_name = brainstorm_identity["slug"]
		target_dir = ensure_target_directory(folder_name, force=args.force)
		brainstorm_artifacts = materialize_brainstorm_artifacts(target_dir, brainstorm_artifacts, combination)
		print(f"Saved brainstorm seed to {brainstorm_artifacts['seed_path']}")
		print(f"Saved brainstorm summary to {brainstorm_artifacts['summary_path']}")
		print(f"Saved final brainstorm spec to {brainstorm_artifacts['final_path']}")

		seed_payload = {
			"title": game_title,
			"description": game_description,
			"objective": game_objective,
			"seed": combination,
		}
		create_seed_choice_file(target_dir, seed_payload)
	else:
		# Need these for later stages even if we skip stage 1
		brainstorm_artifacts = {
			"seed_path": target_dir / "seed_brainstorming.json",
			"summary_path": target_dir / "summary_brainstorming.json",
			"final_path": target_dir / "final-brainstorming.json"
		}

	if start_stage <= 2:
		print("\nSTAGE 2: Materialize the canonical concept from the locked brainstorm packet.")
		concept = convert_final_brainstorm_to_concept(game_title, game_description, game_objective, combination, brainstorm_artifacts)
		if not resuming:
			ACTIVE_FRONTIER_MEMORY_PATH = create_frontier_memory(
				target_dir,
				game_title,
				concept.get("game_design_profile", {}),
				brainstorm_artifacts,
				combination,
			)
		record_frontier_stage("stage-1-brainstorm-pipeline", "Locked final-brainstorming.json and initialized gameDesignProfile.")
		update_game_concept_spec(target_dir, game_title, game_description, game_objective, combination, concept)
		record_frontier_stage("stage-2-concept-materialization", "Materialized concept from locked brainstorm packet.")
	else:
		# Minimal concept load for later stages
		concept = convert_final_brainstorm_to_concept(game_title, game_description, game_objective, combination, brainstorm_artifacts)

	if start_stage <= 3:
		print("\nSTAGE 3: Derive the feature sprint spec from the brainstorm packet.")
		feature_packets = collect_feature_branch_packets(game_title, concept)
		create_feature_branch_files(target_dir, feature_packets)
		update_feature_sprint_spec(target_dir, feature_packets)
		record_frontier_stage("stage-3-feature-sprint-loop", "Derived feature sprint packets from canonical brainstorm data.")
	else:
		feature_packets = collect_feature_branch_packets(game_title, concept)

	if start_stage <= 4:
		print("\nSTAGE 4: Assemble the design document from the bundled concept and sprint specs.")
		design_text = compose_design_text(game_title, game_description, game_objective, combination, concept, feature_packets)
		create_design_file(target_dir, design_text)
		record_frontier_stage("stage-4-design-assembly", "Assembled design document.")
	else:
		design_text = compose_design_text(game_title, game_description, game_objective, combination, concept, feature_packets)

	if start_stage <= 5:
		print("\nSTAGE 5: Derive the build-planning payload from the brainstorm packet.")
		planning_bundle = collect_build_planning_bundle(game_title, game_description, game_objective, concept, feature_packets)
		fun_assessment = planning_bundle["fun_assessment"]
		fun_needs = planning_bundle["fun_needs"]
		design_text = append_fun_section_to_design(design_text, fun_assessment, fun_needs)
		create_design_file(target_dir, design_text)
		update_game_concept_spec(target_dir, game_title, game_description, game_objective, combination, concept, fun_assessment, fun_needs)
		record_frontier_stage("stage-5-build-planning-loop", "Derived fun assessment and implementation chapters.")
	else:
		planning_bundle = collect_build_planning_bundle(game_title, game_description, game_objective, concept, feature_packets)
		fun_assessment = planning_bundle["fun_assessment"]
		fun_needs = planning_bundle["fun_needs"]

	if start_stage <= 6:
		print("\nSTAGE 6: Materialize the build spec, story payload, and starter scaffold.")
		chapters = planning_bundle["implementation_chapters"]
		chapters_text = "\n".join(chapters)
		create_implementation_chapters(target_dir, chapters_text)
		update_build_spec(target_dir, chapters)

		create_story_json(target_dir, folder_name, game_title, game_description, {}, concept, design_text, chapters, fun_assessment, fun_needs, feature_packets)
		record_frontier_stage("stage-6-story-and-scaffold-materialization", "Created story payload and runtime scaffold.")
	else:
		chapters = planning_bundle["implementation_chapters"]

	if start_stage <= 7:
		print("\nSTAGE 7: Run one bundled HTML shell review pass.")
		create_game_script(target_dir)
		review_html_loop(target_dir, game_title, game_description, concept, force=args.force)
		record_frontier_stage("stage-7-html-review-loop", "Completed HTML shell review pass.")

	if start_stage <= 8:
		print("\nSTAGE 8: Run the implementation sprint loop with one bundled prompt per pass.")
		run_execution_sprint_loops(target_dir, game_title, feature_packets, default_passes=args.implementation_sprints)
		record_frontier_stage("stage-8-implementation-sprint-loop", "Completed configured implementation sprint passes.")

	if start_stage <= 9:
		print("\nSTAGE 9: Run the validation repair loop with one bundled prompt per pass.")
		run_validation_loops(target_dir, default_loops=args.validation_loops)
		record_frontier_stage("stage-9-validation-repair-loop", "Completed configured validation loops.")

	if start_stage <= 10:
		print("\nSTAGE 10: Register the generated game with the arcade library surfaces.")
		run_arcade_integration_loops(
			target_dir,
			folder_name,
			game_title,
			game_description,
			concept,
			default_passes=args.arcade_integration_passes,
		)
		record_frontier_stage("stage-10-arcade-integration-loop", "Completed arcade integration loop.")

	print(f"\nDone. The new page folder is ready at: {target_dir}")
	print("\nReview GAME-CONCEPT-SPEC.md, FEATURE-SPRINT-SPEC.md, BUILD-SPEC.md, VALIDATION-SPEC.md, and ARCADE-INTEGRATION-SPEC.md for the canonical agent-facing workflow state, then inspect implementation history and open index.html to test the story payload loading from story-structure.json.")


if __name__ == "__main__":
	main()
