---
name: Supervision
description: Keep one task board, one owner report, and one portable brief per role
---

# Supervision

## Applicability

- Applies to every generated team's coordinator and to A-Team when it coordinates work.
- Specialists read the return format in their brief or agent contract. They do not edit the board unless the dispatch assigns that file.

## Rule Content

### Two Ways To Run The Same Team

Grok Build sessions load flat `.grok/agents/*.md`, root `AGENTS.md`, and `.grok/rules/`. That layout stays the native surface.

A lead-and-helpers deployment uses the same roles without relying on agent-file discovery. The lead gives one direct specialist `briefs/<role>.md` plus a task envelope. The specialist starts with no conversation history, returns one result to the lead, and stops. Briefs live outside `.grok/agents/` because they are assignments, not agent definitions. `scripts/render_helper_briefs.py` renders them from Identity, Responsibilities, Input and Output, Workflow, Boundaries, and Completion Contract. Regenerate briefs after those sections change. Do not hand-edit them.

Those six sections must be enough to do the role. Startup lists of other policy files stay in the agent file for native sessions. Put any limit the helper must obey inside Boundaries or the brief preamble.

The task envelope names the task id, goal, owned paths, forbidden paths, acceptance criteria, inputs, and deadline when one exists. The lead attaches the brief. The helper does not spawn further helpers, does not message other helpers, and does not message the user. `disallowedTools: [Task]` is the source-backed directive when a Grok client loads the agent file. The brief repeats the limit because a helper started from the brief is not selected through that file. Neither the brief nor this policy proves the host enforced the limit. Report that observation as UNVERIFIED until a session shows it.

### Task Board

The coordinator keeps `.worklog/task-board.json` current when a task is created, dispatched, blocked, returned, or finished. The tracked contract is `schemas/task-board.schema.json`. Generated teams copy it to `docs/task-board.schema.json`. `.worklog/` is runtime state and stays gitignored. Team validation does not read `.worklog/`. Check a live board with `python scripts/validate_grok_team.py --board <path>`.

Each task records `id`, `owner_role`, `phase`, `status`, `blockers`, `human_decision_needed`, `artifacts`, `started_at`, and `finished_at`. Status is exactly `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`.

- `DONE` and `DONE_WITH_CONCERNS` set `finished_at`.
- `BLOCKED` and `NEEDS_CONTEXT` leave `finished_at` null and name every gap in `blockers`.
- Set `human_decision_needed` to true only when a person must choose. A missing input the lead can attach is `NEEDS_CONTEXT` with `human_decision_needed` false.
- `deadline`, `cost`, and `tokens` are optional. Leave `cost` and `tokens` null or omit them unless the host reported those numbers. Do not estimate them.
- Timestamps use UTC `YYYY-MM-DDTHH:MM:SSZ`. A deadline may be that form or `YYYY-MM-DD`.

One row per task id. Update the row in place. The phase narrative under `.grok/policies/worklog.md` does not replace the board.

### Owner Report

After updating the board, the coordinator writes `.worklog/owner-report.md` for the person or assistant supervising this team. Use these lines, in this order, each with a value:

- Team:
- Board: `.worklog/task-board.json`
- Updated:
- Needs human:
- Blocked:
- Needs context:
- Done:
- Next:

Write `none` when a status line has no tasks. `Next` is one recommendation. A tracked sample may live at `docs/owner-report.example.md`. Do not paste specialist transcripts into the report.

## Violation Determination

- A role with `## Identity` lacks a required brief section, or `briefs/<role>.md` differs from the renderer -> Violation.
- The coordinator finishes a status change without updating the board row, or records a cost or token figure the host did not report -> Violation.
- A helper spawned from a brief spawns another helper, messages a peer, or messages the user -> Violation.
- The owner report omits a required line or uses a status outside the four board statuses -> Violation.

## Exceptions

A single-agent target with no specialists still keeps one board row for the active task and may omit `briefs/` only when it has no `.grok/agents/` role to render. A-Team's designer roles are rendered anyway so the same briefs can be handed to direct specialists.

Tradeoff: The coordinator writes the board and a short owner report at each status change. That is one JSON row and eight report lines, including tasks that never leave the main session.
