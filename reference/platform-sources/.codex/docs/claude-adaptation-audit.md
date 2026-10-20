# Claude To Codex Adaptation Audit

## Authority

For A-Team itself, root `CLAUDE.md` and `.claude/` are canonical for shared role intent, workflow, ownership, authority, and quality. Root `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/` are regenerated Codex projections or deliberate Codex-only runtime artifacts. Bounded execution details are injected from the exact runtime adaptation inputs below, not copied into Claude's runtime instructions. Generated teams retain their own manifest-declared authority.

The validator accepts a generated platform-neutral `shared/` authority only when its manifest, `shared/team.yaml`, both root entries, and mapping declaration agree and the local authority root is safe. This behavior changes no M5 inventory path: no platform-only artifact was added or removed.

`.codex/docs/claude-adaptation-manifest.toml` is the machine-readable M5 inventory. This file supplies rationale and must stay in one-to-one agreement with its `platform_only` and `deliberately_not_copied` paths.

## Adaptation Decisions

| Claude Source | Codex Projection | Rationale |
|---|---|---|
| `CLAUDE.md` | `AGENTS.md` | Preserve purpose, phases, gates, and existing-team evolution while translating runtime tools. |
| `.claude/agents/**/*.md` | `.codex/agents/**/*.md` + `agents/**/*.toml` | Keep role semantics; split authoritative Codex playbooks from thin runtime TOML configs. |
| `.claude/skills/*/SKILL.md` | `.codex/skills/*/SKILL.md` + `.agents/skills/*/SKILL.md` | Adapt frontmatter/tool vocabulary; keep authored and runtime Codex copies byte-identical. |
| `.claude/rules/context-management.md` | `.codex/rules/context-management.md` | Map delegation intent to task paths, selective forks, lifecycle tools, joins, and shared-filesystem ownership. |
| `.claude/rules/coordinator-mandate.md` | `.codex/rules/coordinator-mandate.md` | Preserve the single coordinator while allowing one bounded specialist helper hop under v2. |
| `.claude/rules/context-tier.md` + inventoried Codex runtime inputs | `.codex/rules/context-tier.md` | Preserve shared context principles; inject Codex model/effort and fork details from native inputs. Claude retains its own tier mapping; explicit target runtime pins take precedence. |
| `.claude/rules/frontmatter-optional-patterns.md` | `.codex/rules/codex-agent-config-patterns.md` | Codex runtime roles are TOML configs rather than Claude Markdown frontmatter. |
| `.claude/rules/settings-json.md` + `hooks-integration.md` | `.codex/rules/codex-runtime-config.md` | Codex uses trusted project `.codex/config.toml`, sandbox/approval policy, and protected metadata. |
| `.claude/rules/skill-context-fork.md` | `.codex/rules/context-isolation.md` | Codex uses explicit `fork_turns`, task paths, and summary handoffs. |


## Runtime Adaptation Inputs

These three existing platform-only specifications inject only the bounded runtime details listed here into exact mapped projections. They do not override canonical shared role intent, workflow, ownership, authority, or quality, and they do not grant whole-tree ownership. Claude reads them only when the requested target includes Codex.

