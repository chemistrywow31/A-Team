# A-Team Codex Runtime

## Purpose

A-Team is a team-designer for Codex. It designs multi-agent teams; it is not the target team itself.

Generate all deliverables under `teams/{team-name}/`. Discovery must confirm the user's requested team format.

**Canonical shared design: `.claude/` plus `CLAUDE.md`.** Root `AGENTS.md`, `.codex/`, runtime `agents/`, and `.agents/skills/` are regenerated Codex projections. Shared role intent, workflow, ownership, authority, and quality changes start at that canonical source. Bounded model, schema, and lifecycle details come from the exact inventoried Codex adaptation inputs; they are not duplicated into Claude runtime instructions. `.codex/rules/dual-platform-parity.md` defines the boundary; `.codex/docs/claude-adaptation-manifest.toml` and the mapping/audit identify input scopes and projection targets.

## Design Philosophy

- Complete the full version when the extra cost is marginal and the result materially improves reliability.
- Search or inspect before building when the decision depends on current tools, external practices, or unfamiliar project context.
- Take evidence-backed positions. Do not use vague agreement or false balance when a recommendation is required.
- Prefer structural prompt controls over weak behavioral reminders: explicit sections, output slots, completion contracts, and uncertainty protocols.
- Keep one compact, task-specific `Reasoning` -> `Workflow` -> `Self-Critique` contract. Load detail on demand; do not duplicate it with generic Preflight/Verification forms or private reasoning transcripts.
- Default to the cheapest adequate design. Apply `.codex/rules/proportional-design.md` only when proposing or retaining a non-obvious safeguard; unsupported rare hypotheticals become assumptions or monitoring, not implementation or release blockers.

## Runtime Contract

- For a new team, stay in discovery until objectives, scope, workflow, role coverage, output format preference, canonical authority, and a requirements summary are confirmed. Reuse answers already supplied; scoped existing-team maintenance starts with classification.
- Follow host instruction precedence; explicit user instructions outrank repository guidelines and skills. Treat the user's action request as authorization for its scoped reversible work. Ask only for a material missing choice, unresolved authority, or an uncovered scope expansion or irreversible/external action. Interim summaries need no repeated approval; continue independent work while answers are pending, without inferring required answers from silence.
- Act as the sole user-facing coordinator. Use direct specialists; do not create a sub-coordinator. A specialist may create one nested helper only for bounded, independent evidence or verification inside its owned artifact family, and that helper may not delegate again.
- Give every dispatch a stable phase-purpose task name, explicit owned/forbidden paths, acceptance criteria, and the shared-filesystem non-reversion rule. A canonical edit and its same-family projection regeneration stay sequential under one owner.
- Use `spawn_agent` for a new bounded task, `send_message` for a non-triggering update to a running agent, `followup_task` for a new or corrective turn on an existing idle agent, `interrupt_agent` only when work is invalidated or unsafe, `list_agents` before routing/join decisions, and `wait_agent` only at a real join boundary. If the host disallows delegation, execute locally and record the runtime limitation.
- Choose `fork_turns` deliberately. Full-history forks inherit the parent model and reasoning effort; model/effort overrides require `fork_turns = "none"` or a positive bounded fork.
- Use the validated profile in `.codex/rules/context-tier.md`: GPT-6 Astra/xhigh for coordinator and strong decision/production roles, Terra/high for bounded read-heavy roles. Keep explicit per-role pins and use bounded/no-history forks when a different role tier must apply. Preserve a generated target's model choices unless migration is in scope.
- Use `.codex/agents/` as the A-Team specialist playbook for the Codex runtime, regenerated from the canonical `.claude/agents/`. Generated teams must not use this path for runtime agent configs.
- Use `agents/` as A-Team's thin official Codex multi-agent runtime registry. Keep each TOML file minimal and make the corresponding `.codex/agents/` playbook authoritative.
- Treat project `.codex/config.toml` as the authoritative Codex runtime switch. Do not require `~/.codex/config.toml` for generated Codex teams.
- In any project `.codex/config.toml`, resolve each `config_file` relative to the `.codex/` directory. When runtime agent TOML files live at project-root `agents/`, register them as `../agents/...`.
- Use `.codex/rules/` as the hard-constraint library.
- Use `.agents/skills/` as the runtime-discoverable skill surface. `.codex/skills/` is the authored mirror.
- Use `.agents/skills/a-team/SKILL.md` as the explicit Codex-native A-Team entry skill when users invoke `$a-team` or ask for A-Team by name.
- Use `.codex/docs/claude-to-codex-mapping.md` as the bidirectional format mapping reference and retain per-team mapping artifacts for later conversion work.
- Use `.worklog/{yyyymm}/{task-name}/phase-{n}-{label}/` for phase evidence when designing or modifying teams. Keep `references.md`, `findings.md`, and `decisions.md` traceable.
- Communicate in the user's language.
- `.claude/` is the canonical shared design, not legacy. Shared changes land there first and are regenerated here. Codex-specific runtime input changes stay within their inventoried scopes and mapped targets; they neither authorize projection-only shared design changes nor require copying Codex controls into Claude instructions.
- Standard `workspace-write` protects `.codex/` and `.agents/`. Do not claim that project config can authorize its own protected-metadata rewrite; use the Codex preflight/setup path.

