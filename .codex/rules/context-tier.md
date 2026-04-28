---
name: Context Tier
description: Assign model, effort, and startup context by decision scope for generated Codex agents
---

# Context Tier

## Applicability

- Applies to: `team-architect` and `agent-writer`

## Rule Content

### Tier System

Every generated multi-agent config must document its context tier inside `developer_instructions`.

| Tier | Scope | Model Guidance | Effort | Startup Context |
| --- | --- | --- | --- | --- |
| 1 | deterministic utility | `gpt-5.4-mini` or project default | `low` or `medium` | role plus immediate task |
| 2 | bounded execution | project default, usually `gpt-5.4` | `high` | Tier 1 plus upstream worklog paths |
| 3 | planning, research, review | project default or stronger configured model | `xhigh` | Tier 2 plus workflow and decision context |
| 4 | coordinator or cross-cutting audit | strongest approved project model | `xhigh` | full project constraints, worklog chain, and role map |

### Default Bias

Default to Tier 2 when uncertain. Use Tier 1 only when the task has no judgment calls. Use Tier 3 or 4 when decisions affect other agents or downstream phases.

### TOML Alignment

Set `model` and `model_reasoning_effort` in each `agents/**/*.toml` file to match the tier. If the project intentionally pins a model family, keep the pin and document the tier rationale.

### Startup Context Discipline

Do not send Tier 4 context to Tier 1 utilities. Do not starve Tier 3 or Tier 4 agents by passing only immediate task text.

## Violation Determination

- generated agent config lacks a context tier note -> Violation
- Tier 1 role performs judgment or planning -> Violation
- `model_reasoning_effort` conflicts with the documented tier without rationale -> Violation
- coordinator sends broad project context to a deterministic utility -> Violation
- analysis or review agent receives no upstream worklog or decision context -> Violation

## Exceptions

During debugging, the coordinator may temporarily raise a specialist's model or effort. Log the reason in the worklog.
