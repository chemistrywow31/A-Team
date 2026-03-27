#!/usr/bin/env python3
"""
Knowledge file selector for A-Team prompt engineering knowledge base.

Scans YAML frontmatter in knowledge files and returns paths matching
the given scenario or tags.

Usage:
    python select.py --scenario generating-coordinator
    python select.py --tags "compaction,parallel"
    python select.py --scenario generating-coding-team --tags "anti-hallucination"
    python select.py --list-scenarios
    python select.py --list-tags
"""

import argparse
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent
ASSETS_DIR = SKILL_DIR / "assets"
CATEGORIES = ["templates", "context-strategies", "advanced-techniques", "claude-4-patterns"]


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    raw = match.group(1)

    # Parse simple YAML fields
    current_key = None
    current_list = []

    for line in raw.split("\n"):
        # Key-value pair
        kv = re.match(r"^(\w[\w-]*):\s*(.+)$", line)
        if kv:
            if current_key and current_list:
                frontmatter[current_key] = current_list
                current_list = []
            key, val = kv.group(1), kv.group(2).strip()
            # Handle inline list [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                frontmatter[key] = [v.strip().strip("\"'") for v in val[1:-1].split(",")]
            else:
                frontmatter[key] = val.strip("\"'")
                current_key = None
            continue

        # List start
        list_start = re.match(r"^(\w[\w-]*):\s*$", line)
        if list_start:
            if current_key and current_list:
                frontmatter[current_key] = current_list
            current_key = list_start.group(1)
            current_list = []
            continue

        # List item
        item = re.match(r"^\s+-\s+(.+)$", line)
        if item and current_key:
            current_list.append(item.group(1).strip("\"'"))

    if current_key and current_list:
        frontmatter[current_key] = current_list

    return frontmatter


def scan_knowledge_files() -> list[dict]:
    """Scan all knowledge files and return their metadata."""
    entries = []
    for category in CATEGORIES:
        cat_dir = ASSETS_DIR / category
        if not cat_dir.exists():
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            fm = parse_frontmatter(md_file)
            if fm:
                rel_path = str(md_file.relative_to(ASSETS_DIR))
                entries.append({
                    "path": rel_path,
                    "full_path": str(md_file),
                    "name": fm.get("name", md_file.stem),
                    "category": fm.get("category", category),
                    "applies_when": fm.get("applies_when", []),
                    "tags": fm.get("tags", []),
                })
    return entries


def match_entries(entries: list[dict], scenarios: list[str], tags: list[str]) -> list[dict]:
    """Filter entries matching any of the given scenarios or tags."""
    if not scenarios and not tags:
        return entries

    matched = []
    for entry in entries:
        score = 0
        # Check scenario matches
        for s in scenarios:
            if s in entry["applies_when"]:
                score += 2  # Scenario match is weighted higher
        # Check tag matches
        for t in tags:
            t_lower = t.lower()
            if any(t_lower in tag.lower() for tag in entry["tags"]):
                score += 1
            # Also check applies_when for partial tag matches
            if any(t_lower in aw.lower() for aw in entry["applies_when"]):
                score += 1
        if score > 0:
            entry["_score"] = score
            matched.append(entry)

    return sorted(matched, key=lambda x: (-x["_score"], x["path"]))


def main():
    parser = argparse.ArgumentParser(description="Select relevant knowledge files for A-Team writers")
    parser.add_argument("--scenario", "-s", help="Scenario keyword (e.g., generating-coordinator)")
    parser.add_argument("--tags", "-t", help="Comma-separated tags to match")
    parser.add_argument("--list-scenarios", action="store_true", help="List all available scenarios")
    parser.add_argument("--list-tags", action="store_true", help="List all available tags")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show names and categories")
    parser.add_argument("--prefix", default=".claude/skills/prompt-patterns/assets/", help="Path prefix for output")
    args = parser.parse_args()

    entries = scan_knowledge_files()

    if args.list_scenarios:
        scenarios = set()
        for e in entries:
            scenarios.update(e["applies_when"])
        for s in sorted(scenarios):
            print(s)
        return

    if args.list_tags:
        tags = set()
        for e in entries:
            tags.update(e["tags"])
        for t in sorted(tags):
            print(t)
        return

    scenarios = [args.scenario] if args.scenario else []
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

    if not scenarios and not tags:
        parser.print_help()
        sys.exit(1)

    matched = match_entries(entries, scenarios, tags)

    if not matched:
        print("No matching knowledge files found.", file=sys.stderr)
        sys.exit(1)

    for entry in matched:
        path = args.prefix + entry["path"]
        if args.verbose:
            print(f"{path}  # {entry['name']} ({entry['category']})")
        else:
            print(path)


if __name__ == "__main__":
    main()
