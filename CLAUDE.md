# A-Team

A-Team is a **team designer**, not a target team. It interviews users, decomposes responsibilities, plans skills and rules, and generates ready-to-run multi-agent team structures under `teams/{team-name}/`.

## Design Philosophy

### Complete Deliverables, Focused Context

Optimize prompt effectiveness first using current official guidance for the selected platform and model. Preserve useful examples, XML boundaries, task steps, and verification even when they require more context; concision is secondary. Complete the requested outcome and verify the behavior that matters. Add tests, detail, or safeguards when they cover a concrete requirement or credible failure; stop broadening checks once the applicable acceptance criteria pass.

Keep one authoritative statement of each policy. Load role-specific references on demand; use compact task-specific decision notes and checks instead of repeated generic reasoning forms. Preserve executable contracts and meaningful examples when shortening prompts.

### Search Before Building

Inspect unfamiliar project context and verify current tools or external facts before decisions that depend on them. Use evidence and first-principles analysis to choose the smallest adequate design; routine implementation choices do not require a new research phase.

### Position Over Hedging

Every recommendation must state a clear position with evidence. Vague agreement, false balance, and non-committal language are prohibited. See `.claude/rules/anti-sycophancy.md`.

### Proportional Design

Default to the cheapest adequate design. Only when proposing or retaining a non-obvious safeguard, apply `.claude/rules/proportional-design.md`: show the evidence and likelihood, protected impact, cheapest adequate alternative, ordinary-path cost and new failure modes, and removal, override, or monitoring trigger. Unsupported rare hypotheticals become assumptions or monitoring, not code or release blockers. Preserve justified high-impact controls without breaking routine configuration, update, deployment, restart, or recovery paths.

## Deployment Mode

This project uses **subagent mode**. The coordinator (`team-architect`) delegates specialist work via the Agent tool (`Task` is its legacy alias). All agents run within a single Claude Code session.

The coordinator role executes in the MAIN session: when `/A-Team` is invoked, the current session adopts `.claude/agents/team-architect.md` as its playbook. Never spawn the coordinator as a subagent. Claude Code supports nested subagents; A-Team's native policy keeps delegation and user conversation with the main-session coordinator, enforced by `disallowedTools: [Agent]` on its direct specialists. A specialist that needs user input ends its run with `NEEDS_CONTEXT` and a QUESTIONS block; the coordinator relays the questions, appends every exchange to the task's `.worklog/{yyyymm}/{task-name}/dialogue-log.md`, and re-dispatches with the answers.

## Execution Contract and Precedence

Follow `.claude/rules/execution-contract.md` for specialist reports, retries, fresh-context acceptance, precedence, and context economy. Host system/developer instructions and explicit user instructions take precedence over repository guidance and skills. Local rule precedence is defined by EC-4. Judgment rubrics live in `JUDGMENT.md`; dispatch templates live in `templates/`.

Accept coherent frozen artifact batches with an independent reviewer. After a correction, invalidate every criterion citing a changed file and dependent mapping/parity criteria; recheck them before acceptance. Preserve valid unrelated evidence.

Assign evidence persistence at dispatch. When the selected runtime prevents a specialist from writing its report, use the bounded `INLINE-FALLBACK` in the execution contract and let the coordinator persist the returned evidence. Keep the specialist's sandbox intact.

## Communication

Communicate in the user's language. Detect and match the language the user is using. Technical terms may remain in English.

Point out issues directly when the user's ideas are unreasonable — always provide alternative solutions alongside.

Treat an action request as authorization for its scoped reversible work. Reuse confirmed requirements and existing authorization; ask only for a material missing choice, unresolved authority, or an unapproved scope expansion or irreversible/external action. Interim summaries are nonblocking. Continue independent work while a question is pending; a required answer is never inferred from silence.

## Phase Overview

| Phase | Purpose | Agent(s) |
|-------|---------|----------|
| 1. Discovery | Requirements interview + role decomposition + domain research | `requirements-analyst`, `role-designer`, `domain-researcher` |
| 2. Planning | Skill/rule planning with external skill search | `skill-planner` |
| 3. Generation | Canonical entry document + requested runtime projection | `rule-writer`, `skill-writer`, `agent-writer` |
| 3.5 Preflight | Probe the selected live runtime, write `docs/RUNTIME-SETUP.md` | `runtime-preflight-advisor` |
| 4. Optimization | Prompt review and refinement (optional) | `prompt-optimizer` |
| 5. Review | Structure validation + user feedback | `team-architect` |
| 6. Dialogue Review | Retrospective after substantial discovery or when requested | `dialogue-reviewer` |
| 7. Evolution | Optimize or restructure an existing generated team, including its Codex runtime (on-demand) | `prompt-optimizer`, `team-restructuring-master` |

Cross-phase support agents (available at any phase):
- `domain-researcher` — External domain investigation and best practice research
- `decision-auditor` — Independent audit of design decisions at phase boundaries

## Existing-Team Evolution

Choose the requested scope first: A-Team capability maintenance, maintenance of named target teams, or explicitly requested fleet work. Improving A-Team's ability to restructure prior teams authorizes designer changes; it does not itself request a target inventory, downstream writes, or target-authority questions. Use a bounded read-only example only when needed to reproduce a designer defect.

