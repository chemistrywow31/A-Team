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
| 3. Generation | Canonical entry document + requested runtime projection | `rule-writer`, `skill-writer`, `agent-writer` |
| 3.5 Preflight | Probe the selected live runtime, write `docs/RUNTIME-SETUP.md` | `runtime-preflight-advisor` |
| 4. Optimization | Prompt review and refinement (optional) | `prompt-optimizer` |
| 5. Review | Structure validation + user feedback | `team-architect` |
| 6. Dialogue Review | Consultation quality audit (mandatory) | `dialogue-reviewer` |
| 7. Evolution | Optimize or restructure an existing generated team, including its Codex runtime (on-demand) | `prompt-optimizer`, `team-restructuring-master` |

Cross-phase support agents (available at any phase):
- `domain-researcher` — External domain investigation and best practice research
- `decision-auditor` — Independent audit of design decisions at phase boundaries

## Existing-Team Codex Evolution

Existing A-Team outputs are not assumed to share one runtime layout or one canonical authority. Before changing a team, classify its layout and runnable surfaces, compare generation stamps, and read its mapping/manifest. Respect the team's explicit canonical declaration; an ambiguous declaration permits assessment only, and a reference-only mirror is never promoted implicitly.

Use the optimization lane only when roles, rules, runtime, ownership, mapping, canonical authority, and parity behavior stay unchanged: `prompt-optimizer` tightens the owned Codex text, then `decision-auditor` verifies it. Any structural, runtime, ownership, mapping, or parity change uses the restructuring lane: `team-restructuring-master` produces the smallest-change plan, `decision-auditor` audits the recommendation, the user approves it, targeted writers implement it, and fresh verification plus runtime preflight close the change.

Classify every restructuring gap as either `Codex-only runtime gap` or `cross-platform design gap`. A platform-only change must already be allowed by the team's mapping inventory. A cross-platform gap starts at that team's declared canonical source and regenerates only affected projections. If the gap exposes an A-Team generator defect, backport the fix to this repository's canonical `.claude/` design and regenerate A-Team's Codex surfaces in the same maintenance task.

## Worklog

Structure, required files, and the evidence chain live in `.claude/rules/worklog.md`; context-offloading behavior in `.claude/rules/context-management.md`. Both load unconditionally, so this section points rather than restates — a second copy is paid on every session and every dispatch, and drifts.

## Output

All generated teams go to `teams/{team-name}/`. The structure follows `.claude/rules/output-structure.md`.

Every generated team must include:
- A coordinator (flat architecture, no sub-coordinators; runs in the main session, never spawned)
- A process reviewer (separate from QA)
- A code reviewer (separate from QA testing) when the team's deliverables include executable artifacts; a deliverable-QA reviewer otherwise
- Worklog, context management, reasoning/self-critique, and execution contract rules in the selected runtime tree
- Worklog/context, precedence, deployment, and generator-stamp sections in the selected root entry document
- A format mapping and machine-readable manifest whenever conversion retention or dual-format output is requested
- `docs/RUNTIME-SETUP.md` from Phase 3.5 — what the user must configure outside the team before first run

Claude-runnable output additionally includes the output-mode component: `.claude/output-styles/adhd-friendly.md` copied verbatim from A-Team, plus the first-run ask hook in `settings.json`. Codex-runnable output instead includes project `.codex/config.toml`, a runtime agent registry, runtime-discoverable `.agents/skills/`, strict-config validation, and a current Subagents/multi-agent preflight.

Some runtime configuration cannot ship inside a generated team. Claude Code's auto-mode carve-outs are honored only from user settings, and no agent may write them — attempting it is a classified violation. A-Team's answer is advisory: probe the live runtime, emit a document plus a user-run command. See `.claude/rules/settings-json.md` (Auto Mode Reality) and `scripts/preflight-permissions.sh`.

## Dual-Platform

This A-Team repository maintains four trees: `.claude/` (canonical source design), `.codex/` + `AGENTS.md` (Codex runtime), `agents/**.toml` (Codex runtime registry), and `.agents/skills/` (Codex skill surface). **For A-Team itself, `.claude/` is canonical; the other three are regenerated from it and never fixed in isolation** (`rules/dual-platform-parity.md` M1/M2). `AGENTS.md` is the Codex entrypoint; `.codex/docs/claude-adaptation-manifest.toml` is the machine-readable M5 inventory and `.codex/docs/claude-adaptation-audit.md` explains its adaptation decisions.

Generated teams follow the format and canonical authority confirmed during their own Discovery, not A-Team's self-hosting authority automatically. Their mapping artifacts control future conversion and restructuring.

The Codex projection prefers current Subagents / multi-agent tools and explicitly enables the v2 task-path runtime. Agents share the same filesystem, so every parallel dispatch carries non-overlapping path ownership. Standard `workspace-write` protects `.codex/` and `.agents/`; project config cannot authorize its own rewrite, so preflight documents the required approval/bootstrap posture.

---

Generated by A-Team on 2026-08-05
