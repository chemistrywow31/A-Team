#!/usr/bin/env python3
"""Strict local Grok team validation; discovery is not effective runtime evidence.

Authoring subset is pinned to the documented 1.0.62/source contract. Unknown
fields fail closed because Grok's permissive loader silently ignores them.
No network, trust grants, installation, model requests, or target writes occur.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys

if sys.version_info < (3, 11):
    raise SystemExit("Python >=3.11 required. Set PYTHON to a local virtual environment interpreter.")
import tomllib
try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML==6.0.3 required; install requirements.txt in a local virtual environment.")

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
TOOL_IDS = frozenset("run_terminal_cmd task get_task_output wait_tasks kill_task read_file grep list_dir search_replace write todo_write web_search web_fetch search_tool use_tool ask_user_question".split())
AGENT_KEYS = frozenset("name description promptMode model effort tools disallowedTools skills agentsMd discoverSkills inheritSkills injectDefaultTools maxTurns mcpInheritance permissionMode isolation background capabilityMode".split())
SKILL_KEYS = frozenset("name description when-to-use allowed-tools argument-hint user-invocable disable-model-invocation model effort license compatibility metadata".split())
REPO_COUNTS = {"roles": 13, "skills": 11, "policies": 19}
FOREIGN_ROOTS = ("CLAUDE.md", ".claude", ".codex", ".agents", "agents", ".cursor")
# This one documented, ignored skill-discovery settings file is user-local data,
# not an authored projection. Do not generalize to ignored paths or config.json
# elsewhere: authored examples, native config and new sources still need mapping.
LOCAL_RUNTIME_FILES = frozenset({".grok/skills/skill-discovery/config.json"})


class Invalid(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise Invalid("YAML mapping keys must be strings")
        if key in result:
            raise Invalid(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def require(condition, message):
    if not condition:
        raise Invalid(message)


def string(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value):
    return isinstance(value, list) and all(string(item) for item in value)


def keys(data, allowed, label, required=()):
    require(isinstance(data, dict), f"{label}: expected mapping")
    require(set(data) <= set(allowed), f"{label}: unknown keys {sorted(set(data) - set(allowed))}")
    require(set(required) <= set(data), f"{label}: missing keys {sorted(set(required) - set(data))}")


def confined(root, relative, *, must_exist=True):
    require(string(relative), "path must be a nonempty string")
    p = PurePosixPath(relative)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in relative,
            f"path escapes root: {relative}")
    target = root / p
    require(target.resolve().is_relative_to(root.resolve()), f"symlink escapes root: {relative}")
    if must_exist:
        require(target.exists(), f"missing path: {relative}")
    return target


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", text, re.S)
    require(match is not None, f"{path.name}: missing YAML frontmatter")
    try:
        data = yaml.load(match[1], Loader=UniqueLoader)
    except yaml.YAMLError as error:
        raise Invalid(f"{path.name}: invalid YAML: {error}") from error
    require(isinstance(data, dict), f"{path.name}: frontmatter must be a mapping")
    require(bool(match[2].strip()), f"{path.name}: empty instruction body")
    return data, match[2]


def tool_entries(value, label, *, skill=False):
    # Source config.rs tokenizes Task(a, b) as one directive even in a string.
    # Native skill strings additionally allow whitespace-separated tool names.
    if isinstance(value, str):
        token = r"(?i:Task|Agent)\([^)]*\)|[^\s,]+" if skill else r"(?i:Task|Agent)\([^)]*\)|[^,]+"
        entries = [item.strip() for item in re.findall(token, value) if item.strip()]
    else:
        require(string_list(value), f"{label}: expected tool-string list or comma-separated string")
        entries = value
    for item in entries:
        directive = re.fullmatch(r"(?i:Task|Agent)(?:\(([a-z0-9, -]*)\))?", item)
        if directive and directive[1]:
            require(all(NAME.fullmatch(name.strip()) for name in directive[1].split(",")), f"{label}: invalid role directive")
        require(item in TOOL_IDS or directive is not None,
                f"{label}: unknown/unverified tool ID {item!r}; an unknown allowlist ID can restore all tools")
    return entries


def validate_agent(path, repo_self=False):
    data, body = frontmatter(path)
    keys(data, AGENT_KEYS, str(path), ("name", "description"))
    require(string(data["name"]) and NAME.fullmatch(data["name"]), f"{path.name}: invalid role name")
    require(data["name"] == path.stem, f"{path.name}: name must equal filename stem")
    require(string(data["description"]), f"{path.name}: description must be nonempty string")
    for field in ("agentsMd", "discoverSkills", "inheritSkills", "injectDefaultTools", "background"):
        if field in data:
            require(type(data[field]) is bool, f"{path.name}: {field} must be boolean")
    for field in ("tools", "disallowedTools"):
        if field in data:
            tool_entries(data[field], f"{path.name}: {field}")
    if "skills" in data:
        require(string_list(data["skills"]), f"{path.name}: skills must be list of names")
    if "model" in data:
        require(string(data["model"]), f"{path.name}: model must be nonempty string")
    enums = {"promptMode": {"extend", "full"}, "effort": {"low", "medium", "high", "xhigh", "max"},
             "isolation": {"none", "worktree"}, "capabilityMode": {"all", "read-only", "read-write"},
             "permissionMode": {"default", "acceptEdits", "auto", "dontAsk", "bypassPermissions", "plan"}}
    for field, choices in enums.items():
        if field in data:
            require(isinstance(data[field], str) and data[field] in choices, f"{path.name}: invalid {field}")
    if "maxTurns" in data:
        require(type(data["maxTurns"]) is int and 0 < data["maxTurns"] <= 2**32 - 1,
                f"{path.name}: maxTurns must be a positive u32")
    if "mcpInheritance" in data:
        value = data["mcpInheritance"]
        require(value in ("all", "none") if isinstance(value, str) else
                isinstance(value, dict) and len(value) == 1 and set(value) <= {"named", "except"}
                and string_list(next(iter(value.values()))), f"{path.name}: invalid mcpInheritance")
    if repo_self:
        require(data.get("model", "inherit") == "inherit" and "effort" not in data,
                f"{path.name}: repo-self model strategy requires inherited model and omitted effort")
        require(data.get("agentsMd", True) and data.get("discoverSkills", True),
                f"{path.name}: repo-self requires instruction and skill discovery")
        require(data.get("permissionMode", "default") == "default", f"{path.name}: repo-self permission defaults required")
        if data["name"] == "team-architect":
            require("tools" not in data, "team-architect: omit tools to preserve native coordinator toolset")
        else:
            require("Task" in tool_entries(data.get("disallowedTools", []), str(path)), f"{path.name}: specialist requires disallowedTools: [Task]")
    return data, body


def validate_skill(path):
    data, body = frontmatter(path)
    keys(data, SKILL_KEYS, str(path), ("name", "description"))
    require(string(data["name"]) and NAME.fullmatch(data["name"]) and len(data["name"]) <= 64,
            f"{path}: invalid skill name")
    require(data["name"] == path.parent.name, f"{path}: skill name must equal directory name")
    require(string(data["description"]), f"{path}: description must be nonempty string")
    for field in ("user-invocable", "disable-model-invocation"):
        if field in data:
            require(type(data[field]) is bool, f"{path}: {field} must be boolean")
    for field in SKILL_KEYS - {"name", "description", "user-invocable", "disable-model-invocation", "allowed-tools", "metadata"}:
        if field in data:
            require(string(data[field]), f"{path}: {field} must be string")
    if "allowed-tools" in data:
        tool_entries(data["allowed-tools"], f"{path}: allowed-tools (advisory only)", skill=True)
    if "metadata" in data:
        require(isinstance(data["metadata"], dict) and all(isinstance(k, str) and isinstance(v, str)
                for k, v in data["metadata"].items()), f"{path}: metadata must be string pairs")
    return data, body


def validate_config(path):
    try:
        with path.open("rb") as stream:
            data = tomllib.load(stream)
    except tomllib.TOMLDecodeError as error:
        raise Invalid(f"config.toml: invalid TOML: {error}") from error
    keys(data, {"permission", "mcp_servers", "plugins"}, "project config")
    unverified = []
    for extension in ("mcp_servers", "plugins"):
        if extension in data:
            require(isinstance(data[extension], dict), f"{extension}: expected table")
            if data[extension]:
                unverified.append(f"{extension}: nonempty extension needs native schema review and preflight; outside validated subset")
    if "permission" in data:
        keys(data["permission"], {"rules"}, "permission")
        rules = data["permission"].get("rules", [])
        require(isinstance(rules, list), "permission.rules must be array")
        for rule in rules:
            keys(rule, {"action", "tool", "pattern", "pattern_mode"}, "permission rule", ("action",))
            require(rule["action"] in ("allow", "deny", "ask"), "invalid permission action")
            require(rule.get("tool", "any") in ("any", "bash", "edit", "read", "grep", "mcp", "webfetch", "agent_message", "agentmessage"), "invalid permission tool")
            require("pattern" not in rule or string(rule["pattern"]), "permission pattern must be string")
            require(rule.get("pattern_mode", "glob") in ("glob", "domain"), "invalid permission pattern_mode")
    return data, unverified


def native_files(root):
    files = set()
    for base in (".grok", "scripts", "tests", "templates"):
        for path in (root / base).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                files.add(path.relative_to(root).as_posix())
    files.update(p for p in ("AGENTS.md", "GROK.md", "JUDGMENT.md", "requirements.txt") if (root / p).is_file())
    return files - {".grok/docs/format-mapping.json", ".grok/docs/format-mapping.md"} - LOCAL_RUNTIME_FILES


def read_json(path):
    def pairs(items):
        value = {}
        for k, v in items:
            require(k not in value, f"duplicate JSON key: {k}")
            value[k] = v
        return value
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)
    except json.JSONDecodeError as error:
        raise Invalid(f"{path.name}: invalid JSON: {error}") from error


def validate_mapping(root, mapping, inventory, repo_self):
    allowed = {"schema_version", "kind", "generated_on", "authority", "runnable_surfaces", "reference_only_surfaces", "source_snapshot", "mappings", "source_only"}
    keys(mapping, allowed, "mapping", allowed - {"source_snapshot"})
    require(type(mapping["schema_version"]) is int and mapping["schema_version"] == 1, "mapping schema_version must be 1")
    require(mapping["kind"] in ("a-team-designer", "generated-team"), "invalid mapping kind")
    require(isinstance(mapping["generated_on"], str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", mapping["generated_on"]), "generated_on must be YYYY-MM-DD")
    require(not repo_self or mapping["kind"] == "a-team-designer", "repo-self requires a-team-designer mapping")
    authority = mapping["authority"]
    keys(authority, {"runtime", "root", "entry", "migration"}, "authority", ("runtime", "root", "entry", "migration"))
    require(authority["runtime"] == "grok" and authority["root"] == ".grok/" and authority["entry"] == "AGENTS.md", "mapping must declare unique active Grok authority")
    require(string(authority["migration"]), "authority migration must be explicit")
    require(mapping["runnable_surfaces"] == ["grok"], "reference-only/foreign surface cannot become runnable implicitly")
    confined(root, authority["root"]); confined(root, authority["entry"])
    refs = mapping["reference_only_surfaces"]
    require(isinstance(refs, list), "reference_only_surfaces must be array")
    for ref in refs:
        keys(ref, {"runtime", "root", "entry"}, "reference-only surface", ("runtime", "root", "entry"))
        require(ref["runtime"] != "grok", "active Grok cannot also be reference-only")
        for field in ("root", "entry"):
            confined(root, ref[field])
            require(ref[field].startswith("reference/"), "reference-only surface must be under reference/")
    archives = {}
    if "source_snapshot" in mapping:
        snapshot = mapping["source_snapshot"]
        keys(snapshot, {"base_commit", "root", "manifest", "manifest_sha256"}, "source_snapshot", ("base_commit", "root", "manifest", "manifest_sha256"))
        require(isinstance(snapshot["base_commit"], str) and re.fullmatch(r"[0-9a-f]{40}", snapshot["base_commit"]), "snapshot base_commit must be a full Git SHA")
        require(isinstance(snapshot["manifest_sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", snapshot["manifest_sha256"]), "snapshot manifest_sha256 must be a SHA-256")
        snap_root = confined(root, snapshot["root"])
        require(snapshot["root"].startswith("reference/"), "snapshot must be under reference/")
        manifest_path = confined(root, snapshot["manifest"])
        require(manifest_path.is_relative_to(snap_root), "snapshot manifest outside snapshot root")
        require(sha(manifest_path) == snapshot["manifest_sha256"], "snapshot manifest SHA-256 mismatch")
        manifest = read_json(manifest_path)
        keys(manifest, {"schema_version", "base_commit", "entries"}, "snapshot manifest", ("schema_version", "base_commit", "entries"))
        require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 1 and manifest["base_commit"] == snapshot["base_commit"], "snapshot version/base mismatch")
        require(isinstance(manifest["entries"], list), "snapshot entries must be list")
        source_names = []
        for entry in manifest["entries"]:
            keys(entry, {"source", "archive", "sha256", "mode"}, "snapshot entry", ("source", "archive", "sha256", "mode"))
            confined(root, entry["source"], must_exist=False)
            file = confined(root, entry["archive"])
            require(file.is_file() and not file.is_symlink(), f"snapshot entry not regular file: {entry['archive']}")
            require(entry["archive"] == str(PurePosixPath(snapshot["root"]) / entry["source"]), "archive/source path mismatch")
            require(entry["archive"] not in archives, "duplicate archive entry")
            require(entry["mode"] in ("100644", "100755"), "unsupported snapshot Git mode")
            require(sha(file) == entry["sha256"], f"snapshot bytes mismatch: {entry['archive']}")
            executable = bool(stat.S_IMODE(file.stat().st_mode) & 0o111)
            require(executable == (entry["mode"] == "100755"), f"snapshot mode mismatch: {entry['archive']}")
            archives[entry["archive"]] = file
            source_names.append(entry["source"])
        require(source_names == sorted(set(source_names)), "snapshot sources must be unique and sorted")
        if repo_self:
            require(len(archives) == 201, "repo-self snapshot requires all 201 baseline files")
    else:
        require(not repo_self and not refs, "repo-self/conversion references require source snapshot")
    mappings = mapping["mappings"]
    keys(mappings, {"roles", "skills", "policies", "other"}, "mappings", ("roles", "skills", "policies", "other"))
    targets, covered = set(), set()
    for family, entries in mappings.items():
        require(isinstance(entries, list), f"mappings.{family} must be array")
        ids, family_targets = set(), set()
        for entry in entries:
            keys(entry, {"id", "sources", "target", "mode"}, "mapping entry", ("id", "sources", "target", "mode"))
            require(string(entry["id"]) and entry["id"] not in ids, f"duplicate/empty {family} mapping id")
            ids.add(entry["id"])
            require(string_list(entry["sources"]), "mapping sources must be list of strings")
            require(entry["mode"] in ("adapted", "native", "copied"), "invalid mapping mode")
            require(entry["mode"] == "native" or entry["sources"], "adapted/copied mapping needs source")
            target = confined(root, entry["target"])
            require(target.is_file() and not entry["target"].startswith("reference/"), "mapping target must be active file")
            require(entry["target"] not in targets, "duplicate mapping target")
            if family in ("roles", "skills"):
                require(entry["id"] == frontmatter(target)[0]["name"], f"{family} mapping id differs from native name")
            targets.add(entry["target"]); family_targets.add(entry["target"])
            for source in entry["sources"]:
                require(source in archives, f"mapping source outside snapshot inventory: {source}")
                covered.add(source)
                if entry["mode"] == "copied":
                    require(target.read_bytes() == archives[source].read_bytes(), f"copied mapping bytes differ: {entry['target']}")
        if family != "other":
            require(family_targets == set(inventory[family]), f"{family} mapping must match exact active inventory")
    require(isinstance(mapping["source_only"], list), "source_only must be array")
    only = set()
    for item in mapping["source_only"]:
        keys(item, {"source", "reason"}, "source_only", ("source", "reason"))
        require(item["source"] in archives and item["source"] not in only, "unknown/duplicate source_only path")
        require(string(item["reason"]), "source_only requires concrete reason")
        only.add(item["source"])
    require(not (covered & only), "mapped source cannot also be source_only")
    require(covered | only == set(archives), "mapping/source_only does not cover complete snapshot")
    if repo_self:
        require(native_files(root) <= targets, f"unmapped active files: {sorted(native_files(root) - targets)}")


def reference_checks(root, path):
    text = path.read_text(encoding="utf-8")
    # Explicit native policy and skill paths are stable local contracts. Template
    # slots and globs intentionally describe future output and are not dereferenced.
    for value in re.findall(r"\.grok/(?:policies|skills)/[A-Za-z0-9_./-]+", text):
        value = value.rstrip("./")
        if value.endswith((".md", ".py")):
            confined(root, value)


def classify_team(root):
    native = (root / ".grok").is_dir()
    foreign = [p for p in FOREIGN_ROOTS if (root / p).exists()]
    map_path = root / ".grok/docs/format-mapping.json"
    mapping = read_json(map_path) if map_path.is_file() else None
    if mapping and "grok" not in mapping.get("runnable_surfaces", []):
        label = "reference-only"
    elif native and foreign:
        label = "multi-surface/authority-conflict"
    elif native and (root / "AGENTS.md").is_file():
        label = "grok-only"
    elif native:
        label = "incomplete/activation-gated"
    elif foreign:
        label = "foreign-platform"
    else:
        label = "non-team"
    return {"layout": label, "foreign_roots": foreign, "runnable": "UNVERIFIED", "activation": "NOT_PROBED"}


def validate(root, repo_self=False):
    root = Path(root).resolve()
    report = {"root": str(root), "status": "INVALID_METADATA", "errors": [], "warnings": [],
              "effective_runtime": "UNVERIFIED", "model_access": "NOT_PROBED", "inventory": {}}
    def check(label, action):
        try:
            return action()
        except (Invalid, OSError, ValueError, TypeError, KeyError) as error:
            report["errors"].append(f"{label}: {error}")
            return None
    require(root.is_dir(), f"target root is not a directory: {root}")
    report["classification"] = check("classification", lambda: classify_team(root))
    check("authority", lambda: require(report["classification"] and report["classification"]["layout"] == "grok-only", "requires native Grok root with no active foreign/reference-only surface"))
    entry = root / "AGENTS.md"
    def entry_check():
        text = confined(root, "AGENTS.md").read_text(encoding="utf-8")
        require("grok" in text.lower() and ".grok/" in text and any(word in text.lower() for word in ("authority", "canonical", "權威")), "AGENTS.md must explicitly declare Grok authority and .grok/")
    check("entry", entry_check)
    for required in (".grok/config.toml", ".grok/rules/core.md"):
        check("required artifact", lambda p=required: confined(root, p))
    config = check("config", lambda: validate_config(confined(root, ".grok/config.toml")))
    if config:
        report["warnings"].extend(config[1])
    agents, skills, policies = {}, {}, []
    for path in sorted((root / ".grok/agents").rglob("*.md")):
        if path.parent != root / ".grok/agents":
            report["errors"].append(f"nested agent ignored by native loader: {path.relative_to(root)}")
            continue
        result = check(str(path.relative_to(root)), lambda p=path: (confined(root, p.relative_to(root).as_posix()), validate_agent(p, repo_self))[1])
        if result:
            data, body = result
            if data["name"] in agents:
                report["errors"].append(f"duplicate role ID: {data['name']}")
            agents[data["name"]] = path
            if "tools" in data and not tool_entries(data["tools"], str(path)):
                report["warnings"].append(f"{data['name']}: empty tools inherits all tools; it does not declare zero tools")
            if data.get("model", "inherit") != "inherit" or "effort" in data:
                report["warnings"].append(f"{data['name']}: model/effort catalog availability and effective routing UNVERIFIED")
    for path in sorted((root / ".grok/skills").rglob("SKILL.md")):
        if path.parent.parent != root / ".grok/skills":
            report["errors"].append(f"skill must be .grok/skills/<name>/SKILL.md: {path.relative_to(root)}")
            continue
        result = check(str(path.relative_to(root)), lambda p=path: (confined(root, p.relative_to(root).as_posix()), validate_skill(p))[1])
        if result:
            data, body = result
            if data["name"] in skills:
                report["errors"].append(f"duplicate skill ID: {data['name']}")
            skills[data["name"]] = path
            if set(data) & {"model", "effort", "allowed-tools"}:
                report["warnings"].append(f"{data['name']}: skill model/effort/allowed-tools are not effective runtime controls")
    for path in sorted((root / ".grok/policies").rglob("*.md")):
        if path.parent != root / ".grok/policies":
            report["errors"].append("policies must be flat")
        check("policy", lambda p=path: confined(root, p.relative_to(root).as_posix()))
        policies.append(path)
    for path in sorted((root / ".grok/rules").rglob("*.md")):
        if path.parent != root / ".grok/rules":
            report["errors"].append(f"nested rule ignored by native loader: {path.relative_to(root)}")
    for path in list(agents.values()) + list(skills.values()) + policies + list((root / ".grok/rules").glob("*.md")) + ([entry] if entry.exists() else []):
        check("references", lambda p=path: reference_checks(root, p))
    for path in agents.values():
        data, _ = frontmatter(path)
        for name in data.get("skills", []):
            if name not in skills:
                report["errors"].append(f"{path.name}: unknown skill preload {name}")
    inventory = {"roles": [p.relative_to(root).as_posix() for p in agents.values()],
                 "skills": [p.relative_to(root).as_posix() for p in skills.values()],
                 "policies": [p.relative_to(root).as_posix() for p in policies]}
    report["inventory"] = inventory
    for family in inventory:
        check(family, lambda f=family: require(len(inventory[f]) > 0, f"at least one {f} artifact required"))
    if repo_self:
        for family, count in REPO_COUNTS.items():
            check("repo-self", lambda f=family, n=count: require(len(inventory[f]) == n, f"requires exactly {n} {f}"))
        check("coordinator", lambda: require("team-architect" in agents, "missing team-architect"))
    else:
        check("runtime setup", lambda: confined(root, "docs/RUNTIME-SETUP.md"))
    mapping = root / ".grok/docs/format-mapping.json"
    if mapping.is_file():
        check("mapping", lambda: validate_mapping(root, read_json(mapping), inventory, repo_self))
    elif repo_self:
        report["errors"].append("repo-self requires .grok/docs/format-mapping.json")
    if not report["errors"]:
        report["status"] = "SCHEMA_REVIEW_REQUIRED" if config and config[1] else "STATIC_VALID"
    return report


def maintenance_change(root, baseline):
    before, after = validate(baseline), validate(root)
    require(before["status"] == "STATIC_VALID" and after["status"] == "STATIC_VALID", "maintenance requires validated native authority in both roots; foreign/reference-only targets cannot be promoted")
    old_files, new_files = native_files(baseline), native_files(root)
    changed = sorted(p for p in old_files | new_files if p not in old_files or p not in new_files or (baseline / p).read_bytes() != (root / p).read_bytes())
    structural = old_files != new_files
    for p in changed:
        if p not in old_files or p not in new_files:
            continue
        if p.startswith(".grok/agents/") or (p.startswith(".grok/skills/") and p.endswith("/SKILL.md")):
            structural |= frontmatter(baseline / p)[0] != frontmatter(root / p)[0]
        else:
            structural = True
    # Mapping and authority files are checked even though self-mapping is omitted.
    for p in (".grok/docs/format-mapping.json", ".grok/docs/format-mapping.md"):
        a, b = baseline / p, root / p
        if a.exists() != b.exists() or (a.exists() and a.read_bytes() != b.read_bytes()):
            structural = True; changed.append(p)
    return {"classification": "structural-runtime" if structural else "text-only" if changed else "unchanged",
            "changed": sorted(set(changed)), "required_gates": ["recommendation", "mapping", "runtime-preflight", "artifact-review"] if structural else ["artifact-review"] if changed else [],
            "note": "Routing only; no gate execution or approval is implied. Semantic role/workflow/ownership changes require structural review even when body-only."}


def inspect_discovery(root, evidence, inventory):
    require(evidence.get("projectTrusted") is True, "project is untrusted")
    require(Path(evidence.get("projectRoot", "")).resolve() == root.resolve(), "inspect projectRoot mismatch")
    ambient = {"agents": [], "skills": [], "instructions": []}
    for family, field in (("roles", "agents"), ("skills", "skills")):
        expected = {frontmatter(root / p)[0]["name"]: (root / p).resolve() for p in inventory[family]}
        found = {}
        require(isinstance(evidence.get(field), list), f"inspect missing {field} inventory")
        for item in evidence[field]:
            name, source = item.get("name"), item.get("source", {})
            path = Path(source.get("path", "/__no_source__")).resolve()
            if name in expected:
                require(path == expected[name] and source.get("type") == "project", f"{field} wrong source for {name}")
                require(name not in found, f"duplicate inspected name: {name}")
                found[name] = path
            elif source.get("type") == "project":
                raise Invalid(f"unexpected project {field}: {name}")
            else:
                ambient[field].append(item)
        require(set(found) == set(expected), f"inspect missing {field}: {sorted(set(expected) - set(found))}")
    expected = {(root / "AGENTS.md").resolve()} | {p.resolve() for p in (root / ".grok/rules").glob("*.md")}
    found = set()
    for item in evidence.get("projectInstructions", []):
        path = Path(item.get("path", "/__no_source__")).resolve()
        # macOS case-insensitive lookup may display Agents.md for AGENTS.md.
        matches = [p for p in expected if path == p or (path.exists() and p.exists() and os.path.samefile(path, p))]
        if matches:
            found.add(matches[0])
        elif item.get("scope") == "project":
            raise Invalid(f"unexpected project instruction: {path}")
        else:
            ambient["instructions"].append(item)
    require(found == expected, f"inspect missing instructions: {sorted(str(p) for p in expected - found)}")
    return ambient


def preflight(root, repo_self=False, grok_bin=None):
    report = validate(root, repo_self)
    if report["status"] != "STATIC_VALID":
        return (6 if report["status"] == "SCHEMA_REVIEW_REQUIRED" else 1), report
    binary = grok_bin or shutil.which("grok")
    if not binary or not Path(binary).is_file() or not os.access(binary, os.X_OK):
        report["status"] = "MISSING_BINARY"
        return 2, report
    report["command"] = [str(Path(binary).resolve()), "inspect", "--json"]
    try:
        process = subprocess.run(report["command"], cwd=root, text=True, capture_output=True, timeout=60, check=False)
        if process.returncode != 0:
            report.update(status="INSPECT_UNAVAILABLE", inspect_exit_code=process.returncode)
            # Avoid forwarding diagnostics that might contain account identifiers.
            return 5, report
        evidence = json.loads(process.stdout)
        require(isinstance(evidence, dict), "inspect output must be JSON object")
        report["grok_version"] = evidence.get("grokVersion", "UNKNOWN")
        report["project_trusted"] = evidence.get("projectTrusted")
        if evidence.get("projectTrusted") is False:
            report["status"] = "UNTRUSTED_PROJECT"
            return 3, report
        report["ambient_sources"] = inspect_discovery(root, evidence, report["inventory"])
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        report.update(status="INSPECT_UNAVAILABLE", diagnostic=type(error).__name__)
        return 5, report
    except (Invalid, TypeError, ValueError, KeyError) as error:
        report.update(status="DISCOVERY_MISMATCH", diagnostic=str(error))
        return 4, report
    report.update(status="DISCOVERY_READY", effective_runtime="UNVERIFIED", model_access="NOT_PROBED")
    return 0, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--repo-self", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--classify", action="store_true", help="read-only layout and authority classification")
    parser.add_argument("--baseline", type=Path, help="read-only maintenance classification against validated prior root")
    parser.add_argument("--preflight", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--grok-bin", help="explicit installed Grok binary for preflight")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.preflight:
            code, result = preflight(root, args.repo_self, args.grok_bin)
        elif args.baseline:
            result = maintenance_change(root, args.baseline.resolve()); code = 0
        elif args.classify:
            result = classify_team(root); code = 0
        else:
            result = validate(root, args.repo_self)
            code = 0 if result["status"] == "STATIC_VALID" else 6 if result["status"] == "SCHEMA_REVIEW_REQUIRED" else 1
    except (Invalid, OSError, ValueError, TypeError, KeyError) as error:
        result = {"status": "INVALID_METADATA", "errors": [str(error)]}; code = 1
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result.get("status", result.get("classification", result.get("layout", "UNKNOWN"))))
        for error in result.get("errors", []): print(f"ERROR: {error}")
        for warning in result.get("warnings", []): print(f"UNVERIFIED: {warning}")
        if "effective_runtime" in result:
            print(f"effective_runtime={result['effective_runtime']} model_access={result['model_access']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
