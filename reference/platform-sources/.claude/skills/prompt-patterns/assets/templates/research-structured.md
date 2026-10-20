---
name: Structured Research
category: templates
applies_when:
  - generating-research-agent
  - long-running-tasks
tags: [research, hypothesis-tracking, calibration, systematic]
source: raw/claude-4-best-practices.md
---

# Structured Research

## When to Use

Inject into research agents, domain investigators, or any agent that gathers and synthesizes information from multiple sources over extended workflows.

## Template

```text
Search for this information in a structured way. As you gather data, develop several competing hypotheses. Track your confidence levels in your progress notes to improve calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or research notes file to persist information and provide transparency. Break down this complex research task systematically.
```

## Adaptation Notes

Customize "hypothesis tree or research notes file" to match the team's worklog structure (e.g., replace with `.worklog/.../findings.md`). For teams using A-Team's worklog system, direct the agent to write hypotheses and confidence levels into `findings.md`.
