---
name: Progressive Disclosure
category: context-strategies
applies_when:
  - generating-execution-agent
  - generating-research-agent
  - generating-coding-team
  - context-constrained
tags: [just-in-time, lazy-loading, metadata, exploration]
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/context-engineering-blog.md
source: https://code.claude.com/docs/en/memory
reviewed: 2026-10-06
---

# Progressive Disclosure

## Core Principle

Keep useful identifiers in startup context and retrieve detail when the task needs it. Match context loading to the decision, rather than requiring directory traversal or a document stack before every action.

## Retrieval Options

| Identifier | Retrieve when needed |
| --- | --- |
| File path or section | Actual source content for the relevant claim |
| Saved query | Current results for the task's question |
| Source URL | The referenced current document |
| Schema location | Definitions needed to interpret the selected data |

Names, sizes, dates, and folder locations can guide search; they do not establish authority, freshness, or correctness. Inspect the actual declaration/source when those facts matter.

## Worked Example

```text
Task: verify how a role registration resolves its config_file.
Start with the named project config and the native path-resolution rule.
Read the referenced role file when checking the resolved target.
Do not load all roles or all worklogs merely because they are available.
```

## Native Loading

For Grok, root AGENTS.md and the flat native core rule provide the shared bootstrap. Read exact `.grok/policies/` paths for conditional detail; do not assume an `@path/to/file` import expands automatically. Use the target's supported tools and loading behavior; do not assume an import syntax or inherited skill content transfers to another runtime.

## A-Team Application

Pass the role, task, exact inputs, and necessary decision paths. Retrieve additional source evidence when a question depends on it. Keep the skill's main entry useful for routing, with substantial conditional procedures in linked references.

## Examples

### Rejection Case

Reject classifying a target's canonical authority from its directory name alone. Read its declaration and required mappings before allowing a mutation, even when metadata appears familiar.

## Sources And Attribution

A-Team-authored retrieval example and authority boundary, informed by [Claude memory/imports](https://code.claude.com/docs/en/memory), checked 2026-10-06. The historical-source article provides context for on-demand retrieval, not a mandatory preload recipe.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/context-strategies/progressive-disclosure.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
