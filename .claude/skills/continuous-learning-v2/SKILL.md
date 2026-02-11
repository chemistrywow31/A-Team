---
name: Continuous Learning V2
description: Instinct-based learning system that captures team design patterns via hooks and evolves them into reusable knowledge
---

# Continuous Learning V2

## Description

Capture team design patterns from A-Team sessions using hook-based observation. Detected patterns become "instincts" — atomic learned behaviors with confidence scoring that improve future team designs.

## Users

Infrastructure-level skill. Operates via hooks in `settings.json` and benefits all agents automatically. No explicit agent invocation required.

## Core Concept

An instinct is a small learned behavior:

```yaml
---
id: always-propose-qa-role
trigger: "when designing a team that produces deliverables"
confidence: 0.9
domain: "role-design"
---

# Always Propose QA Role

## Action
Proactively propose a quality checker/reviewer role during requirements exploration.

## Evidence
- User added QA role in 3/4 recent designs after initial omission
```

**Properties:**
- **Atomic** — one trigger, one action
- **Confidence-weighted** — 0.3 tentative, 0.7 auto-applied, 0.9 core behavior
- **Domain-tagged** — role-design, skill-planning, model-selection, workflow
- **Evidence-backed** — tracks observations that created it

## How It Works

```
Team Design Session
      │
      │ Hooks capture tool use + user feedback (100% reliable)
      ▼
  observations.jsonl
      │
      │ Observer agent (background, Haiku)
      ▼
  PATTERN DETECTION
  • User corrections → instinct
  • Repeated structures → instinct
  • Successful designs → instinct
      │
      ▼
  instincts/personal/
  • always-propose-qa-role.md (0.9)
  • writers-use-sonnet.md (0.7)
  • check-tech-feasibility.md (0.8)
```

## Team Design Patterns to Detect

### Role Structure Patterns
- Roles users consistently add or request (QA, tech feasibility)
- Role granularity preferences per team complexity
- Coordinator scope patterns across teams

### User Correction Patterns
- Roles the user added after initial design
- Model selection corrections (e.g., writer agents downgraded from opus)
- Skill/rule additions the user requested

### Workflow Patterns
- Common phase structures across designed teams
- Typical agent/skill/rule counts per team size
- Deployment mode preferences (subagent vs Agent Teams)

### Quality Patterns
- Cross-validation issues that recur across teams
- Common reference consistency problems
- Naming convention preferences

## Hook Configuration

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh pre"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh post"
      }]
    }]
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/instinct-status` | Show learned team design instincts with confidence |
| `/evolve` | Cluster related instincts into reusable skills |
| `/instinct-export` | Export instincts for sharing |
| `/instinct-import` | Import instincts from other A-Team instances |

## Integration with A-Team Memory

Instincts complement the auto memory system (`MEMORY.md`):
- **MEMORY.md**: Manually curated, high-confidence project-level patterns
- **Instincts**: Automatically detected, confidence-scored session-level patterns
- Promote instincts at 0.9+ confidence to MEMORY.md for persistence

## Example

### Input

After 5 team design sessions, observer detects: in 4/5 sessions, the user asked to add a "technical feasibility assessor" role that was not in the initial design.

### Output

```yaml
---
id: propose-tech-feasibility-role
trigger: "when designing a technology-oriented team"
confidence: 0.8
domain: "role-design"
---

# Propose Technical Feasibility Role

## Action
When the team's output involves technology, proactively ask the user if a technical feasibility assessment role is needed.

## Evidence
- User added tech feasibility role in 4/5 recent tech team designs
- Pattern first observed: 2025-01-20
```
