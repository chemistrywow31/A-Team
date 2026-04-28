---
name: A-Team
description: Start the A-Team Codex coordinator workflow for designing or restructuring teams
---

# A-Team

## Description

Use this skill when the user asks A-Team to design, generate, review, or restructure an agent team. This is the Codex-native entry skill; it complements `AGENTS.md` instead of replacing it.

## Users

- Team Architect
- Users invoking A-Team explicitly with `$a-team`, `A-Team`, or equivalent wording

## Core Knowledge

- `AGENTS.md` is the project-level runtime contract.
- `.codex/agents/team-architect.md` is the coordinator playbook.
- `.codex/config.toml` registers specialist subagents when multi-agent delegation is available.
- Generated teams must be written under `teams/{team-name}/`.
- `.claude/` remains legacy/source design and must not be modified unless explicitly requested.

## Trigger Rules

Use this skill when the request matches one of these intents:

- create a new Codex team
- design a multi-agent workflow
- generate team files under `teams/{team-name}/`
- restructure an existing generated team
- compare or adapt Claude team assets into Codex-native output

Do not use this skill for unrelated coding tasks inside this repository.

## Execution

1. Read `AGENTS.md`.
2. Read `.codex/agents/team-architect.md`.
3. If the request targets an existing team with new feedback or requirements, run Phase 7 Team Restructuring.
4. Otherwise start Phase 1 Discovery and keep discovery open until objectives, scope, workflow, role coverage, output format, execution mode, and requirements summary are confirmed.
5. Use registered specialists when delegation is available and useful. If delegation is unavailable, execute locally and state the fallback in the worklog or final response.
6. Keep canonical output Codex-native unless the user explicitly requests conversion artifacts.

## Input Handling

### With Arguments

Treat the arguments as the initial team brief. Extract objective, target team name, requested format, and existing team path when present.

### Without Arguments

Ask one focused discovery question: what team the user wants A-Team to design or restructure.

## Boundaries

- Do not modify `.claude/` unless the user explicitly asks for Claude conversion or legacy updates.
- Do not bypass Discovery for a new team.
- Do not use Claude-only fields such as `allowed-tools`, `disable-model-invocation`, or `context: fork` in Codex-native skills.
- Do not place generated runtime agent configs under `.codex/agents/`; use project-root `agents/`.

## Examples

### Normal Case

Input: `$a-team design a research writing team for long-form technical articles`

Output: Start Discovery, confirm requested format and execution mode, then produce the requirements summary before planning.

### Restructuring Case

Input: `$a-team restructure teams/content-studio because review handoffs are too slow`

Output: Run Phase 7, inspect the existing team, classify the handoff problem, and recommend the smallest effective structural change.

### No Arguments

Input: `$a-team`

Output: Ask what team the user wants designed or restructured, then continue Discovery in the user's language.
