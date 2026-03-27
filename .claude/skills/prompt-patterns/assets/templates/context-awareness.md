---
name: Context Awareness
category: templates
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - long-running-tasks
  - context-constrained
tags: [context-window, compaction, persistence, autonomy]
source: raw/claude-4-best-practices.md
---

# Context Awareness

## When to Use

Inject into coordinators or long-running execution agents that operate in harnesses with context compaction. Prevents agents from prematurely stopping work when context budget shrinks.

## Template

```text
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining.
```

## Adaptation Notes

Replace "memory" with the team's specific persistence mechanism (e.g., `.worklog/`, `progress.txt`, git commits). For teams using A-Team's worklog system, direct the agent to save state to the current phase worklog before compaction.
