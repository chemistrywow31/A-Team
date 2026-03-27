---
name: Writing Quality Standard
description: Specify writing style, language requirements, and quality standards for all generated .md files
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

- Each **skill .md** must contain at least three examples: normal case, edge case, and rejection/failure case. Happy-path-only examples cause Claude to produce plausible output on invalid input.
- Each **agent .md** must contain an Examples section with at least three cases: normal, edge, and rejection (demonstrating the Uncertainty Protocol).
- Each **rule .md** must contain at least one violation scenario description.

### Structural Over Instructional

When a behavioral constraint can be enforced by prompt structure (dedicated sections, labeled output slots, fixed templates), use structure instead of instructions. Claude reliably follows structural boundaries but frequently ignores negative instructions like "do not X".

- Use dedicated sections (`## Boundaries`, `## Uncertainty Protocol`) instead of inline prohibitions
- Use output templates with labeled slots instead of "output in X format" instructions
- Use escape hatch phrases (`INSUFFICIENT_DATA`, `BLOCKED`) instead of "don't guess"

## Violation Determination

- Using descriptive tone instead of imperative sentences → Violation
- Prohibited vague words appear without accompanying judgment criteria → Violation
- File exceeds length limit → Violation
- Skill .md has fewer than three examples (normal, edge, rejection) → Violation
- Agent .md has no Examples section or fewer than three cases → Violation
- Rule .md has no violation determination → Violation
- Behavioral constraint enforced solely by instruction when a structural alternative exists → Violation

## Exceptions

This rule has no exceptions.
