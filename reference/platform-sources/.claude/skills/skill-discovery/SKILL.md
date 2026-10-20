---
name: Skill Discovery
description: Search external skill sources and evaluate candidates for reuse before creating custom skills
---

# Skill Discovery

## Description

Search external skill repositories and marketplaces to find existing skills that match capability requirements. Evaluate candidates using a weighted scoring system and classify them for reuse, reference, or discard. This skill enforces the "reuse before create" principle.

## Users

This skill is used by the following agents:
- `skill-planner`: Search external sources during Phase 2 planning to identify reusable skills before designing custom ones

## Configuration

Read `skills/skill-discovery/config.json` if it exists. If not found, use these defaults:

```json
{
  "sources": {
    "skillsmp": { "enabled": true },
    "aitmpl": { "enabled": true },
    "github": {
      "enabled": true,
      "repos": ["anthropics/skills"]
    }
  },
  "search": {
    "max_results_per_source": 5,
    "min_score_threshold": 3.5
  }
}
```

## Search Strategy

### Step 1: Generate Search Queries

For each capability requirement extracted from the role design document:
1. Identify the core capability keyword (e.g., "SEO optimization")
2. Generate 2-3 search query variants:
   - Exact match: the capability name itself
   - Synonym variant: an alternative phrasing
   - Broader category: a more general term that may surface related skills

### Step 2: Search Each Source

Execute searches against all enabled sources using WebSearch. No API keys are required.

#### Source: SkillsMP

- **Search query**: `site:skillsmp.com {keywords} skill`
- **URL pattern**: Match results containing `skillsmp.com/skills/`
- **Detail retrieval**: Use WebFetch on matched URLs to read the skill's description, installation command, and GitHub source link
- **Extract**: Skill name, description, source repository URL

#### Source: aitmpl.com

- **Search query**: `site:aitmpl.com {keywords} skill`
- **URL pattern**: Match results containing `aitmpl.com/component/skill/`
- **Detail retrieval**: Use WebFetch on matched URLs to read the skill's metadata and content
- **Extract**: Skill name, description, content preview

#### Source: GitHub

- **Search query**: `github.com SKILL.md "claude code" {keywords}`
- **Additional search**: `site:github.com anthropics/skills {keywords}` (and any repos listed in config)
- **Detail retrieval**: Use WebFetch on the raw SKILL.md URL (convert `github.com/{owner}/{repo}/blob/main/` to `raw.githubusercontent.com/{owner}/{repo}/main/`)
- **Extract**: Full SKILL.md content, repository stars, last update date

### Step 3: Deduplicate Results

If the same skill appears in multiple sources, keep the entry with the most complete information. Note all sources where it was found.

## Evaluation Criteria

Score each candidate skill on a 1-5 scale across four dimensions:

| Dimension | Weight | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|-----------|--------|-----------|---------------|----------------|
| Relevance | 40% | Tangentially related | Partially matches the requirement | Directly matches the capability need |
| Quality | 25% | No structure, no examples | Has structure but missing examples | Complete SKILL.md with frontmatter, sections, and examples |
| Freshness | 15% | Over 12 months since last update | Updated within 6-12 months | Updated within 6 months |
| Adoption | 20% | No stars, no platform listing | Listed on one platform or 10+ stars | Listed on multiple platforms or 50+ stars |

**Weighted score** = (Relevance x 0.4) + (Quality x 0.25) + (Freshness x 0.15) + (Adoption x 0.2)

## Decision Thresholds

| Score Range | Decision | Integration Pattern |
|-------------|----------|---------------------|
| >= 3.5 | **Recommend reuse** | Pattern A (Direct Install) or Pattern B (Adapted Install) |
| 2.5 - 3.4 | **Reference material** | Pattern C (Reference Only) — do not install, provide to Skill Writer as reference |
| < 2.5 | **Discard** | Create custom skill from scratch |

### Pattern A: Direct Install

Use when the external skill scores >= 3.5 and requires no modifications:
1. Download the SKILL.md content via WebFetch
2. Verify frontmatter compliance (must have `name` and `description`)
3. Place in `skills/{skill-name}/SKILL.md`
4. Append Source Attribution section to the file

### Pattern B: Adapted Install

Use when the external skill scores >= 3.5 but requires modifications:
1. Download the SKILL.md content via WebFetch
2. Document required modifications (e.g., adjust terminology, add missing sections)
3. Place modified version in `skills/{skill-name}/SKILL.md`
4. Append Source Attribution section noting modifications

### Pattern C: Reference Only

Use when the external skill scores 2.5-3.4:
1. Record the skill URL and a brief summary of useful content
2. Pass as reference material to Skill Writer
3. Skill Writer creates a custom skill, optionally noting the reference source

## Source Attribution Format

Every installed external skill (Pattern A or B) must include this section at the end of the SKILL.md:

```markdown
## Source Attribution

- **Origin**: {source platform} ({URL})
- **Integration**: {Pattern A: Direct Install | Pattern B: Adapted Install}
- **Retrieved**: {date}
- **Modifications**: {None | list of changes made}
```

## Output Format

The search results must be reported in this structure:

```markdown
## External Skills Discovery

### Search Summary
- Sources searched: {list of enabled sources}
- Total candidates found: {number}
- Recommended for reuse: {number}
- Reference materials: {number}
- Discarded: {number}

### Recommended External Skills

#### {skill-name} (Score: {x.x})
- **Source**: {platform} — {URL}
- **Relevance**: {score}/5 — {brief justification}
- **Quality**: {score}/5 — {brief justification}
- **Freshness**: {score}/5 — {brief justification}
- **Adoption**: {score}/5 — {brief justification}
- **Integration**: Pattern {A|B}
- **Target agents**: {agent-1}, {agent-2}

### Reference Materials

#### {skill-name} (Score: {x.x})
- **Source**: {URL}
- **Useful content**: {what can be referenced}
- **Target capability**: {which capability requirement this relates to}
```

## Quality Checkpoints

- [ ] All enabled sources were searched for each capability requirement
- [ ] Each candidate has scores for all four evaluation dimensions
- [ ] Weighted scores are calculated correctly
- [ ] Decision thresholds are applied consistently
- [ ] Recommended skills have a clear integration pattern assigned
- [ ] No duplicate skills across sources in the final output

## Example

### Input
Capability requirement: "Structured content writing for blog posts"

### Output
```markdown
### Recommended External Skills
#### structured-writing (Score: 3.8)
- **Source**: SkillsMP — https://skillsmp.com/skills/structured-writing
- **Relevance**: 4/5 — Directly addresses content structuring methodology
- **Quality**: 4/5 — Complete SKILL.md with frontmatter and examples
- **Freshness**: 3/5 — Last updated 8 months ago
- **Adoption**: 4/5 — Listed on SkillsMP, 35 GitHub stars
- **Integration**: Pattern A
- **Target agents**: content-writer, editor

### Reference Materials
#### blog-seo-basics (Score: 3.0)
- **Source**: https://github.com/example/blog-seo-skill
- **Useful content**: SEO checklist and keyword density guidelines
- **Target capability**: SEO optimization checking
```
