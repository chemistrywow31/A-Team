---
name: Context Management
description: Keep Codex multi-agent work isolated, resumable, and summary-driven
---

# Context Management

## Applicability

- Applies to: `team-architect` and every generated `multi-agent` coordinator or specialist

## Rule Content

### Dispatch With Paths, Not Dumps

When spawning a specialist, include:

1. the current worklog path
2. upstream worklog paths the specialist must read
3. the narrow task scope
4. owned write paths and read-only reference paths
5. expected completion contract

Do not paste full upstream documents into the dispatch when the files are available locally.

### Use Codex Delegation Semantics

Use `spawn_agent` for bounded independent work, `send_input` for follow-up instructions, and `wait` only when the next coordinator step is blocked on a result. Do not use Claude-only terms such as `Task tool`, `Agent tool`, or `context: fork` in generated Codex teams.

### Return Structured Summaries

Every specialist must end with one status:

- `DONE`: task completed
- `DONE_WITH_CONCERNS`: task completed with issues the coordinator must evaluate
- `BLOCKED`: task cannot continue without a specific action or information
- `NEEDS_CONTEXT`: task lacks required input

Return only the summary, decisions, changed files, worklog paths, and blockers. Put long findings in the worklog.

### Split Noisy Work

Delegate codebase exploration, web research, broad audits, and verbose test runs to specialists when the work can run without blocking the coordinator's immediate next step.

### Resume From Worklog

After interruption or compaction, restore state by reading the latest phase `decisions.md`, then `findings.md`, then pending audit notes.

## Violation Determination

- spawned specialist receives no worklog path for phase work -> Violation
- dispatch includes full upstream documents when paths would suffice -> Violation
- generated Codex team uses Claude-only `Task tool` or `Agent tool` terminology -> Violation
- specialist returns an unstructured long narrative instead of a status summary -> Violation
- coordinator waits on a non-blocking specialist instead of doing independent work -> Violation

## Exceptions

Inline execution is allowed for small coordinator tasks that create fixed runtime scaffolding, such as `AGENTS.md`, `.codex/config.toml`, or mapping manifests.