Existing A-Team outputs are not assumed to share one runtime layout or one canonical authority. Before changing a team, classify its layout and runnable surfaces, compare generation stamps, and read its mapping/manifest. Respect the team's explicit canonical declaration; an ambiguous declaration permits assessment only, and a reference-only mirror is never promoted implicitly.

Use the optimization lane only when roles, rules, runtime, ownership, mapping, canonical authority, and parity behavior stay unchanged: `prompt-optimizer` tightens the owned text, then `decision-auditor` verifies it. Structural, runtime, ownership, mapping, or parity changes use `team-restructuring-master` for the smallest-change plan, an independent recommendation audit, targeted writers, a fresh artifact audit, and runtime preflight when runtime files changed. Record how existing user authorization covers the plan; obtain approval for any uncovered material change before implementing it. Scoped maintenance does not restart a new-team interview.

Classify every restructuring gap as either `Codex-only runtime gap` or `cross-platform design gap`. A platform-only change must already be allowed by the team's mapping inventory. A cross-platform gap starts at that team's declared canonical source and regenerates only affected projections. If the gap exposes an A-Team generator defect, backport the fix to this repository's canonical `.claude/` design and regenerate A-Team's Codex surfaces in the same maintenance task.

Generated-team work normally stays under `teams/{team-name}/`. A writer may work at an external target root only when the user explicitly authorizes that exact real root, the dispatch names exact owned paths, and one canonical authority is declared consistently: Claude authority uses `CLAUDE.md` as its declaration, Codex authority uses `AGENTS.md`, and platform-neutral authority uses `shared/team.yaml`. Every other runnable entry and every required mapping artifact must agree; multi-surface or conversion-retained teams require `.codex/docs/format-mapping.manifest.yaml`. Missing or conflicting authority, dual-canonical claims, reference-only promotion, incomplete required mappings, `..` traversal, an outside absolute path, or a root/owned-path/nearest-parent symlink escape fails closed without writing. Edit the declared canonical family first and regenerate only mapped projections sequentially under the same owner, with scoped verification and rollback evidence.

## Worklog

Structure, required files, and the evidence chain live in `.claude/rules/worklog.md`; context-offloading behavior in `.claude/rules/context-management.md`. Both load unconditionally, so this section points rather than restates — a second copy is paid on every session and every dispatch, and drifts.

## Output

All generated teams go to `teams/{team-name}/`. The structure follows `.claude/rules/output-structure.md`.

Every generated team must include:
- A coordinator (flat architecture, no sub-coordinators; runs in the main session, never spawned)
- Process review duties separate from QA, with a dedicated reviewer unless the small-team exception in `reviewer-mandate.md` applies
- A code reviewer (separate from QA testing) when the team's deliverables include executable artifacts; a deliverable-QA reviewer otherwise
- Worklog, context management, reasoning/self-critique, and execution contract rules in the selected runtime tree
- A proportional-design rule in the declared canonical family, projected to every requested runtime; relevant producers use the conditional safeguard slot and an existing independent reviewer returns its criterion-level verdict
- Worklog/context, precedence, deployment, and generator-stamp sections in the selected root entry document
- A format mapping and machine-readable manifest whenever conversion retention or dual-format output is requested
- `docs/RUNTIME-SETUP.md` from Phase 3.5 — what the user must configure outside the team before first run

Claude-runnable output additionally includes the output-mode component: `.claude/output-styles/adhd-friendly.md` copied verbatim from A-Team, plus the first-run ask hook in `settings.json`. Codex-runnable output instead includes project `.codex/config.toml`, a runtime agent registry, runtime-discoverable `.agents/skills/`, strict-config validation, and a current Subagents/multi-agent preflight.

Some runtime configuration cannot ship inside a generated team. Claude Code's auto-mode carve-outs are honored only from user settings, and no agent may write them — attempting it is a classified violation. A-Team's answer is advisory: probe the live runtime, emit a document plus a user-run command. See `.claude/rules/settings-json.md` (Auto Mode Reality) and `scripts/preflight-permissions.sh`.

## Dual-Platform

This A-Team repository keeps `.claude/` plus `CLAUDE.md` canonical for shared role intent, workflow, ownership, authority, and quality. `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/` are the Codex projection, with bounded native runtime details supplied by the inventoried Codex adaptation inputs. Shared design changes start here; platform-specific settings do not become instructions for the other host. See `rules/dual-platform-parity.md` and `.codex/docs/claude-adaptation-manifest.toml` for exact input scopes and projection targets.

Generated teams follow the format and canonical authority confirmed during their own Discovery, not A-Team's self-hosting authority automatically. Their mapping artifacts control future conversion and restructuring.

Only when producing or maintaining a Codex surface, read `.codex/rules/codex-runtime-config.md`, `.codex/rules/codex-agent-config-patterns.md`, and `.codex/rules/context-isolation.md` for that target's runtime specification. Claude-only work uses native Claude rules and probes; it does not load or copy Codex model profiles, schema, or dispatch controls. Preserve the target's explicit model and effort choices unless their migration is authorized.

---

Generated by A-Team on 2026-10-06
