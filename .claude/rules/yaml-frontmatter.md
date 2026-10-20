---
name: YAML Frontmatter
description: Mandate YAML frontmatter as the first content in every generated .md file
paths:
  - "teams/**"
---

# YAML Frontmatter

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Every .md File Must Start with YAML Frontmatter

The very first line of every generated .md file must be `---`, opening a YAML frontmatter block. No content, comments, or blank lines may precede it.

### Agent .md Fields

Required by A-Team (native requirements and project conventions are distinct):

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent name, English title case |
| `description` | string | One sentence describing core responsibility (no period, under 120 chars) |
| `model` | string | Supported alias (`opus`, `sonnet`, `haiku`, `fable`), full model ID, or `inherit` |

Optional:

| Field | Type | When to use |
|-------|------|-------------|
| `effort` | string | `low` / `medium` / `high` / `xhigh` / `max` — match Context Tier |
| `tools` | array | Allowlist (e.g., `["Read", "Grep"]`) — restrict to minimum tools required |
| `disallowedTools` | array | Denylist, takes precedence over `tools` |
| `skills` | array | Full skill content preloaded for a subagent; parent skills are not inherited automatically |
| `mcpServers` | array | MCP servers available to this agent |
| `color` | string | UI color hint for multi-agent sessions |
| `maxTurns` | integer | Circuit breaker for runaway loops |

### Skill .md Fields

Required by A-Team (native requirements and project conventions are distinct):

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill name, English title case |
| `description` | string | One sentence describing the capability (no period, under 120 chars) |

Optional:

| Field | Type | When to use |
|-------|------|-------------|
| `disable-model-invocation` | boolean | `true` for entry-point skills — blocks Claude auto-trigger |
| `user-invocable` | boolean | `false` to hide from `/` menu (Claude-only reference skill) |
| `allowed-tools` | array | Tools pre-approved while skill active (reduces permission prompts) |
| `model` | string | Skill-level model override supported by the target client |
| `effort` | string | Skill-level thinking effort override |
| `context` | string | `fork` to run SKILL.md body in isolated subagent context |
| `agent` | string | Subagent `name` to use when `context: fork` |
| `argument-hint` | string | Autocomplete hint (e.g., `"[issue-number]"`) |
| `paths` | array | Glob patterns scoping auto-activation (skills support this) |
| `metadata` | map | Native free-form tooling metadata; does not cause skill loading |
| `benefits-from` | array | A-Team-only dependency label; existing top-level form is tooling metadata, not Claude runtime behavior |

### Rule .md Fields

Required: `name`, `description`.
Optional: `paths` — glob array scoping when rule loads.

### A-Team Conventions And Native Semantics

Native Claude requires agent `name` and `description`; A-Team additionally requires explicit agent `model` and tier `effort`. Native omission permits inheritance, and `inherit` is a supported model value. Preserve existing names/pins; Title Case and short descriptions below are A-Team authoring conventions, not native alias/name validation limits. For child skills, use explicit `skills` preload or instruct reads of exact skill files. Agent Teams teammates do not receive definition `skills` preload. `benefits-from` never implies inheritance or automatic loading; prefer `metadata` for newly introduced tooling data and validate existing labels only as A-Team metadata. See [subagents](https://code.claude.com/docs/en/sub-agents) and [skills](https://code.claude.com/docs/en/skills), checked 2026-10-06.

### Defaults

- Select new-team model/effort defaults from `rules/context-tier.md`; preserve existing explicit user/target pins and supported inheritance selections.
- `effort`: Default **`high`**. Use `xhigh` for planning / analysis / research / review agents, `max` for coordinators and cross-cutting audits. Use `medium` or `low` only for Tier 1 agents.
- `description`: One sentence, no period, under 120 chars.
- `name`: English, title case.
- `paths`: Standard glob syntax; `**` for recursive match, `{ts,tsx}` for brace expansion.

### Entry-Point Skill Mandate

Every skill serving as a team entry point — the folder name is the team's choice, e.g. `skills/tongzheng/SKILL.md` or `skills/a-team/SKILL.md` — must declare:

```yaml
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[one-line hint for expected arguments]"
```

Identify the coordinator entry by its workflow purpose or main-session adoption contract, then check these fields separately. A manual-only flag alone does not identify an entry. Entry skills adopt the coordinator in the current session and serve explicit user invocation; they do not spawn the coordinator or fork its workflow.

### Validation Timing

Team Architect must validate frontmatter during Phase 3 cross-validation, before marking any file complete.

## Violation Determination

- File does not start with `---` on line 1 → Violation
- Agent .md missing `name`, `description`, or `model` → Violation
- Skill .md or Rule .md missing `name` or `description` → Violation
- `model` is empty or unsupported by the selected native client; do not reject supported aliases, full IDs, or `inherit` by a three-alias whitelist → Violation
- `effort` not in `[low, medium, high, xhigh, max]` → Violation
- A default overrides a preserved target model/effort without authorized migration → Violation
- Entry-point skill missing `disable-model-invocation: true` → Violation
- `context: fork` used without companion `agent` field → Violation
- A-Team `benefits-from` references a non-existent skill, or is claimed to preload/inherit content → Violation
- Blank line or content before opening `---` → Violation
- `paths` contains non-glob values → Violation

## Exceptions

This rule has no exceptions.
