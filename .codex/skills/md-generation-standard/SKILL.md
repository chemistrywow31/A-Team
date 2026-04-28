---
name: MD Generation Standard
description: Apply consistent frontmatter, structure, and path references across authored markdown files
---

# MD Generation Standard

## Description

Use this skill when writing agent, skill, and rule documents for the Codex layer.

## Users

- `.codex/agents/generation/agent-writer.md`
- `.codex/agents/generation/skill-writer.md`
- `.codex/agents/generation/rule-writer.md`

## Format Rules

### Frontmatter

Agent docs:

```yaml
---
name: {Agent name}
description: {One sentence description}
agent_type: {default | worker | explorer}
---
```

Skill docs:

```yaml
---
name: {Skill name}
description: {One sentence description}
---
```

Rule docs:

```yaml
---
name: {Rule name}
description: {One sentence description}
---
```

### Path References

- skill path: `.agents/skills/{skill-name}/SKILL.md`
- authored skill path: `.codex/skills/{skill-name}/SKILL.md`
- agent path: `.codex/agents/{group}/{agent-name}.md`
- rule path: `.codex/rules/{rule-name}.md`

### Writing Style

- one `#` heading per file
- imperative language
- kebab-case file names
- keep paths exact

## Checklist

- frontmatter is present and valid
- only one h1 exists
- all paths resolve
- no vague fillers remain
- the file stays within the size budget

## Example

### Input

`請為 reviewer 角色產出 agent prompt。`

### Output

`frontmatter + Identity + Responsibilities + Input and Output + Workflow + Available Skills + Applicable Rules + Collaboration Relationships + Boundaries`
