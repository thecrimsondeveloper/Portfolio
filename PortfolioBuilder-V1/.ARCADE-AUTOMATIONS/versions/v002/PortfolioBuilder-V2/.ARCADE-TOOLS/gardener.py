#!/usr/bin/env python3
import argparse
import json
import random
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SEED_FILE = ROOT / ".ARCADE-SYSTEM" / "library" / "arcade-seed.json"
DEFAULT_ENDPOINT = "http://10.0.0.137:1234/v1/chat/completions"
DEFAULT_MODEL = "qwen3.5-2b@q8_0"

CATEGORIES = [
    "themes", "environments", "characterMotivations", "coreLoops", "antagonists", "visualStyles",
    "weatherEffects", "uiAesthetics", "movementQuirks", "environmentalHazards", "powerSources",
    "lightingStyles", "narrativeTone", "deathAnimations", "crowdDynamics", "mapModifiers",
    "soundscapes", "colorPalettes", "architecture", "artifactTypes", "gameTempo", "bossMechanics",
    "playerPerks", "enemyArchetypes", "narrativeStakes", "postProcessing"
]

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def call_llm(prompt: str, model: str, endpoint: str, temperature: float = 1.2) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a creative game designer. Reply only with a comma-separated list of items. No explanation."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": 256,
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res = json.load(response)
            return res.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        print(f"  [!] LLM Error: {e}")
        return ""

def expand_category(seed_data: dict, cat: str, count: int, model: str, endpoint: str, temp: float):
    options = seed_data.get("options", {}).get(cat, [])
    if not options:
        print(f"  [!] Category {cat} not found in options.")
        return 0
    
    # Pick a random base to inspire the LLM
    base_item = random.choice(options)
    prompt = (
        f"The category is '{cat}'. Based on the existing item '{base_item}', "
        f"generate {count} new, wild, and highly unique variations for an arcade game library. "
        "Avoid common clichés. Reply with a comma-separated list only."
    )
    
    print(f"  Expanding {cat} using '{base_item}' as inspiration...")
    response = call_llm(prompt, model, endpoint, temp)
    
    if not response:
        return 0
    
    raw_items = re.split(r"[,;|\n]+", response)
    new_items = [re.sub(r"^[-*0-9.\s]+", "", i).strip().lower() for i in raw_items if i.strip()]
    
    added_count = 0
    for item in new_items:
        if item and item not in options:
            options.append(item)
            print(f"    [+] Added: {item}")
            added_count += 1
            
    return added_count

def main():
    parser = argparse.ArgumentParser(description="Bulk expand the arcade-seed.json library using an LLM.")
    parser.add_argument("--loops", type=int, default=1, help="Number of times to loop through all categories.")
    parser.add_argument("--count", type=int, default=5, help="Number of items to add per category per loop.")
    parser.add_argument("--endpoint", type=str, default=DEFAULT_ENDPOINT, help="LLM API endpoint.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="LLM model name.")
    parser.add_argument("--temp", type=float, default=1.2, help="LLM sampling temperature.")
    parser.add_argument("--seed-file", type=str, default=str(DEFAULT_SEED_FILE), help="Path to arcade-seed.json.")
    
    args = parser.parse_args()
    seed_path = Path(args.seed_file)
    
    if not seed_path.exists():
        print(f"Error: Seed file not found at {seed_path}")
        return 1
    
    seed_data = load_json(seed_path)
    total_added = 0
    
    print(f"Starting expansion: {args.loops} loops, {args.count} items/cat per loop.")
    print(f"Target file: {seed_path}")
    print(f"Endpoint: {args.endpoint}")
    
    for i in range(args.loops):
        print(f"\n--- Loop {i+1}/{args.loops} ---")
        for cat in CATEGORIES:
            total_added += expand_category(seed_data, cat, args.count, args.model, args.endpoint, args.temp)
            
    if total_added > 0:
        save_json(seed_path, seed_data)
        print(f"\nSUCCESS: Added a total of {total_added} new items to the library.")
    else:
        print("\nNo new items were added.")
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
