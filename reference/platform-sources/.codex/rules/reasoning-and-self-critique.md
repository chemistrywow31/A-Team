---
name: Reasoning and Self-Critique
description: Require compact role-specific decision and verification instructions around every agent workflow
---

# Reasoning and Self-Critique

## Applicability

- Applies to: A-Team specialists, coordinators, and generated agents that produce artifacts or decisions
- Include this rule or an equivalent in every generated team's canonical rule family and requested runtime projections.

## Rule Content

### One Agent Contract

Keep these adjacent sections in every agent, in this order:

```markdown
## Reasoning
- Establish the task's material inputs, assumptions, authority, and chosen approach.
## Workflow
- Execute the role's assigned work.
## Self-Critique
- Check the actual output against its acceptance criteria and likely failure points.
```

Specialize the bullets for the role. Use the skeleton above and preserve the exact headers required by `JUDGMENT.md` J5.1. Keep the contract once; do not add duplicate `## Preflight` or `## Verification` blocks or require four reasoning slots and five critique slots.

These sections instruct the agent; they are not forms to reproduce in each return. Report only concise decisions, material assumptions, unresolved gaps, and verification evidence in the existing EC-1 fields or worklog. Do not request or expose private reasoning transcripts.

### Before Delegation

In the coordinator's existing Reasoning/Workflow contract, define the dispatch outcome, correct owner, ready inputs, exact owned and forbidden paths, and acceptance criteria. Do not add a second pre-dispatch form. Delegate only bounded work that can proceed independently alongside useful coordinator work; preserve runtime and shared-filesystem controls.

### Verify Before Submission

The producer checks its own output before every artifact or decision handoff. Check task coverage, evidence, authority and ownership, and realistic failure modes relevant to that role. Independent acceptance under `.codex/rules/execution-contract.md` EC-3 remains required and does not replace this check.

After a correction, invalidate and rerun every criterion citing a changed file, plus dependent mapping and parity checks. Recheck other criteria when new evidence affects them. Never carry forward a stale same-file PASS or rerun an unrelated generic checklist by default.

### Resolve Known Gaps

Fix gaps within the EC-2 attempt bound; do not submit known-flawed output as DONE. For missing information, use `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {items}` in `CONCLUSIONS`. For a hard blocker, use `STATUS: BLOCKED`. Preserve all four EC-1 statuses; the insufficient-data marker is not a status.

## Violation Determination

- An agent omits or reorders Reasoning, Workflow, or Self-Critique, or separates them with unrelated sections -> Violation
- An agent duplicates the contract with mandatory Preflight/Verification forms or fixed four/five slots -> Violation
- Generic skeleton bullets replace role-specific decision and verification checks -> Violation
- A prompt requests private reasoning transcripts, or the producer submits without checking its output -> Violation
- A correction retains PASS for a criterion citing a changed file or omits dependent mapping/parity rechecks -> Violation
- A generated team omits this rule or an equivalent from a requested runtime -> Violation
- A return uses an invalid EC-1 status or conceals an unresolved blocker -> Violation

## Exceptions

- Deterministic Tier 1 utilities may reduce the section content to input validity, format, and input coverage; retain all three J5.1 headers and document why the task has no judgment calls.
- A clarification-only conversation turn does not require an artifact verification pass. Requirements summaries and other artifacts still require it.
