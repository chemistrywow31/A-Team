---
name: team-retrospective
description: Facilitate team retrospective to identify problems, improvement opportunities, and skill gaps after task completion or blockers
---

# Team Retrospective

## When to Invoke

Trigger this retrospective when:
- ✅ Task completed successfully (learn what worked)
- ⚠️ Token consumption exceeded expectation by > 30%
- 🔴 Task stuck for > 3 rounds of back-and-forth dialogue
- ❌ Critical error occurred
- 📊 Sprint/milestone ends

Do NOT trigger for:
- Simple tasks that completed smoothly without issues
- Routine work with no learning opportunities

## Retrospective Framework

Use the "What-So What-Now What" structure:

### 1. What Happened? (Facts)

Gather objective data:
- **Task description**: What was the goal?
- **Token consumed**: Actual vs expected (if available)
- **Rounds of dialogue**: How many back-and-forths occurred?
- **Errors encountered**: List specific error messages or blockers
- **Time taken**: Actual vs expected duration

### 2. So What? (Analysis)

Analyze root causes using the 5 Whys technique:

```
Problem: [Describe the issue]
- Why did this happen? [First answer]
  - Why? [Dig deeper]
    - Why? [Dig deeper]
      - Why? [Dig deeper]
        - Why? [Root cause]
```

Common patterns to look for:
- ❌ **Capability gap**: Agent lacked necessary skill or tool
- ❌ **Unclear requirements**: Task description was vague
- ❌ **Communication breakdown**: Handoff between agents failed
- ❌ **Inefficiency**: Repetitive work or unnecessary steps
- ❌ **Quality issue**: Output didn't meet standards

### 3. Now What? (Actions)

Generate actionable improvements:

#### Short-term Fixes (apply immediately)
- Specific changes to current workflow
- Workarounds for known issues

#### Long-term Improvements (recommend to PM/Lead)
- **New skills needed**: "We need a skill for [specific capability]"
- **Rule adjustments**: "Modify [rule name] to add [specific guideline]"
- **Process changes**: "Change workflow to [specific improvement]"
- **Tool additions**: "Grant [agent] access to [specific tool]"

## Output Format

Generate a `retro.md` file in `.deliver/current/` with this structure:

```markdown
# Retrospective - Sprint {number} / Task {id}

**Date**: {YYYY-MM-DD}
**Facilitator**: {agent-name}
**Participants**: {list of agents involved}

## What Happened (Facts)

- **Task**: {brief description}
- **Outcome**: {Success | Partial | Failed | Blocked}
- **Token consumed**: {actual} (expected: {expected}, diff: {+/-}%)
- **Dialogue rounds**: {number}
- **Duration**: {time}

### Key Events
- {event 1}
- {event 2}
- {event 3}

## So What (Analysis)

### Root Causes
1. **[Category]**: {explanation using 5 Whys}
2. **[Category]**: {explanation using 5 Whys}

### What Went Well
- {positive point 1}
- {positive point 2}

### What Needs Improvement
- {pain point 1}
- {pain point 2}

## Now What (Actions)

### Immediate Actions (apply now)
- [ ] {action 1}
- [ ] {action 2}

### Recommendations for PM/Lead
- **New Skills**:
  - [ ] Create `{skill-name}` skill for {purpose}
- **Rule Updates**:
  - [ ] Modify `{rule-name}` to {specific change}
- **Process Changes**:
  - [ ] {process improvement}

### Lessons Learned
- **Do more of**: {behavior to amplify}
- **Do less of**: {behavior to reduce}
- **Start doing**: {new practice to adopt}
- **Stop doing**: {practice to eliminate}

## Follow-up

- **Next retro date**: {date or condition}
- **Owner for actions**: {agent responsible for tracking}
```

## Facilitation Tips

1. **Be specific**: "Communication was bad" → "Agent X delivered file path without explaining its purpose, causing Agent Y to re-read the entire file"

2. **Focus on systems, not blame**: "Agent X made a mistake" → "Our handoff protocol doesn't require verification, so errors propagate"

3. **Quantify impact**: "It was slow" → "Took 50K tokens and 12 rounds, expected 20K tokens and 4 rounds"

4. **Generate actionable outputs**: "We should improve" → "Add checklist to delivery-management rule requiring X, Y, Z"

5. **Celebrate wins**: Always list at least 2 "What Went Well" items

## Integration with Delivery Management

- Save output to `.deliver/current/retro.md`
- Reference this retro in next sprint's planning
- Track recommended actions in sprint backlog

## Example Invocation

**User**: "We just spent 80K tokens debugging an API issue that should have taken 20K. Let's retro."

**Agent**: [Facilitates retrospective, generates retro.md with analysis that skill gap exists - need a "api-debugging" skill that provides systematic debugging steps]
