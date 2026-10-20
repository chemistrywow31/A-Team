#!/usr/bin/env python3
"""Validate the bounded A-Team Grok skill authoring profile (not all vendor fields)."""
import re
import sys
from pathlib import Path
import yaml
try:
    from scripts.utils import read_frontmatter
except ModuleNotFoundError:
    from utils import read_frontmatter

ALLOWED_PROPERTIES = {"name", "description", "license", "metadata", "compatibility",
                      "disable-model-invocation", "user-invocable", "argument-hint"}


def validate_skill(skill_path):
    path = Path(skill_path)
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return False, "SKILL.md not found"
    try:
        metadata, body = read_frontmatter(skill_md.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return False, f"Invalid frontmatter: {exc}"
    unknown = set(metadata) - ALLOWED_PROPERTIES
    if unknown:
        return False, f"Unsupported A-Team Grok skill fields: {', '.join(sorted(unknown))}; model/effort/allowed-tools are not enforced skill controls"
    name = metadata.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        return False, "Name must be nonempty kebab-case, at most 64 characters (A-Team profile)"
    if name != path.name:
        return False, "Skill name must match its folder in the A-Team profile"
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        return False, "Description must be nonempty text, at most 1024 characters (A-Team profile)"
    for key in ("disable-model-invocation", "user-invocable"):
        if key in metadata and type(metadata[key]) is not bool:
            return False, f"{key} must be a boolean"
    for key in ("license", "compatibility", "argument-hint"):
        if key in metadata and not isinstance(metadata[key], str):
            return False, f"{key} must be text"
    if "metadata" in metadata:
        pairs = metadata["metadata"]
        if not isinstance(pairs, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in pairs.items()
        ):
            return False, "metadata must be string pairs"
    if not body.strip() or not re.search(r"(?m)^# .+", body):
        return False, "Skill body must contain useful instructions and a title"
    return True, "Native skill profile valid; J5 semantic review and runtime discovery remain separate"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python quick_validate.py <skill_directory>")
    valid, message = validate_skill(sys.argv[1])
    print(message)
    raise SystemExit(0 if valid else 1)
