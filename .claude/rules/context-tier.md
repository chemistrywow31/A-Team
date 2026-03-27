---
name: Context Tier
description: Define four tiers of context budget for generated agents based on decision scope
---

# Context Tier

## Applicability

- Applies to: `agent-writer`, `team-architect`

## Rule Content

### Tier System for Generated Agents

Every generated agent must include a Context Tier section that defines its startup context budget. This prevents over-feeding simple agents and under-feeding complex ones.

| Tier | Scope | Agents | Startup Context |
|------|-------|--------|-----------------|
| 1 | Minimal | Single-purpose utilities (formatters, validators, linters) | Role definition + immediate task input only |
| 2 | Standard | Execution agents (writers, builders, implementers) | Tier 1 + upstream worklog paths + project constraints |
| 3 | Expanded | Planning and analysis agents (planners, researchers, reviewers) | Tier 2 + full workflow context + design principles |
| 4 | Full | Coordinators and cross-cutting agents (auditors, process reviewers) | All available context including team norms and project history |

### Assignment Criteria

- **Tier 1**: Receives fully specified input, produces deterministic output. No judgment calls.
- **Tier 2**: Makes local decisions within defined scope. Needs upstream context, not project-wide.
- **Tier 3**: Makes decisions affecting other agents or downstream phases. Needs broad context.
- **Tier 4**: Orchestrates agents or audits cross-cutting concerns. Needs maximum context.

### Documentation in Agent .md

Include the following section in every generated agent file:

```markdown
## Context Tier: {1|2|3|4}

Recommended effort: {low|medium|high|max}

Startup context:
- {Exactly what context this agent receives at dispatch}
```

### Adaptive Thinking Effort Mapping

Map each tier to Claude's adaptive thinking `effort` parameter to optimize reasoning depth versus speed:

| Tier | Effort | Rationale |
|------|--------|-----------|
| 1 | `low` | Deterministic output, no judgment calls — fast execution preferred |
| 2 | `medium` | Local decisions within defined scope — balanced reasoning |
| 3 | `high` | Cross-agent decisions, broad context — deep reasoning needed |
| 4 | `high` or `max` | Orchestration and cross-cutting audits — maximum reasoning depth |

When dispatching tasks, the coordinator sets the `effort` parameter based on the target agent's tier. Include the recommended effort level in the Context Tier section of each generated agent.

### Coordinator Dispatch Rule

The coordinator must match dispatch context and thinking effort to the agent's tier:
- Do not send Tier 4 context to a Tier 1 agent (wastes context window)
- Do not restrict a Tier 3+ agent to Tier 1 context (starves decision-making)
- Match `effort` parameter to the agent's tier (see mapping table above)

## Violation Determination

- Generated agent .md has no Context Tier section → Violation
- Coordinator dispatches full project context to a Tier 1 agent → Violation
- Tier 3+ agent receives only immediate task input with no upstream context → Violation

## Exceptions

- During debugging or incident response, any agent may temporarily receive Tier 4 context
