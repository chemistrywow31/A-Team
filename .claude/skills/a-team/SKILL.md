---
name: A-Team
description: Entry point that makes this session adopt the Team Architect workflow to run the full team design process
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team description | existing-team request]"
---

# A-Team

## Description

Adopt the Team Architect workflow in the current session and run the full A-Team process: Phases 1-6 for a new team, or the correct existing-team lane for optimization or restructuring.

## Users

- Main-session invocation of `/A-Team`

## Core Knowledge

- A-Team repo-self keeps `.claude/` as its canonical source; its Codex surfaces are regenerated projections.
- Generated teams do not inherit A-Team's canonical authority automatically. Discovery must confirm each generated team's requested format, and existing-team work must respect the target team's own canonical declaration.
- Existing-team work starts with deterministic classification: direct `teams/*` root, layout, runnable surfaces, activation or reference-only state, generation stamp, canonical authority, and mapping state.
- The optimization lane is text-only. Any structural, runtime, ownership, mapping, canonical-authority, or parity change belongs to restructuring.
- A `Codex-only runtime gap` stays inside already-allowed platform-only surfaces. A `cross-platform design gap` starts at the target team's canonical source and regenerates only affected projections.

## Application Guide

1. If `/A-Team` is invoked inside a dispatched task instead of the main user session, stop and return `BLOCKED: wrong-context invocation - /A-Team must run in the main session.`
2. Read `CLAUDE.md` and `.claude/agents/team-architect.md`, then adopt that workflow for the rest of the task.
3. Initialize the worklog and keep the dialogue log current. Reuse requirements and authorization already supplied in the session; interim summaries communicate progress without another approval gate.
4. For a new team, confirm objective, scope, workflow, role coverage, requested format, execution mode, canonical authority, surface activation, mapping retention, and requirements summary before leaving Discovery. An explicit user delegation of routine decisions can supply confirmation within that scope.
5. For existing-team maintenance, classify the target and use the scoped maintenance lane. If canonical authority is ambiguous, limit work to assessment until it is confirmed; do not restart new-team Discovery.
6. Route text-only prompt improvements for the selected runtime that leave roles, rules, runtime, ownership, mapping, canonical authority, and parity unchanged to `prompt-optimizer`. Route other changes to `team-restructuring-master` and require recommendation audit before implementation. Proceed within existing authorization; request user approval only for a proposal that exceeds it.
7. Ask only for material missing decisions, unresolved authority, or required authorization. Use asynchronous clarification when the host supports it and continue independent work while awaiting the answer; dependent work waits for required input.
8. Give every dispatch a stable task path, exact owned and forbidden paths, acceptance criteria, and the shared-filesystem non-reversion rule. Apply `.claude/rules/dual-platform-parity.md` authority and path-confinement gates before mutation.
9. Backport generator defects to A-Team's canonical `.claude/` design, then regenerate the affected Codex projections sequentially under the same family owner.
10. Freeze one coherent artifact batch for independent review. After corrections, rerun every criterion citing a changed file and dependent mapping/parity checks. Run runtime preflight after runtime freeze for new delivery, changed active runtime artifacts, or missing current readiness evidence; reuse its current validation evidence for each selected runtime. Keep dialogue review retrospective.

## Examples

### Rejection Case

Reject a proposed runtime change that promotes an existing team's reference-only surface without explicit authorization and consistent authority/mapping declarations. Continue the authorized assessment and obtain the missing decision before mutation.
