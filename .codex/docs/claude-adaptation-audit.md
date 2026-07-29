# Claude To Codex Adaptation Audit

## Scope

This audit compares `CLAUDE.md` and `.claude/` against the active Codex runtime surface: `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/`.

## Migration Decisions

| Claude Source | Codex Action | Rationale |
| --- | --- | --- |
| `CLAUDE.md` design philosophy | merged into `AGENTS.md` and coordinator playbook | portable team-design behavior |
| `.claude/agents/research/domain-researcher.md` | added as `.codex/agents/research/domain-researcher.md` and `agents/research/domain-researcher.toml` | cross-phase research remains useful in Codex |
| `.claude/agents/research/decision-auditor.md` | added as `.codex/agents/research/decision-auditor.md` and `agents/research/decision-auditor.toml` | phase-boundary evidence audit remains useful in Codex |
| `.claude/skills/a-team/SKILL.md` | adapted as `.codex/skills/a-team/SKILL.md` and `.agents/skills/a-team/SKILL.md` | Codex benefits from an explicit `$a-team` entry skill, but Claude-only slash-command frontmatter was removed |
| `.claude/rules/worklog.md` | adapted as `.codex/rules/worklog.md` | portable evidence-chain requirement |
| `.claude/rules/context-management.md` | adapted as `.codex/rules/context-management.md` | `Task` semantics replaced with `spawn_agent`, `send_input`, and `wait` |
| `.claude/rules/reasoning-and-self-critique.md` | adapted as `.codex/rules/reasoning-and-self-critique.md` | preserves verification gates without requiring private chain-of-thought output |
| `.claude/rules/anti-sycophancy.md` | adapted as `.codex/rules/anti-sycophancy.md` | portable recommendation-quality rule |
| `.claude/rules/prompt-engineering-patterns.md` | adapted as `.codex/rules/prompt-engineering-patterns.md` | removes Claude 4.x-specific claims and keeps structural prompt patterns |
| `.claude/rules/context-tier.md` | adapted as `.codex/rules/context-tier.md` | maps Opus/Sonnet/Haiku tiers to Codex model and reasoning-effort guidance |
| `.claude/rules/frontmatter-optional-patterns.md` | adapted as `.codex/rules/codex-agent-config-patterns.md` | Codex runtime agents are TOML configs, not Claude markdown frontmatter |
| `.claude/rules/settings-json.md` and `.claude/rules/hooks-integration.md` | adapted as `.codex/rules/codex-runtime-config.md` | Codex uses project `.codex/config.toml`; hooks are optional and non-portable |
| `.claude/rules/skill-context-fork.md` | adapted as `.codex/rules/context-isolation.md` | Codex uses subagent isolation and summary handoffs instead of Claude `context: fork` |
| `.claude/skills/prompt-patterns/SKILL.md` | added as lightweight Codex skill in `.codex/skills/` and `.agents/skills/` | portable reusable prompt design method |

## Deliberately Not Copied

- `.claude/settings.json` was not copied because generated Codex teams must use project-local `.codex/config.toml`.
- `.claude/skills/a-team/SKILL.md` was not copied verbatim because Codex entry is `AGENTS.md` plus repo skills, not a Claude slash-command entrypoint.
- `.claude/skills/prompt-patterns/assets/raw/*` was not copied because those files are Claude-version-specific research notes, not canonical Codex rules.
- `.claude/skills/skill-creator` scripts were not duplicated because Codex has a system `skill-creator` skill and this repo keeps only a lightweight bridge.
- `.claude/output-styles/` was not copied because output styles are a Claude Code runtime feature (selected via `outputStyle` in project-local settings, main-session only, first-run ask via SessionStart hook); Codex has no equivalent surface, so the output-mode component is Claude-tree-only.
- `.claude/` was not modified; it remains the legacy/source design.

## Validation Notes

- Codex project instructions belong in `AGENTS.md`.
- Project-scoped Codex settings belong in `.codex/config.toml`.
- Repo-discoverable skills belong in `.agents/skills/`.
- Generated multi-agent teams must preserve `config_file` paths relative to `.codex/`.
