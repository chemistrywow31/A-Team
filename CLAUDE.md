# A-Team

A-Team is a **team designer**, not a target team. It interviews users, decomposes responsibilities, plans skills and rules, and generates ready-to-run multi-agent team structures under `teams/{team-name}/`.

## Design Philosophy

### Boil the Lake — for deliverables, not for context

When the complete version costs only marginally more than the shortcut, produce the complete version. AI-assisted generation compresses authoring effort dramatically — full test coverage, all edge cases, complete error paths, comprehensive documentation. Do not cut corners when completeness is cheap.

Completeness is cheap to *write* and expensive to *carry*. Text in an always-loaded file is re-injected into the main session and into every subagent dispatch — 12–15 times per run, forever; text in a file read on demand is paid once, when needed. So: be exhaustive in what A-Team **produces**, and ruthless about what A-Team **carries**.

Before adding a line to an always-loaded file, answer two questions. **Does something execute it** — `scripts/validate-team.sh`, a dispatched verifier, a hook? If nothing does, it is decoration; build the check or drop the line. Measured: requirements with a mechanical check are met ~100% of the time, requirements without one ~1%. **Does it need to be loaded before the agent asks for it?** If not, `paths`-scope it, move it into a skill, or cite it by path. A rule that is right as a specification for generated teams and wrong as always-on context gets relocated, not deleted.

### Search Before Building

Apply three layers of knowledge before making any design decision:
1. **Layer 1 — Established patterns**: Known best practices and industry standards
2. **Layer 2 — Current trends**: Recent community practices and popular approaches
3. **Layer 3 — First-principles reasoning**: Original analysis of why conventional wisdom may not apply

Prize Layer 3 insights above all. Search and understand Layers 1-2, then apply Layer 3 to discover what the standard approach misses.

### Position Over Hedging

Every recommendation must state a clear position with evidence. Vague agreement, false balance, and non-committal language are prohibited. See `.claude/rules/anti-sycophancy.md`.

## Deployment Mode

This project uses **subagent mode**. The coordinator (`team-architect`) delegates specialist work via the Task tool. All agents run within a single Claude Code session.

The coordinator role executes in the MAIN session: when `/A-Team` is invoked, the current session adopts `.claude/agents/team-architect.md` as its playbook. Never spawn the coordinator as a subagent — subagents cannot dispatch further agents and cannot converse with the user. A specialist that needs user input ends its run with `NEEDS_CONTEXT` and a QUESTIONS block; the coordinator relays the questions, appends every exchange to the task's `.worklog/{yyyymm}/{task-name}/dialogue-log.md`, and re-dispatches with the answers.

## Execution Contract and Precedence

Every agent follows `.claude/rules/execution-contract.md`: EC-1 six-field report schema, EC-2 escalation ladder (haiku: zero retries; sonnet: one changed-approach retry; global cap 3 attempts plus one escalation attempt at an untried higher tier), EC-3 fresh-context verification — a producer never accepts its own work, EC-4 precedence, EC-5 context economy (paths not pastes; 60-line message cap; task reports max 40 lines). When instructions conflict, cite EC-4: safety > charter (CLAUDE.md + contract) > verification > reporting > escalation > other rules > dispatch instructions > style. Judgment rubrics live in `JUDGMENT.md` (J1 escalate, J2 done, J3 stop-and-ask, J4 wrong-direction, J5 quality floors); dispatches are built from `templates/`.

## Communication

Communicate in the user's language. Detect and match the language the user is using. Technical terms may remain in English.

Point out issues directly when the user's ideas are unreasonable — always provide alternative solutions alongside.

## Phase Overview

| Phase | Purpose | Agent(s) |
|-------|---------|----------|
| 1. Discovery | Requirements interview + role decomposition + domain research | `requirements-analyst`, `role-designer`, `domain-researcher` |
| 2. Planning | Skill/rule planning with external skill search | `skill-planner` |
| 3. Generation | CLAUDE.md + folder structure + file generation | `rule-writer`, `skill-writer`, `agent-writer` |
| 3.5 Preflight | Probe the live permission runtime, write `docs/RUNTIME-SETUP.md` | `runtime-preflight-advisor` |
| 4. Optimization | Prompt review and refinement (optional) | `prompt-optimizer` |
| 5. Review | Structure validation + user feedback | `team-architect` |
| 6. Dialogue Review | Consultation quality audit (mandatory) | `dialogue-reviewer` |
| 7. Restructuring | Evaluate and restructure existing teams (on-demand) | `team-restructuring-master` |

Cross-phase support agents (available at any phase):
- `domain-researcher` — External domain investigation and best practice research
- `decision-auditor` — Independent audit of design decisions at phase boundaries

## Worklog

All work is documented in `.worklog/yyyymm/task-name/phase-n-label/` with three core files per phase:
- `references.md` — Sources consulted
- `findings.md` — Key discoveries and analysis
- `decisions.md` — Decisions with rationale, alternatives, and evidence chain

The worklog serves dual purpose: **verifiable decision trail** and **context offloading** (agents read from worklog instead of carrying full context). See `.claude/rules/worklog.md` and `.claude/rules/context-management.md`.

## Output

All generated teams go to `teams/{team-name}/`. The structure follows `.claude/rules/output-structure.md`.

Every generated team must include:
- A coordinator (flat architecture, no sub-coordinators; runs in the main session, never spawned)
- A process reviewer (separate from QA)
- A code reviewer (separate from QA testing) when the team's deliverables include executable artifacts; a deliverable-QA reviewer otherwise
- Worklog rule, context management rule, and execution contract rule in `rules/`
- Worklog and context management section, precedence order, and generator version stamp in CLAUDE.md
- `docs/RUNTIME-SETUP.md` from Phase 3.5 — what the user must configure outside the team before first run

Some runtime configuration cannot ship inside a generated team. Claude Code's auto-mode carve-outs are honored only from user settings, and no agent may write them — attempting it is a classified violation. A-Team's answer is advisory: probe the live runtime, emit a document plus a user-run command. See `.claude/rules/settings-json.md` (Auto Mode Reality) and `scripts/preflight-permissions.sh`.

## Dual-Platform

This repo maintains four trees: `.claude/` (canonical source design), `.codex/` + `AGENTS.md` (Codex runtime), `agents/**.toml` (Codex runtime registry), `.agents/skills/` (Codex skill surface). **`.claude/` is canonical; the other three are regenerated from it and never hand-edited** (`rules/dual-platform-parity.md` M1/M2). Fix defects in `.claude/` first, then regenerate. `AGENTS.md` is the Codex entrypoint; `.codex/docs/claude-adaptation-audit.md` is the M5 platform-only inventory.

---

Generated by A-Team on 2026-07-25
