---
name: Demo Driven Delivery
description: Enforce milestone-based demonstrable outcomes to ensure continuous stakeholder visibility
---

# Demo Driven Delivery

## Applicability

- Applies to: Coordinator (PM, Tech Lead) and all team members

## Rule Content

### Core Principle

Every milestone must produce demonstrable output that external stakeholders can understand without technical knowledge.

**Definition of "Demonstrable"**:
- Can be shown to stakeholders within 5 minutes
- Requires no setup or explanation beyond: "Here's what we built"
- Provides visual or tangible proof of progress

### Milestone Planning

Coordinator must:
1. Define demo checkpoints when breaking down work
2. Each checkpoint must specify: "What will we demo?"
3. No milestone can span > 3 days without a demo checkpoint

### Demo Types by Audience

| Audience | Acceptable Demo Format | Examples |
|----------|----------------------|----------|
| Technical team | Running code, API response, test results | `curl` output, passing test suite, debugger screenshot |
| Management | Visual artifacts, metrics, diagrams | Architecture diagram, progress chart, before/after comparison |
| End users | Interactive prototype, video, screenshots | Clickable mockup, screen recording, UI screenshots |

### Member Delivery Requirements

When completing work, include a `DEMO.md` file alongside deliverables:

```markdown
# Demo Guide - [Task ID]

## Quick Demo (< 2 min)
[One-paragraph explanation + visual/command to run]

## Full Demo (< 5 min)
1. Setup (if any)
2. Steps to demonstrate functionality
3. Expected outcome

## Demo Artifacts
- Screenshot: [path/to/screenshot.png]
- Video: [path/to/demo.mp4]
- Live URL: [if applicable]
```

### Half-Finished Work Rule

If work is 50-90% done but not demo-ready:
1. Identify the "demoable subset"
2. Complete that subset to 100%
3. Demo the subset, defer the rest to next milestone

**Example**:
- ❌ "User registration 80% done" (not demoable)
- ✅ "Registration form UI 100% done, backend pending" (demoable: show form, explain backend is next)

### Coordinator Demo Preparation

Before stakeholder update, coordinator must:
1. Review all `DEMO.md` files from completed work
2. Prepare unified demo script combining all milestones
3. Verify demos work (run commands, check screenshots)

## Violation Determination

- Milestone defined without "What will we demo?" specification → Violation
- Member completes work without `DEMO.md` → Violation
- Demo requires > 5 minutes setup → Violation
- Coordinator reports "90% done" without demonstrable output → Violation
- Demo fails when coordinator attempts to run it → Violation

## Exceptions

- Infrastructure work (CI/CD, tooling) can substitute metrics for demos (e.g., "Build time reduced from 10min to 3min")
- Research/spike tasks can demo "findings document" instead of working software
