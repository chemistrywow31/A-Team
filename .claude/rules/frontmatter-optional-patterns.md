---
name: Frontmatter Optional Patterns
description: Common optional frontmatter patterns for typical agent and skill roles
---

# Frontmatter Optional Patterns

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `team-architect`

## Rule Content

This rule provides canonical optional-field patterns. When writing an agent or skill that matches a pattern, apply the full configuration — do not omit fields that the pattern mandates.

### Pattern A: Read-Only Auditor Agent

For agents that audit, review, or validate without writing code or data:

```yaml
---
name: Process Reviewer
description: Audit team execution process and produce retrospective report
model: opus
effort: xhigh
tools: ["Read", "Grep", "Glob", "Write"]   # Write only for audit report
---
```

Apply to: process-reviewer, decision-auditor, dialogue-reviewer, code-reviewer, fact-checker, knowledge-reviewer, security-reviewer.

The `Write` tool stays on the allowlist for the audit report — everything else is removed so the agent cannot Edit / Bash / modify team state.

### Pattern B: Research / Investigation Agent

For agents that gather external information without mutating team state:

```yaml
---
name: Domain Researcher
description: Investigate domain best practices and produce evidence-based recommendations
model: opus
effort: xhigh
tools: ["Read", "Grep", "Glob", "Write", "WebFetch", "WebSearch"]
---
```

Apply to: domain-researcher, market-researcher, literature-reviewer, paper-reader. Add `mcpServers` if the agent needs a specific MCP (e.g., context7 for library docs).

### Pattern C: Planner Agent with Preloaded Reference Skills

For planning agents that repeatedly reference specific skill content:

```yaml
---
name: Skill Planner
description: Plan the skills and rules needed for each agent based on role design
model: opus
effort: xhigh
skills: ["prompt-patterns", "skill-discovery", "md-generation-standard"]
---
```

`skills` preload is only meaningful when the agent would otherwise re-read those skills on every invocation. For one-shot reference, let Claude load skill content on demand.

### Pattern D: Execution Agent (Default)

For most writing, building, and implementation agents:

```yaml
---
name: Agent Writer
description: Specialized in writing high-quality agent .md files
model: opus
effort: high
---
```

No `tools` restriction — execution agents typically need Read, Edit, Write, Bash. No `skills` preload — they read skills on demand via upstream worklog references.

### Pattern E: Coordinator

For the single coordinator per team:

```yaml
---
name: Team Architect
description: Chief coordinator orchestrating the full workflow
model: opus
effort: max
---
```

No `tools` restriction — the coordinator dispatches via Agent / Task tools and must retain full access. No `skills` preload — the coordinator reads context on demand.

### Pattern F: Entry-Point Skill

See `rules/yaml-frontmatter.md` Entry-Point Skill Mandate. Standard shape:

```yaml
---
name: Boss
description: Entry point that spawns the {coordinator} to run {workflow}
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team-specific hint]"
---
```

### Pattern G: Forked-Context Research Skill

For skills that would otherwise pollute parent context with search output (entry-points already use Agent tool; this pattern is for *non-entry* research skills):

```yaml
---
name: Deep Literature Scan
description: Scan literature on a topic and return only the summary
disable-model-invocation: false
context: fork
agent: literature-reviewer
model: opus
effort: xhigh
---
```

See `rules/skill-context-fork.md` for when to prefer `context: fork` over plain Agent dispatch.

## Violation Determination

- Read-only auditor agent without `tools` allowlist → Violation
- Research agent that needs web access missing `WebFetch` or `WebSearch` in `tools` → Violation
- Entry-point skill not matching Pattern F → Violation
- Skill uses `context: fork` without `agent` field → Violation

## Exceptions

- Patterns are defaults — deviations are allowed when the agent's responsibilities genuinely require a different toolset, but must be documented in the agent's `## Boundaries` section.

Tradeoff: Pattern compliance costs one line of frontmatter per field. The payoff is fewer permission prompts, faster startup (preloaded skills), and tighter security (tools allowlist).
