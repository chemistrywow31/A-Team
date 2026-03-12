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

- one agent prompt: 260 lines maximum
- one skill doc: 200 lines maximum
- one rule doc: 100 lines maximum
- if a file exceeds the limit, split it or move detail into references

### Examples Are Required

- every skill must include at least one example
- every rule must include violation determination

## Violation Determination

- descriptive prose replaces imperative instructions -> Violation
- a banned vague phrase appears without criteria -> Violation
- a file exceeds its size budget -> Violation
- a skill has no example -> Violation
- a rule has no violation determination -> Violation

## Exceptions

This rule has no exceptions.
