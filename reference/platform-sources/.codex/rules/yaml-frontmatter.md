---
name: YAML Frontmatter
description: Require YAML frontmatter for all authored Codex prompt, skill, and rule docs
---

# YAML Frontmatter

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Frontmatter Is Mandatory

Every authored markdown file under `.codex/agents/`, `.codex/skills/`, and `.codex/rules/` must start with YAML frontmatter on line 1.

`AGENTS.md` is excluded from this rule because it is the runtime project document, not a prompt-library asset.

### Required Fields By File Type

Agent prompt docs must contain:

```yaml
---
name: {Agent name}
description: {One sentence role summary}
agent_type: {default | worker | explorer}
---
```

Skill docs must contain:

```yaml
---
name: {Skill name}
description: {One sentence capability summary}
---
```

Rule docs must contain:

```yaml
---
name: {Rule name}
description: {One sentence constraint summary}
paths:
  - "src/**/*.ts"
---
```

`paths` is optional in this Codex rule-library format. Do not copy Claude skill activation, tool, preload, or fork fields into Codex skills as runtime controls. Native Claude supports skill `paths`; this Codex format distinction is not a Claude prohibition.

### Field Constraints

- `name`: preserve existing identifiers; English Title Case is A-Team's display convention, not a native naming restriction
- `description`: one sentence, under 120 characters under the A-Team authoring convention
- `agent_type`: one of `default`, `worker`, `explorer`
- `paths`: an array of valid glob patterns

### Separate Prompt Metadata From Runtime Configuration

The playbook fields above are A-Team conventions; role model, effort, sandbox, and permissions live in the paired `agents/**/*.toml`. Apply the target-supported schema under `.codex/rules/codex-agent-config-patterns.md` and preserve explicit pins. Do not infer loading or inheritance from prose-only dependency labels such as `benefits-from`; keep any such label as tooling metadata. Read the required skill file explicitly when invoked.

### Validation Timing

Team Architect must validate frontmatter during Generation cross-validation before delivery.

## Violation Determination

- a file does not begin with `---` on line 1 -> Violation
- an agent prompt doc is missing `name`, `description`, or `agent_type` -> Violation
- a skill or rule doc is missing `name` or `description` -> Violation
- `agent_type` contains an unsupported value -> Violation
- `paths` appears in a non-rule document -> Violation
- `paths` exists but is not a valid glob list -> Violation

## Exceptions

This rule has no exceptions.
