---
name: A-Team
description: Entry point that makes this session adopt the Team Architect workflow to run the full team design process
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team description or --restructure teams/path]"
---

# A-Team

## Description

Adopt the Team Architect coordinator workflow in the CURRENT session and run the complete team design process (Phases 1–6, or Phase 7 for restructuring).

## Why Main-Session Adoption, Not Spawning

A spawned coordinator subagent cannot dispatch further agents and cannot converse with the user — the workflow dead-locks at the first interview question (production evidence: teams/toeic-daily-prep-team first run, 2026-06, hand-patched). The coordinator must run where the user channel and the Agent tool both exist: this session.

## Execution

When this skill is invoked:

0. Context guard: if this invocation arrived inside a Task dispatch rather than a user's conversation turn (you are a dispatched subagent), STOP and return `BLOCKED: wrong-context invocation — /A-Team must run in the main session.`
1. Read `.claude/agents/team-architect.md` and adopt it as your operating playbook for this task. Its Runtime Placement, Dispatch Protocol, Workflow, and Self-Critique sections govern you until the task ends.
2. Create the worklog structure per its Worklog Initialization: `brief.md`, an empty `dialogue-log.md`, and phase directories as phases begin.
3. Parse arguments:
   - `/A-Team {description}` → begin Phase 1 Discovery, interviewing the user directly about {description}
   - `/A-Team --restructure teams/{path}` → run Phase 7 against that team
   - `/A-Team` (bare) → begin Phase 1 Discovery from scratch
4. Dispatch specialists via the Agent tool per the playbook. You keep the user channel; specialists route questions back through `NEEDS_CONTEXT` returns, which you relay and log to `dialogue-log.md`.

## Invocation Modes

Two entry paths and one refusal — these document distinct routing, not example diversity.

### Normal Case

User: `/A-Team 自動化測試團隊`

Action: Read team-architect.md → adopt its workflow → open Phase 1 in this conversation with the first interview question about 自動化測試團隊's objectives → append the exchange to `dialogue-log.md`.

### Restructuring Case (second invocation mode)

User: `/A-Team --restructure teams/english-teaching-content`

Action: Read team-architect.md → adopt its workflow → run Phase 7: dispatch `team-restructuring-master` per `templates/review.md` with the target path, relay its findings to the user before any change is executed.

### Rejection Case

User: `/A-Team delete the old teams and rebuild everything`

Action: Adopt the workflow, but do NOT delete anything. Deleting files this task did not create requires explicit per-target authorization (JUDGMENT.md J3.2). Reply asking the user to name the exact directories to remove and confirm each; proceed with the rebuild interview only after that is settled.
