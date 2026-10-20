---
name: Prefill Migration
category: claude-4-patterns
applies_when:
  - generating-coding-team
  - writing-skill-prompts
  - writing-agent-prompts
  - optimizing-prompts
tags: [prefill, migration, structured-outputs, breaking-change, format-control]
source: raw/claude-4-best-practices.md
---

# Prefill Migration

## Behavioral Change

Starting with Claude 4.6 models, prefilled responses on the last assistant turn are no longer supported. Requests with prefilled assistant messages return a 400 error. This is a breaking change, not a deprecation. Adding assistant messages elsewhere in the conversation (for multi-turn context) is not affected.

## Impact on Generated Teams

Any generated skill or agent prompt that relies on prefill for output format control, preamble elimination, continuation, or refusal avoidance must use alternative approaches. Teams that use the API directly (e.g., coding teams with custom tool integrations) are most affected.

## Recommended Pattern

Migration table for all common prefill use cases:

| Prefill Use Case | Old Approach | 4.6 Alternative |
|------------------|-------------|-----------------|
| **JSON/YAML format** | Prefill `{"` or `---\n` | Use Structured Outputs (`output_config.format`) or direct instruction: "Respond with valid JSON matching this schema: {schema}" |
| **Classification** | Prefill category label start | Use tools with enum field containing valid labels, or Structured Outputs |
| **Skip preamble** | Prefill `Here is the summary:\n` | System prompt: "Respond directly without preamble. Do not start with 'Here is...', 'Based on...', etc." |
| **Avoid refusal** | Prefill agreeable opening | Claude 4.6 refuses less inappropriately. Clear user-message prompting is sufficient |
| **Continue interrupted response** | Prefill partial text | User turn: "Your previous response was interrupted and ended with `[last text]`. Continue from where you left off." |
| **Context hydration** | Prefill assistant reminder | Inject as user-turn message. For agentic systems, hydrate via tools or during context compaction |
| **Role consistency** | Prefill character voice | System prompt with role definition. Claude 4.6 follows system prompts more reliably |

For format control in generated agent prompts, prefer XML output tags:

```text
Write your analysis inside <analysis> tags. Write your recommendation inside <recommendation> tags. Do not include any text outside these tags.
```

## Anti-Patterns to Avoid

- Attempting assistant-turn prefill on 4.6 models -- returns 400 error, no graceful degradation
- Over-engineering format control when a direct instruction suffices -- Claude 4.6 follows format instructions reliably
- Using post-processing to strip preambles when a system prompt instruction eliminates them
- Ignoring this change in generated teams that target multi-model deployment (must branch on model version)
