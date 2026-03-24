# A-Team

A-Team is a **team designer**, not a target team. It interviews users, decomposes responsibilities, plans skills and rules, and generates ready-to-run multi-agent team structures under `teams/{team-name}/`.

## Design Philosophy

### Boil the Lake

When the complete version costs only marginally more than the shortcut, produce the complete version. AI-assisted generation compresses effort dramatically — full test coverage, all edge cases, complete error paths, comprehensive documentation. Do not cut corners when completeness is cheap.

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

## Communication

Communicate in the user's language. Detect and match the language the user is using. Technical terms may remain in English.

Point out issues directly when the user's ideas are unreasonable — always provide alternative solutions alongside.

## Phase Overview

| Phase | Purpose | Agent(s) |
|-------|---------|----------|
| 1. Discovery | Requirements interview + role decomposition + domain research | `requirements-analyst`, `role-designer`, `domain-researcher` |
| 2. Planning | Skill/rule planning with external skill search | `skill-planner` |
| 3. Generation | CLAUDE.md + folder structure + file generation | `rule-writer`, `skill-writer`, `agent-writer` |
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
- A coordinator (flat architecture, no sub-coordinators)
- A process reviewer (separate from QA)
- A code reviewer (separate from QA testing)
- Worklog rule and context management rule in `rules/`
- Worklog and context management section in CLAUDE.md

## Dual-Platform

This repo maintains both Claude Code (`.claude/`) and Codex (`.codex/`, `AGENTS.md`) configurations. The `.claude/` tree is the source design for Claude Code. See `AGENTS.md` for the Codex runtime entrypoint.
