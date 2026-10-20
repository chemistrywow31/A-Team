---
name: MD Generation Standard
description: Apply consistent frontmatter, structure, and path references across authored markdown files
---

# MD Generation Standard

Use when writing agent, skill, and rule documents. Preserve the selected runtime's native identifiers and supported metadata while applying A-Team's authoring floors. Read `.codex/rules/yaml-frontmatter.md` for native metadata and `JUDGMENT.md` J5 for quality requirements.

## Frontmatter

Start authored agent, skill, and rule documents with YAML on line 1. A-Team requires `name` and `description`; Codex playbooks also declare `agent_type`, while model/effort and permissions live in their directly paired `agents/**/*.toml`.

```yaml
---
name: Contract Reviewer
description: Check proposed changes against the published contract
agent_type: worker
---
```

Keep the runtime TOML thin and resolve registrations relative to `.codex/`. Select target-supported fields through `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md`; retain existing model/effort/permission choices. A-Team's observed v2 profile is not a universal schema for future targets.

Preserve native skill names, descriptions, and invocation behavior. Codex-discoverable skills live in `.agents/skills/` with byte-identical maintenance copies in `.codex/skills/`. Do not copy Claude-only fields such as `context: fork` or `allowed-tools` into Codex skill frontmatter. When Claude output is also requested, preserve its supported `paths` and native names on that surface; do not reject them because Codex uses a different format.

## Structure And References

- Put one `# Title` after the frontmatter, with task-specific `##`/`###` sections as needed. The opening YAML remains the first line.
- For agents, keep one adjacent `Reasoning` → `Workflow` → `Self-Critique` sequence plus the required role, boundary, uncertainty, and completion sections. Do not ask for private reasoning transcripts.
- Use imperative instructions, concrete inputs, and checkable outcomes. Preserve useful XML, steps, and examples; brevity is secondary to execution quality.
- Use exact, resolvable relative paths. In A-Team's Codex layer, reference `.codex/agents/`, `.agents/skills/`, and `.codex/rules/` from the repository root. A generated team's references follow its actual declared layout.
- Put evidence and conditional detail in the existing linked references when that improves task routing. Avoid duplicating a contract in several documents.

## Quality Checks

1. Parse frontmatter and validate native fields separately from A-Team conventions; a schema-valid field does not prove model availability.
2. Resolve actual references and inspect section order, scope, uncertainty, completion, and examples against J5.
3. Verify Codex authored/runtime skill byte identity. Include at least one meaningful rejection/defer/escalation case in authored agents and skills. Add positive or contrast cases when they clarify behavior.
4. Record line counts. Agent/skill/rule lengths above 300/200/100 are `REVIEW_REQUIRED`; record concrete usefulness and obtain independent resolution. Do not delete useful content just to turn the size indicator green. EC report caps remain separate.
5. Keep static metadata/config validity, actual live tools, and model access separate. Schema success alone does not establish readiness.

## Examples

### Rejection Case

Reject a Codex skill projection that copies Claude `context: fork` to simulate runtime isolation. Use the selected Codex lifecycle and config, preserve the source’s workflow intent, and verify the two Codex skill copies are identical.

## Sources And Adaptation

Shared authoring floors: `.claude/skills/md-generation-standard/SKILL.md` and J5. Native Codex adaptations: `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md`, under the adaptation manifest. [Codex customization guidance](https://learn.chatgpt.com/docs/customization/overview), checked 2026-10-06, distinguishes repository skills from runtime configuration. These A-Team section and size floors are project policy.
