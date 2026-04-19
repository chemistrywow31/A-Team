---
name: Skill Context Fork
description: Decide when a skill should use context fork instead of running inline or via Agent dispatch
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

- **Entry-point skills** — they already spawn a coordinator via the Agent tool; adding `fork` creates double isolation, which breaks argument passing
- Skills that need parent conversation history (e.g., skills that reference previously discussed files)
- Quick single-step skills where Agent dispatch overhead exceeds the skill's work
- Skills that return small deterministic output (use inline)

### Companion `agent` Field

When `context: fork` is declared, the skill must also declare `agent: {subagent-name}` pointing to a defined subagent in `.claude/agents/`. The subagent's frontmatter (model, effort, tools) governs the forked execution.

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

### Entry-Point Exception

Entry-point skills (`skills/boss/SKILL.md`, `skills/a-team/SKILL.md`) do not use `context: fork`. They pre-approve the Agent tool with `allowed-tools: ["Agent"]` and call Agent explicitly inside the skill body — this gives them finer control over argument passing to the coordinator.

## Violation Determination

- Skill declares `context: fork` without companion `agent` field → Violation
- Skill declares `context: fork` and `agent` points to a subagent that does not exist in `.claude/agents/` → Violation
- Entry-point skill declares `context: fork` → Violation (entry-points must use Agent dispatch)
- Skill declares `context: fork` but body requires parent conversation history (references prior messages) → Violation

## Exceptions

- During debugging, a skill may temporarily run inline even if it matches the fork criteria, to inspect intermediate output.

Tradeoff: `context: fork` saves parent context but costs one extra subagent invocation. For skills that run rarely and produce small output, inline is cheaper despite context bloat.
