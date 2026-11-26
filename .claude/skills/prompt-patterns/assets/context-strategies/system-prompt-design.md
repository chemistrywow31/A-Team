---
name: System Prompt Design
category: context-strategies
applies_when:
  - optimizing-prompts
  - generating-coordinator
  - generating-execution-agent
  - generating-review-agent
  - generating-research-agent
tags: [system-prompt, instructions, altitude, minimal-prompt]
source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
historical-source: raw/context-engineering-blog.md
reviewed: 2026-10-06
---

# System Prompt Design

## Make The Intended Behavior Executable

State what the role must accomplish, what evidence it needs, and what authority it has. Provide enough structure to avoid consequential ambiguity while leaving ordinary execution choices to the model. Prompt effectiveness is the criterion; shorter text is useful only when it removes distraction without losing behavior.

## Design And Evaluate

1. Identify representative tasks, expected outputs, and the failure that an instruction must prevent.
2. Select current official guidance for the actual platform, model, and thinking mode. Preserve explicit target settings unless changing them is authorized.
3. Write the task contract with concrete inputs, boundaries, completion, and uncertainty handling. Use steps when order matters and XML or headings when they clarify source boundaries.
4. Include realistic examples when they teach a consequential distinction. Prefer stating the contract to showing a sample of it, and add an example only where the contract leaves a real choice unclear.
5. Evaluate representative behavior and the known failure case. Fix demonstrated ambiguity, conflicting instructions, or omitted context. Do not treat reduced word count as an evaluation result.

## Worked Scope Contrast

```text
Weak: Improve our team system.
Executable: Improve A-Team's future restructuring workflow in the assigned source files.
Use a generated team only as a bounded read-only example if needed to reproduce a defect.
Completion: report source changes and evidence that capability-only intake does not mutate targets.
```

This example supplies a completion condition and a concrete boundary. It does not prescribe a private reasoning transcript or a universal process for every team request.

## A-Team Application

Keep the root entry to what the project is for and its gotchas; use role files for role behavior, scoped rules for constraints, and skills for on-demand procedures. Follow actual native loading semantics rather than assuming that all referenced files are loaded.

When optimizing, compare the before/after behavior against the same acceptance criteria. Keep what changes the reader's behavior and cut what does not; length is not the measure either way. Over-mark authored files get J5's independent review.

## Examples

### Rejection Case

Reject deleting a realistic missing-authority example solely to meet a word target. Keep the example if it prevents an unauthorized mutation, and record any required size review with its usefulness rationale.

## Sources And Attribution

A-Team-authored composition/evaluation workflow and examples, informed by [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked 2026-10-06. Platform-specific prompting and effort details stay in current native sources and their mapped adaptations.
