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
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/context-engineering-blog.md
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

## Native Grok Mode

The main-session coordinator uses the advertised `spawn_subagent` schema; only select `subagent_type` if the live tool exposes the discovered role enum. Observe tasks using `get_command_or_subagent_output` or the advertised waiting fallback. Cancel only obsolete or unsafe work. Messaging is optional and feature-gated.

Grok specialists do not delegate under A-Team policy. The pinned source supports the `disallowedTools: [Task]` directive and a default native depth of one; effective installed tool denial still requires a live trace. Keep coordinator tools unrestricted by an incomplete allowlist and treat the allowed 12-role roster as prompt policy.

Supply exact inputs and explicit skill reads/preloads. For fresh review, create a new child without `resume_from`; source creates a new conversation, while installed effectiveness remains a separate check. A resumed completed child retains context. Do not invent a fork-context parameter; follow `.grok/policies/context-isolation.md`.

## Verification Handoff

Freeze the producer's coherent artifact batch before independent review. Give the fresh reviewer acceptance criteria and actual artifact paths. After a correction, invalidate affected-file criteria and dependent mapping/parity checks. Join only when the next step depends on the result.

## Examples

### Rejection Case

Reject two writers owning the same canonical skill and its projection concurrently. Give that family to one owner and run independent evidence collection in a separate branch.

## Sources And Attribution

A-Team-authored ownership, reporting, and review contracts. Historical native details in the original source followed [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) and [Agent Teams](https://code.claude.com/docs/en/agent-teams), checked 2026-10-06. Historical context-engineering material motivates focused delegation; it does not prescribe A-Team's topology or report caps.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/context-strategies/sub-agent-dispatch.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
