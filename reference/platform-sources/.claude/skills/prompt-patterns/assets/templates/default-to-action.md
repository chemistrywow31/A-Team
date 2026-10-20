---
name: Default to Action
category: templates
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - generating-coding-team
tags: [action-bias, tool-use, proactive, implementation]
source: raw/claude-4-best-practices.md
---

# Default to Action

## When to Use

Inject into agents that must take action autonomously rather than suggesting changes -- coordinators dispatching work, execution agents implementing code, or any agent where passivity wastes cycles.

## Template

```text
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover any missing details instead of guessing. Try to infer the user's intent about whether a tool call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

## Adaptation Notes

Use as-is for execution agents. For coordinators, pair with autonomy-safety guardrails to prevent irreversible actions without confirmation. Omit for research or review agents that should analyze before acting.
