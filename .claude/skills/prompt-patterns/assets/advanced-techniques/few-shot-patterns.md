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

Examples are "probably the single most effective tool in knowledge work for getting Claude to behave as desired" (Anthropic). This holds for few-shot demonstrations INSIDE a prompt, where a set covering normal, edge, and failure cases triangulates the output space. It does NOT apply to the `## Examples` section of a generated agent or skill file, which carries exactly one rejection case — see the scope guard below and `rules/writing-quality-standard.md`.

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

> **Scope guard — do not apply this to the `## Examples` section of ANY generated file: agent .md OR
> skill SKILL.md.** This pattern is about few-shot demonstrations placed inside a prompt to calibrate
> a model's output for one structured task. A generated file's `## Examples` section is a different
> artifact and carries exactly ONE case, the rejection case, per `rules/writing-quality-standard.md`.
> Both are correct in their own place; applying the three-example count to either a generated agent
> or a generated skill violates that rule. `INDEX.md` routes BOTH agent writing and skill writing to
> this file, so both are in scope for this guard.

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

**Diversity requirement (in-prompt few-shot sets only — NOT generated `## Examples` sections):** 3-5 examples minimum. Each example must differ meaningfully in content, not just surface details. Include at least one example that demonstrates correct handling of ambiguous or incomplete input.

## A-Team Application

When generating skills and agent prompts:

- Skill-writer and agent-writer include EXACTLY ONE example per file, and it is the rejection case (enforced by `rules/writing-quality-standard.md`). Do not apply the Three-Example Calibration pattern above to a generated file's `## Examples` section — see the scope guard.
- When generating agents that produce structured output (JSON, reports, evaluations), specify the format as a labeled schema with typed slots rather than as worked examples. A schema constrains the shape without constraining the content the model explores; examples do both.
- For review agents, express the evidence bar as a rule ("every finding cites file:line; a finding with no citation is not a finding") rather than as a passing/failing example pair. The rule generalizes to cases the pair does not cover.
- Agent-writer must never use placeholder examples like "example output here." Every example must contain realistic, complete content.
