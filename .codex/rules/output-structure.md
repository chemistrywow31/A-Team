---
name: Output Structure
description: Define the directory layout and naming rules for generated Codex teams
---

# Output Structure

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Required Layout

Generated teams must use this Codex-native layout:

```text
teams/{team-name}/
├── AGENTS.md
├── docs/
│   └── RUNTIME-SETUP.md            # Phase 3.5 preflight advisory
├── agents/                         # required for multi-agent teams
│   ├── coordinator.toml
│   └── {group}/{agent-name}.toml
├── .codex/
│   ├── config.toml
│   ├── docs/
│   │   ├── format-mapping.md
│   │   └── format-mapping.manifest.yaml
│   ├── rules/
│   └── skills/{skill-name}/SKILL.md
└── .agents/skills/{skill-name}/SKILL.md
```

Single-agent teams may omit `agents/` and `[agents]` registration.

### Naming

- team, folder, markdown, TOML, rule, and skill folder names use kebab-case
- `AGENTS.md` and `SKILL.md` are the only uppercase filenames
- agent registry ids in `.codex/config.toml` use snake_case
- coordinator TOML lives at `agents/coordinator.toml`
- non-coordinator TOML files live under `agents/{group}/`

### AGENTS.md

Place `AGENTS.md` at the team root. Include objective, scope, universal norms, technical constraints, execution mode, runtime prerequisites, format decision, and coordinator contract. Put role-specific or file-type-specific constraints in `agents/**/*.toml` or `.codex/rules/`, not in `AGENTS.md`.

### Runtime Config

Every generated team must include `.codex/config.toml`. Multi-agent teams must set:

```toml
[features]
multi_agent = true

[agents]
max_threads = 6
max_depth = 1
```

Each `[agents.<id>]` entry must include `description` and `config_file`. Resolve `config_file` relative to `.codex/`; for project-root agent configs use `../agents/...`.

### Agent Configs

Every generated `agents/**/*.toml` file must include `name`, `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, and non-empty `developer_instructions`.

### Skills And Rules

Each skill must exist in both `.codex/skills/{skill}/SKILL.md` and `.agents/skills/{skill}/SKILL.md`. Rules live under `.codex/rules/`. Multi-agent or multi-phase teams must include worklog, context-management, and reasoning/self-critique rules or documented equivalents.

### Runtime Setup Advisory

Every generated team must ship `docs/RUNTIME-SETUP.md`, produced by `runtime-preflight-advisor` at the Phase 3 -> Phase 5 boundary. It records what the user's actual runtime will do with the team's files and what the user must configure before the first run — sandbox and approval posture for Codex, auto-mode carve-outs for Claude Code.

It exists because some runtime configuration cannot live inside the team: it is user-scope, and no agent may write it. A document plus a user-run command is the only delivery mechanism.

The advisory must carry a probe stamp (`Probed: {runtime version} on {os} at {yyyy-mm-dd}`) so staleness after an upgrade is visible, and must state backup, apply, verify, and rollback commands for the probed OS.

### Mapping Artifacts

Every generated team must retain `.codex/docs/format-mapping.md` and `.codex/docs/format-mapping.manifest.yaml`. They must record requested format, canonical Codex format, Codex <-> Claude mapping, lossy conversions, sidecar needs, and round-trip notes.

### Path-Scoped Rules

Rules may include optional `paths` frontmatter for file-specific constraints. Process and behavioral rules remain unconditional.

## Violation Determination

- `AGENTS.md` is missing or not at team root -> Violation
- `docs/RUNTIME-SETUP.md` is missing, or lacks the probe stamp or the rollback command -> Violation
- `.codex/config.toml` or mapping docs are missing -> Violation
- a multi-agent team omits `agents/` or `[features] multi_agent = true` -> Violation
- coordinator TOML is not at `agents/coordinator.toml` -> Violation
- non-coordinator TOML appears at `agents/` root -> Violation
- an agent registry entry is missing `description` or `config_file` -> Violation
- a registered `config_file` does not resolve from `.codex/` -> Violation
- an agent TOML misses a required runtime key -> Violation
- a skill exists only in `.codex/skills/` or only in `.agents/skills/` -> Violation
- required process rules are missing without documented equivalents -> Violation
- file or folder names break naming conventions -> Violation

## Exceptions

Single-agent teams may omit `agents/`, `[agents]` registration, and coordinator TOML.
