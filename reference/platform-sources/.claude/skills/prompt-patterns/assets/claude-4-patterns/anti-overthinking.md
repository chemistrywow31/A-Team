---
name: Anti-Overthinking
category: claude-4-patterns
applies_when:
  - generating-execution-agent
  - generating-coding-team
  - writing-agent-prompts
  - writing-skill-prompts
  - optimizing-prompts
tags: [overthinking, exploration, tool-use, effort, commitment]
source: raw/claude-4-best-practices.md
---

# Anti-Overthinking

## Behavioral Change

Claude Opus 4.6 performs significantly more upfront exploration than previous models, especially at higher effort settings. It gathers extensive context, pursues multiple research threads, and reads broadly before acting. Prompts that previously encouraged thoroughness (common with older models that undertriggered) now cause excessive exploration -- inflated thinking tokens, slower responses, and unnecessary tool calls.

## Impact on Generated Teams

Execution agents (code writers, content generators, builders) in generated teams inherit the thoroughness bias. If their prompts contain legacy anti-laziness language ("Default to using [tool]", "If in doubt, use [tool]", "Be thorough"), they will over-explore before producing output, wasting context window and latency.

## Recommended Pattern

Replace blanket tool defaults with conditional guidance:

```text
# Before (causes over-exploration on 4.6)
Default to using the Read tool to understand code before making changes.
If in doubt, read the file.

# After (targeted triggering)
Use the Read tool when it would enhance your understanding of the problem.
Read files that are directly relevant to the change you are making.
```

Add the commitment-over-exploration pattern to execution agent prompts:

```text
When deciding how to approach a problem, choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning. If you are weighing two approaches, pick one and see it through. You can course-correct later if the chosen approach fails.
```

Use effort as a lever when prompt adjustments are insufficient. Lower the effort setting for agents that still over-explore:

| Symptom | Fix |
|---------|-----|
| Agent reads 10+ files before a single-file edit | Add "Read files directly relevant to the change" |
| Agent explores multiple approaches before a clear task | Add commitment pattern above |
| Agent still over-explores after prompt fixes | Lower effort to `medium` |

## Anti-Patterns to Avoid

- "Default to using [tool]" -- causes indiscriminate tool use on 4.6
- "If in doubt, use [tool]" -- removes judgment, triggers tool on every ambiguity
- "Be thorough and comprehensive" without scope bounds -- licenses unlimited exploration
- "Always read all related files before making changes" -- causes full-codebase scanning on trivial edits
