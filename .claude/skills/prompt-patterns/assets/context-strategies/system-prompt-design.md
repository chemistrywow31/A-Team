---
name: System Prompt Design
category: context-strategies
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - generating-review-agent
  - generating-research-agent
tags: [system-prompt, instructions, altitude, minimal-prompt]
source: raw/context-engineering-blog.md
---

# System Prompt Design

## Core Principle

System prompts must hit the "right altitude" — specific enough to guide behavior, flexible enough to provide strong heuristics. Too specific creates brittle, high-maintenance logic. Too vague fails to give the model concrete signals and falsely assumes shared context. Strive for minimal information that fully outlines expected behavior.

## Pattern

**Two failure modes:**
- Over-specified: Hardcoded complex logic for exact behavior. Fragile, high maintenance. Model ignores rules when the prompt is too long and important rules get lost in noise.
- Under-specified: Vague high-level guidance. Model lacks concrete signals for desired output.

**Development process:**
1. Start with a minimal prompt using the strongest available model
2. Test against representative inputs
3. Add instructions only based on identified failure modes
4. Iterate: observe behavior, add/prune, re-test

**Organization:** Use XML tags (`<background_information>`, `<instructions>`) or Markdown headers (`## Tool guidance`, `## Output description`) to create distinct sections.

**CLAUDE.md principle:** For each line, ask "Would removing this cause Claude to make mistakes?" If not, cut it. Bloated CLAUDE.md files cause Claude to ignore actual instructions.

**Curate examples, not edge cases:** Provide diverse canonical examples portraying expected behavior. Avoid stuffing exhaustive edge cases — "examples are the pictures worth a thousand words."

## A-Team Application

When generating agent .md files: apply the right-altitude principle — imperative sentences, no vague words (per writing-quality-standard.md), but avoid over-specifying logic that the model handles natively. When generating CLAUDE.md: include only team-wide norms that agents cannot infer from code. Role-specific rules go in `rules/` with path-scoping where applicable. When generating skills: each SKILL.md must contain canonical examples (per writing-quality-standard.md), not exhaustive edge case lists. The prompt-optimizer agent must evaluate altitude during Phase 4.
