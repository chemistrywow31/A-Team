---
name: A-Team
description: Entry point that spawns the Team Architect coordinator to run the full team design workflow
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team description or --restructure teams/path]"
---

# A-Team

## Description

Launch the Team Architect coordinator to run the complete team design workflow (Phase 1-6). Use this skill as the standard entry point for all team design requests.

## Trigger

Use when the user wants to design, create, or build a new multi-agent team structure.

## Execution

When this skill is invoked, spawn the Team Architect agent to handle the entire workflow:

1. Parse any arguments the user provided (team name, domain hints, constraints)
2. Spawn the `team-architect` agent via the Agent tool with subagent_type `Team Architect`
3. Pass the user's request and any arguments as the agent's prompt
4. The Team Architect runs its full 6-phase workflow: Discovery → Planning → Generation → Optimization → Review → Dialogue Review

### Spawn Instructions

Use the Agent tool with these parameters:

- `subagent_type`: `Team Architect`
- `model`: `opus`
- `prompt`: Include the user's original request and any arguments. If the user provided no details, instruct the Team Architect to begin with Phase 1 Discovery (requirements interview).

### With Arguments

If the user provides arguments after `/A-Team`, pass them as context:

```
/A-Team 英文教學內容團隊
```

→ Spawn Team Architect with prompt: "Design a team for: 英文教學內容團隊. Begin with Phase 1 Discovery."

```
/A-Team --restructure teams/existing-team
```

→ Spawn Team Architect with prompt: "Restructure the existing team at teams/existing-team. Run Phase 7."

### Without Arguments

```
/A-Team
```

→ Spawn Team Architect with prompt: "The user wants to design a new team. Begin with Phase 1 Discovery — start the requirements interview."

## Examples

### Normal Case

User: `/A-Team 自動化測試團隊`

Action: Spawn Team Architect → "Design a team for: 自動化測試團隊. Begin with Phase 1 Discovery."

### Restructuring Case

User: `/A-Team --restructure teams/english-teaching-content`

Action: Spawn Team Architect → "Restructure the existing team at teams/english-teaching-content. Run Phase 7 (Team Restructuring)."

### No Arguments Case

User: `/A-Team`

Action: Spawn Team Architect → "The user wants to design a new team. Begin with Phase 1 Discovery — start the requirements interview."
