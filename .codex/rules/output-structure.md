---
name: Output Structure
description: Define the directory layout and naming rules for generated Codex teams
---

# Output Structure

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Directory Structure

All generated teams must follow this layout:

```text
teams/{team-name}/
├── AGENTS.md
├── .codex/
│   ├── config.toml
│   ├── docs/
│   │   ├── format-mapping.md
│   │   └── format-mapping.manifest.yaml
│   ├── agents/
│   │   ├── {coordinator}.md
│   │   ├── {group-a}/
│   │   │   ├── {agent-1}.md
│   │   │   └── {agent-2}.md
│   │   └── {group-b}/
│   │       └── {agent-3}.md
│   ├── skills/
│   │   ├── {skill-1}/
│   │   │   └── SKILL.md
│   │   └── {skill-2}/
│   │       └── SKILL.md
│   └── rules/
│       ├── {rule-1}.md
│       └── {group}/
│           └── {rule-2}.md
└── .agents/
    └── skills/
        ├── {skill-1}/
        │   └── SKILL.md
        └── {skill-2}/
            └── SKILL.md
```

### Naming Conventions

- Team names: kebab-case
- Directory names: kebab-case
- Markdown files: kebab-case, except `AGENTS.md` and `SKILL.md`
- No spaces, underscores, or uppercase folder names

### AGENTS.md Content Guidelines

Place `AGENTS.md` at the team root. It is the Codex entrypoint for the generated team.

Include:

- team objective and scope summary
- universal behavioral norms
- project-wide technical constraints
- execution mode instructions and any runtime prerequisites that must be enabled outside the repo
- the requested delivery format if it differs from the canonical Codex-native authored format
- any `@path/to/file` imports that all team members truly need

Do not put role-specific rules or file-type-specific constraints in `AGENTS.md`. Those belong in `.codex/rules/`.

### Format Mapping Artifact

Every generated team must retain `.codex/docs/format-mapping.md`.

Include:

- requested delivery format
- canonical authored format
- Codex -> Claude path mapping
- Claude -> Codex path mapping
- lossy or unsupported conversions
- round-trip preservation notes

Also retain `.codex/docs/format-mapping.manifest.yaml` so future conversion can use machine-readable artifact relationships. Add sidecars under `.codex/docs/mapping-sidecars/` only when a conversion is lossy or bundle-based.

### Execution Mode Section

Every generated `AGENTS.md` must define one of these modes:

- `single-agent`: one Codex thread performs the work inline with minimal delegation
- `multi-agent`: the coordinator delegates in parallel with `spawn_agent`, uses `send_input` for follow-up, and joins work with `wait`

When `multi-agent` is chosen, the team must also define:

- parallel-safe file ownership
- coordinator follow-up triggers
- completion contracts for each spawned specialist
- runtime prerequisites for Claude Code and/or Codex
- setup fallback when the required user-level setting is missing

### Path-Scoped Rules

Rules may include optional `paths` frontmatter to scope them to file patterns. This is an internal A-Team convention for rule organization; it does not replace `AGENTS.md`.

### Placement Rules

- `AGENTS.md` must live at the team root
- `.codex/config.toml` must exist
- `.codex/docs/format-mapping.md` must exist
- `.codex/docs/format-mapping.manifest.yaml` must exist
- the coordinator file must live at `.codex/agents/` root
- non-coordinator agents must live under group subfolders in `.codex/agents/`
- every skill must exist in both `.codex/skills/{skill}/SKILL.md` and `.agents/skills/{skill}/SKILL.md`
- rules must live under `.codex/rules/`

## Violation Determination

- `AGENTS.md` is missing or not at the team root -> Violation
- `.codex/config.toml` is missing -> Violation
- `.codex/docs/format-mapping.md` is missing -> Violation
- `.codex/docs/format-mapping.manifest.yaml` is missing -> Violation
- coordinator file is not at `.codex/agents/` root -> Violation
- non-coordinator agents are placed beside the coordinator -> Violation
- a skill exists only in `.codex/skills/` or only in `.agents/skills/` -> Violation
- a `multi-agent` `AGENTS.md` omits runtime prerequisites or setup fallback -> Violation
- file or folder names break kebab-case -> Violation

## Exceptions

- If only one specialist group exists, it still must use a subfolder. Do not place worker agents directly beside the coordinator.
