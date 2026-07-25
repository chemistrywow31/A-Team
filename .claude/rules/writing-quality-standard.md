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

### Length Limits

- Single agent .md: No more than 300 lines
- Single skill .md: No more than 200 lines
- Single rule .md: No more than 100 lines
- If content exceeds limits, must split into multiple files or use references for detailed content

### Example Requirements

Every generated .md that contains examples must meet these standards:

- Each **skill .md** and each **agent .md** must contain exactly one worked example: the **rejection case** — the input the agent must refuse, defer, or escalate on, demonstrating the Uncertainty Protocol. One is the floor and the ceiling unless the dispatch asks for more.
- Do NOT write normal-case or edge-case examples. Examples constrain the model to the exploration space they demonstrate; for normal operation an expressive interface does the job better and costs less. Express the normal path as an enumerated trigger list in `## Uncertainty Protocol` and as named, typed slots in `## Input and Output`, not as a worked scenario.
- The rejection case is the exception because it carries information no enumeration conveys: *when not to act*. A parameter type cannot express a refusal boundary; a concrete failing input can.
- Each **rule .md** must contain at least one violation scenario description.

### A Template Outranks Its Own Prose

When a file contains BOTH a policy statement and a template/example block the reader copies, the
copied block wins — readers fill the slots they are given, they do not diff them against the prose.

So: after changing any policy, sweep every template block, frontmatter example, section skeleton,
and checklist item that instantiates it — not just the paragraph that states it. Two sites in the
SAME FILE can disagree, and the copied one is what ships. Measured three times in one pass on
2026-07-25 (trace: `.worklog/202607/context-engineering-realignment/phase-3-execution/decisions.md` D14).

Compliance check: for each policy statement, grep the same file and its writers for a template block
or example on the same subject, and confirm the two agree. `scripts/validate-team.sh` cannot catch
this — the disagreement is between two prose artifacts, so it is a review obligation.

### Structural Over Instructional

When a behavioral constraint can be enforced by prompt structure (dedicated sections, labeled output slots, fixed templates), use structure instead of instructions. Claude reliably follows structural boundaries but frequently ignores negative instructions like "do not X".

- Use dedicated sections (`## Boundaries`, `## Uncertainty Protocol`) instead of inline prohibitions
- Use output templates with labeled slots instead of "output in X format" instructions
- Use escape hatch phrases (`INSUFFICIENT_DATA`, `BLOCKED`) instead of "don't guess"

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
- File exceeds length limit → Violation
- Skill .md or agent .md has no rejection-case example → Violation
- Skill .md or agent .md carries normal-case or edge-case examples not requested by the dispatch → Violation
- Agent .md has no Examples section → Violation
- A file's template/example block contradicts a policy stated elsewhere in the same file, or in the rule that file implements → Violation
- Rule .md has no violation determination → Violation
- Behavioral constraint enforced solely by instruction when a structural alternative exists → Violation
- Rule with non-obvious compliance cost has no Tradeoff disclosure → Violation

## Exceptions

This rule has no exceptions.
