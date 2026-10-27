---
name: Worklog
description: Separate the task board from phase notes that record a decision
---

# Worklog

## Applicability

Applies to the lead. Specialists write only the artifact paths named in the dispatch.

## Rule Content

Operational tasks update `.worklog/task-board.json` under `.grok/policies/supervision.md`. That board is the status record.

When a decision changes roles, acceptance criteria, or sources the team will trust, also write:

```
.worklog/{yyyymm}/{task-name}/phase-{n}-{label}/
  references.md
  findings.md
  decisions.md
```

Each decision names the finding or reference it uses. A mechanical edit that decides nothing does not open a new phase folder.

## Violation Determination

- A decision that changes the team has no phase folder, or `decisions.md` cites no finding or reference -> Violation.
- Phase notes are treated as a substitute for the task board -> Violation.

## Exceptions

A task that only collects a user answer and makes no design choice records the answer on the board and may leave `decisions.md` as the sentence "No decisions made in this phase."
