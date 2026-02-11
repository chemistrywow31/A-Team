---
name: Continuous Improvement
description: Mandate retrospective execution and improvement tracking to build organizational learning capability
---

# Continuous Improvement

## Applicability

- Applies to: All agents (mandatory for coordinator, encouraged for all members)

## Rule Content

### Retrospective Triggers

Coordinator MUST trigger `/team-retrospective` when:

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Token overconsumption | Actual tokens > Expected + 30% | Mandatory retro |
| Task stuck | > 3 rounds of back-and-forth without progress | Mandatory retro |
| Critical error | Build failure, security issue, data loss | Mandatory retro |
| Sprint end | Every sprint/milestone completion | Mandatory retro |

Any team member MAY request retro when:
- Discovering recurring problems
- Identifying skill gaps
- Experiencing communication breakdown

### Retro Execution Protocol

1. **Coordinator invokes**: `/team-retrospective` (or delegate to facilitator)
2. **Facilitator generates**: `retro.md` in `.deliver/current/`
3. **Coordinator reviews**: All recommendations within 24 hours (or next work session)
4. **Coordinator decides**: Accept/reject/modify each recommendation
5. **Coordinator tracks**: Approved improvements in sprint backlog

### Improvement Backlog Structure

Maintain `.deliver/improvements.md` tracking all recommendations:

```markdown
# Improvement Backlog

## In Progress
- [ ] **[Sprint-002-R1]** Create `api-debugging` skill (Owner: skill-writer, Due: Sprint 003)

## Approved (Not Started)
- [ ] **[Sprint-001-R2]** Add checklist to delivery-management rule
- [ ] **[Sprint-002-R3]** Grant agent-writer access to Bash tool

## Completed
- [x] **[Sprint-001-R1]** Reduce deliverables.md verbosity (Completed: 2026-02-05)

## Rejected (with rationale)
- [x] **[Sprint-001-R3]** Use opus for all agents (Reason: Cost too high, use selectively)
```

### Decision Criteria for Recommendations

Coordinator evaluates recommendations using:

| Criterion | Weight | Questions |
|-----------|--------|-----------|
| **Impact** | 40% | Will this prevent future issues? How many times would this help? |
| **Cost** | 30% | Token/time cost to implement? Ongoing maintenance burden? |
| **Urgency** | 20% | Is this blocking work? Can we delay? |
| **Feasibility** | 10% | Do we have capability to implement? Any dependencies? |

Score 1-5 for each criterion, weighted total ≥ 3.5 → Approve.

### Knowledge Transfer

After each retro:
1. **Update team knowledge base**: Add lessons to relevant skill/rule files
2. **Brief incoming team**: If handover occurs, include retro summary in handover-notes.md
3. **Pattern recognition**: After 3 sprints, identify recurring issues and systemic solutions

### Learning Metrics (Optional Tracking)

Track these metrics to measure improvement culture health:

| Metric | Target | Tracking Method |
|--------|--------|-----------------|
| Retro completion rate | 100% for mandatory triggers | Count retros vs triggers |
| Avg time to action | < 1 sprint | Date approved → date implemented |
| Repeat issue rate | < 10% | Same root cause in multiple retros |
| Skill gap closure | > 70% addressed | Recommended skills vs created skills |

## Violation Determination

- Mandatory retro trigger occurs but coordinator does not invoke `/team-retrospective` → Violation
- Retro completes but `retro.md` not saved to `.deliver/current/` → Violation
- Coordinator does not review recommendations within 24 hours (or next session) → Violation
- Improvement backlog not maintained (no tracking of approved actions) → Violation
- Same issue appears in 3 consecutive retros without systemic fix → Violation

## Exceptions

- If user explicitly requests "skip retro", coordinator may skip but must document reason in sprint notes
- For experimental/prototype teams (lifespan < 1 day), retro can be optional
