---
name: YAML Frontmatter
description: Mandate YAML frontmatter as the first content in every generated .md file
---

# YAML Frontmatter

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Every .md File Must Start with YAML Frontmatter

The very first line of every generated .md file must be `---`, opening a YAML frontmatter block. No content, comments, or blank lines may precede it.

### Agent .md Fields

Required:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent name, English title case |
| `description` | string | One sentence describing core responsibility (no period, under 120 chars) |
| `model` | string | `opus`, `sonnet`, or `haiku` |

Optional:

| Field | Type | When to use |
|-------|------|-------------|
| `effort` | string | `low` / `medium` / `high` / `xhigh` / `max` — match Context Tier |
| `tools` | array | Allowlist (e.g., `["Read", "Grep"]`) — restrict to minimum tools required |
| `disallowedTools` | array | Denylist, takes precedence over `tools` |
| `skills` | array | Skill names preloaded into startup context (Task dispatch only) |
| `mcpServers` | array | MCP servers available to this agent |
| `color` | string | UI color hint for multi-agent sessions |
| `maxTurns` | integer | Circuit breaker for runaway loops |

### Skill .md Fields

Required:

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
| `model` | string | Skill-level model override (`opus` / `sonnet` / `haiku`) |
| `effort` | string | Skill-level thinking effort override |
| `context` | string | `fork` to run SKILL.md body in isolated subagent context |
| `agent` | string | Subagent `name` to use when `context: fork` |
| `argument-hint` | string | Autocomplete hint (e.g., `"[issue-number]"`) |
| `paths` | array | Glob patterns scoping auto-activation (skills support this) |
| `benefits-from` | array | A-Team custom — declare upstream skill dependencies |

### Rule .md Fields

Required: `name`, `description`.
Optional: `paths` — glob array scoping when rule loads.

### Defaults

- `model`: Default **`opus`**. Use `sonnet` or `haiku` only when the task is deterministic and trivial (see `rules/context-tier.md` Tier 1 criteria).
- `effort`: Default **`high`**. Use `xhigh` for planning / analysis / research / review agents, `max` for coordinators and cross-cutting audits. Use `medium` or `low` only for Tier 1 agents.
- `description`: One sentence, no period, under 120 chars.
- `name`: English, title case.
- `paths`: Standard glob syntax; `**` for recursive match, `{ts,tsx}` for brace expansion.

### Entry-Point Skill Mandate

Every skill serving as a team entry point (e.g., `skills/boss/SKILL.md`, `skills/a-team/SKILL.md`) must declare:

```yaml
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[one-line hint for expected arguments]"
```

Entry-point skills exist for explicit user invocation only. Claude must not auto-trigger full team workflows from conversational context.

### Validation Timing

Team Architect must validate frontmatter during Phase 3 cross-validation, before marking any file complete.

## Violation Determination

- File does not start with `---` on line 1 → Violation
- Agent .md missing `name`, `description`, or `model` → Violation
- Skill .md or Rule .md missing `name` or `description` → Violation
- `model` not in `[opus, sonnet, haiku]` → Violation
- `effort` not in `[low, medium, high, xhigh, max]` → Violation
- Agent or skill uses `model: sonnet` or `model: haiku` without stating the task is deterministic and trivial → Violation
- Entry-point skill missing `disable-model-invocation: true` → Violation
- `context: fork` used without companion `agent` field → Violation
- Skill `benefits-from` references non-existent skill → Violation
- Blank line or content before opening `---` → Violation
- `paths` contains non-glob values → Violation

## Exceptions

This rule has no exceptions.
