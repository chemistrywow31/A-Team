---
name: Chain of Thought
category: advanced-techniques
applies_when:
  - optimizing-prompts
  - generating-coordinator
  - generating-research-agent
  - generating-review-agent
  - writing-agent-prompts
tags: [precognition, reasoning, CoT, structured-thinking, order-sensitivity]
source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
historical-source: raw/tutorial-advanced-techniques.md
reviewed: 2026-10-06
---

# Chain of Thought

## Choose The Thinking Mode

Check the selected model and runtime before adding reasoning instructions. Claude's current guidance distinguishes native adaptive thinking with supported effort controls from manual worked-solution prompting when thinking is disabled. Some models keep thinking always on; do not infer a disabled mode from omitted configuration. Preserve existing model/effort choices unless migration is authorized.

Do not request private reasoning transcripts or hidden thinking blocks. Public calculations, evidence summaries, assumptions, and decision explanations remain useful deliverables. Choose them for the reader's task, rather than making them a ritual before every answer.

## Patterns

**Native thinking enabled:** state the outcome, evidence standard, and completion criteria. Let the supported model control internal deliberation.

```xml
<task>Review the proposed schema migration against the supplied compatibility criteria.</task>
<output>
Give a verdict, cite the checks that support it, and name any unresolved assumption.
</output>
```

**Thinking disabled, when supported:** a task-specific worked solution can help a multistep problem. Ask for a useful derivation, not a record of private deliberation.

```text
Explain the capacity calculation for 240 requests per minute with 20 requests
per worker per minute. Show the arithmetic and state the equal-load assumption.
Expected worked result: 240 / 20 = 12 workers before any separately justified reserve.
```

**Decision summary:** for a comparison, request the decisive evidence and relevant tradeoff. Do not force equal arguments for options whose evidence is unequal, or order PASS/FAIL labels to manipulate a supposed positional bias.

## A-Team Application

Preserve one role-specific `Reasoning` → `Workflow` → `Self-Critique` contract under `.claude/rules/reasoning-and-self-critique.md`. It defines decision criteria, work, and checks; it is not an instruction to print internal thought. Use the existing EC-1 evidence and conclusions fields for public results. Do not insert a second thinking/scratchpad form.

## Examples

### Rejection Case

Reject a reviewer instruction to reveal every internal thought before each verdict. Replace it with a verdict, the decisive source or test, and any missing evidence. Keep a calculation or worked example when it helps the user check the result.

## Sources And Attribution

A-Team-authored examples and workflow adaptation, informed by [Claude prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#thinking-and-reasoning) and [native effort controls](https://platform.claude.com/docs/en/build-with-claude/effort), checked 2026-10-06. The historical-source field records provenance only; it is not active guidance or a read trigger.
