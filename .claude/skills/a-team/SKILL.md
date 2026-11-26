---
name: A-Team
description: Entry point that makes this session adopt the Team Architect workflow to run the full team design process
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team description | A-Team capability maintenance | named-target request]"
---

# A-Team

## Description

Adopt the Team Architect workflow in the current session and run the A-Team process: design a new team, maintain A-Team itself, or optimize or restructure a named existing team.

## Application Guide

1. If `/A-Team` is invoked inside a dispatched task instead of the main user session, stop and return `BLOCKED: wrong-context invocation - /A-Team must run in the main session.`
2. Read `CLAUDE.md` and `.claude/agents/team-architect.md`, then adopt that workflow for the rest of the task. Create the task worklog (`.claude/rules/worklog.md`) and keep `dialogue-log.md` current.
3. Choose the lane from the request: a new team, A-Team capability maintenance, a named existing team, or explicitly requested fleet work. Capability maintenance stays in A-Team source. It does not authorize a target inventory or writes to any team; read one target only when you need it to reproduce a designer defect.
4. For a new team, interview with `.claude/skills/structured-interview/SKILL.md`. Then decide the shape of each user flow with `.claude/skills/work-shape/SKILL.md` and write `teams/{team-name}/docs/work-shape.json` before any role is designed. Confirm the objective, the flows, the shape, the delivery format, the canonical authority and the requirements summary with the user before planning.
5. Build what the shape calls for. A skill-workflow team needs no role design and no rule pack: plan and write its skills, settings and a short `CLAUDE.md`. An agent-group team gets only the roles its triggers justify. `.claude/rules/output-structure.md` lists what each shape ships.
6. For a named existing team, classify it first: surfaces, activation state, stamp, canonical authority, mapping. Ambiguous authority allows assessment only. Wording-only improvement goes to `prompt-optimizer`. Anything that changes roles, rules, runtime, ownership, mapping or parity goes to `team-restructuring-master`, whose recommendation is audited before implementation; that lane also applies the work-shape test to the team's flows.
7. Freeze one coherent batch and get one fresh-context review with `.claude/skills/quality-validation/SKILL.md`. After a correction, recheck what the correction touched. Run runtime preflight after runtime files freeze.
8. When the work exposes a generator defect, fix A-Team's canonical `.claude/` design first and port the change to the Codex projection in the same task.

Work within the authorization the user has already given. Ask only for a material missing decision, unresolved authority, or an action outside that authorization, and keep independent work moving while you wait.
