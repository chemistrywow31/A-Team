---
name: Anti Hard-Coding
category: templates
applies_when:
  - generating-execution-agent
  - generating-coding-team
tags: [general-purpose, anti-test-gaming, robustness, coding]
source: raw/claude-4-best-practices.md
---

# Anti Hard-Coding

## When to Use

Inject into coding agents or test-writing agents to prevent solutions that pass tests through hard-coded values rather than genuine logic. Especially important for agents that iterate against test suites.

## Template

```text
Please write a high-quality, general-purpose solution using the standard tools available. Do not create helper scripts or workarounds to accomplish the task more efficiently. Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values or create solutions that only work for specific test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm. Tests are there to verify correctness, not to define the solution. Provide a principled implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please inform me rather than working around them. The solution should be robust, maintainable, and extendable.
```

## Adaptation Notes

Use as-is for coding agents. For non-coding teams, the principle generalizes: agents must solve the actual problem, not game the validation criteria. Adapt "tests" to whatever acceptance criteria the team uses.
