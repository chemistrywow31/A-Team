---
name: Few-Shot Patterns
category: advanced-techniques
applies_when:
  - optimizing-prompts
  - writing-skill-prompts
  - writing-agent-prompts
  - generating-execution-agent
  - generating-rules
tags: [few-shot, examples, calibration, edge-cases, knowledge-work]
source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
historical-source: raw/tutorial-advanced-techniques.md
reviewed: 2026-10-06
---

# Few-Shot Patterns

## Select Examples By The Behavior They Teach

Use realistic demonstrations when a schema or instruction leaves a consequential choice unclear. Show the expected output, relevant evidence, and a boundary response; vary the cases enough to avoid teaching an accidental rule. A schema defines shape, while examples can clarify judgment. Use both when they help.

The number of examples depends on the task and observed failures. Do not impose exactly three cases, a universal minimum, or a one-example ceiling. A-Team J5 requires at least one meaningful rejection/defer/escalation case in authored agents and skills; useful positive or contrast cases can supplement it.

## Worked Calibration Pair

The following A-Team-authored examples teach evidence coverage without printing private thinking:

```xml
<examples>
  <example>
    <input>Criterion: configuration parses. Evidence: parser exited 0 with no diagnostics.</input>
    <output>PASS — parser result satisfies the static parsing criterion.</output>
  </example>
  <example>
    <input>Criterion: live reviewer tools are available. Evidence: parser exited 0.</input>
    <output>UNVERIFIED — static parsing does not demonstrate the live tool namespace.</output>
  </example>
</examples>
```

These are illustrative criterion judgments, not EC-1 report statuses. A-Team's overall acceptance still follows the execution contract; an unverified required criterion cannot produce overall PASS.

## Application

- Preserve task-specific steps and useful public derivations in worked examples. Do not add hidden-thinking transcripts as a demonstration of style.
- Use descriptive XML or other clear delimiters when several examples and live input appear together. Mark which material is illustrative.
- Test the task on a realistic input that is not copied from the demonstrations. Add an example when it resolves an observed ambiguity; remove one only when it is redundant, misleading, or conflicts with the intended behavior.
- Use supported native structured output controls when machine parsing is required. Do not assume an assistant prefill is available for the target model.

## Examples

### Rejection Case

Reject three samples that differ only in names while all show success. Keep the useful success sample and add the missing-evidence case when that boundary is material to the task.

## Sources And Attribution

A-Team-authored demonstrations and J5 policy, informed by [Claude example guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#use-examples-effectively), checked 2026-10-06. Vendor recommendations are guidance to evaluate for a task, not A-Team-wide fixed counts.
