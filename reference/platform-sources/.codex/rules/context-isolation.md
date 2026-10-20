---
name: Context Isolation
description: Isolate Codex work through bounded delegation depth, owned paths, and narrow forks instead of Claude frontmatter
---

# Context Isolation

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, and every generated Codex multi-agent runtime

## Rule Content

### Select The Target Lifecycle

Keep published CLI documentation, installed-client support, and live host tools separate. The published stable profile names `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`; A-Team's current v2 host exposes the six-tool lifecycle below. Use only the target's actual tool contracts and record the selected profile in setup/mapping metadata, never as invented config fields. See [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), checked 2026-10-06.

- `spawn_agent`: new bounded task; `send_message`: non-triggering update.
- `followup_task`: new/corrective turn on an existing idle agent; send updates to a running agent instead.
- `interrupt_agent`: unsafe or invalidated work; `list_agents`: inspect state before routing/join decisions.
- `wait_agent`: wait only at a real join boundary after independent local work is exhausted.

### Direct Specialists Plus One Helper Hop

- The coordinator delegates directly to specialists on a host that permits delegation. When delegation is unavailable, execute locally and record the limitation without inventing tool success.
- Delegate only bounded independent work that can run alongside useful local work; batch repetitive items under one owner and freeze producers before independent review.
- Where supported and allowed by the dispatch, a specialist may spawn at most one nested helper, and only for bounded independent evidence collection or verification inside that specialist's owned artifact family.
- A nested helper may not delegate again, reassign ownership, or cross artifact families.

### Shared Filesystem Ownership

- Assume every agent sees the same workspace unless the runtime explicitly provisions isolation.
- Every dispatch must name owned write paths and forbidden paths.
- Agents must not revert, overwrite, or clean up edits they did not make.
- If unexpected foreign edits appear inside an owned path, adapt to them or escalate the conflict. Do not blindly overwrite.

### Isolation Comes From Task Scope, Not Claude Frontmatter

- Do not use Claude-only `context: fork` frontmatter in Codex-native skills.
- Codex isolation comes from task-scoped agents, worklog paths, owned paths, and narrow forks.
- Runtime permissions belong in `.codex/config.toml` and `agents/**/*.toml`, not in skill frontmatter.

### Fork Override Rule

These are observed v2-host constraints, not a promise about every Codex runtime. Preserve the target's supported equivalent when its tool API differs.

- Full-history forks inherit the parent model and reasoning effort.
- Any explicit model or reasoning override requires `fork_turns = "none"` or a positive bounded fork.
- Override plus omitted or `all` fork history is forbidden.
- Prefer bounded/no-history forks with explicit model/effort for role-specific routing; provide the necessary artifact and decision paths. A role TOML pin alone does not prove its effective model on a full-history fork.

### Return Summaries Only

Isolated work returns the execution-contract summary. Bulky findings stay in owned files; if live sandbox/host restrictions block report persistence, use only the dispatch-bounded EC-1.12 `INLINE-FALLBACK` with coordinator persistence. Never bypass the restriction through a different write tool.

## Violation Determination

- A profile assumes unavailable lifecycle tools or undocumented capacity/fork behavior -> Violation
- A specialist spawns more than one helper, or a helper spawns another helper -> Violation
- A helper writes outside the parent specialist's owned artifact family -> Violation
- A dispatch omits owned paths or a branch reverts non-owned edits -> Violation
- A Codex-native skill uses Claude-only `context: fork` frontmatter -> Violation
- Runtime permissions are embedded in skill frontmatter instead of config or TOML -> Violation
- A model or reasoning override is combined with full-history inheritance -> Violation
- Isolated work returns unbounded raw dumps or a fallback without its dispatch cap and persistence owner -> Violation

## Exceptions

- If the user explicitly asks for a Claude-compatible compatibility surface, Claude-only frontmatter may appear there when the mapping docs mark it non-canonical.
