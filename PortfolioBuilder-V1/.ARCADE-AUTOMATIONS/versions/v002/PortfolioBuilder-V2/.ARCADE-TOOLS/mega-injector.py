#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_FILE = ROOT / ".ARCADE-SYSTEM" / "library" / "arcade-seed.json"
BUILDER_FILE = ROOT / ".ARCADE-CLI" / "builder-frontier.py"

def inject_seed_data():
    if not SEED_FILE.exists():
        print(f"Error: {SEED_FILE} not found.")
        return

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 20 New Categories with 100 placeholder items each (to be expanded by user/LLM)
    # I will provide 10-20 strong ones for each to start, then placeholders
    new_cats = {
        "weatherEffects": ["acid rain", "solar flares", "midnight sun", "ember storm", "static mist", "magnetic hail", "plasma wind", "gravity waves", "neon lightning", "chrono-fog"],
        "uiAesthetics": ["crt scanlines", "minimalist vector", "holographic glitch", "tactical overlay", "brutalist terminal", "liquid metal", "paper sketch", "retro-futurist", "bio-interface", "ethereal glow"],
        "movementQuirks": ["low gravity", "magnetic boots", "teleport dashes", "momentum sliding", "grappling hooks", "wall-run", "triple jump", "hover", "burrow", "phase-shift"],
        "environmentalHazards": ["leaking coolant", "exposed wires", "unstable floor", "void rifts", "laser grids", "acid pools", "falling debris", "crushing walls", "moving platforms", "steam vents"],
        "powerSources": ["battery cells", "solar charge", "kinetic energy", "bio-essence", "void energy", "steam", "nuclear", "magic", "soul-shards", "chemical"],
        "lightingStyles": ["volumetric fog", "hard shadows", "dynamic strobes", "flickering neon", "pitch black", "bioluminescent glow", "sepia wash", "high-key", "low-key", "chiaroscuro"],
        "narrativeTone": ["melancholy", "adrenaline-fueled", "eerie", "heroic", "cynical", "whimsical", "brutal", "hopeful", "existential", "paranoic"],
        "deathAnimations": ["digital disintegration", "shattering glass", "fade to static", "structural collapse", "vaporization", "slow motion fall", "implosion", "pixel explosion", "smoke puff", "ghostly ascent"],
        "crowdDynamics": ["fleeing citizens", "silent observers", "hostile swarms", "indifferent drones", "panic-stricken herds", "cheering fans", "gathering cultists", "curious wildlife", "automated patrols", "shadowy figures"],
        "mapModifiers": ["shifting rooms", "infinite loop", "mirrored world", "vertical tower", "narrow catwalks", "collapsing bridge", "rotating floor", "vanishing paths", "recursive geometry", "gravity-flipped zones"],
        "soundscapes": ["bioluminescent hum", "glitch static", "industrial clang", "orchestral swell", "distant sirens", "whispering wind", "mechanical heartbeat", "echoing footsteps", "digital chirping", "sub-bass rumble"],
        "colorPalettes": ["vaporwave pink", "monochrome rust", "neon cyberpunk", "sepia wasteland", "bioluminescent deep", "pastel surgical", "high-contrast yellow", "obsidian and gold", "frozen blue", "emerald toxic"],
        "architecture": ["solarpunk", "brutalist sci-fi", "gothic revival", "organic hive", "ancient ruins", "steampunk factory", "modular space station", "underwater dome", "floating spire", "subterranean vault"],
        "artifactTypes": ["encoded keys", "crystal cores", "data shards", "ancient relics", "bio-samples", "memory modules", "power cells", "mechanical gears", "forged sigils", "alien artifacts"],
        "gameTempo": ["slow burn", "frantic rush", "rhythmic pulse", "sudden spikes", "escalating chaos", "zen-like flow", "stop-and-go", "steady climb", "burst-driven", "hypnotic"],
        "bossMechanics": ["pattern recognition", "speed check", "environmental manipulation", "endurance test", "resource management", "phased transformation", "summoning adds", "teleportation", "invulnerability windows", "radial attacks"],
        "playerPerks": ["time dilation", "invisibility cloak", "weaponized dash", "overclocking", "shield pulse", "health regen", "double damage", "infinite stamina", "radar sense", "gravity manipulation"],
        "enemyArchetypes": ["data leeches", "fractal shadows", "sentient static", "rust hulks", "pulse sentinels", "mimics", "shriekers", "tankers", "snipers", "swarmer drones"],
        "narrativeStakes": ["save the last data", "escape the simulation", "avenge the mentor", "stop the leak", "find the cure", "uncover the truth", "prevent the collapse", "protect the hatchling", "rebuild the engine", "close the rift"],
        "postProcessing": ["film grain", "chromatic aberration", "motion blur", "depth of field", "vignette", "fisheye lens", "bloom", "sharpening", "denoising", "color grading"]
    }

    # Expand each to 100 items by adding generic numbered variations (user can refine later with LLM)
    for cat in new_cats:
        base_items = new_cats[cat]
        while len(new_cats[cat]) < 100:
            new_cats[cat].append(f"{random.choice(base_items)} variation {len(new_cats[cat])}")

    # Merge into options
    for cat, items in new_cats.items():
        data["options"][cat] = items

    # Update sample rules
    for cat in new_cats:
        data["randomGenerator"]["sampleRules"][cat] = 1

    with open(SEED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully injected 20 new categories into {SEED_FILE}.")

def update_builder_script():
    if not BUILDER_FILE.exists():
        print(f"Error: {BUILDER_FILE} not found.")
        return

    with open(BUILDER_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Add to BRAINSTORM_SEED_CATEGORY_MAP
    # Line 70 is where it starts
    new_mappings = """
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
	"postProcessing": "Post-Process Seeds","""

    target = '"twistConstraints": "Twist Constraint Seeds",'
    if target in content:
        content = content.replace(target, target + new_mappings)
        print("Updated BRAINSTORM_SEED_CATEGORY_MAP in builder script.")

    # Add to diversify_seed_library categories
    target_cats = 'categories = ["themes", "environments", "characterMotivations", "coreLoops", "antagonists", "visualStyles"]'
    new_cats_list = 'categories = ["themes", "environments", "characterMotivations", "coreLoops", "antagonists", "visualStyles", "weatherEffects", "uiAesthetics", "movementQuirks", "environmentalHazards", "powerSources", "lightingStyles", "narrativeTone", "deathAnimations", "crowdDynamics", "mapModifiers", "soundscapes", "colorPalettes", "architecture", "artifactTypes", "gameTempo", "bossMechanics", "playerPerks", "enemyArchetypes", "narrativeStakes", "postProcessing"]'
    if target_cats in content:
        content = content.replace(target_cats, new_cats_list)
        print("Updated diversification categories in builder script.")

    with open(BUILDER_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    import random
    inject_seed_data()
    update_builder_script()
