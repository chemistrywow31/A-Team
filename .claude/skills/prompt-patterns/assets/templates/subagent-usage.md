---
name: Subagent Usage
category: templates
applies_when:
  - generating-coordinator
  - long-running-tasks
  - context-constrained
tags: [subagent, delegation, orchestration, task-isolation]
source: raw/claude-4-best-practices.md
---

# Subagent Usage

## When to Use

Inject into coordinators or any agent with access to the Task tool to prevent excessive subagent spawning for trivial operations.

## Template

```text
Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating.
```

## Adaptation Notes

For teams using subagent mode, this block goes into the coordinator prompt. Adjust the threshold for "simple tasks" based on the team's typical workload. For teams with strict coordinator-mandate (no inline execution), soften the "work directly" guidance to "dispatch as a single focused task" instead.
