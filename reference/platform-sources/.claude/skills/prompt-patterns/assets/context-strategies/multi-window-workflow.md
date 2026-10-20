---
name: Multi-Window Workflow
category: context-strategies
applies_when:
  - long-running-tasks
  - generating-coding-team
  - context-constrained
tags: [multi-window, state-management, fresh-context, git, setup-scripts]
historical-source: raw/context-engineering-blog.md
source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
reviewed: 2026-10-06
---

# Multi-Window Workflow

## Core Principle

For work that spans context windows, preserve enough state to resume and verify what changed. Reuse the project's existing workflow before adding setup scripts or tracking files.

## Initial Work

1. Identify the existing entrypoints, test commands, worklog, and current state.
2. Record the objective, boundaries, completed work, unresolved decisions, and next step.
3. Add a setup script, structured test record, or checkpoint only when the task needs repeatable recovery and owns that artifact.

`init.sh`, `tests.json`, and `progress.txt` are possible names, not required output files. Git commits are optional checkpoints only when authorized; do not introduce a commit requirement through a prompt pattern.

## Resume

Read the recorded state and inspect the current files or git diff before changing anything. Reuse a safe existing setup command if the environment needs restoration. Continue from the next unresolved item rather than restarting completed work or assuming the summary is current.

Fresh context is useful when durable artifacts capture the state. Compaction can preserve conversational nuance. Select the host-supported method; neither guarantees complete retention or extends an explicit resource limit.

## Verification Continuity

Keep current evidence for unchanged criteria. After a correction, recheck the affected files and dependent mapping/parity. Never weaken a test merely to produce green output. A test proven obsolete or incorrect may be corrected within authorized scope, with its requirement evidence and the changed behavior reviewed under the existing contract.

## Examples

### Authorized Test Repair

A test expects a deprecated config field, while the selected client's documented schema and actual parser reject that field. Record the evidence, correct the test and implementation within their owners' scope, and retain coverage of the intended behavior.

### Rejection Case

Reject deleting a failing assertion solely because the new implementation violates it. Fix the behavior or demonstrate a real requirement conflict through the existing escalation path.

## Sources And Attribution

A-Team-authored continuation and test-repair workflow, informed by [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked 2026-10-06. Example state files and checkpoints are conditional techniques, not mandatory scaffolding.
