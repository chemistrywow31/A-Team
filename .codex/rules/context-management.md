---
name: Context Management
description: Keep Codex multi-agent work path-driven, target-lifecycle correct, and resumable without replaying whole context
---

# Context Management

## Applicability

- Applies to: `team-architect` and every generated Codex multi-agent coordinator or specialist

## Rule Content

### Dispatch By Stable Task Path

- Every delegation branch uses a stable phase-purpose task path such as `discovery_requirements`, `planning_skill_plan`, `generation_rules`, `generation_agents`, `restructure_assessment`, or `review_runtime_preflight`.
- Every dispatch must include the stable task path, worklog or BRIEF paths, owned write paths, forbidden paths, acceptance criteria, and the shared-filesystem non-reversion rule.

### Use The Selected Runtime Lifecycle

Apply `.codex/rules/context-isolation.md` and the target's recorded runtime profile. The following is A-Team's observed v2 host contract; do not require these names on a host exposing the documented portable CLI lifecycle.

- `spawn_agent` starts new bounded independent work.
- `send_message` carries a non-triggering update to an existing branch.
- `followup_task` gives an idle existing agent a new or corrective turn.
- `interrupt_agent` is reserved for unsafe work, invalidated work, or non-owned writes.
- `list_agents` is required before routing a follow-up to an existing branch or before a join decision.
- `wait_agent` is used only at a real join boundary when no independent coordinator work remains.

### Pass Paths, Not Dumps

Do not paste full upstream documents into a dispatch when the files are available locally. The receiving agent reads the files itself.

### Follow Up With Deltas

- A follow-up on an existing task path carries only the delta: changed assumptions, invalidated evidence, updated acceptance criteria, or new paths.
- Do not clone a new branch for the same task path unless the prior branch was invalidated or closed.

### Return Structured Summaries

- Every specialist return follows `rules/execution-contract.md`.
- Long findings, research notes, and logs go to the worklog or owned artifact files. Each dispatch names the report destination and persistence owner. If the live host blocks the specialist's report write, EC-1.12 permits only a dispatch-bounded `INLINE-FALLBACK` for coordinator persistence; do not claim an unwritten file exists or bypass the restriction with another tool.

### Resume From Worklog

After interruption or compaction, restore state from the task BRIEF, the current phase `decisions.md`, the latest relevant `findings.md`, and pending verifier notes.

## Violation Determination

- A dispatch omits the stable task path, worklog or BRIEF path, owned paths, forbidden paths, acceptance criteria, or non-reversion rule -> Violation
- A coordinator uses `send_message` as if it were a new work turn, or uses `followup_task` on a running branch -> Violation
- A coordinator routes or joins without checking live agent state first -> Violation
- `wait_agent` is used while independent coordinator work still remains -> Violation
- A dispatch includes full upstream documents when file paths would suffice -> Violation
- A specialist returns an unstructured long narrative, or fallback lacks its finite cap/destination/persistence owner -> Violation
- An unverified target is required to expose A-Team's observed v2 lifecycle -> Violation

## Exceptions

- Inline context under 200 words is allowed for a micro-dispatch when no useful file path exists yet.
