---
name: Sub-Agent Dispatch
category: context-strategies
applies_when:
  - generating-coordinator
  - generating-research-agent
  - context-constrained
  - long-running-tasks
tags: [sub-agents, context-isolation, delegation, multi-agent]
source: https://code.claude.com/docs/en/sub-agents
historical-source: raw/context-engineering-blog.md
reviewed: 2026-10-06
---

# Sub-Agent Dispatch

## Delegate Bounded Independent Work

Use a specialist when its distinct task or fresh evidence can improve the outcome while useful work continues elsewhere. Direct reads, small sequential operations, and tightly coupled edits usually need no extra agent. Context isolation alone does not guarantee independent judgment; the reviewer must inspect the actual artifacts against explicit criteria.

## Dispatch Contract

Give each specialist a stable task name, objective, relevant input paths, exact owned and forbidden paths, acceptance criteria, and a return/evidence destination. State that agents share the filesystem unless isolation is provisioned and must not revert other writers. Keep canonical edits and their same-family projections sequential under one owner.

```xml
<task id="review_contract">
Check whether the endpoint change preserves the supplied contract.
</task>
<inputs>docs/api-contract.md; docs/change-plan.md</inputs>
<ownership>
Read production files. Write only the assigned review report.
Other agents share this filesystem; do not revert their edits.
</ownership>
<acceptance>Each compatibility verdict cites the relevant contract and change.</acceptance>
<return>Use the agreed report contract and point to persisted evidence.</return>
```

The coordinator handles user dialogue, integration, and explicitly owned synthesis. Specialist-owned work stays with its assigned owner. If a sandbox blocks evidence persistence, use the dispatch-bounded EC-1 `INLINE-FALLBACK` and named coordinator persistence owner; do not bypass the restriction.

## Native Claude Mode

In A-Team's Claude subagent mode, the main-session coordinator uses `Agent`; `Task` remains a compatibility alias. Native Claude supports nesting, but A-Team prohibits specialist delegation and enforces it with `disallowedTools: [Agent]`. Supply exact inputs and explicit skill preload/read instructions; parent skills and conversation are not assumed to transfer.

Keep experimental Agent Teams distinct from subagent mode. Do not infer teammate capabilities or skill preload from a subagent definition. A target's runtime preflight must establish its selected mode. For Codex output, adapt through `.codex/rules/context-isolation.md` rather than copying Claude lifecycle controls.

## Verification Handoff

Freeze the producer's coherent artifact batch before independent review. Give the fresh reviewer acceptance criteria and actual artifact paths. After a correction, invalidate affected-file criteria and dependent mapping/parity checks. Join only when the next step depends on the result.

## Examples

### Rejection Case

Reject two writers owning the same canonical skill and its projection concurrently. Give that family to one owner and run independent evidence collection in a separate branch.

## Sources And Attribution

A-Team-authored ownership, reporting, and review contracts. Native details follow [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) and [Agent Teams](https://code.claude.com/docs/en/agent-teams), checked 2026-10-06. Historical context-engineering material motivates focused delegation; it does not prescribe A-Team's topology or report caps.
