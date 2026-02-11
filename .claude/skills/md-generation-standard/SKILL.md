---
name: MD Generation Standard
description: Define universal writing standards, format specifications, and quality requirements for all .md files
---

# MD Generation Standard

## Description

Define universal writing standards, format specifications, and quality requirements for all .md files. All writer agents must follow these when generating files.

## Users

- `agent-writer`: Follow when writing agent .md files
- `skill-writer`: Follow when writing skill .md files
- `rule-writer`: Follow when writing rule .md files

## Universal Format Specifications

### YAML Frontmatter

All .md files must begin with YAML frontmatter in the following format:

**Agent files:**
```yaml
---
name: {Agent name, English}
description: {One sentence description}
model: {opus | sonnet | haiku}
---
```

**Skill files:**
```yaml
---
name: {Skill name, English}
description: {One sentence description}
---
```

**Rule files:**
```yaml
---
name: {Rule name, English}
description: {One sentence description}
---
```

### File Naming
- Use kebab-case: `content-reviewer.md`, not `contentReviewer.md` or `content_reviewer.md`
- Name should directly reflect the core function of the role/skill/rule
- Keep concise, typically 2-4 words

### Document Structure
- First line must be `# Title` (h1), entire file can only have one h1
- Use `##` (h2) as main section headings
- Use `###` (h3) as subsection headings
- Do not use h4 or below, avoid excessive nesting

### Language Specifications
- Content should match the user's language preference
- Technical terms may remain in English (e.g., agent, skill, rule, PR, CI/CD, API)
- Technical terms may have explanation in user's language on first occurrence, then use English directly
- Instructional content uses imperative sentences ("You must..." not "should...")

### Path References
- Use relative paths when referencing other files
- Skill path format: `skills/{skill-name}/SKILL.md`
- Agent path format: `agents/{group}/{agent-name}.md`
- Rule path format: `rules/{rule-name}.md`
- Example: `skills/structured-interview/SKILL.md`

## Quality Checklist

Each .md file must pass before delivery:
- [ ] File begins with correctly formatted YAML frontmatter (including name and description, agents additionally include model)
- [ ] File has exactly one h1 heading
- [ ] All referenced file paths actually exist
- [ ] No vague words like "try to", "appropriately", "reasonably" (unless followed by judgment criteria)
- [ ] Single file does not exceed 300 lines
- [ ] No duplicate descriptions of content already covered in other files
