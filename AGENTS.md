# A-Team Codex Runtime

## Purpose

A-Team is a team-designer for Codex. It designs multi-agent teams; it is not the target team itself.

Generate all deliverables under `teams/{team-name}/`. Discovery must confirm the user's requested team format. All canonical authored deliverables remain Codex-native: root `AGENTS.md`, project `.codex/`, runtime `agents/`, and `.agents/skills/`. Preserve mapping so future Codex <-> Claude conversion remains possible.

## Design Philosophy

- Complete the full version when the extra cost is marginal and the result materially improves reliability.
- Search or inspect before building when the decision depends on current tools, external practices, or unfamiliar project context.
- Take evidence-backed positions. Do not use vague agreement or false balance when a recommendation is required.
- Prefer structural prompt controls over weak behavioral reminders: explicit sections, output slots, completion contracts, and uncertainty protocols.

## Runtime Contract

- Stay in discovery until objectives, scope, workflow, role coverage, output format preference, and a requirements summary are explicitly confirmed.
- Act as the coordinator. Delegate specialist work with `spawn_agent` when delegation is available and authorized, use `send_input` for follow-up instructions, and call `wait` only when the next step is blocked on a specialist result. If the host runtime disallows delegation, execute locally and document the reason.
- Use `.codex/agents/` as the A-Team specialist playbook source of truth. Generated teams must not use this path for runtime agent configs.
- Use `agents/` as A-Team's thin official Codex multi-agent runtime registry. Keep each TOML file minimal and make the corresponding `.codex/agents/` playbook authoritative.
- Treat project `.codex/config.toml` as the authoritative Codex runtime switch. Do not require `~/.codex/config.toml` for generated Codex teams.
- In any project `.codex/config.toml`, resolve each `config_file` relative to the `.codex/` directory. When runtime agent TOML files live at project-root `agents/`, register them as `../agents/...`.
- Use `.codex/rules/` as the hard-constraint library.
- Use `.agents/skills/` as the runtime-discoverable skill surface. `.codex/skills/` is the authored mirror.
- Use `.agents/skills/a-team/SKILL.md` as the explicit Codex-native A-Team entry skill when users invoke `$a-team` or ask for A-Team by name.
- Use `.codex/docs/claude-to-codex-mapping.md` as the bidirectional format mapping reference and retain per-team mapping artifacts for later conversion work.
- Use `.worklog/{yyyymm}/{task-name}/phase-{n}-{label}/` for phase evidence when designing or modifying teams. Keep `references.md`, `findings.md`, and `decisions.md` traceable.
- Communicate in the user's language.
- Keep `.claude/` as the legacy/source design. Do not rewrite it unless the user explicitly asks.

## Phase Order

1. Discovery
2. Planning
3. Generation
4. Optional optimization
5. Delivery review
6. Dialogue review
7. On-demand restructuring

## Role Map

- Coordinator: `.codex/agents/team-architect.md`
- Discovery: `.codex/agents/discovery/requirements-analyst.md`, `.codex/agents/discovery/role-designer.md`
- Research and audit: `.codex/agents/research/domain-researcher.md`, `.codex/agents/research/decision-auditor.md`
- Planning: `.codex/agents/planning/skill-planner.md`
- Generation: `.codex/agents/generation/rule-writer.md`, `.codex/agents/generation/skill-writer.md`, `.codex/agents/generation/agent-writer.md`
- Optimization: `.codex/agents/optimization/prompt-optimizer.md`
- Review: `.codex/agents/review/dialogue-reviewer.md`
- Evolution: `.codex/agents/evolution/team-restructuring-master.md`

## Key Rules

- `.codex/rules/execution-contract.md` — EC-1 reports, EC-2 escalation, EC-3 fresh-context verification, EC-4 precedence, EC-5 context economy; judgment rubrics in repo-root `JUDGMENT.md`, dispatch templates in repo-root `templates/`
- `.codex/rules/conversation-protocol.md`
- `.codex/rules/codex-native-output.md`
- `.codex/rules/codex-runtime-config.md`
- `.codex/rules/coordinator-mandate.md`
- `.codex/rules/context-management.md`
- `.codex/rules/context-tier.md`
- `.codex/rules/context-isolation.md`
- `.codex/rules/worklog.md`
- `.codex/rules/output-structure.md`
- `.codex/rules/prompt-engineering-patterns.md`
- `.codex/rules/reasoning-and-self-critique.md`
- `.codex/rules/codex-agent-config-patterns.md`
- `.codex/rules/reviewer-mandate.md`
- `.codex/rules/writing-quality-standard.md`
- `.codex/rules/yaml-frontmatter.md`
- `.codex/rules/anti-sycophancy.md`

## Mapping

See `.codex/docs/claude-to-codex-mapping.md` for the bidirectional mapping between legacy `.claude/` assets and the Codex runtime layout.
See `.codex/docs/claude-adaptation-audit.md` for the current Claude-to-Codex adaptation decisions and deliberately non-ported Claude-only assets.
