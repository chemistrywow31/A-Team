---
name: Supervision
description: Keep the research-desk task board and owner report current
---

# Supervision

## Applicability

Applies to `research-lead`. Specialists return EC-1 results and do not edit the board.

## Rule Content

Update `.worklog/task-board.json` when a task is created, dispatched, blocked, returned, or finished. The file matches `docs/task-board.schema.json`. Validate a live board with `python scripts/validate_grok_team.py --board <path>` from the A-Team repository. Team validation does not read gitignored `.worklog/`.

Each task uses status `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`.

- `DONE` and `DONE_WITH_CONCERNS` set `finished_at`.
- `BLOCKED` and `NEEDS_CONTEXT` leave `finished_at` null and name every gap in `blockers`.
- Set `human_decision_needed` to true only when a person must choose.
- Leave `cost` and `tokens` null or omit them unless the host reported those numbers. Do not estimate them.

When a specialist is not started from its agent file, pass `briefs/<role>.md` and a task envelope. The envelope names the task id, goal, owned paths, forbidden paths, acceptance criteria, inputs, and deadline when one exists. The specialist starts with no conversation history, returns one result, and does not spawn or message peers or the user.

After each board update, write `.worklog/owner-report.md` with these lines, in order:

- Team:
- Board:
- Updated:
- Needs human:
- Blocked:
- Needs context:
- Done:
- Next:

Write none on a status line that has no tasks. Next is one recommendation.

## Violation Determination

- The lead changes task status without updating the board row -> Violation.
- The owner report omits a required line -> Violation.
- A recorded cost or token figure was not reported by the host -> Violation.

## Exceptions

A task that stays in the main session still gets one board row.

Tradeoff: The lead writes one JSON row and eight report lines at each status change.
