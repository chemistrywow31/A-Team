---
name: Chain of Thought
category: advanced-techniques
applies_when:
  - generating-coordinator
  - generating-research-agent
  - generating-review-agent
  - writing-agent-prompts
tags: [precognition, reasoning, CoT, structured-thinking, order-sensitivity]
source: raw/tutorial-advanced-techniques.md
---

# Chain of Thought

## Core Principle

Giving Claude time to think step by step makes it more accurate, particularly for complex tasks. Thinking only counts when it is "out loud" — visible in the output. You cannot ask Claude to think internally and output only the answer; the reasoning must be externalized.

## Pattern

**Structured thinking template (Anthropic verbatim):**
```
[Task]. First, [write/brainstorm about X] in <tag-name> tags,
then [provide answer/final output].
```

**Positive/negative argument tags for balanced analysis:**
```
Is this review sentiment positive or negative? First, write the best
arguments for each side in <positive-argument> and <negative-argument>
XML tags, then answer.
```

**Classification with reasoning-first and prefill:**
```
Think through your reasoning in <reasoning> tags, then provide your
classification in <answer> tags.
```
Prefill: `<reasoning>`

**Brainstorm-then-answer for recall tasks:**
```
Name a famous movie starring an actor who was born in the year 1956.
First brainstorm about some actors and their birth years in <brainstorm>
tags, then give your answer.
```

**Order sensitivity warning:** Claude is more likely to choose the second of two options (in training data, second options were more likely correct). When order matters, place the preferred or more-likely answer second.

## A-Team Application

When generating agents that make judgment calls (coordinators, reviewers, researchers, auditors):

- Include a `<thinking>` or `<reasoning>` step before every decision output. Agent-writer must embed this in the agent's workflow instructions, not leave it to the agent's discretion.
- For review agents evaluating multiple dimensions, use named argument tags (`<positive-argument>`, `<negative-argument>`) to force balanced consideration before verdict.
- For classification tasks in rules (e.g., violation detection), structure the prompt as: analyze in tags first, then classify. This prevents snap judgments.
- When presenting binary choices to Claude (e.g., PASS/FAIL), place the less common outcome first (FAIL first, PASS second) to counteract second-option bias.
