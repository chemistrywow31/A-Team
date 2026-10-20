---
name: Conservative Action
category: templates
applies_when:
  - generating-research-agent
  - generating-review-agent
tags: [caution, research-first, non-destructive, analysis]
source: raw/claude-4-best-practices.md
---

# Conservative Action

## When to Use

Inject into agents that must analyze, research, or review before making changes -- research agents, auditors, reviewers, or any role where premature action causes harm.

## Template

```text
<do_not_act_before_instructions>
Do not jump into implementatation or changes files unless clearly instructed to make changes. When the user's intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action. Only proceed with edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

## Adaptation Notes

Use as-is for research and review agents. The typo "implementatation" is verbatim from Anthropic. For agents that split between analysis and execution phases, combine with `default-to-action` in the execution phase only.
