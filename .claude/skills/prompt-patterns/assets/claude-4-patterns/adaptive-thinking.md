---
name: Adaptive Thinking
category: claude-4-patterns
applies_when:
  - generating-coordinator
  - generating-research-agent
  - generating-coding-team
  - writing-agent-prompts
  - optimizing-prompts
tags: [thinking, effort, adaptive, budget-tokens, migration]
source: raw/claude-4-best-practices.md
---

# Adaptive Thinking

## Behavioral Change

Claude 4.6 replaces manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) with adaptive thinking (`thinking: {type: "adaptive"}`). Claude now dynamically decides when and how much to think based on query complexity and the `effort` parameter. The `budget_tokens` approach is deprecated and will be removed. In internal evaluations, adaptive thinking reliably outperforms fixed-budget extended thinking.

The `effort` parameter controls thinking depth: `low`, `medium`, `high` (default), `max` (Opus 4.6 only). Adaptive mode automatically enables interleaved thinking (thinking between tool calls), which previously required a beta header.

When extended thinking is disabled, Claude Opus 4.5 is sensitive to the word "think" and its variants. Use "consider", "evaluate", or "reason through" instead in prompts targeting that model.

## Impact on Generated Teams

Every generated agent prompt that references reasoning depth or thinking behavior must use effort-based language, not budget-based language. Coordinator dispatch instructions that set thinking budgets per agent tier must migrate to effort levels.

## Recommended Pattern

Map effort levels to agent task types in generated teams:

| Task Type | Effort | Rationale |
|-----------|--------|-----------|
| Formatting, validation, linting (Tier 1) | `low` | Deterministic output, no reasoning needed |
| Code writing, content generation (Tier 2) | `medium` | Local decisions within defined scope |
| Planning, research, analysis (Tier 3) | `high` | Cross-cutting decisions, broad context |
| Coordination, auditing, deep research (Tier 4) | `max` | Maximum reasoning for complex orchestration |

In agent prompts, guide thinking behavior explicitly:

```text
After receiving tool results, reflect on their quality and determine next steps before proceeding. Use thinking to plan and iterate, then take the best action.
```

To reduce unnecessary thinking:

```text
Extended thinking adds latency. Use it only when it meaningfully improves answer quality -- typically for multi-step reasoning. When in doubt, respond directly.
```

## Anti-Patterns to Avoid

- Setting `budget_tokens` in new agent configurations -- use `effort` instead
- Using the word "think" in prompts for Opus 4.5 when thinking is disabled -- use "consider" or "evaluate"
- Applying `max` effort to simple execution agents -- wastes tokens on deterministic tasks
- Omitting effort guidance entirely -- lets the default `high` apply to all agents regardless of tier
