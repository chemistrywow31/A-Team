---
name: Prompt Engineering Patterns
description: Claude-optimized prompt patterns that all generation agents must apply when producing .md files
paths:
  - "teams/**"
---

# Prompt Engineering Patterns

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`

## Rule Content

### Structural Solutions Over Instructional Solutions

When a behavioral constraint can be enforced by structure (dedicated sections, fixed templates, explicit output slots), use structure. Claude reliably follows structural boundaries but frequently ignores negative instructions.

| Problem | Instructional (weak) | Structural (strong) |
|---------|---------------------|---------------------|
| Prevent premature answers | "Think before answering" | Add `## Reasoning` section before `## Workflow` (see `rules/reasoning-and-self-critique.md`) |
| Prevent unchallenged output | "Review your work" | Add `## Self-Critique` section after `## Workflow` (see `rules/reasoning-and-self-critique.md`) |
| Prevent scope creep | "Only do what's asked" | Define `## Boundaries` with explicit exclusion list |
| Force evidence-backed decisions | "Provide evidence" | Require `## Evidence` section with source references |
| Prevent hallucination | "Don't make things up" | Use `STATUS: NEEDS_CONTEXT` and put `INSUFFICIENT_DATA: {what is missing}` in `CONCLUSIONS` |
| Enforce output format | "Output JSON" | Use structured template with labeled slots |
| Separate data from instructions | Embed data inline | Wrap variable data in XML tags |

### XML Tag Separation for Variable Data

Claude is trained to recognize XML boundaries. Wrap variable input in descriptive tags such as `<user_requirements>`, `<upstream_context>`, and `<source_document>`; keep instructions outside and data inside. Coordinator dispatches must tag variable data per `rules/context-management.md`.

### Element Ordering in Generated Prompts

Order every generated .md file as: identity and context; reference data, rules, and examples; then task workflow, output format, and boundaries.

Placing actionable instructions at the end of a prompt measurably improves instruction adherence. The agent template already follows this order — do not rearrange sections.

### One Example, and It Is the Rejection Case

Every generated agent .md and skill .md carries exactly one worked example — the rejection case — per `rules/writing-quality-standard.md`. Do not add normal or edge cases. Examples narrow the model to the exploration space they demonstrate, so the normal path is better expressed as an enumerated `## Uncertainty Protocol` trigger list and typed `## Input and Output` slots. The rejection case survives because a refusal boundary is the one thing no parameter type can express.

### Full Scenario Before/After Examples

For behavioral guidance, use a Full Scenario Before/After with three parts: **Trigger**, **Common mistake** with a complete response and named problems, and **Correct approach** with the complete response shape. Reserve one-line comparisons for self-evident format or style rules.

### Escape Hatches for Uncertainty

Every generated agent must define an explicit protocol for when it lacks sufficient information:
- Use `STATUS: NEEDS_CONTEXT` for an informational gap.
- Put `INSUFFICIENT_DATA: {what is missing}` in `CONCLUSIONS`; it is a marker, not a fifth status.
- Use `STATUS: BLOCKED` for a hard blocker that more information cannot resolve.
- Conditions that trigger this response
- Escalation target (coordinator or user)

Claude defaults to producing helpful-sounding output even when data is insufficient. An explicit escape hatch overrides this tendency.

### Tone Calibration for Claude 4.6

Claude 4.6 responds more strongly to system prompt language than previous versions. Urgency modifiers (`CRITICAL`, `ALWAYS`, `NEVER`) that were previously necessary now cause over-triggering and rigid behavior.

| Severity | Use | Phrasing |
|----------|-----|----------|
| Safety boundary | Data loss, security, destructive actions | "CRITICAL: ..." or "MUST ..." |
| Mandatory process | Required workflow steps, format compliance | "Required:" prefix, normal tone |
| Behavioral preference | Default approaches, style choices | "Prefer X" or "Default to X" |
| Guidance | Soft recommendations | "When X, use Y" |

Reserve urgency language for true safety boundaries. Use normal language for everything else.

### Commitment Over Exploration

Opus 4.6 tends to over-explore when given open-ended instructions. Generated planning and coordinator agents must include: "Choose an approach and commit to it. Revisit decisions only when new evidence directly contradicts your reasoning." Avoid "If in doubt, investigate further" — this triggers excessive exploration loops.

### Parallel Execution Instructions

Every generated coordinator must include explicit parallel execution guidance. Required: list concurrent agent groups, define sequential gates, instruct dispatching independent tasks in the same message, and state a batch-size rule for repetitive work (batch items into one dispatch when more than 5 similar items exist; never dispatch per-item — measured cost in ground truth: ~25× overhead).

## Violation Determination

- Generated agent has no rejection-case example, or carries normal/edge cases → Violation
- Behavioral guidance example uses one-line comparison when a Full Scenario Before/After would clarify the mistake → Violation
- Generated agent has no escape hatch or uncertainty protocol → Violation
- Generated prompt uses `INSUFFICIENT_DATA` as a status or defines any status outside the four EC-1 statuses → Violation
- Generated agent has no `## Reasoning` section before `## Workflow` (see `rules/reasoning-and-self-critique.md`) → Violation
- Generated agent has no `## Self-Critique` section after `## Workflow` (see `rules/reasoning-and-self-critique.md`) → Violation
- Generated coordinator has no `## Pre-Dispatch Reasoning` section in addition to `## Reasoning` → Violation
- Generated prompt uses `CRITICAL`/`MUST` for non-safety behavioral preferences → Violation
- Generated coordinator has no parallelism strategy → Violation
- Instructional-only solution used when a structural alternative exists → Violation
- Generated prompt mixes variable data with instructions without XML tag separation → Violation

## Exceptions

- Tier 1 agents (simple utilities with fully validated upstream input) may omit escape hatches.
- External skills (Pattern A direct install) keep their upstream examples as-is; the one-rejection-case rule governs authored files, not vendored ones.
