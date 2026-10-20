---
name: md-generation-standard
description: Apply native Grok frontmatter, useful document structure and exact path references to authored agents, skills and policies.
---

# MD Generation Standard

Use `.grok/policies/yaml-frontmatter.md` for native metadata, `.grok/policies/grok-agent-config.md` for supported agent fields, and `JUDGMENT.md` J5 for authoring floors. Vendor parsing and A-Team quality policy are distinct checks.

## Frontmatter

Start authored agents, skills and policies with YAML on line 1. Require nonempty `name` and `description`. For native skills, use stable lowercase hyphenated identifiers matching their folder; for flat native agents, match the filename stem.

```yaml
---
name: contract-reviewer
description: Check proposed changes against the published contract.
disallowedTools: [Task]
agentsMd: true
discoverSkills: true
---
```

This example is an agent definition, not skill metadata. Omit model and effort unless target-supported settings and an authorized migration justify them. Omitted/inherit agent model uses the parent model in the pinned source; omitted effort leaves the installed session/default behavior. Neither parser success nor `inspect` proves effective routing.

Skills live at `.grok/skills/{name}/SKILL.md`. Their `model` and `effort` are ignored; `allowed-tools` does not grant or restrict tools. Do not emit them as controls. Use skill names/descriptions and supported invocation flags; coordinator entries must adopt the main-session playbook instead of spawning it. Agent `skills` preload and explicit file reads are distinct from skill metadata and require correct target behavior.

## Structure and References

- Put one `# Title` after frontmatter and task-specific sections below it.
- Agents contain one adjacent `Reasoning` → `Workflow` → `Self-Critique` sequence, plus identity, input/output, ownership, boundaries, uncertainty and completion. Ask for public decisions/evidence, not private reasoning transcripts.
- Use imperative steps, concrete inputs, checkable outcomes, useful examples and XML boundaries. Brevity is secondary to execution quality.
- Use exact repository-relative `.grok/agents/`, `.grok/skills/` and `.grok/policies/` paths. Agent/rule discovery is flat; only `.grok/rules/core.md` is the shared automatic policy bootstrap here. On-demand policy references must name actual files.
- Keep substantial conditional procedures in linked resources and specify when to read them. Do not turn historical source references into runtime preload instructions.

## Quality Checks

1. Parse YAML and validate allowed keys/types. Unknown agent fields can be silently ignored by Grok, so their mere presence is not a guarantee.
2. Resolve references, scope, section order, uncertainty, completion and examples against J5.
3. Require a meaningful rejection/defer/escalation case in every skill and agent. Add positive/contrast cases when useful.
4. Record line counts; above agent/skill/policy 300/200/100 lines is `REVIEW_REQUIRED`, with a concrete usefulness rationale for independent acceptance. Preserve useful content rather than deleting it to satisfy a size indicator.
5. Confirm a single target authority and mapped source order. This branch has one native skill surface, so no Codex mirror is created. Any separately requested conversion must declare its own mapped mirrors and validate byte identity when required.
6. Report static validity, installed discovery and effective tools/model as separate evidence levels.

## Rejection Case

Reject a skill that adds `allowed-tools: [Task]` and claims this confines delegation. Remove the false enforcement claim and use the selected native agent/runtime contract. Also reject a Markdown-only change that silently renames a target role or migrates its model.

## Source Attribution

- **Origin**: A-Team canonical skill, preserved at `reference/platform-sources/.claude/skills/md-generation-standard/SKILL.md`.
- **Integration**: Pattern B: Adapted Install; native Grok branch authority is `AGENTS.md` plus `.grok/`.
- **Retrieved**: 2026-10-20 from the verified base snapshot.
- **Modifications**: Native paths, loading and lifecycle; preserved task intent, examples and useful assets. Archive is reference-only.
