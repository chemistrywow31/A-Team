---
name: Investigate Before Answering
category: templates
applies_when:
  - generating-coding-team
  - generating-execution-agent
  - generating-review-agent
tags: [anti-hallucination, grounding, code-reading, verification]
source: raw/claude-4-best-practices.md
---

# Investigate Before Answering

## When to Use

Inject into any agent that works with code or files -- coding agents, code reviewers, QA agents, or any role where claims about existing code must be grounded in actual file reads.

## Template

```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer - give grounded and hallucination-free answers.
</investigate_before_answering>
```

## Adaptation Notes

Use as-is for all code-touching agents. For non-coding teams, adapt "code" to "content" or "documents" as appropriate. Pair with `parallel-tool-calls` so file reads happen efficiently.
