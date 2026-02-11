---
name: Quality Validation
description: Provide validation methods to check if final team structure output is complete and consistent
---

# Quality Validation

## Description

Provide validation methods to check if final output (entire team's agents/skills/rules structure) is complete and consistent.

## Belongs To

This skill belongs exclusively to `agents/team-architect.md`

## Validation Process

### Level 1: Structural Completeness

```
✓ teams/{team-name}/ directory exists
✓ agents/ directory exists and contains at least one coordinator .md
✓ skills/ directory exists and contains skill folders
✓ rules/ directory exists and contains at least one .md file
✓ All .md file names use kebab-case
✓ All agent group folder names use kebab-case
```

### Level 2: Content Completeness

```
✓ Each agent .md contains: Identity, Responsibilities, Input and Output, Workflow, Available Skills, Applicable Rules, Collaboration Relationships, Boundaries
✓ Coordinator .md additionally contains: Team Overview, Subordinate Agent List, Task Assignment Strategy, Quality Control Mechanism
✓ Each skill .md contains: Description, Users/Belongs To, Core Knowledge
✓ Each rule .md contains: Applicability, Rule Content, Violation Determination
✓ Each external skill (Pattern A or B) contains a Source Attribution section with Origin, Integration, Retrieved, and Modifications fields
```

### Level 3: Reference Consistency

```
✓ Each skill path referenced in agent .md corresponds to an actual existing file
✓ Each rule path referenced in agent .md corresponds to an actual existing file
✓ Users listed in skill .md correspond to actual existing agents
✓ Applicability scope in rule .md corresponds to actual existing agents
✓ Coordinator's subordinate list covers all non-coordinator agents
✓ External skill Source Attribution URLs match the source recorded in the Phase 2 plan
✓ External skill Integration type (Pattern A/B) is consistent between Source Attribution and the Phase 2 plan
```

### Level 4: Logical Consistency

```
✓ No two agents have overlapping responsibilities (unless designed as review relationship)
✓ All agent responsibilities combined cover the team's complete scope of work
✓ No agent appears in two different groups simultaneously
✓ Collaboration relationships are bidirectionally consistent (A says downstream is B, B should say upstream is A)
```

## Validation Result Format

```markdown
# Quality Validation Report: {team-name}

## Structural Completeness: ✓ Pass / ✗ Fail
{If failed, list specific issues}

## Content Completeness: ✓ Pass / ✗ Fail
{If failed, list specific issues}

## Reference Consistency: ✓ Pass / ✗ Fail
{If failed, list specific issues}

## Logical Consistency: ✓ Pass / ✗ Fail
{If failed, list specific issues}

## Summary
{Pass / Needs correction, and correction recommendations}
```
