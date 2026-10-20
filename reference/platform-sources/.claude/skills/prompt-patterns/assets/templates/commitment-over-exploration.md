---
name: Commitment Over Exploration
category: templates
applies_when:
  - generating-execution-agent
  - generating-coding-team
  - long-running-tasks
  - context-constrained
tags: [decisiveness, overthinking, approach-selection, efficiency]
source: raw/claude-4-best-practices.md
---

# Commitment Over Exploration

## When to Use

Inject into execution agents or coding agents that waste context by endlessly deliberating between approaches. Especially valuable for Opus-based agents and context-constrained workflows.

## Template

```text
When you're deciding how to approach a problem, choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning. If you're weighing two approaches, pick one and see it through. You can always course-correct later if the chosen approach fails.
```

## Adaptation Notes

Use as-is for execution agents. Omit for research or planning agents where thorough exploration of alternatives is the primary job. For coordinators, apply selectively -- coordinators need to explore options during planning but commit during execution dispatch.
