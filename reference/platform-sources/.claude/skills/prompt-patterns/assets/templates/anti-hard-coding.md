---
name: Anti Hard-Coding
category: templates
applies_when:
  - generating-execution-agent
  - generating-coding-team
tags: [general-purpose, anti-test-gaming, robustness, coding]
historical-source: raw/claude-4-best-practices.md
source: https://code.claude.com/docs/en/best-practices
reviewed: 2026-10-06
---

# Anti Hard-Coding

## When To Use

Use for implementation or test-writing tasks where passing the observed examples could conceal incorrect general behavior.

## Template

```text
Implement the requested behavior for the valid input domain. Do not hard-code observed
answers, bypass checks, or conceal incorrect requirements to make tests pass.
Use available tools and a helper script when they materially support the task and are
within scope. Respect an actual task-specific tool restriction.
Check the implementation against the requirement, including a relevant input not copied
from the examples. If a test contradicts the requirement, cite the conflict and correct
it only through the authorized change and review process.
```

## Adaptation Notes

For non-coding work, apply the same principle to the actual acceptance criteria. Choose checks that discriminate a real implementation from an example-specific workaround; do not add a universal test or tooling checklist.

## Examples

### Rejection Case

Reject a parser that returns a stored expected result for the test filename. Implement parsing for the supported format and verify another representative file. A small helper that constructs valid fixtures is allowed when it serves that check.

## Sources And Attribution

This revised template and example are A-Team-authored adaptations of the historical-source block. [Claude Code best practices](https://code.claude.com/docs/en/best-practices), checked 2026-10-06, supports concrete verification. The valid-domain, scope, and evidence-preserving repair contract is A-Team policy.
