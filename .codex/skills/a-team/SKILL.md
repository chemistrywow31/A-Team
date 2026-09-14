---
name: A-Team
description: Start the A-Team Codex coordinator workflow for designing or restructuring teams
---

# A-Team

## Description

Adopt the Team Architect workflow in the main session for new-team design, generation, review, or scoped existing-team optimization and restructuring.

## Core Knowledge

- `AGENTS.md` is the Codex runtime contract; `.codex/agents/team-architect.md` is the coordinator playbook.
- A-Team repo-self keeps `.claude/` canonical. Generated teams follow their own confirmed Claude, Codex, or platform-neutral canonical declaration.
- Classify existing targets by root, layout, runnable surfaces, activation/reference state, generation stamp, authority, and mapping state.
- `prompt-optimizer` owns text-only changes that leave roles, rules, runtime, ownership, mapping, authority, and parity unchanged.
- `team-restructuring-master` owns other changes and distinguishes `Codex-only runtime gap` from `cross-platform design gap`.

## Application Guide

1. Run as the main-session coordinator. If this skill is invoked inside a dispatched specialist task, return `BLOCKED: wrong-context invocation`. Read `AGENTS.md` and `.codex/agents/team-architect.md`.
2. Initialize the worklog and keep the dialogue log current. Reuse requirements and authorization already supplied in the session; interim summaries need no repeated approval.
3. For a new team, confirm objective, scope, workflow, role coverage, requested format, execution mode, canonical authority, surface activation, mapping retention, and requirements summary before leaving Discovery. Explicit user delegation of routine decisions can supply confirmation within that scope.
4. For existing-team maintenance, classify the target and use the scoped maintenance lane. Ambiguous authority permits assessment only until resolved; do not restart new-team Discovery.
5. Route text-only changes to `prompt-optimizer`; route other changes to `team-restructuring-master` and require recommendation audit. Proceed within existing authorization; request user approval only for a proposal that exceeds it.
6. Ask only for material missing decisions, unresolved authority, or required authorization. Use asynchronous clarification when supported and continue independent work while awaiting the answer; dependent work waits for required input.
7. Give every dispatch a stable phase-purpose task path, exact owned/forbidden paths, acceptance criteria, and the shared-filesystem non-reversion rule. Apply `.codex/rules/dual-platform-parity.md` authority and path-confinement gates before mutation.
8. Use `spawn_agent` for a new bounded task, `send_message` for an update, `followup_task` for a new/corrective turn on an idle agent, `interrupt_agent` only for invalidated or unsafe work, `list_agents` before routing/join decisions, and `wait_agent` only at a real join boundary.
9. Backport generator defects to A-Team's canonical `.claude/` source, then regenerate affected Codex projections sequentially under the same family owner.
10. Freeze one coherent artifact batch for independent review. After corrections, rerun every criterion citing a changed file and dependent mapping/parity checks. Run preflight after runtime freeze for new delivery, changed active runtime artifacts, or missing current readiness evidence; reuse its current validator and strict-model evidence. Keep dialogue review retrospective.

## Examples

### Rejection Case

Reject a proposed runtime change that promotes an existing team's reference-only surface without explicit authorization and consistent authority/mapping declarations. Continue the authorized assessment and obtain the missing decision before mutation.
