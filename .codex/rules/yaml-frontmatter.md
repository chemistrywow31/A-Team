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

`paths` is optional and valid only for rules.

### Field Constraints

- `name`: English, title case
- `description`: one sentence, under 120 characters
- `agent_type`: one of `default`, `worker`, `explorer`
- `paths`: an array of valid glob patterns

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
