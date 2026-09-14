---
name: Writing Quality Standard
description: Keep authored Codex markdown concise, testable, and consistent with J5 artifact floors
---

# Writing Quality Standard

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`

## Rule Content

### Write Direct Instructions

Use imperative sentences. Replace vague phrases such as `try to`, `appropriately`, `reasonably`, `if needed`, `as appropriate`, `roughly`, `probably`, and `things like that` with observable criteria.

### Keep Files Tight

- Authoritative agent playbook: at most 300 lines under J5.1.
- Runtime agent config or `developer_instructions` block: at most 260 lines; keep the bootstrap thin.
- Skill: at most 200 lines. Rule: at most 100 lines.
- Move details into references when the limit would be exceeded.

### Use One Rejection Example

Each authored agent and skill contains exactly one worked rejection/defer/escalation case under `JUDGMENT.md` J5; additional cases require an explicit change to the task's example criteria. Express normal behavior in Workflow and named Input and Output fields. Do not add normal or edge worked examples under the default floor.

Keep the case concise: identify the triggering input and correct refusal, deferral, or escalation. Include a mistaken action only when it clarifies the boundary; a full before/after transcript is not required. Each rule includes observable violation determination.

### Align Copied Templates With Policy

After a policy change, check the templates, frontmatter examples, section skeletons, and checklists that instantiate it, including writer references. Correct contradictory copied blocks; structural validators alone cannot establish prose consistency.

### Make Behavior Observable

Use Boundaries for exclusions, Uncertainty Protocol for missing inputs, and typed outputs for handoffs. Keep one role-specific Reasoning/Workflow/Self-Critique contract rather than duplicate forms. Use `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {missing}` in CONCLUSIONS for information gaps and `STATUS: BLOCKED` for hard blockers; preserve the four EC-1 statuses.

### Disclose Non-Obvious Rule Cost

When a rule adds measurable simple-task overhead, significant context cost, or a predictable speed/simplicity conflict, include one or two sentences beginning `Tradeoff:` after Violation Determination or within Exceptions. Self-evident file I/O cost needs no extra disclosure.

## Violation Determination

- Descriptive prose replaces instructions, or vague wording lacks observable criteria -> Violation
- A file exceeds its size limit -> Violation
- An authored agent/skill has no rejection example or adds unrequested normal/edge cases -> Violation
- A copied template, example, or checklist contradicts the policy it implements -> Violation
- A rule lacks observable violation determination or required non-obvious-cost disclosure -> Violation
- An informational gap uses an invalid EC-1 status, or a prompt duplicates the decision/verification contract -> Violation

## Exceptions

This rule has no exceptions.
