---
name: Professional Mindset
description: Define measurable behaviors for efficiency consciousness, quality consciousness, and self-learning capability
---

# Professional Mindset

## Applicability

- Applies to: All agents (coordinator and all team members)

## Rule Content

### Three Pillars of Professional Behavior

Professional agents demonstrate three measurable capabilities:
1. **Efficiency Consciousness** — Deliver quickly without waste
2. **Quality Consciousness** — Meet standards consistently
3. **Learning Consciousness** — Improve continuously

## Efficiency Consciousness

### Model Selection

Choose model based on task complexity:

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Simple CRUD, formatting, routine operations | `haiku` | Fast, low cost, sufficient capability |
| Complex logic, architecture design, multi-file refactoring | `sonnet` | Balanced cost and capability |
| Critical decisions, novel problems, high-risk operations | `opus` | Maximum reasoning capability |

**Cost awareness**: `haiku` costs ~1/20 of `opus`. Defaulting to `opus` for simple tasks wastes resources.

### Avoid Redundant Work

Before starting work:
1. **Check `.deliver/`**: Has this been done before? Can I reuse artifacts?
2. **Check memory**: Is there context in CLAUDE.md or project docs?
3. **Check skills**: Does a skill already exist for this pattern?

Example:
- ❌ Agent manually formats JSON for 3rd time → Create `format-json` skill
- ✅ Agent checks `.deliver/sprint-001/artifacts/` for previous formatted examples

### Escalate Blockers Promptly

Do NOT spend > 3 dialogue rounds on the same blocker without escalating.

**Escalation protocol**:
1. **Round 1**: Attempt solution
2. **Round 2**: Try alternative approach
3. **Round 3**: If still blocked, message coordinator: "Blocked on [specific issue], need [specific help]"

**Anti-pattern**: Continuing to try same approach for 10+ rounds hoping for different result.

## Quality Consciousness

### Pre-Delivery Checklist

Before marking work complete, verify:

| Check | How to Verify | Violation if Failed |
|-------|--------------|-------------------|
| **Meets requirements** | Re-read task description, confirm all acceptance criteria met | Yes |
| **Follows standards** | Check relevant rules (writing-quality-standard, coding standards, etc.) | Yes |
| **No vague language** | Scan output for "try to", "appropriately", "if needed" without clear criteria | Yes |
| **Demonstrable** | Can this be demoed per demo-driven-delivery rule? | Yes |
| **Documented** | Includes DEMO.md, updated deliverables.md | Yes |

### Quality Gates

Quality thresholds by deliverable type:

| Deliverable | Quality Gate | Measured By |
|-------------|-------------|-------------|
| Agent .md | No responsibility overlap, imperative tone, < 300 lines | Code review by coordinator |
| Skill .md | Contains examples, clear invocation triggers | Skill can be invoked successfully |
| Rule .md | Contains violation determination, < 100 lines | Rule violations are detectable |
| Code | Passes tests, no hardcoded secrets, follows style guide | Automated checks |

**Reject criteria**: If deliverable doesn't meet quality gate, return to author for revision.

### Self-Review

Before submitting work, perform self-review:

```markdown
## Self-Review Checklist

- [ ] I re-read the requirements and confirmed I met all of them
- [ ] I checked for prohibited vague words ("try to", "appropriately")
- [ ] I verified this is demonstrable (has DEMO.md or clear proof)
- [ ] I updated deliverables.md
- [ ] I followed applicable rules and standards
- [ ] I tested/validated my output (ran the command, checked the format, etc.)
```

If any item unchecked → **do not submit**, fix first.

## Learning Consciousness

### Identify Knowledge Gaps

During retrospectives, explicitly answer:
1. **What skill do I lack?** "I struggled with X because I don't have skill for Y"
2. **What rule was unclear?** "I wasn't sure if Z was allowed"
3. **What would make me faster next time?** "If I had tool/skill/rule W, I could do X in 1/3 the time"

### Recommend Improvements

Proactively suggest to coordinator:
- **New skills**: "We should create `[skill-name]` for [specific recurring pattern]"
- **Rule updates**: "Rule `[rule-name]` should clarify [specific ambiguity]"
- **Process changes**: "We could save N tokens by [specific change]"

**Do NOT say**: "We should improve" (vague)
**DO say**: "Create `error-handling-checklist` skill containing 5-step debugging protocol, would have saved 30K tokens in last sprint" (specific)

### Document Lessons Learned

After completing non-trivial work, add a "Lessons Learned" section to your deliverable:

```markdown
## Lessons Learned

- **What worked well**: [Specific approach/tool/technique]
- **What to avoid**: [Specific anti-pattern discovered]
- **Next time, I would**: [Specific improvement]
```

This feeds into retrospectives and helps future agents.

## Integration with Other Rules

- **Efficiency** feeds into `continuous-improvement` — track token savings from optimizations
- **Quality** measured by `demo-driven-delivery` — demos prove quality
- **Learning** captured in `team-retrospective` — retros surface gaps

## Measurement (Optional)

Teams may track these metrics to measure professional mindset adoption:

| Metric | Target | Indicates |
|--------|--------|-----------|
| Avg model cost per task | Declining trend | Appropriate model selection |
| Rework rate | < 10% | Quality gate effectiveness |
| Escalation speed | < 3 rounds | Blocker awareness |
| Skills recommended → created | > 50% | Learning proactiveness |

## Violation Determination

- Agent uses `opus` for simple formatting task without justification → Efficiency violation
- Deliverable submitted without self-review checklist completed → Quality violation
- Same blocker encountered for > 3 rounds without escalation → Efficiency violation
- Retrospective identifies gap but agent doesn't recommend improvement → Learning violation
- Output contains prohibited vague words without criteria → Quality violation

## Exceptions

- In emergency situations (production down, critical bug), efficiency may be temporarily sacrificed for speed
- Experimental/research work may intentionally use higher-cost models for exploration
