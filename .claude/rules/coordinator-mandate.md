---
name: Coordinator Mandate
description: Mandatory rule that every generated team must have a coordinator role
---

# Coordinator Mandate

## Applicability

- Applies to: All agents (all members of the design team must understand and follow this rule)

## Rule Content

### Coordinator Must Exist

Every generated team structure must contain at least one coordinator role. The coordinator's .md file is placed at the root level of the `agents/` directory (not inside subfolders).

### Coordinator Does Not Execute

The coordinator role is only responsible for: task planning, task assignment, progress tracking, quality control. The coordinator must not simultaneously undertake execution responsibilities of other agents in the team.

Two carve-outs, both narrow and both declared here rather than assumed:

1. **User-facing conversation** — interviewing, relaying questions, presenting results. This is coordination, not execution (`rules/context-management.md` Exceptions). Only the main session has a user channel, so it cannot be delegated.
2. **The team charter (`CLAUDE.md`)** — the coordinator is the only role holding the full cross-phase picture the charter must summarize. It writes this one file directly.

Everything else the coordinator might be tempted to write itself — agent files, skill files (including the team's entry-point skill), rule files, `settings.json` — goes to the owning writer via dispatch. The reason is mechanical, not stylistic: a self-assigned step produces no dispatch record, no EC-1 report, and no producer to bounce a failure back to, so a verification FAIL on it routes to nobody. Production evidence: `skills/boss/SKILL.md` was self-assigned to the coordinator and is absent from 11 teams generated after the step was introduced.

A carve-out file still requires fresh-context verification per `rules/execution-contract.md` EC-3 — writing it directly changes who produces it, never who accepts it.

### Flat Architecture

Every team must use a flat architecture: one coordinator directly manages all worker agents. Sub-coordinators are prohibited because they add context relay overhead and degrade information quality in Claude Code's Task tool.

### Worktree Isolation for File-Mutating Agents

When the coordinator dispatches an agent that will modify files (Edit, Write, Bash that touches the working tree), evaluate whether to use `isolation: "worktree"` in the Agent tool parameters. Worktree isolation creates a fresh git worktree for the agent, sandboxing its writes from the main working tree.

**Use worktree isolation when**:
- The agent runs experimental changes that may need to be discarded
- Multiple agents need to modify the same files in parallel without conflict
- The agent's work crosses a major refactor boundary that may need rollback
- A code review agent rewrites code in place to demonstrate suggestions

**Do not use worktree isolation when**:
- The agent's output is the worklog or a single new file (no existing-file mutation)
- The agent must observe the latest user changes in the main worktree
- The agent's work is small and atomic (single function edit) — overhead exceeds benefit
- The team is in Agent Teams mode (worktree isolation interacts unpredictably with shared task lists)

After a worktree-isolated agent completes, the coordinator must decide: merge (cherry-pick or rebase the worktree's commits), discard, or hand off to a review agent before merging. The decision must be logged in `decisions.md` with rationale.

## Violation Determination

- Generated team structure has no coordinator .md file in `agents/` root directory → Violation
- Coordinator's .md assigns itself the production of any file ANYWHERE in the file (not only in a "Responsibilities" section) beyond the two declared carve-outs → Violation. Check: grep the coordinator .md for self-authoring phrases (`you write this directly`, `write ... yourself`, `you generate`) and confirm each hit targets `CLAUDE.md` or a user-facing conversation step.
- Team contains a sub-coordinator agent whose sole purpose is to coordinate other agents → Violation
- Coordinator dispatches a file-mutating agent without considering worktree isolation (and the choice is not documented in worklog) → Violation
- Coordinator merges a worktree-isolated agent's changes without logging the merge decision → Violation

## Exceptions

This rule has no exceptions.
