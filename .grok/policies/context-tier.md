---
name: Context Tier
description: Assign startup context by decision scope without inventing Grok model or effort quality tiers
---

# Context Tier

## Applicability

- Applies to agent writers, coordinators, planners, and reviewers selecting startup inputs or runtime profiles.

## Rule Content

### Assign Context By Decision Scope

Every authoritative role declares its context tier and exact startup inputs. Tier measures the decision scope, not model quality or privilege.

| Tier | Scope | Startup context |
| --- | --- | --- |
| 1 | Deterministic utility with no judgment | Role and immediate input only |
| 2 | Local execution: writing, building, implementation | Tier 1 plus upstream paths and constraints |
| 3 | Planning, analysis, review affecting downstream work | Relevant workflow, prior decisions, criteria, and worklog paths |
| 4 | Coordination, restructuring, cross-cutting decisions | Project constraints, role map, relevant history and phase decision chain |

Default to Tier 2 when uncertain. Tier 1 requires a documented zero-judgment justification. Assign Tier 3 or 4 from the actual decision scope. Independent acceptance always follows the fresh-context restriction in EC-3, regardless of tier.

### Separate Context From Model Selection

For this native branch, omit role `model` and `effort`. Source supports omitted or `inherit` model using the parent model. Omitted effort means the installed session/default behavior remains; it is not evidence of effort inheritance or a chosen effective value. Context tiers do not authorize substituting a model.

A later model/effort pin requires an actual supported model identifier, availability evidence, and task-relevant evaluation. Record configured values separately from the effective invocation and quality evidence. Parser success and an agent listing do not prove model access or routing. Do not derive provider equivalence from names, prices, or another runtime's role tiers.

Preserve existing explicit target model AND effort choices during unrelated maintenance. A model-only migration preserves supported effort unless changing it is also authorized. An unavailable preserved pin is a readiness concern to report, not permission to silently replace it. Retaining a supported pin needs no repeated user approval.

### Declare Runtime Choices Once

Agent frontmatter is the runtime declaration for an explicitly selected override. The role's Context Tier section names scope and startup paths, not duplicate model/effort settings. Project `.grok/config.toml` cannot persist these overrides. Skills' accepted `model` and `effort` metadata are not effective routing controls.

### Bound Startup Context

Load the role's named startup policies and exact task inputs. Supply Tier 1 no broad project history. Give planning and review the actual decisions and constraints needed for their work, without producer reasoning in independent acceptance. Load optional details only when their trigger applies.

## Violation Determination

- A role omits tier/startup inputs or calls judgment work Tier 1 without justification -> Violation.
- A context tier implies an unmeasured model hierarchy or an effective effort value -> Violation.
- Model/effort choices are duplicated, changed outside scope, or placed in ineffective project/skill fields as controls -> Violation.
- An independent reviewer receives producer history, or a role lacks required decision inputs -> Violation.

## Exceptions

Incident response may select a supported stronger profile or wider context within existing authorization when the worklog names the observed need and evidence. This does not remove retry bounds or independent acceptance.
