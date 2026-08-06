---
name: Context Tier
description: Assign GPT-5.6 model and effort tiers by decision scope for Codex agents
---

# Context Tier

## Applicability

- Applies to: `team-architect` and `agent-writer`

## Rule Content

### Tier System

Every generated role must document its context tier in the same-relative authoritative `.codex/agents/{path}.md` playbook. The thin `agents/{path}.toml` may carry only runtime keys and a nonempty `developer_instructions` bootstrap to that playbook; do not duplicate the tier section in TOML.

| Tier | Scope | Model Guidance | Effort | Startup Context |
| --- | --- | --- | --- | --- |
| 1 | deterministic utility | inherited project default or lower approved utility tier | `low` or `medium` | role plus immediate task |
| 2 | read-heavy bounded execution | `gpt-5.6-terra` | `high` | Tier 1 plus upstream worklog paths |
| 3 | planning, generation, optimization, restructuring | `gpt-5.6-sol` | `xhigh` | Tier 2 plus workflow and decision context |
| 4 | coordinator or cross-cutting artifact gate | `gpt-5.6-sol` or stronger approved project pin | `xhigh` | full project constraints, worklog chain, role map, and live routing state |

### Default Bias

Default to Tier 2 when uncertain. Use Tier 1 only when the task has no judgment calls. Use Tier 3 or 4 when decisions affect other agents or downstream phases.

### TOML Alignment

Set `model` and `model_reasoning_effort` in each `agents/**/*.toml` file to match the tier. If the project intentionally pins a model family, keep the pin and document the tier rationale in the authoritative playbook.

### Startup Context Discipline

Do not send Tier 4 context to Tier 1 utilities. Do not starve Tier 3 or Tier 4 agents by passing only immediate task text.

### A-Team Role Guidance

- Tier 2 by default: `domain-researcher`, `runtime-preflight-advisor`, `dialogue-reviewer`
- Tier 3 by default: `requirements-analyst`, `role-designer`, `skill-planner`, `rule-writer`, `skill-writer`, `agent-writer`, `prompt-optimizer`, `team-restructuring-master`
- Tier 4 by default: `team-architect`, `decision-auditor`

## Violation Determination

- authoritative `.codex/agents/{path}.md` playbook lacks a context tier note -> Violation
- TOML bootstrap is empty, does not point to the same-relative playbook, or points to a missing file -> Violation
- Tier 1 role performs judgment or planning -> Violation
- `model_reasoning_effort` conflicts with the documented tier without rationale -> Violation
- a new or regenerated Codex role still uses `gpt-5.4` examples or defaults -> Violation
- coordinator sends broad project context to a deterministic utility -> Violation
- analysis or review agent receives no upstream worklog or decision context -> Violation

## Exceptions

During debugging, the coordinator may temporarily raise a specialist's model or effort. Log the reason in the worklog.
