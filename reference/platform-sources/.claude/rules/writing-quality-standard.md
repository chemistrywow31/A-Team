---
name: Writing Quality Standard
description: Specify writing style, language requirements, and quality standards for all generated .md files
paths:
  - "teams/**"
---

# Writing Quality Standard

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`

## Rule Content

### Tone and Style

All generated .md files must use imperative sentences as the primary tone.

- Correct: "You must confirm input completeness after receiving a task"
- Incorrect: "This role should confirm input completeness after receiving a task"
- Incorrect: "It is recommended to confirm input completeness after receiving a task"

### Prohibited Vague Words

The following words are prohibited in .md files unless immediately followed by clear judgment criteria:

Prohibited words: "try to", "appropriately", "reasonably", "if needed", "as appropriate", "roughly", "probably", "things like that"

- Violation: "Try to maintain code quality"
- Correct: "All code must pass linter checks and have test coverage no less than 80%"
- Allowed: "Reasonable error handling (defined as: every public function must have error return with context)"

### Effectiveness And Size Review

Prioritize prompt effectiveness using current official platform/model guidance. Preserve useful XML, examples, task steps, and checks; concision is secondary.

- Agent, skill, and rule targets remain 300, 200, and 100 lines respectively.
- An over-target authored file is `REVIEW_REQUIRED`. Record the current size, concrete usefulness rationale, and evidence in the ordinary worklog or criterion report. The independent reviewer accepts or rejects that current file; an author-only note cannot produce unconditional PASS.
- Move detail to references when task routing preserves its usefulness. Do not delete effective instructions just to meet a number. EC report caps and explicit dispatch limits remain separate and bounded.

### Example Requirements

Every generated .md that contains examples must meet these standards:

- Each authored **skill .md** and **agent .md** contains at least one meaningful rejection/defer/escalation case under `JUDGMENT.md` J5. Add useful positive or contrast examples that clarify behavior or a testable boundary; no universal example count applies.
- Express normal behavior in `## Workflow` and named `## Input and Output` fields; examples may explain how those instructions apply.
- Keep the rejection example concise: identify the triggering input and correct refusal, deferral, or escalation. Include the mistaken action only when it clarifies the boundary; a full before/after transcript is not required.
- Each **rule .md** must contain at least one violation scenario description.

### A Template Outranks Its Own Prose

When a file contains BOTH a policy statement and a template/example block the reader copies, the copied block wins — readers fill the slots they are given, they do not diff them against the prose.

After changing any policy, sweep every template block, frontmatter example, section skeleton, and checklist item that instantiates it. Two sites in the same file can disagree, and the copied one ships. Evidence: `.worklog/202607/context-engineering-realignment/phase-3-execution/decisions.md` D14.

For each policy statement, grep the same file and its writers for a template or example on the same subject and confirm agreement. `scripts/validate-team.sh` cannot detect prose contradictions.

### Structural Over Instructional

When a behavioral constraint can be enforced by prompt structure (dedicated sections, labeled output slots, fixed templates), use structure instead of instructions. Use current model guidance and a concrete task outcome to judge whether the structure helps; do not claim a universal success rate.

- Use dedicated sections (`## Boundaries`, `## Uncertainty Protocol`) instead of inline prohibitions
- Use output templates with labeled slots instead of "output in X format" instructions
- For informational gaps, use `STATUS: NEEDS_CONTEXT` and put `INSUFFICIENT_DATA: {missing}` in `CONCLUSIONS`; for hard blockers, use `STATUS: BLOCKED`

### Tradeoff Disclosure for Rules

When a generated rule's compliance cost is non-obvious, the rule must include a `## Tradeoff` line or section stating what the agent pays to comply. This complements the Exceptions section — Exceptions answer "when can I skip this", Tradeoff answers "what does following this cost".

Tradeoff disclosure is required when any of the following apply:
- Strict compliance adds measurable overhead in simple scenarios (e.g., 3x time for a trivial task)
- Compliance consumes significant context window budget
- The rule conflicts with speed or simplicity in predictable situations

Tradeoff disclosure is not required when the cost is self-evident (e.g., "write a worklog file" obviously costs file I/O time).

Format: one to two sentences after Violation Determination or within Exceptions, starting with "Tradeoff:".

## Violation Determination

- Using descriptive tone instead of imperative sentences → Violation
- Prohibited vague words appear without accompanying judgment criteria → Violation
- An over-target file is marked PASS without independent usefulness review, or useful content is cut only to satisfy length → Violation
- Skill .md or agent .md has no rejection-case example → Violation
- An example contradicts the intended workflow or boundary → Violation
- Agent .md has no Examples section → Violation
- A file's template/example block contradicts a policy stated elsewhere in the same file, or in the rule that file implements → Violation
- Rule .md has no violation determination → Violation
- Behavioral constraint enforced solely by instruction when a structural alternative exists → Violation
- Template or example uses `INSUFFICIENT_DATA` as a status, or defines a status outside the four EC-1 statuses → Violation
- Rule with non-obvious compliance cost has no Tradeoff disclosure → Violation

## Exceptions

This rule has no exceptions.
