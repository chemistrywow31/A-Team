---
name: Anti Over-Engineering
category: templates
applies_when:
  - generating-execution-agent
  - generating-coding-team
tags: [simplicity, minimal-changes, scope-control, coding]
source: raw/claude-4-best-practices.md
---

# Anti Over-Engineering

## When to Use

Inject into coding agents, implementers, or any execution agent that tends to add unrequested features, abstractions, or defensive code. Especially valuable for bug-fix agents and focused-task workers.

## Template

```text
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task.
```

## Adaptation Notes

Use as-is for execution agents. Omit or soften for architecture agents or agents explicitly tasked with refactoring. Pair with `anti-hard-coding` to cover both over-engineering and under-engineering failure modes.
