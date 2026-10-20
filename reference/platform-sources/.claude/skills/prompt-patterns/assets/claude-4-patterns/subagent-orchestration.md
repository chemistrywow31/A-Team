---
name: Subagent Orchestration
category: claude-4-patterns
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - generating-research-agent
  - generating-coding-team
  - writing-agent-prompts
tags: [subagent, orchestration, delegation, overuse, task-tool]
source: raw/claude-4-best-practices.md
---

# Subagent Orchestration

## Behavioral Change

Claude 4.6 has strong native subagent orchestration -- it recognizes when tasks benefit from delegation and spawns subagents proactively without explicit instruction. This is a significant shift from older models that required detailed delegation prompts. The risk is overuse: Claude 4.6 has a strong predilection for subagents and may spawn them when a direct grep, read, or single-file edit is faster.

## Impact on Generated Teams

Coordinator agents in generated teams no longer need verbose delegation instructions. The bigger concern is preventing coordinators from over-delegating simple tasks. Execution agents may also attempt to sub-delegate when they should work directly.

## Recommended Pattern

Add delegation boundaries to coordinator prompts:

```text
Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that do not need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating.
```

Decision matrix for generated coordinator prompts:

| Situation | Delegate | Work Directly |
|-----------|----------|---------------|
| Parallel independent workstreams | Yes | |
| Task needs isolated context (prevents pollution) | Yes | |
| Research across multiple domains | Yes | |
| Single file read or edit | | Yes |
| Grep/search for a specific pattern | | Yes |
| Sequential steps that share state | | Yes |
| Quick validation or check | | Yes |

For execution agents, add explicit non-delegation guidance:

```text
Execute your assigned work directly. Do not delegate subtasks to subagents. Use tools (read, edit, search) yourself.
```

## Anti-Patterns to Avoid

- Detailed delegation instructions in coordinator prompts -- 4.6 orchestrates natively, verbose instructions waste context
- No delegation boundaries at all -- leads to subagent spawning for trivial grep calls
- Execution agents spawning subagents for their own subtasks -- creates unnecessary nesting
- Assuming subagent overhead is free -- each subagent consumes a fresh context window and adds latency
