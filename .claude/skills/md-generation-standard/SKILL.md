---
name: MD Generation Standard
description: Apply native frontmatter, useful document structure, and exact path references to authored markdown
---

# MD Generation Standard

Use when writing agent, skill, and rule documents. This skill covers frontmatter, structure and path mechanics. What to write is in `.claude/rules/writing-quality-standard.md`; the native schema is in `.claude/rules/yaml-frontmatter.md`.

## Frontmatter

Start authored agent, skill, and rule documents with YAML on line 1. A-Team requires `name` and `description`; Claude-runnable agents additionally declare model/effort under the context-tier rule.

```yaml
---
name: Contract Reviewer
description: Check proposed changes against the published contract
model: inherit
effort: high
---
```

This illustrates native fields, not a model migration. Claude supports target-valid aliases, full model IDs, and inheritance; retain explicit target pins. Skill `paths` is supported. `metadata` is tooling data; A-Team's `benefits-from` label does not preload skills or imply parent-to-child inheritance. Use explicit subagent `skills` preload or exact file reads when skill content is required. Preserve current skill names and native paths; do not rename files or commands as formatting cleanup.

For a Claude coordinator entry, retain explicit invocation metadata and main-session adoption of its coordinator playbook under J5.2. A manual-only review skill is not thereby a coordinator entry.

## Structure And References

- Put one `# Title` after the frontmatter, with task-specific `##`/`###` sections as needed. The opening YAML remains the first line.
- No section is mandatory in a generated agent, skill or rule. Add a section when it says something specific to that file. When an agent uses `Reasoning`, `Workflow` and `Self-Critique`, keep them adjacent and in that order.
- Use exact, resolvable relative paths. In A-Team's Claude layer, reference `.claude/agents/`, `.claude/skills/`, and `.claude/rules/` from the repository root. A generated team's references follow its actual declared layout.
- Put evidence and conditional detail in the existing linked references when that improves task routing. Avoid duplicating a contract in several documents.

## Quality Checks

1. Parse frontmatter and validate native fields separately from A-Team conventions; a schema-valid field does not prove model availability.
2. Resolve every path the file references.
3. Record line counts. Agent, skill and rule files above 300, 200 and 100 lines are `REVIEW_REQUIRED` until the independent reviewer accepts them.
4. For Codex output, use the mapped native metadata and skill mirrors rather than copying Claude-only frontmatter; inspect `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md` only for that projection.

Do not rename a skill or drop supported metadata such as `paths` as formatting cleanup; change an identifier only for a demonstrated schema or behaviour defect.

## Sources

Native metadata: [Claude subagents](https://code.claude.com/docs/en/sub-agents) and [Claude skills](https://code.claude.com/docs/en/skills), checked 2026-10-06. Size review is A-Team policy in J5, not vendor schema.
