---
name: Compaction
category: context-strategies
applies_when:
  - long-running-tasks
  - context-constrained
  - generating-coordinator
tags: [compaction, summarization, context-window, long-horizon]
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/context-engineering-blog.md
source: https://code.claude.com/docs/en/memory
reviewed: 2026-10-06
---

# Compaction

## Core Principle

Compaction can preserve useful task state within a smaller context. Its exact behavior depends on the host; do not assume a fixed restored-file count or complete retention. Persist consequential state where it can be reread.

## What To Preserve

- The current objective, authorization, ownership, and active phase.
- Decisions with evidence pointers, unresolved issues, and remaining dependencies.
- Changed paths, actual test commands/results, and the next actionable step.
- User corrections and constraints that still apply.

Drop redundant or superseded material only when required evidence remains retrievable. An old tool response that is the sole record of a result must be preserved or persisted before discarding it.

## Pattern

```text
Before compaction, update the current phase worklog with changed paths, current checks,
and unresolved work. After continuation, read that checkpoint and inspect any mutable
artifact whose current state matters before relying on an earlier conclusion.
```

Use the installed Grok client's advertised compaction/continuation controls only after checking support. Preserve a bounded worklog checkpoint before compaction; do not promise a fixed restoration list or that omitted facts will survive.

## A-Team Application

Use the existing worklog/context-management cadence. Keep decision and evidence pointers available to the resumed worker, and retain fresh-context independent review as a separate acceptance requirement.

## Examples

### Defer Case

A resumed reviewer finds only “tests passed” without the command or artifact state. Reconstruct the relevant evidence before reusing that verdict; a compaction summary is not proof of the current result.

## Sources And Attribution

A-Team-authored checkpoint example and evidence rules. [Claude memory/compaction guidance](https://code.claude.com/docs/en/memory) and the [historical context-engineering article](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked 2026-10-06, inform the pattern; neither is treated as a universal fixed-file restoration contract.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/context-strategies/compaction.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
