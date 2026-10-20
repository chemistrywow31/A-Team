---
name: Frontmatter Optional Patterns
description: Common optional frontmatter patterns for typical agent and skill roles
paths:
  - "teams/**"
---

# Frontmatter Optional Patterns

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `team-architect`

## Rule Content

This rule provides canonical optional-field patterns. When writing an agent or skill that matches a pattern, apply the full configuration — do not omit fields that the pattern mandates. These are A-Team policy patterns, not a complete native schema; preserve existing model/effort pins under the context-tier rule.

### Pattern A: Read-Only Auditor Agent

For agents that audit, review, or validate without writing code or data:

```yaml
---
name: Process Reviewer
description: Audit team execution process and produce retrospective report
model: opus
effort: xhigh
disallowedTools: [Agent]
tools: ["Read", "Grep", "Glob", "Write"]   # Write only for audit report
---
```

Apply to: process-reviewer, decision-auditor, dialogue-reviewer, code-reviewer, fact-checker, knowledge-reviewer, security-reviewer.

The allowlist limits available tools; it does not scope `Write` to a report path. Exact ownership and the live sandbox determine permitted writes. If the host blocks report persistence, use the coordinator-owned EC-1.12 handoff; do not grant broader permissions or claim tool presence proves path isolation.

### Pattern B: Research / Investigation Agent

For agents that gather external information without mutating team state:

```yaml
---
name: Domain Researcher
description: Investigate domain best practices and produce evidence-based recommendations
model: opus
effort: xhigh
disallowedTools: [Agent]
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
disallowedTools: [Agent]
skills: ["prompt-patterns", "skill-discovery", "md-generation-standard"]
---
```

`skills` injects full content into the subagent startup context. Preload references used on every run; otherwise instruct reads of exact files. Parent skills are not inherited automatically, and Agent Teams teammates do not receive definition skill preload. See [subagents](https://code.claude.com/docs/en/sub-agents) and [Agent Teams](https://code.claude.com/docs/en/agent-teams), checked 2026-10-06.

### Pattern D: Execution Agent (Default)

For most writing, building, and implementation agents:

```yaml
---
name: Agent Writer
description: Specialized in writing high-quality agent .md files
model: opus
effort: high
disallowedTools: [Agent]
---
```

No `tools` allowlist restriction — execution agents typically need Read, Edit, Write, Bash. `disallowedTools: [Agent]` enforces the specialist no-delegation policy supported by the coordinator-mandate rule. No `skills` preload — they read skills on demand via upstream worklog references.

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

No `tools` restriction — the coordinator dispatches via Agent tool (`Task` is a compatibility alias) and must retain full access. No `skills` preload — the coordinator reads context on demand.

### Pattern F: Entry-Point Skill

See `rules/yaml-frontmatter.md` Entry-Point Skill Mandate and the requested-surface guidance in `rules/output-structure.md`. The skill makes the CURRENT session adopt the coordinator playbook — it never spawns the coordinator as a subagent. Keeping phase ownership in the main session is A-Team policy; native subagents can nest, so runtime impossibility is not the rationale. Standard shape:

```yaml
---
name: {EntryPointName}                 # Preserve the team-chosen command/display identifier
description: Entry point that makes the current session adopt the {coordinator} workflow to run {workflow}
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team-specific hint]"
---
```

Identify the coordinator entry from its declared workflow purpose or main-session adoption contract, then verify `disable-model-invocation`, `allowed-tools`, and `argument-hint`. An ordinary manual-only skill is not an entry. Preserve the team-chosen `name` and directory; native command naming uses those fields, not an A-Team-mandated display-name equality.

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

- Read-only auditor agent without `tools` allowlist, or specialist missing its `disallowedTools: [Agent]` restriction → Violation
- Research agent that needs web access missing `WebFetch` or `WebSearch` in `tools` → Violation
- Entry-point skill not matching Pattern F → Violation
- Skill uses `context: fork` without `agent` field → Violation

## Exceptions

- Patterns are defaults — deviations are allowed when the agent's responsibilities genuinely require a different toolset, but must be documented in the agent's `## Boundaries` section.

Tradeoff: Preload spends startup context on full skill content, while on-demand reads spend tool calls. Choose from actual reuse; a tool allowlist narrows capability but does not enforce report-path ownership.
