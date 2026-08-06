---
name: Writing Quality Standard
description: Set style and length rules for generated Codex markdown assets
---

# Writing Quality Standard

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`

## Rule Content

### Use Imperative Language

Write instructions as direct actions.

- Correct: `Confirm input completeness before starting work`
- Incorrect: `This role should confirm input completeness`

### Ban Vague Fillers

Do not use vague phrases unless followed by explicit criteria:

- `try to`
- `appropriately`
- `reasonably`
- `if needed`
- `as appropriate`
- `roughly`
- `probably`
- `things like that`

### Keep Files Tight

- one agent config or `developer_instructions` block: 260 lines maximum
- one skill doc: 200 lines maximum
- one rule doc: 100 lines maximum
- if a file exceeds the limit, split it or move detail into references

### Examples Are Required

- every skill must include at least one example
- when examples are used to teach behavior, include normal, edge, and rejection or escalation cases
- every rule must include violation determination

### Use EC Status Vocabulary

- Use `STATUS: NEEDS_CONTEXT` for informational gaps.
- Put `INSUFFICIENT_DATA: {missing}` in `CONCLUSIONS`; treat it as a marker, not a fifth status.
- Use `STATUS: BLOCKED` for hard blockers.

## Violation Determination

- descriptive prose replaces imperative instructions -> Violation
- a banned vague phrase appears without criteria -> Violation
- a file exceeds its size budget -> Violation
- a skill has no example -> Violation
- behavioral examples omit edge or rejection behavior when those cases are necessary to clarify the boundary -> Violation
- a template or example uses `INSUFFICIENT_DATA` as a status or defines a status outside the four EC-1 statuses -> Violation
- a rule has no violation determination -> Violation

## Exceptions

This rule has no exceptions.
