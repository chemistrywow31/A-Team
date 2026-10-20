---
name: MD Generation Standard
description: Apply native frontmatter, useful document structure, and exact path references to authored markdown
---

# MD Generation Standard

Use when writing agent, skill, and rule documents. Preserve the selected runtime's native identifiers and supported metadata while applying A-Team's authoring floors. Read `.claude/rules/yaml-frontmatter.md` for the native schema and `JUDGMENT.md` J5 for quality requirements.

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
- For agents, keep one adjacent `Reasoning` → `Workflow` → `Self-Critique` sequence plus the required role, boundary, uncertainty, and completion sections. Do not ask for private reasoning transcripts.
- Use imperative instructions, concrete inputs, and checkable outcomes. Preserve useful XML, steps, and examples; brevity is secondary to execution quality.
- Use exact, resolvable relative paths. In A-Team's Claude layer, reference `.claude/agents/`, `.claude/skills/`, and `.claude/rules/` from the repository root. A generated team's references follow its actual declared layout.
- Put evidence and conditional detail in the existing linked references when that improves task routing. Avoid duplicating a contract in several documents.

## Quality Checks

1. Parse frontmatter and validate native fields separately from A-Team conventions; a schema-valid field does not prove model availability.
2. Resolve actual references and inspect section order, scope, uncertainty, completion, and examples against J5.
3. Include at least one meaningful rejection/defer/escalation case in authored agents and skills. Add positive or contrast cases when they clarify behavior.
4. Record line counts. Agent/skill/rule lengths above 300/200/100 are `REVIEW_REQUIRED`; record concrete usefulness and obtain independent resolution. Do not delete useful content just to turn the size indicator green. EC report caps remain separate.
5. For Codex output, use the mapped native metadata and skill mirrors rather than copying Claude-only frontmatter; inspect `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md` only for that projection.

## Examples

### Rejection Case

Reject a skill rewrite that removes supported `paths` or renames “Quality Validation” solely to satisfy a guessed universal naming rule. Preserve the native identifier and metadata; correct only a demonstrated schema or behavior defect.

## Sources

Native metadata: [Claude subagents](https://code.claude.com/docs/en/sub-agents) and [Claude skills](https://code.claude.com/docs/en/skills), checked 2026-10-06. Required sections, example floors, and size review are A-Team policy in J5, not vendor schema.
