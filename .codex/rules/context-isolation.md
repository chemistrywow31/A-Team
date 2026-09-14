---
name: Context Isolation
description: Isolate Codex work through bounded delegation depth, owned paths, and narrow forks instead of Claude frontmatter
---

# Context Isolation

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, and every generated Codex multi-agent runtime

## Rule Content

### Direct Specialists Plus One Helper Hop

- The coordinator delegates directly to specialists.
- Delegate only bounded independent work that can run alongside useful local work; batch repetitive items under one owner and freeze producers before independent review.
- A specialist may spawn at most one nested helper, and only for bounded independent evidence collection or verification inside that specialist's owned artifact family.
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

- Full-history forks inherit the parent model and reasoning effort.
- Any explicit model or reasoning override requires `fork_turns = "none"` or a positive bounded fork.
- Override plus omitted or `all` fork history is forbidden.
- Prefer bounded/no-history forks with explicit model/effort for role-specific routing; provide the necessary artifact and decision paths. A role TOML pin alone does not prove its effective model on a full-history fork.

### Return Summaries Only

Isolated work returns the execution-contract summary only. Bulky findings stay in the worklog or owned artifacts.

## Violation Determination

- A specialist spawns more than one helper, or a helper spawns another helper -> Violation
- A helper writes outside the parent specialist's owned artifact family -> Violation
- A dispatch omits owned paths or a branch reverts non-owned edits -> Violation
- A Codex-native skill uses Claude-only `context: fork` frontmatter -> Violation
- Runtime permissions are embedded in skill frontmatter instead of config or TOML -> Violation
- A model or reasoning override is combined with full-history inheritance -> Violation
- Isolated work returns raw dumps instead of the structured summary -> Violation

## Exceptions

- If the user explicitly asks for a Claude-compatible compatibility surface, Claude-only frontmatter may appear there when the mapping docs mark it non-canonical.
