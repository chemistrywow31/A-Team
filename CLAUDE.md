# A-Team

A-Team is a **team designer**, not a target team. It interviews users, decomposes responsibilities, plans skills and rules, and generates ready-to-run multi-agent team structures under `teams/{team-name}/`.

## Deployment Mode

This project uses **subagent mode**. The coordinator (`team-architect`) delegates specialist work via the Task tool. All agents run within a single Claude Code session.

## Communication

Communicate in the user's language. Detect and match the language the user is using. Technical terms may remain in English.

Point out issues directly when the user's ideas are unreasonable — always provide alternative solutions alongside.

## Phase Overview

| Phase | Purpose | Agent(s) |
|-------|---------|----------|
| 1. Discovery | Requirements interview + role decomposition | `requirements-analyst`, `role-designer` |
| 2. Planning | Skill/rule planning with external skill search | `skill-planner` |
| 3. Generation | CLAUDE.md + folder structure + file generation | `rule-writer`, `skill-writer`, `agent-writer` |
| 4. Optimization | Prompt review and refinement (optional) | `prompt-optimizer` |
| 5. Review | Structure validation + user feedback | `team-architect` |
| 6. Dialogue Review | Consultation quality audit (mandatory) | `dialogue-reviewer` |
| 7. Restructuring | Evaluate and restructure existing teams (on-demand) | `team-restructuring-master` |

## Output

All generated teams go to `teams/{team-name}/`. The structure follows `.claude/rules/output-structure.md`.

Every generated team must include:
- A coordinator (flat architecture, no sub-coordinators)
- A process reviewer (separate from QA)
- A code reviewer (separate from QA testing)
- Context management guidelines in CLAUDE.md or rules/

## Dual-Platform

This repo maintains both Claude Code (`.claude/`) and Codex (`.codex/`, `AGENTS.md`) configurations. The `.claude/` tree is the source design for Claude Code. See `AGENTS.md` for the Codex runtime entrypoint.
