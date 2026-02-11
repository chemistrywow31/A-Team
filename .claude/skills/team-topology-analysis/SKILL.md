---
name: Team Topology Analysis
description: Provide framework for analyzing team structure rationality and evaluating collaboration topology efficiency between agents
---

# Team Topology Analysis

## Description

Provide framework for analyzing team structure rationality, used to evaluate whether collaboration topology between agents is efficient and whether bottlenecks or redundancies exist.

## Belongs To

This skill belongs exclusively to `agents/discovery/role-designer.md`

## Core Knowledge

### Topology Patterns

#### 1. Pipeline Topology
```
A → B → C → D
```
- Applicable scenario: Work has strict sequential order
- Advantages: Clear responsibilities, predictable process
- Risk: Any blocked node causes entire chain to stall

#### 2. Hub & Spoke Topology
```
    B
    ↑
A ← Coordinator → C
    ↓
    D
```
- Applicable scenario: Multiple parallel work streams coordinated by one coordinator
- Advantages: Flexible assignment, easy to add/remove nodes
- Risk: Coordinator becomes single point of bottleneck

#### 3. Hybrid Topology
```
Coordinator → [GroupA: A1 → A2] → Review → [GroupB: B1, B2] → Final
```
- Applicable scenario: Complex teams with some sequential work, some parallel
- Usually the recommended final pattern

### Topology Health Check

1. **Bottleneck detection**: Is any agent the upstream of 3+ other agents simultaneously?
2. **Island detection**: Is any agent without any interaction with other team members?
3. **Cycle detection**: Does A→B→C→A circular dependency exist? (review cycles excluded)
4. **Coordinator load**: Does coordinator directly manage more than 7 agents? If so, recommend splitting into separate teams.

## Agent Teams Mode Considerations

### Shared Task List Patterns
- Use task dependencies (`blockedBy`) to enforce sequential gates
- Parallel agents claim tasks independently — no coordinator bottleneck
- Task ownership prevents duplicate work on the same deliverable

### File Ownership Rules
- Parallel agents must write to non-overlapping file sets
- Define ownership in each agent's "Communication Patterns" section
- On conflict: coordinator mediates, or designate a primary owner

### Communication Decision Framework

| Scenario | Channel | Rationale |
|----------|---------|-----------|
| Agent needs input from specific peer | Direct message | Avoids noise for others |
| Architecture decision change | Broadcast | Affects all agents |
| Task reassignment or priority change | Via coordinator | Coordinator tracks assignments |
| Review feedback | Direct message | Only reviewer ↔ author |

### Coordinator Bottleneck Mitigation
- Allow peer-to-peer communication for review pairs
- Limit broadcast to 2-3 defined critical triggers
- Coordinator focuses on: task assignment, dependency resolution, final quality gate
- Avoid routing routine status updates through coordinator

## Quality Checkpoints

- [ ] Every agent has at least one upstream or downstream connection
- [ ] Coordinator is at the logical center of topology
- [ ] No meaningless circular dependencies
- [ ] Parallel work agents are correctly grouped
- [ ] (Agent Teams) File ownership is non-overlapping between parallel agents
- [ ] (Agent Teams) Communication channels are defined for every peer-to-peer pair
- [ ] (Agent Teams) Broadcast triggers are limited and clearly defined