| Input | Bounded scope | Projections |
|---|---|---|
| `.codex/rules/codex-runtime-config.md` | Codex target-supported model/effort inheritance, config schema, installed-client/live-host profiles, approval/protected-path guidance | `AGENTS.md`<br>`.codex/rules/context-tier.md`<br>`.codex/rules/execution-contract.md`<br>`.codex/rules/output-structure.md`<br>`.codex/agents/generation/agent-writer.md`<br>`.codex/agents/review/runtime-preflight-advisor.md`<br>`.codex/skills/quality-validation/SKILL.md`<br>`.codex/agents/team-architect.md`<br>`.codex/skills/a-team/SKILL.md`<br>`.codex/rules/codex-native-output.md`<br>`.codex/agents/evolution/team-restructuring-master.md`<br>`.codex/skills/prompt-optimization/SKILL.md`<br>`.codex/skills/md-generation-standard/SKILL.md` |
| `.codex/rules/codex-agent-config-patterns.md` | Codex agent TOML/MCP/registry/runtime metadata validation | `.codex/agents/generation/agent-writer.md`<br>`.codex/agents/team-architect.md`<br>`.codex/rules/context-tier.md`<br>`.codex/rules/output-structure.md`<br>`.codex/skills/prompt-patterns/SKILL.md`<br>`.codex/skills/quality-validation/SKILL.md`<br>`.codex/agents/review/runtime-preflight-advisor.md`<br>`.codex/rules/yaml-frontmatter.md`<br>`.codex/skills/md-generation-standard/SKILL.md`<br>`.codex/agents/evolution/team-restructuring-master.md` |
| `.codex/rules/context-isolation.md` | Codex target-supported fork/delegation/isolation lifecycle adaptation | `AGENTS.md`<br>`.codex/rules/context-tier.md`<br>`.codex/rules/execution-contract.md`<br>`.codex/agents/team-architect.md`<br>`.codex/skills/prompt-optimization/SKILL.md`<br>`.codex/skills/prompt-patterns/SKILL.md`<br>`.codex/rules/output-structure.md`<br>`.codex/agents/generation/agent-writer.md`<br>`.codex/agents/generation/rule-writer.md`<br>`.codex/agents/generation/skill-writer.md`<br>`.codex/agents/review/runtime-preflight-advisor.md`<br>`.codex/agents/evolution/team-restructuring-master.md`<br>`.codex/skills/a-team/SKILL.md`<br>`.codex/rules/context-management.md`<br>`.codex/rules/coordinator-mandate.md`<br>`.codex/skills/team-topology-analysis/SKILL.md` |

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

- 2026-09-14: compact canonical role contracts retain one Reasoning/Workflow/Self-Critique triad, required boundaries/uncertainty and a rejection example. Codex projections omit duplicate Preflight/Verification forms. Existing authorization covers its scoped reversible changes; independent batch acceptance and material-choice approval remain intact.
- 2026-09-14 historical profile: strong-role pins migrated to GPT-6 Astra/xhigh; the three Terra/high TOMLs stayed unchanged. On 2026-10-06, existing project root/default-subagent pins are absent by user choice; host defaults remain authoritative and all per-role pins are preserved. No platform-only inventory path is added or removed.
- Project `config_file` values resolve relative to `.codex/`; A-Team's root registry therefore uses `../agents/...`.
- Codex v2 uses task-path lifecycle tools and shared filesystem semantics. Prompt policy enforces the helper-depth bound because legacy `agents.max_depth` does not.
- Standard `workspace-write` protects `.codex/` and `.agents/`; repo-self regeneration needs the documented approval/bootstrap posture.
- Static strict-config and registry checks do not prove the active host exposes every collaboration tool. Preflight records host readiness separately.

## 2026-10-06 Native Refresh

- Prompt effectiveness takes priority over brevity. Useful XML, examples, steps, and checks are retained; the approved J5 size targets require an independent usefulness verdict when exceeded.
- Claude native [Agent definitions](https://code.claude.com/docs/en/sub-agents) support nesting, model inheritance/full IDs, effort, and skill preloads. A-Team keeps direct specialists and enforces that native policy with `disallowedTools: [Agent]`; the coordinator remains in the main session. The Codex one-helper policy stays a separate host adaptation.
- Current installed Codex 0.160.1 reports both multi_agent and multi_agent_v2 stable/enabled. The [published config reference](https://learn.chatgpt.com/docs/config-file/config-reference) documents the stable base and spawned-thread capacity excluding root; observed v2 tools/total-slot accounting are recorded separately. Preserve the working project config; generate future targets from their own supported profile and preflight.
- Shared scope intake distinguishes designer capability maintenance from actual named-target/fleet mutation. Read-only evidence persistence uses the existing bounded INLINE-FALLBACK with coordinator ownership.
- Claude-only metadata adjustments do not inject unsupported keys into Codex. Exact additional adaptation targets above cover native schema, lifecycle and profile instructions; authored/runtime skill mirrors remain byte-identical.
- Official references were fetched 2026-10-06. Published documentation does not establish account entitlement or disclose an unpublished internal system prompt.
