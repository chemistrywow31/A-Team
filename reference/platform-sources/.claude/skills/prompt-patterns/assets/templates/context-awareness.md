---
name: Context Awareness
category: templates
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - long-running-tasks
  - context-constrained
tags: [context-window, compaction, persistence, autonomy]
historical-source: raw/claude-4-best-practices.md
source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
reviewed: 2026-10-06
---

# Context Awareness

## When To Use

Use for a long-running task when the host actually supports continuation or compaction. Distinguish recoverable context-window pressure from a finite task budget.

## Template

```text
When continuation is available, preserve progress before context pressure interrupts
the task, then resume from the recorded state. Keep the objective, scope, changed files,
current checks, unresolved decisions, and next action in the assigned worklog.
A shrinking context window alone need not end authorized work. Explicit time, token,
turn, or resource limits and user stop instructions still govern. When a hard limit
prevents completion, report the actual partial state and a useful handoff.
```

## Adaptation Notes

Use the team's existing persistence mechanism. Check the host's real continuation behavior; do not promise indefinite execution or lossless recall. Saving progress does not itself authorize commits, new files outside ownership, or actions after a stop instruction.

## Examples

### Boundary Case

A host can compact the conversation, but the user sets a ten-minute work limit. Preserve the completed work and remaining checks when that limit arrives; compaction availability does not extend it.

## Sources And Attribution

A-Team-authored persistence and budget contract, informed by [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked 2026-10-06. Native continuation behavior must be established for the target host.
