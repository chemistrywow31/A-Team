---
name: Structured Notes
category: context-strategies
applies_when:
  - long-running-tasks
  - generating-coordinator
  - generating-execution-agent
  - context-constrained
tags: [memory, note-taking, persistence, state-tracking]
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/context-engineering-blog.md
source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
reviewed: 2026-10-06
---

# Structured Notes

## Core Principle

Persist the state required to resume a task and check the current artifacts when resuming. Notes improve continuity; they do not guarantee lossless recall or automatically refresh stale evidence.

## Choose A Useful Form

- Existing phase worklog: decisions, evidence references, changed paths, and remaining work.
- A structured record: test/task status when a downstream consumer needs machine-readable fields.
- A short checklist: outstanding items when that is clearer than prose.
- Git history/checkpoints: useful when already available or explicitly authorized; this pattern does not require a commit.

Reuse the accepted worklog unless a separate artifact serves a concrete need. Keep production files and evidence ownership explicit; a notes pattern is not permission to create a second tracking system.

## Checkpoint Example

```text
Changed: canonical review skill and its two mapped mirrors.
Verified: metadata parses; mirror bytes match at the recorded state.
Pending: independent usefulness review for the added conversion example.
Next: freeze these files and hand the criterion/evidence paths to the reviewer.
```

## A-Team Application

Use `.worklog/` references, findings, and decisions according to the existing context-management cadence. Preserve critical state before context pressure. On resumption, check for intervening changes before reusing current-state claims. Keep notes about conclusions and evidence rather than private deliberation.

## Examples

### Rejection Case

Reject creating `progress.txt` solely because the task is long when the phase worklog already records every required handoff. Add a separate structured artifact only if its consumer and use are clear.

## Sources And Attribution

A-Team-authored checkpoint and ownership policy, informed by [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked 2026-10-06. The article supplies examples of persistent notes, not a guarantee of perfect continuation or a required file schema.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/context-strategies/structured-notes.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
