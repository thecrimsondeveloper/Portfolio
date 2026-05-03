#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / ".ARCADE-SYSTEM" / "prompts" / "themes"
TEMPLATES_DIR = ROOT / ".ARCADE-SYSTEM" / "prompts" / "templates"
FIXTURES_FILE = ROOT / ".ARCADE-SYSTEM" / "fixtures" / "prompts.json"

def load_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()

def mix_prompt(theme_name: str, template_name: str) -> str:
    theme_text = load_file(THEMES_DIR / f"{theme_name}.md")
    template_text = load_file(TEMPLATES_DIR / f"{template_name}.md")
    
    if not theme_text or not template_text:
        return ""
    
    # Simple injection logic
    mixed = template_text.replace("{{THEME_CONTEXT}}", theme_text)
    return mixed

def save_to_fixtures(theme_name: str, task_name: str, prompt_text: str):
    fixtures = {}
    if FIXTURES_FILE.exists():
        with open(FIXTURES_FILE, "r", encoding="utf-8") as f:
            fixtures = json.load(f)
            
    if theme_name not in fixtures:
        fixtures[theme_name] = {}
        
    fixtures[theme_name][task_name] = prompt_text
    
    with open(FIXTURES_FILE, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
    
    print(f"[✔] Saved winning prompt for '{theme_name}' task '{task_name}' to fixtures.")

def main():
    parser = argparse.ArgumentParser(description="PortfolioBuilder Prompt Engine")
    parser.add_argument("--theme", type=str, required=True, help="Theme name (e.g. gothic)")
    parser.add_argument("--template", type=str, required=True, help="Template name (e.g. scaffold)")
    parser.add_argument("--task", type=str, help="Task name for storage (defaults to template name)")
    
    args = parser.parse_args()
    task_name = args.task or args.template
    
    mixed = mix_prompt(args.theme, args.template)
    
    if not mixed:
        print(f"Error: Could not mix prompt for theme '{args.theme}' and template '{args.template}'.")
        return
    
    print("\n--- MIXED PROMPT PREVIEW ---")
    print(mixed[:500] + "...")
    
    confirm = input("\nSave this prompt to fixtures? (yes/no): ").strip().lower()
    if confirm == "yes":
        save_to_fixtures(args.theme, task_name, mixed)

if __name__ == "__main__":
    main()
