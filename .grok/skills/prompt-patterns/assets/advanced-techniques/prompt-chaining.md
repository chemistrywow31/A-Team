---
name: Prompt Chaining
category: advanced-techniques
applies_when:
  - generating-review-agent
  - generating-execution-agent
  - writing-skill-prompts
  - generating-coding-team
tags: [chaining, self-correction, iterative, multi-turn, extract-then-process]
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/tutorial-advanced-techniques.md
source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
reviewed: 2026-10-06
---

# Prompt Chaining

## Chain Only When The Handoff Adds Value

Break work into stages when an intermediate result needs inspection, a later step depends on verified output, or independent review is required. A simple skill may complete its work in one procedure. Stage count, separate API calls, and agent dispatches are not universal requirements.

## Conditional Verification

```text
Check that every extracted identifier occurs in the source and appears once.
Correct only unsupported or duplicate entries. If the list is valid, retain it.
```

This A-Team-authored check makes the success condition explicit and permits no change when the artifact is already correct.

## Worked Extract-Then-Process Example

```xml
<source>Owners: Lee, Rao, Lee.</source>
<task>Extract distinct owner names, then sort them alphabetically.</task>
<output>["Lee", "Rao"]</output>
```

Extraction and sorting have a real dependency. They can occur within one task; no separate worker or API round trip is needed unless inspection or isolation adds value. Use a supported output schema when machine parsing matters. Do not assume assistant prefill support for the selected model.

## Review And Correction

A substantial generated artifact can use producer → independent reviewer → producer correction. Freeze the coherent batch before review; correction runs only when findings require it. A producer self-check does not replace A-Team's independent acceptance gate. After a change, rerun affected criteria and dependent mapping/parity evidence rather than automatically repeating every check.

Keep native lifecycle choices in the target runtime contract. In Grok, the main coordinator uses the advertised `spawn_subagent` only when a separate specialist is needed; do not force every workflow step into a dispatch. Specialists return to the coordinator instead of delegating. Public evidence and results remain the handoff; no private scratchpad transcript is required.

## Examples

### Rejection Case

Reject an obligatory generate/review/rewrite sequence for a valid two-item extraction. Run the relevant check and retain the correct output; add an independent reviewer only when the task's acceptance contract calls for one.

## Sources And Attribution

A-Team-authored examples and acceptance workflow, informed by [Claude prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-10-06. Historical tutorial provenance does not prescribe current native API support or a universal pipeline.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/advanced-techniques/prompt-chaining.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
