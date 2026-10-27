#!/usr/bin/env python3
"""Render portable helper briefs from flat Grok agent files.

A brief is a zero-context assignment for one direct specialist. It is not a
Grok agent definition and it is not loaded from `.grok/agents/`. Grok Build
sessions keep using the agent files. A lead-and-helpers deployment hands the
brief plus a task envelope to a specialist that starts with no conversation.

The renderer copies named sections only. It does not call a model, invent
cost or token figures, or claim the host enforces tool denial.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("Python >=3.11 required.")
try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML==6.0.3 required; install requirements.txt in a local virtual environment.")

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = (
    "Identity",
    "Responsibilities",
    "Input and Output",
    "Workflow",
    "Boundaries",
    "Completion Contract",
)
OPTIONAL_SECTIONS = ("Uncertainty Protocol",)
HEADING = re.compile(r"(?m)^## (.+?)\s*$")
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", re.S)


class RenderError(ValueError):
    pass


def split_frontmatter(text: str, label: str) -> tuple[dict, str]:
    match = FRONTMATTER.match(text)
    if match is None:
        raise RenderError(f"{label}: missing YAML frontmatter")
    try:
        data = yaml.safe_load(match[1])
    except yaml.YAMLError as error:
        raise RenderError(f"{label}: invalid YAML: {error}") from error
    if not isinstance(data, dict):
        raise RenderError(f"{label}: frontmatter must be a mapping")
    return data, match[2]


def section_map(body: str) -> dict[str, str]:
    matches = list(HEADING.finditer(body))
    found: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        if title == "Input/Output":
            title = "Input and Output"
        if title in found:
            raise RenderError(f"duplicate section: {title}")
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        found[title] = f"## {title}\n\n{content}\n" if content else f"## {title}\n"
    return found


def _preamble(name: str, description: str) -> str:
    return (
        f"# Helper brief: {name}\n\n"
        "You start with no conversation history and no messages from other helpers or from the user.\n"
        "Perform only the task in the lead's envelope. Return the result only to that lead.\n"
        "Do not spawn helpers, agents, or further tasks. Do not message another helper or the user.\n"
        "If a required input is missing, return NEEDS_CONTEXT and name every gap once.\n"
        "If the host blocks the work, return BLOCKED.\n"
        "Do not invent cost, token counts, deadlines, or claims that a tool restriction was enforced.\n\n"
        "This file is the portable role contract. It is not a Grok agent definition.\n"
        f"Grok Build sessions load `.grok/agents/{name}.md` instead of this brief.\n\n"
        f"Role name: {name}\n"
        f"Description: {description}\n"
    )


def _return_format() -> str:
    return (
        "## Return format\n\n"
        "Return these fields, in this order, and no preamble before STATUS:\n\n"
        "STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT\n"
        "CONCLUSIONS:\n"
        "EVIDENCE:\n"
        "ARTIFACTS:\n"
        "RISKS/UNKNOWNS:\n"
        "NEXT:\n\n"
        "Use exactly one of those four STATUS tokens.\n"
        "State in CONCLUSIONS whether the acceptance criteria are met, partially met, or not met.\n"
        "DONE and DONE_WITH_CONCERNS require nonempty EVIDENCE naming a file or a command.\n"
        "Write none under RISKS/UNKNOWNS when there are no risks.\n"
        "NEXT names one recommendation.\n"
        "Do not include a private reasoning transcript.\n"
    )


def render_agent_text(data: dict, body: str) -> tuple[str, dict[str, str]]:
    name = data.get("name")
    description = data.get("description")
    if not isinstance(name, str) or not name.strip():
        raise RenderError("agent name must be a nonempty string")
    if not isinstance(description, str) or not description.strip():
        raise RenderError(f"{name}: description must be a nonempty string")
    sections = section_map(body)
    parts = [_preamble(name.strip(), description.strip())]
    if "Identity" in sections:
        for title in REQUIRED_SECTIONS:
            if title in sections:
                parts.append("\n" + sections[title])
        for title in OPTIONAL_SECTIONS:
            if title in sections:
                parts.append("\n" + sections[title])
    else:
        instruction = body.strip()
        parts.append("\n## Role instructions\n\n" + (instruction + "\n" if instruction else ""))
        parts.append(
            "\n## Portable sections\n\n"
            "This role file has no `## Identity` section, so the brief copies the full instruction body.\n"
            "Add Identity, Responsibilities, Input and Output, Workflow, Boundaries, and Completion Contract "
            "before handing this brief to a helper that has no other context.\n"
        )
    parts.append("\n" + _return_format())
    return "".join(parts).rstrip() + "\n", sections


def render_agent_file(path: Path) -> tuple[str, dict[str, str]]:
    data, body = split_frontmatter(path.read_text(encoding="utf-8"), path.name)
    if data.get("name") != path.stem:
        raise RenderError(f"{path.name}: name must equal filename stem")
    return render_agent_text(data, body)


def render_team(root: Path) -> dict[str, str]:
    root = Path(root)
    base = root / ".grok" / "agents"
    rendered: dict[str, str] = {}
    if not base.is_dir():
        return rendered
    for path in sorted(base.glob("*.md")):
        if not path.is_file() or path.parent != base:
            continue
        text, _sections = render_agent_file(path)
        rendered[f"briefs/{path.stem}.md"] = text
    return rendered


def write_briefs(root: Path) -> list[str]:
    root = Path(root)
    expected = render_team(root)
    brief_dir = root / "briefs"
    brief_dir.mkdir(parents=True, exist_ok=True)
    for relative, text in expected.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    for path in brief_dir.glob("*.md"):
        relative = path.relative_to(root).as_posix()
        if relative not in expected:
            path.unlink()
    return sorted(expected)


def briefs_match(root: Path) -> list[str]:
    """Return human-readable drift messages. Empty means the tree matches."""
    root = Path(root)
    expected = render_team(root)
    brief_dir = root / "briefs"
    actual: dict[str, str] = {}
    if brief_dir.is_dir():
        for path in sorted(brief_dir.glob("*.md")):
            actual[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
    messages = []
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing or extra:
        messages.append(f"brief inventory mismatch missing={missing} extra={extra}")
    for relative, text in expected.items():
        if relative in actual and actual[relative] != text:
            messages.append(f"stale helper brief: {relative}")
    return messages


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true", help="exit 1 when briefs differ from agent sections")
    parser.add_argument(
        "--write-schema-copy",
        action="store_true",
        help="copy schemas/task-board.schema.json to docs/task-board.schema.json",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.check:
            messages = briefs_match(root)
            if messages:
                print("\n".join(messages))
                return 1
            print("BRIEFS_CURRENT")
        else:
            written = write_briefs(root)
            print(f"WROTE {len(written)} briefs")
        if args.write_schema_copy:
            source = ROOT / "schemas" / "task-board.schema.json"
            destination = root / "docs" / "task-board.schema.json"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"WROTE {destination.relative_to(root) if destination.is_relative_to(root) else destination}")
    except (RenderError, OSError) as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
