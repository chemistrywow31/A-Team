---
name: Context Management
description: Keep multi-agent work path-driven, minimally scoped, and resumable in Claude subagent mode without replaying whole conversations
---

# Context Management

## Applicability

- Applies to: all agents; the coordinator owns dispatch shape and resume discipline

## Rule Content

### Dispatch By Task Path And File Paths

- Every delegation dispatch must include:
  1. the stable task path
  2. the current worklog path
  3. upstream reference paths the agent must read
  4. the narrow task scope
  5. owned write paths and forbidden paths
  6. acceptance criteria
  7. the BRIEF path from `rules/execution-contract.md` EC-5.1 when one exists

Pass paths, not document dumps. The dispatched agent reads the files itself.

### Pass The Smallest Effective Context

- Default to a fresh Task dispatch plus file paths.
- Inline only the smallest extra context the specialist needs when that context is not already captured in files.
- If the coordinator uses a non-default model or other runtime override, state the override in the dispatch rather than assuming the specialist infers it from prior conversation.

### Re-Dispatch With Deltas, Not Replays

- A corrective or resumed Task on an existing task path carries only what changed: new evidence, invalidated assumptions, updated acceptance criteria, or path changes.
- Do not resend the whole conversation or the whole worklog unless the prior task failed to capture required context in files.

### Corrections Happen Between Task Runs

- Specialists report `BLOCKED` or `NEEDS_CONTEXT` when work is unsafe, invalidated, or missing required input.
- The coordinator corrects direction by issuing a new Task dispatch after the current specialist return, not by layering hidden side-channel instructions into an active run.
- When user input is required, the specialist ends with `NEEDS_CONTEXT` and a QUESTIONS block. The coordinator relays the questions, appends the exchange to `dialogue-log.md`, and re-dispatches with the answers.

### Resume From Worklog

After interruption or compaction, restore state from:

1. the task BRIEF
2. the current phase `decisions.md`
3. the latest relevant `findings.md`
4. pending verifier or audit notes, if any

## Violation Determination

- A dispatch omits the stable task path, worklog path, owned paths, forbidden paths, acceptance criteria, or BRIEF path when one exists -> Violation
- A dispatch pastes upstream documents inline when file paths would suffice -> Violation
- A corrective or resumed Task replays unchanged full context instead of passing the delta -> Violation
- A specialist attempts to rely on an undeclared side-channel correction instead of a new Task dispatch -> Violation
- A resumed task skips the worklog recovery order above and proceeds from memory alone -> Violation

## Exceptions

- Phase 1 user conversation is coordination, not delegated execution.
- Inline context under 200 words is allowed for a micro-dispatch when no useful file path exists yet.
