#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = ROOT / ".ARCADE-SYSTEM" / "sessions"
ARCHIVE_DIR = ROOT / ".ARCADE-SYSTEM" / "archives"
PAGES_ROOT = Path("/Users/crimsonwheeler/Documents/GitHub/Portfolio/Portfolio-Vite/Pages")

def cleanup_sessions():
    print(f"Cleaning up sessions in {SESSIONS_DIR}...")
    if not SESSIONS_DIR.exists():
        return
    for item in SESSIONS_DIR.iterdir():
        if item.is_file():
            item.unlink()
            print(f"  [x] Deleted file: {item.name}")
        elif item.is_dir():
            shutil.rmtree(item)
            print(f"  [x] Deleted directory: {item.name}")

def archive_memories():
    print(f"Archiving frontier memories in {PAGES_ROOT}...")
    if not PAGES_ROOT.exists():
        return
    if not ARCHIVE_DIR.exists():
        ARCHIVE_DIR.mkdir(parents=True)

    for game_dir in PAGES_ROOT.iterdir():
        if game_dir.is_dir():
            memory_file = game_dir / "frontier-memory.json"
            if memory_file.exists():
                archive_name = f"{game_dir.name}-memory.json"
                shutil.copy(memory_file, ARCHIVE_DIR / archive_name)
                print(f"  [>] Archived memory for: {game_dir.name}")

def remove_empty_games():
    print(f"Checking for empty game folders in {PAGES_ROOT}...")
    for game_dir in PAGES_ROOT.iterdir():
        if game_dir.is_dir():
            files = list(game_dir.iterdir())
            if len(files) <= 1: # Only .DS_Store or similar
                print(f"  [!] Found empty folder: {game_dir.name}. Deleting...")
                shutil.rmtree(game_dir)

def main():
    parser = argparse.ArgumentParser(description="PortfolioBuilder Workspace Cleaner")
    parser.add_argument("--sessions", action="store_true", help="Clean up the sessions folder.")
    parser.add_argument("--archive", action="store_true", help="Archive game memories.")
    parser.add_argument("--all", action="store_true", help="Run all cleanup tasks.")
    
    args = parser.parse_args()
    
    if args.sessions or args.all:
        cleanup_sessions()
    
    if args.archive or args.all:
        archive_memories()
        
    if args.all:
        remove_empty_games()

    print("\nCleanup complete.")

if __name__ == "__main__":
    main()
