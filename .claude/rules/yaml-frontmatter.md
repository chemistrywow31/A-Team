---
name: YAML Frontmatter
description: Mandate YAML frontmatter as the first content in every generated .md file
---

# YAML Frontmatter

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Every .md File Must Start with YAML Frontmatter

The very first line of every generated .md file must be `---`, opening a YAML frontmatter block. No content, comments, or blank lines may precede it.

### Required Fields by File Type

**Agent .md files** must contain exactly these three fields:

```yaml
---
name: {Agent name, English}
description: {One sentence describing this agent's core responsibility}
model: {model identifier}
---
```

**Skill .md files** must contain these fields:

```yaml
---
name: {Skill name, English}
description: {One sentence describing the capability this skill provides}
benefits-from:                      # OPTIONAL — declare upstream skill dependencies
  - "{skill-name-1}"
  - "{skill-name-2}"
---
```

- `name` and `description` are required
- `benefits-from` is optional. When present, it declares which upstream skills produce context that improves this skill's output. The coordinator uses this to determine skill execution order and context passing chains

**Rule .md files** must contain these fields:

```yaml
---
name: {Rule name, English}
description: {One sentence describing this rule's core constraint}
paths:                              # OPTIONAL — omit for unconditional rules
  - "src/**/*.ts"
  - "**/*.test.*"
---
```

- `name` and `description` are required
- `paths` is optional. When present, the rule loads only when Claude reads files matching any listed glob pattern. When omitted, the rule loads unconditionally at session start

### Field Value Constraints

- `name`: English only, title case (e.g., "Content Planner", not "content-planner")
- `description`: One sentence, no period at end, under 120 characters
- `model`: A valid Claude model identifier. Accepted values: `opus`, `sonnet`, `haiku`. Select based on task complexity — use `opus` for tasks requiring deep reasoning, `sonnet` for balanced capability and cost, `haiku` for fast lightweight tasks. Default to `sonnet` when unspecified by the user.
- `paths`: An array of glob patterns (e.g., `["src/**/*.ts", "**/*.test.*"]`). Use standard glob syntax with `**` for recursive directory matching and `{ts,tsx}` for brace expansion. Only valid in rule .md files.

### Validation Timing

Team Architect must validate frontmatter presence and correctness during Phase 3 cross-validation, before marking any file as complete.

## Violation Determination

- File does not start with `---` on the first line → Violation
- Agent .md missing any of the three required fields (`name`, `description`, `model`) → Violation
- Skill .md missing required fields (`name`, `description`) → Violation
- Rule .md missing required fields (`name`, `description`) → Violation
- Skill .md has `benefits-from` field with values that do not match any skill name in the team → Violation
- `model` field contains a value not in the accepted list (`opus`, `sonnet`, `haiku`) → Violation
- Blank line or content before the opening `---` → Violation
- Rule .md has `paths` field but values are not valid glob patterns → Violation
- Non-rule .md file contains a `paths` field → Violation (only rules support `paths`)

## Exceptions

This rule has no exceptions.
