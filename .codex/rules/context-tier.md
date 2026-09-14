---
name: Context Tier
description: Assign GPT-6 strong roles and GPT-5.6 read-heavy roles with explicit runtime pins and bounded context
---

# Context Tier

## Applicability

- Applies to: `team-architect` and `agent-writer`

## Rule Content

### Assign Context By Decision Scope

Every role documents its tier and exact startup inputs in the same-relative authoritative `.codex/agents/{path}.md`. Keep `agents/{path}.toml` thin: runtime fields and a nonempty bootstrap to that playbook. Do not duplicate the tier section or runtime model/effort pins in prose.

Model/effort values below are defaults for new teams without explicit pins or explicitly authorized profile migration. Preserve explicit user or target model AND effort pins during unrelated regeneration/restructuring; retaining a pin requires no fresh compatibility approval. A model-only migration preserves existing supported effort unless the authorized scope also changes effort.

| Tier | Scope | Model default | Effort default | Startup context |
| --- | --- | --- | --- | --- |
| 1 | Deterministic utility, no judgment | Explicit approved utility pin | `low` or `medium` | Role and immediate input |
| 2 | Read-heavy bounded execution | `gpt-5.6-terra` | `high` | Tier 1 plus upstream worklog paths and constraints |
| 3 | Planning, generation, optimization, restructuring | `gpt-6-astra` | `xhigh` | Tier 2 plus workflow and decision context |
| 4 | Coordination and cross-cutting artifact gates | `gpt-6-astra` | `xhigh` | Relevant project constraints, worklog chain, role map, live routing |

Default to Tier 2 when uncertain. Tier 1 requires an explicit zero-judgment justification. Use Tier 3/4 when decisions affect other agents or phases. Record the scope and evidence for any authorized effort change.

### Pin Runtime Fields Explicitly

Set `model` and `model_reasoning_effort` in every `agents/**/*.toml` from the preserved target pins or applicable defaults above. Full-history forks inherit parent model/effort; use explicit role overrides with `fork_turns = "none"` or a positive bounded fork. Supply relevant paths and criteria so bounded context does not starve judgment tasks.

### Approved A-Team Repo-Self Profile And Roles

- Root and strong roles use `gpt-6-astra`/`xhigh`; project subagent default stays `gpt-5.6-terra`/`high`.
- Tier 2: `domain-researcher`, `runtime-preflight-advisor`, `dialogue-reviewer`.
- Tier 3: `requirements-analyst`, `role-designer`, `skill-planner`, `rule-writer`, `skill-writer`, `agent-writer`, `prompt-optimizer`, `team-restructuring-master`.
- Tier 4: `team-architect`, `decision-auditor`.

### Bound Startup Context

Give Tier 1 only the role and immediate task. Give Tier 3/4 relevant upstream decisions and constraints through paths, rather than automatically copying all history. Independent acceptance retains EC-3 fresh-context restrictions.

## Violation Determination

- An authoritative playbook omits tier/startup context or gives Tier 1 judgment work without justification -> Violation
- A TOML lacks explicit model/effort or a resolvable same-relative playbook bootstrap -> Violation
- Defaults override explicit user/target pins outside authorized migration, a model-only migration changes supported effort without authorization, or retaining a target pin triggers fresh compatibility approval -> Violation
- A playbook duplicates runtime model/effort fields, or a dispatch claims a role override on full history -> Violation
- Tier 1 receives broad history, or a judgment role lacks required upstream context -> Violation

## Exceptions

- Debugging or incident response may temporarily raise model, effort, or context when supported by the runtime and documented in the worklog.
