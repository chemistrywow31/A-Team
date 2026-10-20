"""Native Grok helpers. No auth reads, trust grants or permission overrides.

Contract: xai-org/grok-build commit 2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8,
crates/codegen/xai-grok-pager/src/{app/cli.rs,headless/reducer/acp.rs};
xai-grok-tools/src/implementations/grok_build/read_file/mod.rs (target_file).
Installed grok 1.0.62 --help confirms flags; live model behavior is NOT_PROBED.
Derived from the archived Anthropic skill-creator bundle; retain LICENSE.txt.
"""

import json
import os
from pathlib import Path
import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject ambiguous frontmatter instead of silently accepting duplicate keys."""


def _mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in mapping:
            raise ValueError(f"Invalid or duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def read_frontmatter(content: str) -> tuple[dict, str]:
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter on line 1")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("Missing closing frontmatter delimiter") from exc
    metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    if not isinstance(metadata, dict):
        raise ValueError("Frontmatter must be a YAML mapping")
    return metadata, "\n".join(lines[end + 1:])


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    content = (Path(skill_path) / "SKILL.md").read_text(encoding="utf-8")
    metadata, _ = read_frontmatter(content)
    for key in ("name", "description"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    return metadata["name"].strip(), metadata["description"].strip(), content


def grok_command(*, query: str | None = None, prompt_file: Path | None = None,
                 model: str | None = None, max_turns: int = 4,
                 output_format: str = "streaming-json", binary: str | None = None) -> list[str]:
    """Build only installed-help-backed flags; preserve runtime permission defaults."""
    if (query is None) == (prompt_file is None):
        raise ValueError("Provide exactly one query or prompt file")
    if max_turns < 1 or output_format not in {"plain", "streaming-json"}:
        raise ValueError("Invalid turns or output format")
    cmd = [binary or os.environ.get("GROK_SKILL_CLI", "grok")]
    cmd += ["--single", query] if query is not None else ["--prompt-file", str(prompt_file)]
    cmd += ["--output-format", output_format, "--max-turns", str(max_turns)]
    if model:
        cmd += ["--model", model]
    return cmd


def parse_native_stream(output: str, skill_file: Path | None = None,
                        cwd: Path | None = None) -> dict:
    """Parse Grok native ACP-derived NDJSON, never Anthropic Messages events.

    Trigger means a completed read_file of the exact SKILL.md. The default
    Grok toolset reads skills directly, so arbitrary text or tool arguments
    containing the skill name are insufficient. A terminal end_turn is needed
    even if a matching read occurred; failures remain operational errors.
    """
    expected = skill_file.resolve() if skill_file else None
    calls = {}
    completed = set()
    ended = False
    text = []
    for line in output.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Invalid native streaming-json event") from exc
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            raise RuntimeError("Malformed native event envelope")
        kind = event["type"]
        known = {"text", "thought", "tool_call", "tool_call_update", "plan", "available_commands",
                 "max_turns_reached", "error", "auto_compact_started", "auto_compact_completed",
                 "auto_compact_failed", "auto_compact_cancelled", "auto_continue_completed",
                 "image_compressed", "memory_flush_started", "memory_flush_completed",
                 "memory_capture_activity", "usage", "end"}
        if kind not in known:
            raise RuntimeError(f"Unsupported native event type: {kind}")
        if kind in {"error", "max_turns_reached"}:
            raise RuntimeError(f"Grok evaluation incomplete: {kind}")
        if kind in {"stream_event", "assistant", "result"}:
            raise RuntimeError("Anthropic Messages events are not native streaming-json")
        if kind == "text" and isinstance(event.get("data"), str):
            text.append(event["data"])
        elif kind == "tool_call":
            call_id = event.get("toolCallId")
            raw = event.get("rawInput")
            if not isinstance(call_id, str) or not isinstance(raw, dict):
                raise RuntimeError("Malformed native tool_call")
            matching = False
            if expected and event.get("toolName") == "read_file":
                target = raw.get("target_file")
                if isinstance(target, str):
                    target_path = Path(target)
                    if not target_path.is_absolute():
                        target_path = (cwd or Path.cwd()) / target_path
                    matching = target_path.resolve() == expected
            if event.get("status") == "failed":
                raise RuntimeError("A native tool call failed; evaluation is unverified")
            calls[call_id] = matching
            if event.get("status") == "completed":
                completed.add(call_id)
        elif kind == "tool_call_update":
            if not isinstance(event.get("toolCallId"), str):
                raise RuntimeError("Malformed native tool_call_update")
            if event.get("status") == "failed":
                raise RuntimeError("A native tool call failed; evaluation is unverified")
            if event.get("status") == "completed":
                completed.add(event.get("toolCallId"))
        elif kind == "end":
            if event.get("stopReason") != "end_turn":
                raise RuntimeError("Grok did not complete normally")
            ended = True
    if not ended:
        raise RuntimeError("Missing native terminal end event; result is unverified")
    return {"triggered": any(match and cid in completed for cid, match in calls.items()),
            "text": "".join(text), "completed": True}
