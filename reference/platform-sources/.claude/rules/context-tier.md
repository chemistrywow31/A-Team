---
name: Context Tier
description: Assign Claude-native startup context and model effort by decision scope
paths:
  - "teams/**"
---

# Context Tier

## Applicability

- Applies to: `agent-writer`, `team-architect`

## Rule Content

### Assign Context By Decision Scope

Every generated agent documents its tier and exact startup inputs in its authoritative role file. Tier measures decision scope; provide the relevant workflow, constraints, and worklog chain rather than automatically copying all history.

The Claude model/effort values below are defaults for new teams without explicit pins or explicitly authorized profile migration. Preserve explicit user or target model AND effort pins during unrelated regeneration/restructuring; retaining a pin requires no fresh compatibility approval. A model-only migration preserves existing supported effort unless the authorized scope also changes effort.

| Tier | Scope | Claude model / effort defaults | Startup context |
| --- | --- | --- | --- |
| 1 | Deterministic utility, no judgment | `sonnet` or `haiku` / `medium` or `low` | Role and immediate input |
| 2 | Local execution decisions: writers, builders, implementers | `opus` / `high` | Tier 1 plus upstream paths and constraints |
| 3 | Planning, analysis, and review affecting downstream work | `opus` / `xhigh` | Tier 2 plus workflow and decision context |
| 4 | Coordination, restructuring, and cross-cutting decisions | `opus` / `max` | Relevant project constraints, worklog chain, role map, and project history |

Default to Tier 2 when uncertain. Tier 1 requires an explicit zero-judgment justification. Assign Tier 3 or 4 from decision scope, not another platform's role label; record the scope and evidence for any authorized effort change.

### Declare Once In Claude Frontmatter

- Write `model` and `effort` directly in agent YAML frontmatter under A-Team policy; dispatch overrides require a stated reason. Native Claude supports aliases including `fable`, full model IDs, and `inherit`; an omitted native effort inherits session effort. These native options do not authorize replacing a target pin. Check the selected model/client supports the requested effort.
- A-Team tier defaults are design choices, not vendor model defaults. Record configured values separately from the effective invocation and model availability. See [Claude subagents](https://code.claude.com/docs/en/sub-agents) and [effort guidance](https://platform.claude.com/docs/en/build-with-claude/effort), checked 2026-10-06.
- Put the Context Tier and Startup context notes in the authoritative role file. Do not duplicate model/effort in those notes; frontmatter is their single source.
- When the selected output includes Codex, use `.codex/rules/codex-runtime-config.md`, `.codex/rules/codex-agent-config-patterns.md`, and `.codex/rules/context-isolation.md` for that target's runtime adaptation. Their platform defaults and controls do not change Claude model/effort or context assignments.

### Bound Startup Context

Give Tier 1 only the role and task input. Give Tier 3/4 relevant upstream decisions, project constraints, and worklog paths. Independent acceptance retains the fresh-context restriction in the execution contract.

## Violation Determination

- An authoritative role file omits tier/startup context or assigns judgment work to Tier 1 without justification -> Violation
- Required Claude frontmatter model/effort is absent, or a default overrides an explicit user/target pin outside authorized migration -> Violation
- Context prose duplicates frontmatter model/effort, or another platform's role label determines a Claude tier without decision-scope evidence -> Violation
- A model-only migration changes supported effort without authorization, or retaining a target pin triggers fresh compatibility approval -> Violation
- Tier 1 receives broad history, or a judgment role lacks required upstream context -> Violation

## Exceptions

- Debugging or incident response may temporarily raise model, effort, or context when the worklog records the reason and the runtime supports it.
