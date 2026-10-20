---
name: Parallel Tool Calls
category: templates
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - generating-coding-team
  - long-running-tasks
tags: [performance, parallel, tool-use, efficiency]
source: raw/claude-4-best-practices.md
---

# Parallel Tool Calls

## When to Use

Inject into any agent that makes multiple tool calls per turn -- coordinators dispatching parallel tasks, coding agents reading multiple files, or agents running independent operations.

## Template

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

## Adaptation Notes

Use as-is for most agents. Especially high-value for coordinators and coding agents that frequently read multiple files or run independent checks.
