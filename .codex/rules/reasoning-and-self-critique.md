---
name: Reasoning And Self Critique
description: Require concise decision notes and verification gates before agent outputs are accepted
---

# Reasoning And Self Critique

## Applicability

- Applies to: generated agents, A-Team specialists, and prompts that produce artifacts or decisions

## Rule Content

### Use A Preflight Gate

Before execution, record a concise preflight note in the task return or worklog. Do not expose private chain-of-thought. Use this structure:

```markdown
## Preflight
### Knowns
- {confirmed inputs}
### Unknowns
- {missing data or assumptions}
### Plan
- {chosen approach}
### Risks
- {failure modes and falsification conditions}
```

### Use A Verification Gate

Before submission, verify the draft with this structure:

```markdown
## Verification
### Evidence Check
- {claims trace to sources, files, or worklog}
### Position Check
- {recommendations are explicit and justified}
### Counterexample Check
- {strongest objection addressed}
### Completeness Check
- {all requested scope covered}
### Failure Mode Check
- {likely break point identified or fixed}
```

### Coordinator Pre-Dispatch Note

Before delegating, coordinators must note:

- what this dispatch must achieve
- why this specialist is the correct owner
- what paths and inputs are ready
- what failure modes will be checked on return

### Escalate Known Gaps

If verification exposes a gap that cannot be fixed after three attempts, return `INSUFFICIENT_DATA` or `BLOCKED` instead of submitting known-bad output.

## Violation Determination

- artifact-producing agent has no preflight or verification gate in its instructions -> Violation
- coordinator has no pre-dispatch note requirement -> Violation
- agent exposes private chain-of-thought instead of concise decision notes -> Violation
- output is submitted after verification identifies an unresolved blocker -> Violation

## Exceptions

Deterministic Tier 1 utilities may replace Preflight and Verification with `Format Check` and `Input Coverage Check` when their task has no judgment calls.
