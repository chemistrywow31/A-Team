---
name: Reduce Thinking
category: templates
applies_when:
  - generating-execution-agent
  - context-constrained
tags: [latency, thinking, efficiency, token-budget]
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/claude-4-best-practices.md
source: https://platform.claude.com/docs/en/build-with-claude/effort
reviewed: 2026-10-06
---

# Reduce Thinking

## When To Use

Use when representative tasks show unnecessary deliberation without a corresponding quality benefit. Do not infer that every formatter, validator, or tier needs lower effort; a validator can still face a difficult judgment.

## Task-Scoped Template

```text
Complete the requested transformation and its relevant check. Revisit the approach
only when new evidence or a failed check justifies it. Report the result and any
material uncertainty; include a worked derivation when the user needs to verify it.
```

## Native Adaptation

For a selected Grok model, check supported session/agent reasoning-effort controls. Do not infer that omitted effort disables thinking, and do not use ignored skill metadata as a control. Change model/effort settings only within authorized scope and evaluate the actual task. Keep public response-length preferences separate from internal effort.

Use installed native controls rather than translating another provider's tier names or manual thinking budgets. Never replace effort configuration with a private-reasoning disclosure request.

## Examples

### Rejection Case

Reject lowering a pinned reviewer’s effort merely because the job label says “validation.” Preserve the pin and assess the actual evidence task; propose a scoped change only when quality and runtime evidence justify it.

## Sources And Attribution

A-Team-authored template and preservation policy, informed by [Claude effort](https://platform.claude.com/docs/en/build-with-claude/effort), checked 2026-10-06. The older block remains traceable through historical-source; it does not establish current model defaults.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/templates/reduce-thinking.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
