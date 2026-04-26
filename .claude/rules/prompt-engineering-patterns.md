---
name: Prompt Engineering Patterns
description: Claude-optimized prompt patterns that all generation agents must apply when producing .md files
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
| Prevent hallucination | "Don't make things up" | Add escape hatch: `INSUFFICIENT_DATA: {what is missing}` |
| Enforce output format | "Output JSON" | Use structured template with labeled slots |
| Separate data from instructions | Embed data inline | Wrap variable data in XML tags |

### XML Tag Separation for Variable Data

Claude is specifically trained to recognize XML tag boundaries — this is a Claude-specific advantage over other LLMs. Wrap all variable or dynamic data in descriptive XML tags to prevent Claude from confusing data content with prompt instructions.

Rules for generated prompts:
- Wrap every variable input in descriptive tags: `<user_requirements>`, `<upstream_context>`, `<source_document>`, etc. Any descriptive name works — no reserved names.
- Keep instructions outside the tags; keep data inside the tags.
- Coordinator dispatch must XML-tag variable data passed to agents (see `rules/context-management.md`).
- Claude mimics input quality — clean, well-tagged prompts produce cleaner output.

### Element Ordering in Generated Prompts

Structure every generated .md file so that:
1. **Identity and context** come first (who the agent is, what it knows)
2. **Reference data, rules, and examples** come in the middle
3. **Task workflow, output format, and boundaries** come last

Placing actionable instructions at the end of a prompt improves response quality by up to 30%. The agent template already follows this order — do not rearrange sections.

### Example Diversity

Every generated .md that contains examples must include at minimum:
1. **Normal case**: Standard input producing expected output
2. **Edge case**: Unusual but valid input testing boundary handling
3. **Rejection case**: Input that triggers rejection, escalation, or `INSUFFICIENT_DATA`

Happy-path-only examples cause Claude to produce plausible-looking output even on garbage or insufficient input.

### Full Scenario Before/After Examples

When an example demonstrates behavioral guidance (how to handle a request, how to respond, how to make decisions), use the Full Scenario Before/After format instead of one-line comparisons. This format has three parts:

1. **Trigger**: The user request or input that starts the scenario
2. **❌ Common mistake**: A complete response showing how agents typically get it wrong, followed by a bullet list of specific problems
3. **✅ Correct approach**: A complete response showing the right behavior

This format works across all domains — coding, content, customer service, research, planning. The key is showing the full response shape, not just a label.

One-line comparisons ("Correct: X / Incorrect: Y") remain valid for format and style rules where the contrast is self-evident. Use Full Scenario format when the mistake is behavioral — the agent does something structurally wrong, not just stylistically wrong.

### Escape Hatches for Uncertainty

Every generated agent must define an explicit protocol for when it lacks sufficient information:
- The specific phrase to use (e.g., `INSUFFICIENT_DATA: {what is missing}`)
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

Every generated coordinator must include explicit parallel execution guidance — this raises parallel tool call success rate to ~100%. Required: list concurrent agent groups, define sequential gates, and instruct dispatching independent tasks in the same message.

## Violation Determination

- Generated agent has only happy-path examples and no edge/rejection cases → Violation
- Behavioral guidance example uses one-line comparison when a Full Scenario Before/After would clarify the mistake → Violation
- Generated agent has no escape hatch or uncertainty protocol → Violation
- Generated agent has no `## Reasoning` section before `## Workflow` (see `rules/reasoning-and-self-critique.md`) → Violation
- Generated agent has no `## Self-Critique` section after `## Workflow` (see `rules/reasoning-and-self-critique.md`) → Violation
- Generated coordinator has no `## Pre-Dispatch Reasoning` section in addition to `## Reasoning` → Violation
- Generated prompt uses `CRITICAL`/`MUST` for non-safety behavioral preferences → Violation
- Generated coordinator has no parallelism strategy → Violation
- Instructional-only solution used when a structural alternative exists → Violation
- Generated prompt mixes variable data with instructions without XML tag separation → Violation

## Exceptions

- Tier 1 agents (simple utilities with fully validated upstream input) may omit escape hatches.
- External skills (Pattern A direct install) are exempt from example diversity requirements.
