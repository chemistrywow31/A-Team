---
name: Context Management
description: Mandatory context isolation and offloading rules to prevent context bloat in multi-agent workflows
---

# Context Management

## Applicability

- Applies to: All agents (coordinator has additional responsibilities)

## Rule Content

### Coordinator Must Include Worklog Paths in Task Dispatch

When the coordinator dispatches a task to any agent via the Task tool, the dispatch must include:

1. **Current worklog path**: The directory where this agent must write its outputs (e.g., `.worklog/202603/english-teaching-team/phase-2-planning/`)
2. **Upstream reference paths**: Paths to relevant upstream phase worklogs that this agent must read for context (e.g., `.worklog/202603/english-teaching-team/phase-1-discovery/decisions.md`)
3. **Task scope summary**: A concise description of what this specific task must accomplish (not the entire project context)
4. **Acceptance criteria**: 1–5 mechanically checkable conditions the deliverable must meet — a fresh-context verifier checks exactly these per `rules/execution-contract.md` EC-3
5. **Scope fence**: an explicit OUT list — files and directories this agent must not touch
6. **BRIEF path**: the task's `.worklog/{yyyymm}/{task-name}/brief.md` per EC-5.1

Before any dispatch, read the matching delegation template in `templates/` (search / implementation / refactoring / research / review) and fill every slot. The coordinator must not pass full upstream content inline. Pass paths; let the agent read what it needs.

### XML Tag Separation in Dispatch

When the coordinator must include variable data in a Task dispatch (task scope, user requirements, small inline context), wrap each variable block in descriptive XML tags. This prevents Claude from confusing data content with dispatch instructions:

```
<task_scope>Write the rule file for test coverage requirements.</task_scope>
<upstream_decisions>Phase 1 decided: minimum 80% coverage, integration tests required.</upstream_decisions>
<worklog_path>.worklog/202603/team-name/phase-3-generation/</worklog_path>
```

Instructions remain outside the tags. Data goes inside.

### Agent Return Format

Every task return follows the six-field report schema in `rules/execution-contract.md` EC-1: `STATUS` / `CONCLUSIONS` (max 10 lines) / `EVIDENCE` (file:line) / `ARTIFACTS` (paths, including worklog files) / `RISKS/UNKNOWNS` / `NEXT` — max 40 lines total; any product over 30 lines goes to a file with the path in ARTIFACTS (EC-1.3). Agents must not return full file contents, complete research dumps, or unstructured narratives. The worklog contains the detail; the return contains the summary. A malformed return bounces once with the schema attached; the second violation counts as a failed attempt (EC-1.6).

### Completion Status Protocol

Every agent must end its task with exactly one of these statuses:

- **DONE** — All steps completed successfully. Evidence of completion provided.
- **DONE_WITH_CONCERNS** — Task completed, but issues exist that the coordinator must be aware of. List each concern with severity and recommended action.
- **BLOCKED** — Cannot proceed. State what was attempted (up to 3 attempts), what failed, and what specific information or action is needed to unblock. Do not retry the same approach more than 3 times.
- **NEEDS_CONTEXT** — Missing information required to begin or continue. List each missing item and where it might be found.

The coordinator handles each status per `rules/execution-contract.md` EC-1.5. Accepting DONE additionally requires the fresh-context verification in EC-3 — the producer's own claim never counts as acceptance. When the missing context in NEEDS_CONTEXT is user input (a QUESTIONS block), the coordinator relays the questions to the user, appends the exchange to the task's `dialogue-log.md`, and re-dispatches with the answers.

### Task Isolation via Subagents

Every independent unit of work must be executed as a separate Task (subagent). This ensures natural context isolation:
- Each Task starts with a fresh context window
- The coordinator's context accumulates only summaries, not execution details
- Parallel tasks cannot pollute each other's context

The coordinator must not perform execution work inline (per `rules/coordinator-mandate.md`). All execution goes through Task dispatch.

### Phase-End Archival

At the end of each phase, the coordinator must:

1. Verify the phase worklog is complete (all three core files present and populated)
2. Write a phase completion summary to the coordinator's own tracking (not to the worklog)
3. Release all phase-specific context — subsequent phases read from worklog, not from memory

### Worklog-Based Context Recovery

When work is interrupted or context must be reset:
1. Read the latest phase worklog to restore context
2. Read `decisions.md` from all completed phases for the decision chain
3. Resume from the last completed phase boundary

This enables any agent (or a new session) to pick up work without the original context.

### Context Budget Awareness

Since agents cannot directly measure context window usage, use these proxy indicators:

- **Task count proxy**: After dispatching 5 or more sequential tasks within a single phase, the coordinator must pause and write an interim summary to the worklog before continuing
- **Conversation round proxy**: If an agent's work requires more than 10 back-and-forth exchanges with the coordinator, the agent must summarize progress to the worklog and the coordinator must consider splitting the remaining work into a new Task
- **Output size proxy**: If an agent's response exceeds 3000 words, it must be split — summary returned to coordinator, full content written to worklog

## Violation Determination

- Coordinator dispatches a Task without the worklog path, acceptance criteria, or scope fence → Violation
- Coordinator dispatches a Task with full upstream content inline instead of passing worklog paths → Violation
- Agent returns raw unstructured output exceeding 500 words without worklog reference → Violation
- Coordinator performs execution work inline instead of dispatching a Task → Violation
- Phase transition occurs without phase-end archival verification → Violation

## Exceptions

- During Phase 1 Discovery, the coordinator may participate in user-facing conversation directly (this is coordination, not execution)
- Ad-hoc investigation requests to Domain Researcher may include inline context when the context is too small to justify a worklog write (under 200 words)
