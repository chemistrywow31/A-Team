---
name: research-desk
description: Make the current session adopt the research-desk lead and run one sourced-brief cycle.
disable-model-invocation: true
argument-hint: "[decision question and audience]"
---

# Research Desk

Adopt `.grok/agents/research-lead.md` in the current main session. Do not spawn a second lead.

## Workflow

1. Read `AGENTS.md`, `.grok/rules/core.md`, `.grok/policies/execution.md`, and `.grok/policies/supervision.md`.
2. Open or create `.worklog/task-board.json` and record the decision question as a task.
3. Dispatch `source-researcher` and then `brief-editor` as direct specialists. In Grok Build, select their agent files. In a lead-and-helpers deployment, hand `briefs/source-researcher.md` or `briefs/brief-editor.md` plus the task envelope.
4. Update the board and write `.worklog/owner-report.md` when status changes.
5. Deliver `notes/brief.md` only after the editor returns a verdict.

## Examples

Rejected: the user asks this skill to spawn `research-lead` as a child, or to let the researcher hire another researcher. Refuse. The current session is the lead, and specialists do not spawn.
