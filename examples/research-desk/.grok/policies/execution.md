---
name: Execution
description: Bind specialist returns to the four statuses and six report fields
---

# Execution

## Applicability

Applies to the lead and both specialists.

## Rule Content

Return these fields, in this order:

STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
CONCLUSIONS:
EVIDENCE:
ARTIFACTS:
RISKS/UNKNOWNS:
NEXT:

- STATUS is one of those four tokens.
- CONCLUSIONS states whether the acceptance criteria are met, partially met, or not met.
- DONE and DONE_WITH_CONCERNS require nonempty EVIDENCE naming a file or a command.
- RISKS/UNKNOWNS says none when there are no risks.
- NEXT names one recommendation.
- Do not include a private reasoning transcript.

The producer does not accept its own artifact. The lead is not the sole acceptor of the brief. The editor's verdict is the independent check for this three-role team.

## Violation Determination

- A return omits a field, reorders the fields, or uses a status outside the four tokens -> Violation.
- A DONE return has empty EVIDENCE -> Violation.

## Exceptions

A question from the user to the lead is not a specialist return. The lead still records that exchange on the task board when it changes task status.
