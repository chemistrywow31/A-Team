---
name: Reduce Thinking
category: templates
applies_when:
  - generating-execution-agent
  - context-constrained
tags: [latency, thinking, efficiency, token-budget]
source: raw/claude-4-best-practices.md
---

# Reduce Thinking

## When to Use

Inject into lightweight or high-throughput agents where extended thinking wastes tokens and adds latency -- formatters, validators, simple task executors, or Tier 1 context agents.

## Template

```text
Extended thinking adds latency and should only be used when it will meaningfully improve answer quality - typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

## Adaptation Notes

Use as-is for Tier 1 and simple Tier 2 agents. Omit for Tier 3+ agents, research agents, and coordinators where deep reasoning is the point. For haiku-based agents, this block is less necessary since haiku naturally uses minimal thinking.
