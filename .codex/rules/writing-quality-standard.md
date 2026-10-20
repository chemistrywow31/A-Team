---
name: Writing Quality Standard
description: Keep authored Codex markdown effective, testable, and consistent with J5 artifact floors
---

# Writing Quality Standard

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`

## Rule Content

### Write Direct Instructions

Use imperative sentences. Replace vague phrases such as `try to`, `appropriately`, `reasonably`, `if needed`, `as appropriate`, `roughly`, `probably`, and `things like that` with observable criteria.

### Review Size For Effectiveness

Prioritize effectiveness using current official platform/model guidance. Preserve useful XML, examples, task steps, and checks; concision is secondary.

- Authored agent, skill, and rule targets remain 300, 200, and 100 lines respectively under J5.
- An over-target file is `REVIEW_REQUIRED`. Record its current size, concrete usefulness rationale, and evidence in the ordinary worklog or criterion report; the independent reviewer accepts or rejects that file. An author-only marker cannot produce unconditional PASS.
- Move detail to references when task routing preserves its usefulness. Do not cut effective instructions only to meet a number.
- Keep runtime TOMLs thin, with an authoritative-playbook bootstrap; the existing 260-line runtime-config/block limit and EC/dispatch report caps remain separately bounded.

### Use Examples That Clarify Behavior

Each authored agent and skill contains at least one meaningful rejection/defer/escalation case under `JUDGMENT.md` J5. Add useful positive or contrast examples when they clarify behavior or a testable boundary; no universal example count applies. Keep normal behavior explicit in Workflow and named Input and Output fields.

Keep the case concise: identify the triggering input and correct refusal, deferral, or escalation. Include a mistaken action only when it clarifies the boundary; a full before/after transcript is not required. Each rule includes observable violation determination.

### Align Copied Templates With Policy

After a policy change, check the templates, frontmatter examples, section skeletons, and checklists that instantiate it, including writer references. Correct contradictory copied blocks; structural validators alone cannot establish prose consistency.

### Make Behavior Observable

Use Boundaries for exclusions, Uncertainty Protocol for missing inputs, and typed outputs for handoffs. Keep one role-specific Reasoning/Workflow/Self-Critique contract rather than duplicate forms. Use `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {missing}` in CONCLUSIONS for information gaps and `STATUS: BLOCKED` for hard blockers; preserve the four EC-1 statuses.

### Disclose Non-Obvious Rule Cost

When a rule adds measurable simple-task overhead, significant context cost, or a predictable speed/simplicity conflict, include one or two sentences beginning `Tradeoff:` after Violation Determination or within Exceptions. Self-evident file I/O cost needs no extra disclosure.

## Violation Determination

- Descriptive prose replaces instructions, or vague wording lacks observable criteria -> Violation
- An over-target authored file is accepted without independent usefulness review, or an explicit runtime/dispatch cap is exceeded -> Violation
- An authored agent/skill has no meaningful boundary example, or an example contradicts required behavior -> Violation
- A copied template, example, or checklist contradicts the policy it implements -> Violation
- A rule lacks observable violation determination or required non-obvious-cost disclosure -> Violation
- An informational gap uses an invalid EC-1 status, or a prompt duplicates the decision/verification contract -> Violation

## Exceptions

This rule has no exceptions.