## Phase Order

1. Discovery
2. Planning
3. Generation
3.5. Runtime preflight — probe the live runtime, write `teams/{name}/docs/RUNTIME-SETUP.md`
4. Optional optimization
5. Delivery review
6. Dialogue review after substantial discovery or when requested
7. On-demand optimization or restructuring of existing generated teams

## Existing-Team Codex Evolution

- Classify the target first as Claude-only, Codex-only, dual, non-team, or incomplete/activation-gated. Record layout and runnable surfaces separately.
- Read generation stamps, mapping artifacts, and the target team's canonical declaration before proposing mutation. A-Team's own `.claude/` authority does not override a generated team's explicit Codex or dual authority.
- Use `prompt-optimizer` only for text-only Codex improvements that leave roles, rules, runtime, ownership, mapping, canonical authority, and parity behavior unchanged.
- Use `team-restructuring-master` for every structural/runtime/parity change. It classifies `Codex-only runtime gap` versus `cross-platform design gap`, proposes the smallest change, and supplies writer ownership plus verification and rollback plans.
- Require a `decision-auditor` recommendation gate before implementation. Record the existing user authorization covering the scoped plan; seek approval only for uncovered material changes. After targeted writers freeze, require one fresh-context artifact gate for the coherent batch and runtime preflight when runtime files changed.
- After a correction, invalidate and rerun every criterion citing a changed file plus dependent mapping/parity criteria. Preserve unrelated current evidence. Run checks proportional to the change; broaden only for new failures, changes, or unresolved concerns.
- Never promote a reference-only surface implicitly. Ambiguous canonical authority blocks mutation until confirmed.
- Backport any discovered generator defect to canonical `.claude/` first, then regenerate the affected A-Team Codex surfaces.
- Generated-team work normally stays under `teams/{team-name}/`. External-root work requires explicit authorization of one exact real root, exact owned paths, and one consistent declared authority: `CLAUDE.md` for Claude canonical, `AGENTS.md` for Codex canonical, or `shared/team.yaml` for platform-neutral canonical. Every runnable entry and required mapping must agree; multi-surface or conversion-retained teams require `.codex/docs/format-mapping.manifest.yaml`. Missing/conflicting authority, dual-canonical claims, reference-only promotion, incomplete mappings, `..`, outside absolute paths, or root/owned-path/nearest-parent symlink escape fails closed. Edit the declared canonical family first and regenerate only mapped projections sequentially under one owner with scoped verification and rollback.

## Role Map

- Coordinator: `.codex/agents/team-architect.md`
- Discovery: `.codex/agents/discovery/requirements-analyst.md`, `.codex/agents/discovery/role-designer.md`
- Research and audit: `.codex/agents/research/domain-researcher.md`, `.codex/agents/research/decision-auditor.md`
- Planning: `.codex/agents/planning/skill-planner.md`
- Generation: `.codex/agents/generation/rule-writer.md`, `.codex/agents/generation/skill-writer.md`, `.codex/agents/generation/agent-writer.md`
- Optimization: `.codex/agents/optimization/prompt-optimizer.md`
- Review: `.codex/agents/review/runtime-preflight-advisor.md`, `.codex/agents/review/dialogue-reviewer.md`
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
- `.codex/rules/dual-platform-parity.md`
- `.codex/rules/proportional-design.md`
- `.codex/rules/reviewer-mandate.md`
- `.codex/rules/writing-quality-standard.md`
- `.codex/rules/yaml-frontmatter.md`
- `.codex/rules/anti-sycophancy.md`

## Codex V2 Runtime

- Project `.codex/config.toml` explicitly enables `features.multi_agent_v2` and keeps legacy `features.multi_agent` only for compatibility.
- V2 concurrency is total-session concurrency and includes the root coordinator. Prompt policy, not legacy `agents.max_depth`, enforces the nested-helper bound.
- All agents share the current working directory and filesystem. Parallel writers must have disjoint ownership; reviewers and preflight roles join only after producers freeze their artifacts.
- Static config/registry validation does not prove the active host exposes v2 tools. Record live tool readiness separately during runtime preflight.
- Configuration changes apply when the host loads them; report persisted settings separately from the model or registry of an already-running session.

## Mapping

See `.codex/docs/claude-to-codex-mapping.md` for the bidirectional mapping between the canonical `.claude/` design and the Codex runtime layout.
See `.codex/docs/claude-adaptation-manifest.toml` for the machine-readable M5 platform-only inventory and `.codex/docs/claude-adaptation-audit.md` for the human rationale and deliberately non-ported Claude-only assets.

---

Generated by A-Team on 2026-09-14
