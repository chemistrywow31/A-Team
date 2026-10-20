---
name: Over-Engineering Prevention
category: claude-4-patterns
applies_when:
  - generating-coding-team
  - generating-execution-agent
  - generating-frontend-team
  - generating-rules
  - writing-agent-prompts
  - optimizing-prompts
tags: [over-engineering, scope, minimalism, hard-coding, test-passing]
source: raw/claude-4-best-practices.md
---

# Over-Engineering Prevention

## Behavioral Change

Claude Opus 4.5 and 4.6 tend to overengineer: creating extra files, adding unnecessary abstractions, building unrequested flexibility, and adding defensive code for impossible scenarios. Separately, Claude can focus too heavily on making tests pass -- hard-coding values or using helper-script workarounds instead of implementing general solutions.

## Impact on Generated Teams

Coding teams are most affected. Without constraints, code-writing agents produce over-abstracted, over-documented, over-defended code. Test-driven agents may optimize for green tests rather than correct logic. Generated rules that lack scope boundaries amplify the problem.

## Recommended Pattern

Include the four-pillar constraint in every code-writing agent prompt:

```text
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused:

- Scope: Do not add features, refactor code, or make improvements beyond what was asked. A bug fix does not need surrounding code cleaned up. A simple feature does not need extra configurability.

- Documentation: Do not add docstrings, comments, or type annotations to code you did not change. Only add comments where the logic is not self-evident.

- Defensive coding: Do not add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

- Abstractions: Do not create helpers, utilities, or abstractions for one-time operations. Do not design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task.
```

Include the anti-hard-coding constraint in test-aware agent prompts:

```text
Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values or create solutions that only work for specific test inputs. Tests verify correctness -- they do not define the solution. If any tests are incorrect, report them rather than working around them.
```

For generated rules scoping code quality:

```text
Clean up only the files you create or modify. Do not touch adjacent code, add type annotations to existing functions, or refactor imports in files outside your task scope.
```

## Anti-Patterns to Avoid

- Omitting scope constraints from code-writing agents -- produces unrequested refactors and feature additions
- "Write comprehensive error handling" without specifying boundaries -- triggers validation for impossible states
- "Add documentation to all functions" -- causes agents to document unchanged code
- "Make sure all tests pass" without "implement general solutions" -- licenses hard-coding
