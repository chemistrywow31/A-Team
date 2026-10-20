---
name: Skill Context Fork
description: Decide when a skill should use context fork instead of running inline or via Agent dispatch
paths:
  - "teams/**"
  - ".claude/skills/**"
---

# Skill Context Fork

## Applicability

- Applies to: `skill-writer`, `team-architect`

## Rule Content

### Three Execution Modes

| Mode | How skill runs | Parent context impact |
|------|---------------|----------------------|
| Inline | Skill body executes in parent session | Full skill content + all intermediate output stays in parent |
| Agent dispatch | Skill instructs Claude to spawn an agent via Agent tool | Agent result summary returned to parent; intermediate output isolated |
| `context: fork` | Claude Code spawns skill body in fresh subagent context automatically | Only skill summary returned to parent; runtime-enforced isolation |

### When to Use `context: fork`

Declare `context: fork` in skill frontmatter when all of the following are true:

1. The skill body performs research, exploration, or long-running work that produces noisy intermediate output
2. The parent conversation does not need the intermediate output — only the final summary
3. The work does not require parent conversation history

Typical candidates:
- Literature scans
- Multi-source web research
- Large codebase exploration
- Test runs that generate verbose logs
- Multi-step data-gathering tasks

### When NOT to Use `context: fork`

Do not use `context: fork` for:

- **Entry-point skills** — they make the main session adopt the coordinator workflow (per `rules/output-structure.md`); adding `fork` would isolate that workflow from the main user-facing phase owner; native nesting support does not change this team policy
- Skills that need parent conversation history (e.g., skills that reference previously discussed files)
- Quick single-step skills where Agent dispatch overhead exceeds the skill's work
- Skills that return small deterministic output (use inline)

### Companion `agent` Field

When `context: fork` is declared, the skill must also declare `agent: {subagent-name}` pointing to a defined subagent in `.claude/agents/`. This companion field is an A-Team convention; native Claude also supports built-in agents and a default when `agent` is omitted. Validate the selected custom agent and preserve its tool/model configuration together with supported skill-level overrides. The body must contain a standalone task, not only reusable background guidelines.

### Format Template

```yaml
---
name: Literature Scan
description: Scan academic literature on a topic and return synthesized findings
context: fork
agent: literature-reviewer   # Must exist in .claude/agents/literature-reviewer.md
---

# Literature Scan

## Execution

[SKILL.md body becomes the prompt for the forked literature-reviewer subagent.]
```

### Explicit Skill Loading

A subagent does not automatically inherit skills used in its parent. Declare `skills` preload for always-needed references or instruct exact file reads in the dispatch. A forked skill supplies its own body as the task; it does not carry the parent conversation. Agent Teams is a separate mode whose teammates do not receive definition `skills` preload. See [skills](https://code.claude.com/docs/en/skills) and [subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-10-06.

### Entry-Point Exception

Entry-point skills — identified by coordinator workflow purpose or a main-session adoption contract, then validated for manual invocation, Agent access, and argument hints — do not use `context: fork`. They run in the main session, pre-approve the Agent tool with `allowed-tools: ["Agent"]`, and dispatch specialists from there — the coordinator workflow itself must keep the user channel.

## Violation Determination

- Skill declares `context: fork` without companion `agent` field → Violation
- Skill declares `context: fork` and `agent` points to a subagent that does not exist in `.claude/agents/` → Violation
- Entry-point skill declares `context: fork` → Violation (entry-points run in the main session)
- Skill declares `context: fork` but body requires parent conversation history (references prior messages) → Violation
- A dispatch assumes parent skills are inherited, or a fork body lacks an executable standalone task → Violation

## Exceptions

- During debugging, a skill may temporarily run inline even if it matches the fork criteria, to inspect intermediate output.

Tradeoff: `context: fork` saves parent context but costs one extra subagent invocation. For skills that run rarely and produce small output, inline is cheaper despite context bloat.
