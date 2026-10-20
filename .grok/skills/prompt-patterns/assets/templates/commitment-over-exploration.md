---
name: Commitment Over Exploration
category: templates
applies_when:
  - generating-execution-agent
  - generating-coding-team
  - long-running-tasks
  - context-constrained
tags: [decisiveness, overthinking, approach-selection, efficiency]
source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/claude-4-best-practices.md
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

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/templates/commitment-over-exploration.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
