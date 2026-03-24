---
name: Reviewer Mandate
description: Mandatory rule that every generated team must include a process reviewer role for continuous iteration
---

# Reviewer Mandate

## Applicability

- Applies to: All agents (all members of the design team must understand and follow this rule)

## Rule Content

### Process Reviewer Must Exist

Every generated team structure must contain a process reviewer role. This role reviews the team's execution process after each project or task cycle, identifies communication and collaboration issues, and produces actionable improvement recommendations.

### Process Reviewer Does Not Overlap with QA

The process reviewer is distinct from a QA or output quality reviewer:
- **QA reviewer** checks whether deliverables meet quality standards (correctness, completeness, format compliance)
- **Process reviewer** checks how the team worked together (communication quality, handoff efficiency, information flow, missed opportunities)

A team may have both roles. They must not be merged into a single agent. If the team has no separate QA role, the process reviewer still must not take on QA responsibilities — QA duties fall to other agents or the coordinator.

### Process Reviewer Scope

The process reviewer must evaluate the following dimensions at minimum:

1. **Inter-agent communication quality** — Were handoff messages clear and complete? Was critical information lost between agents?
2. **Workflow adherence** — Did agents follow the defined workflow phases? Were any steps skipped or executed out of order?
3. **Collaboration efficiency** — Were there unnecessary back-and-forth cycles? Were blockers identified and resolved promptly?
4. **Information completeness** — Did downstream agents receive all the context they needed from upstream agents?
5. **Missed opportunities** — Were there improvements or risks that no agent surfaced during execution?
6. **Scope drift detection** — Did each phase produce exactly what was requested — nothing more, nothing less? Compare stated requirements against actual deliverables. Flag both scope creep (unrequested additions) and requirements gaps (stated work not addressed). This dimension is informational, not blocking.

### Process Reviewer Output

The process reviewer must produce a structured retrospective report after each project cycle. The report must include:
- Scores or ratings for each evaluation dimension
- Specific evidence (references to task IDs, messages, or deliverables) for every identified issue
- Scope drift summary: `[CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]` with specific items
- Actionable recommendations for process improvement
- Positive highlights of what worked well

### Placement

The process reviewer must be placed in a dedicated group folder (e.g., `agents/review/` or `agents/quality/`). It must not be placed in the same group as the agents whose work it reviews.

## Violation Determination

- Generated team structure has no process reviewer agent → Violation
- Process reviewer's responsibilities overlap with QA (checking deliverable correctness instead of process quality) → Violation
- Process reviewer is placed in the same group folder as execution agents it reviews → Violation
- Process reviewer's .md file has no defined evaluation dimensions → Violation
- Process reviewer's .md file has no defined output format for the retrospective report → Violation

## Exceptions

- Teams with 3 or fewer total agents (including coordinator): The coordinator may absorb process review responsibilities as a secondary duty, documented in its Responsibilities section. A dedicated process reviewer agent is not required.
