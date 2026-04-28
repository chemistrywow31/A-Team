---
name: Context Isolation
description: Replace Claude context-fork patterns with Codex subagent isolation and summary handoffs
---

# Context Isolation

## Applicability

- Applies to: `skill-writer`, `agent-writer`, `team-architect`

## Rule Content

### Do Not Use Claude `context: fork`

Codex skills are repo-discoverable instructions under `.agents/skills/`. Do not add Claude-only skill frontmatter such as `context: fork`, `agent`, `allowed-tools`, or `disable-model-invocation` to Codex-native skills unless a documented Codex runtime supports it.

### Use Subagents For Noisy Work

When a skill requires large exploration, research, verbose tests, or broad audits, route that work through a specialist registered in `.codex/config.toml`. The skill should explain when to delegate, and the coordinator should spawn the specialist.

### Return Summaries Only

Isolated work must return a summary with status, key outcomes, changed files, worklog paths, and blockers. Store bulky findings in the worklog or generated artifacts.

### Keep Skills Instruction-Focused

Skills should define reusable method, checklist, examples, and escalation criteria. Agent selection and runtime permissions belong in `.codex/config.toml` and `agents/**/*.toml`.

## Violation Determination

- Codex-native skill uses Claude-only `context: fork` or `allowed-tools` frontmatter -> Violation
- noisy research or exploration runs inline when a registered specialist exists and the coordinator is not blocked -> Violation
- skill embeds agent runtime permissions instead of method guidance -> Violation
- isolated work returns raw dumps instead of structured summaries -> Violation

## Exceptions

If a user explicitly asks for Claude-compatible skill export, include Claude-only frontmatter in the compatibility artifact and mark it as non-canonical in the mapping docs.
