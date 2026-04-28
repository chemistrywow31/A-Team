---
name: Worklog
description: Require phase-level evidence logs for traceable team design decisions
---

# Worklog

## Applicability

- Applies to: `team-architect` and every specialist when a team-design task spans discovery, planning, generation, or review

## Rule Content

### Maintain Phase Worklogs

Create a worklog for each team-design task under:

```text
.worklog/{yyyymm}/{task-name}/phase-{n}-{label}/
```

Each phase folder must contain:

- `references.md`: sources, files, user statements, and tool outputs consulted
- `findings.md`: analysis derived from references
- `decisions.md`: decisions, rationale, alternatives, evidence, and downstream impact
- `audit.md`: optional decision audit output

### Preserve The Evidence Chain

Every decision must trace to findings, and every finding must trace to references. If no external or internal reference exists, write `No established reference found for {topic}` in `references.md` and document first-principles reasoning in `decisions.md`.

### Use Worklog As Context Offload

Pass worklog paths and summaries to specialists instead of copying large upstream content. Downstream phases must read upstream `decisions.md` and relevant findings before producing artifacts.

### Phase Boundary Check

Before moving to the next phase, confirm the three core files exist and contain the evidence needed by downstream agents. Do not proceed with undocumented decisions.

## Violation Determination

- a phase completes without a corresponding worklog folder -> Violation
- a phase worklog is missing `references.md`, `findings.md`, or `decisions.md` -> Violation
- a decision has no traceable evidence chain -> Violation
- a downstream agent receives large inline context instead of upstream worklog paths when paths are available -> Violation
- the coordinator enters the next phase before checking worklog completeness -> Violation

## Exceptions

For a single-turn maintenance change that produces no design decision, write a brief note in the final response instead of creating a worklog.
