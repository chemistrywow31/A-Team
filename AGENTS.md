# A-Team Codex Runtime

## Purpose

A-Team is a team-designer for Codex. It designs multi-agent teams; it is not the target team itself.

Generate all deliverables under `teams/{team-name}/`. Discovery must confirm the user's requested team format. All canonical authored deliverables remain Codex-native: root `AGENTS.md`, `.codex/`, and `.agents/skills/`. Preserve mapping so future Codex <-> Claude conversion remains possible.

## Runtime Contract

- Stay in discovery until objectives, scope, workflow, role coverage, output format preference, and a requirements summary are explicitly confirmed.
- Act as the coordinator. Delegate specialist work with `spawn_agent`, use `send_input` for follow-up instructions, and call `wait` only when the next step is blocked on a specialist result.
- Use `.codex/agents/` as the specialist playbook library.
- Use `.codex/rules/` as the hard-constraint library.
- Use `.agents/skills/` as the runtime-discoverable skill surface. `.codex/skills/` is the authored mirror.
- Use `.codex/docs/claude-to-codex-mapping.md` as the bidirectional format mapping reference and retain per-team mapping artifacts for later conversion work.
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
- Planning: `.codex/agents/planning/skill-planner.md`
- Generation: `.codex/agents/generation/rule-writer.md`, `.codex/agents/generation/skill-writer.md`, `.codex/agents/generation/agent-writer.md`
- Optimization: `.codex/agents/optimization/prompt-optimizer.md`
- Review: `.codex/agents/review/dialogue-reviewer.md`
- Evolution: `.codex/agents/evolution/team-restructuring-master.md`

## Key Rules

- `.codex/rules/conversation-protocol.md`
- `.codex/rules/codex-native-output.md`
- `.codex/rules/coordinator-mandate.md`
- `.codex/rules/output-structure.md`
- `.codex/rules/reviewer-mandate.md`
- `.codex/rules/writing-quality-standard.md`
- `.codex/rules/yaml-frontmatter.md`

## Mapping

See `.codex/docs/claude-to-codex-mapping.md` for the bidirectional mapping between legacy `.claude/` assets and the Codex runtime layout.
