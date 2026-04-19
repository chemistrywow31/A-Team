---
name: Context Tier
description: Define four tiers of context budget, model, and effort for generated agents based on decision scope
---

# Context Tier

## Applicability

- Applies to: `agent-writer`, `team-architect`

## Rule Content

### Tier System for Generated Agents

Every generated agent must include a Context Tier section that defines its startup context budget, model, and effort. This prevents over-feeding simple agents and under-feeding complex ones.

| Tier | Scope | Examples | Model | Effort | Startup Context |
|------|-------|----------|-------|--------|-----------------|
| 1 | Minimal (exception only) | Pure formatters, deterministic validators with fixed rules, single-lookup utilities | `sonnet` or `haiku` | `medium` or `low` | Role definition + immediate task input only |
| 2 | Standard | Execution agents (writers, builders, implementers) | `opus` | `high` | Tier 1 + upstream worklog paths + project constraints |
| 3 | Expanded | Planning and analysis agents (planners, researchers, reviewers, auditors) | `opus` | `xhigh` | Tier 2 + full workflow context + design principles |
| 4 | Full | Coordinators and cross-cutting agents (team lead, process reviewer, evolution master) | `opus` | `max` | All available context including team norms and project history |

### Default Bias

**Default to Tier 2 (`opus` + `high`) when uncertain.** Tier 1 is an exception requiring explicit justification — the task must have zero judgment calls and produce deterministic output from fully specified input. If an agent makes any judgment, it is Tier 2 or higher.

### Assignment Criteria

- **Tier 1**: Receives fully specified input. Produces deterministic output. **No** judgment calls. Requires justification in agent .md (state why the task has zero judgment).
- **Tier 2**: Makes local decisions within defined scope. Needs upstream context, not project-wide.
- **Tier 3**: Makes decisions affecting other agents or downstream phases. Needs broad context. Includes all research, planning, and review agents.
- **Tier 4**: Orchestrates agents or audits cross-cutting concerns. Needs maximum context.

### Documentation in Agent .md

Include the following section in every generated agent file:

```markdown
## Context Tier: {1|2|3|4}

Model: {model from table above, set in frontmatter}
Effort: {effort from table above, set in frontmatter}

Tier 1 justification (only if Tier 1 is declared): {state why the task has zero judgment calls}

Startup context:
- {Exactly what context this agent receives at dispatch}
```

### Frontmatter Requirement

The tier-assigned `model` and `effort` must be written directly into the agent's YAML frontmatter:

```yaml
---
name: Process Reviewer
description: ...
model: opus
effort: xhigh
---
```

Do not rely on coordinator dispatch to set effort. Frontmatter is authoritative. Coordinator dispatch `effort` parameter overrides frontmatter only for debugging / escalation scenarios.

### Coordinator Dispatch Rule

The coordinator must match dispatch context to the agent's tier:
- Do not send Tier 4 context to a Tier 1 agent (wastes context window)
- Do not restrict a Tier 3+ agent to Tier 1 context (starves decision-making)

## Violation Determination

- Generated agent .md has no Context Tier section → Violation
- Agent declares Tier 1 without justification in the Tier 1 justification field → Violation
- Agent declares Tier 1 but its workflow section shows judgment calls (tool choice, content selection, structure decisions) → Violation
- Agent frontmatter `model` or `effort` does not match the declared Context Tier → Violation
- Coordinator dispatches full project context to a Tier 1 agent → Violation
- Tier 3+ agent receives only immediate task input with no upstream context → Violation

## Exceptions

- During debugging or incident response, any agent may temporarily receive Tier 4 context and `max` effort regardless of declared tier.

Tradeoff: Higher tier = higher cost per invocation. Tier 4 with `max` effort on `opus` is expensive. Use Tier 1 only when the task truly has no judgment — misassigning a judgment task to Tier 1 produces low-quality output that costs more to fix than the model savings.
