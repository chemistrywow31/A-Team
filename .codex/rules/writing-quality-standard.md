---
name: Writing Quality Standard
description: Keep authored Codex markdown effective, testable, and consistent with J5 artifact floors
---

# Writing Quality Standard

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`

## Rule Content

### Write For The Selected Model

Use the current official guidance for the model the file targets; do not carry advice written for one provider's models into another's prompts. Claude-target files follow `.claude/rules/writing-quality-standard.md`. For every target, judge a passage by whether the reader would behave differently without it: give each instruction one home, state the reason behind a constraint, and replace a vague phrase with an observable criterion where the vagueness would change the result.

### Do Not Carry A-Team's Contract Into A Team

A-Team's execution contract, worklog triad, section floors, and `JUDGMENT.md` describe how A-Team builds teams. A generated team gets its own files, sized by its work-shape profile (`.codex/rules/output-structure.md`): a group writes its own short handoff contract, and a rule exists only because one of the team's flows needs it.

### Review Size For Effectiveness

- Authored agent, skill, and rule targets remain 300, 200, and 100 lines respectively under J5.
- An over-target file is `REVIEW_REQUIRED`. Record its current size, concrete usefulness rationale, and evidence in the ordinary worklog or criterion report; the independent reviewer accepts or rejects that file. An author-only marker cannot produce unconditional PASS.
- Move detail that is needed only sometimes to references named at the point of use. Length is not the measure either way: keep what changes behavior and cut what does not.
- Keep runtime TOMLs thin, with an authoritative-playbook bootstrap; the existing 260-line runtime-config/block limit and EC/dispatch report caps remain separately bounded.

### Use Examples That Clarify Behavior

State the contract first: named inputs and outputs, a file format, a small set of statuses. Add an example only when it shows something the contract cannot, and keep it concise. No example is mandatory in an agent or skill of a team with a work-shape record.

### Align Copied Templates With Policy

After a policy change, check the templates, frontmatter examples, section skeletons, and checklists that instantiate it, including writer references. Correct contradictory copied blocks; structural validators alone cannot establish prose consistency.

### Make Behavior Observable

Use typed outputs for handoffs and say what each agent does when input is missing. No section is mandatory in a generated agent; when Reasoning/Workflow/Self-Critique sections are used, write them once and make them specific to the role. Use `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {missing}` in CONCLUSIONS for information gaps and `STATUS: BLOCKED` for hard blockers; preserve the four EC-1 statuses.

### Disclose Non-Obvious Rule Cost

When a rule adds measurable simple-task overhead, significant context cost, or a predictable speed/simplicity conflict, include one or two sentences beginning `Tradeoff:` after Violation Determination or within Exceptions. Self-evident file I/O cost needs no extra disclosure.

## Violation Determination

- Descriptive prose replaces instructions, or vague wording lacks observable criteria -> Violation
- An over-target authored file is accepted without independent usefulness review, or an explicit runtime/dispatch cap is exceeded -> Violation
- A generated file copies A-Team's rule pack or section skeleton when no flow of the team needs it, or an example contradicts required behavior -> Violation
- An instruction has more than one home, or two instructions in one team conflict -> Violation
- A copied template, example, or checklist contradicts the policy it implements -> Violation
- A rule with a non-obvious cost lacks its disclosure -> Violation
- An informational gap uses an invalid EC-1 status, or a prompt duplicates the decision/verification contract -> Violation

## Exceptions

- Teams generated before 2026-11-26 without a work-shape record keep the section and example floors the validator applies to them.
- Safety rules stay absolute: no secrets in files, no merge, push, deploy or deletion without an explicit yes.
