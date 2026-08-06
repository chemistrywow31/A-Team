# Claude To Codex Adaptation Audit

## Authority

For A-Team itself, root `CLAUDE.md` and `.claude/` are canonical. Root `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/` are regenerated Codex projections or deliberate Codex-only runtime artifacts. Generated teams retain their own manifest-declared authority.

`.codex/docs/claude-adaptation-manifest.toml` is the machine-readable M5 inventory. This file supplies rationale and must stay in one-to-one agreement with its `platform_only` and `deliberately_not_copied` paths.

## Adaptation Decisions

| Claude Source | Codex Projection | Rationale |
|---|---|---|
| `CLAUDE.md` | `AGENTS.md` | Preserve purpose, phases, gates, and existing-team evolution while translating runtime tools. |
| `.claude/agents/**/*.md` | `.codex/agents/**/*.md` + `agents/**/*.toml` | Keep role semantics; split authoritative Codex playbooks from thin runtime TOML configs. |
| `.claude/skills/*/SKILL.md` | `.codex/skills/*/SKILL.md` + `.agents/skills/*/SKILL.md` | Adapt frontmatter/tool vocabulary; keep authored and runtime Codex copies byte-identical. |
| `.claude/rules/context-management.md` | `.codex/rules/context-management.md` | Map delegation intent to task paths, selective forks, lifecycle tools, joins, and shared-filesystem ownership. |
| `.claude/rules/coordinator-mandate.md` | `.codex/rules/coordinator-mandate.md` | Preserve the single coordinator while allowing one bounded specialist helper hop under v2. |
| `.claude/rules/context-tier.md` | `.codex/rules/context-tier.md` | Map Claude tiers to current GPT-5.6 role/reasoning guidance. |
| `.claude/rules/frontmatter-optional-patterns.md` | `.codex/rules/codex-agent-config-patterns.md` | Codex runtime roles are TOML configs rather than Claude Markdown frontmatter. |
| `.claude/rules/settings-json.md` + `hooks-integration.md` | `.codex/rules/codex-runtime-config.md` | Codex uses trusted project `.codex/config.toml`, sandbox/approval policy, and protected metadata. |
| `.claude/rules/skill-context-fork.md` | `.codex/rules/context-isolation.md` | Codex uses explicit `fork_turns`, task paths, and summary handoffs. |

## Codex-Only Inventory

| Path | Why it is Codex-only |
|---|---|
| `.codex/config.toml` | Project runtime features, approvals, and role registry. |
| `agents/` | Thin official runtime TOML registry configs. |
| `.agents/skills/` | Runtime-discoverable skill mirror. |
| `.codex/docs/claude-to-codex-mapping.md` | Bidirectional adaptation and regeneration contract. |
| `.codex/docs/claude-adaptation-audit.md` | Human M5 rationale. |
| `.codex/docs/claude-adaptation-manifest.toml` | Machine-readable M5 inventory. |
| `.codex/docs/RUNTIME-SETUP.md` | Repo-self Codex setup, verification, and rollback advisory. |
| `.codex/rules/codex-runtime-config.md` | Codex config/schema/protected-path contract. |
| `.codex/rules/codex-agent-config-patterns.md` | Codex agent TOML patterns. |
| `.codex/rules/context-isolation.md` | Codex v2 selective-fork and isolation contract. |
| `scripts/preflight-codex-runtime.sh` | Read-only Codex host/config preflight. |
| `scripts/validate_codex_team.py` | Structured Codex team and repo-self validator. |

## Deliberately Not Copied

| Claude path | Rationale |
|---|---|
| `.claude/settings.json` | Claude Code project settings and hooks have no direct Codex runtime equivalent. |
| `.claude/settings.local.json` | Claude local/user state is not a Codex project artifact. |
| `.claude/output-styles/` | Output styles are Claude Code-only. |
| `.claude/rules/settings-json.md` | Portable intent is adapted into `codex-runtime-config.md`. |
| `.claude/rules/hooks-integration.md` | Claude hook semantics are not copied directly. |
| `.claude/rules/frontmatter-optional-patterns.md` | Portable intent is adapted into Codex TOML patterns. |
| `.claude/rules/skill-context-fork.md` | Portable intent is adapted into Codex v2 context isolation. |
| `.claude/skills/prompt-patterns/assets/raw/` | Claude-version research remains source/reference material, not runtime payload. |

## Runtime Notes

- Project `config_file` values resolve relative to `.codex/`; A-Team's root registry therefore uses `../agents/...`.
- Codex v2 uses task-path lifecycle tools and shared filesystem semantics. Prompt policy enforces the helper-depth bound because legacy `agents.max_depth` does not.
- Standard `workspace-write` protects `.codex/` and `.agents/`; repo-self regeneration needs the documented approval/bootstrap posture.
- Static strict-config and registry checks do not prove the active host exposes every collaboration tool. Preflight records host readiness separately.
