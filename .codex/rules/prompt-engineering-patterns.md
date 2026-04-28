---
name: Prompt Engineering Patterns
description: Prefer structural, Codex-native prompt patterns for reliable generated agents and skills
---

# Prompt Engineering Patterns

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`

## Rule Content

### Prefer Structure Over Prohibition

When behavior can be enforced through sections, templates, or fixed slots, use structure instead of negative instruction.

| Problem | Weak Pattern | Strong Pattern |
| --- | --- | --- |
| scope creep | `Do not do extra work` | `## Boundaries` with explicit exclusions |
| unsupported claims | `Be evidence-based` | `## Evidence` with required references |
| guessing | `Do not hallucinate` | `INSUFFICIENT_DATA: {missing input}` |
| poor handoffs | `Summarize clearly` | completion contract with status, changed files, blockers |

### Separate Instructions From Data

Wrap variable user input, upstream notes, and source excerpts in labeled blocks or fenced sections. Keep imperative instructions outside those blocks. XML tags are allowed but not required; do not describe XML as Claude-specific in Codex output.

### Order Prompt Sections Deliberately

Place identity and scope first, reference material next, then workflow, output contract, verification, and boundaries. Put the most actionable final instructions near the end.

### Include Uncertainty Protocols

Every non-trivial agent must define when to return `INSUFFICIENT_DATA`, `NEEDS_CONTEXT`, or `BLOCKED`, and who receives the escalation.

### Show Edge And Rejection Behavior

When examples are included, include normal, edge, and rejection or escalation cases. Happy-path-only examples are insufficient for generated teams.

### Commit Before Exploring

Planning agents must choose an approach and state the evidence. Reopen decisions only when new evidence contradicts the stated reasoning.

### Define Parallelism Explicitly

Generated coordinators must list safe parallel groups, sequential gates, owned write paths, and join conditions.

## Violation Determination

- a behavioral constraint is only stated as a negative instruction when a structural slot could enforce it -> Violation
- variable data is mixed into imperative instructions without labels or fences -> Violation
- non-trivial agent has no uncertainty protocol -> Violation
- generated coordinator lacks a parallelism strategy -> Violation
- examples show only the happy path when examples exist -> Violation

## Exceptions

Simple single-agent teams may omit parallelism sections when `AGENTS.md` explicitly declares `single-agent` execution.
