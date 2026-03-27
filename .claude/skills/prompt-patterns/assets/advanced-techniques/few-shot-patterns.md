---
name: Few-Shot Patterns
category: advanced-techniques
applies_when:
  - writing-skill-prompts
  - writing-agent-prompts
  - generating-execution-agent
  - generating-rules
tags: [few-shot, examples, calibration, edge-cases, knowledge-work]
source: raw/tutorial-advanced-techniques.md
---

# Few-Shot Patterns

## Core Principle

Examples are "probably the single most effective tool in knowledge work for getting Claude to behave as desired" (Anthropic). Generally more examples = better. Every example set must cover normal cases, edge cases, and failure cases to triangulate the full output space.

## Pattern

**Use `<example>` XML tags for all examples:**
```
Here is an example of how to respond in a standard interaction:
<example>
Customer: Hi, how were you created and what do you do?
Joe: Hello! My name is Joe, and I was created by AdAstra Careers
to give career advice. What can I help you with today?
</example>
```

**Include `<thinking>` tags inside examples to teach reasoning style:**
When examples contain a thinking step, Claude learns both the reasoning process and the output format simultaneously. Show the scratchpad work, not just the final answer.

**Three-Example Calibration pattern (from Anthropic courses):**

For any structured output task, provide exactly three examples covering:
1. **Happy path** -- Complete, successful interaction (e.g., resolved issue, no follow-up)
2. **Partial/escalation path** -- Interaction requiring follow-up or special handling
3. **Failure/edge path** -- Insufficient data, unclear input, or error condition

This triangulates the model's understanding of the full output space.

**Format extraction via examples + prefill (Anthropic verbatim):**
```
[First passage with entities]
<individuals>
1. Dr. Liam Patel [NEUROSURGEON]
2. Olivia Chen [ARCHITECT]
</individuals>

[Second passage with entities]
<individuals>
1. Oliver Hamilton [CHEF]
2. Elizabeth Chen [LIBRARIAN]
</individuals>

[Actual input for Claude to process]
```
Prefill: `<individuals>`

**Diversity requirement:** 3-5 examples minimum. Each example must differ meaningfully in content, not just surface details. Include at least one example that demonstrates correct handling of ambiguous or incomplete input.

## A-Team Application

When generating skills and agent prompts:

- Skill-writer must include at least one input/output example per SKILL.md (enforced by writing-quality-standard). Use the Three-Example Calibration pattern: one normal, one edge, one failure.
- When generating agents that produce structured output (JSON, reports, evaluations), embed 2-3 worked examples directly in the agent's prompt showing the exact output format with realistic content.
- For review agents, examples must show both a passing review and a failing review with specific evidence citations -- this teaches the agent what "sufficient evidence" looks like.
- Agent-writer must never use placeholder examples like "example output here." Every example must contain realistic, complete content.
