---
name: Worklog
description: Require task-path-aware worklogs with classification, probe, and acceptance evidence for team design changes
---

# Worklog

## Applicability

- Applies to: `team-architect` and every specialist when a team-design task spans discovery, planning, generation, or review

## Rule Content

### Maintain Task Worklogs

Create a worklog for each team-design task under:

```text
.worklog/{yyyymm}/{task-name}/phase-{n}-{label}/
```

The coordinator also creates `.worklog/{yyyymm}/{task-name}/brief.md` before the first dispatch unless the task is truly single-dispatch.

Each phase folder must contain:

- `references.md`: sources, files, user statements, and tool outputs consulted
- `findings.md`: analysis derived from references
- `decisions.md`: decisions, rationale, alternatives, evidence, and downstream impact
- `audit.md`: optional decision audit output

### Preserve The Evidence Chain

Every decision must trace to findings, and every finding must trace to references. If no external or internal reference exists, write `No established reference found for {topic}` in `references.md` and document first-principles reasoning in `decisions.md`.

### Record Classification For Existing-Team Work

When the task touches an existing team, record:

- runnable surfaces and activation state
- canonical authority or ambiguity
- stamp state
- mapping completeness
- gap class: `Codex-only runtime gap` or `cross-platform design gap`

### Record Runtime Probe And Acceptance Evidence

When runtime-affecting files change, record or link:

- strict-config output
- validator output
- host-tool or runtime probe evidence
- protected-path observations
- setup, verify, and rollback guidance location
- fresh-context verifier verdicts

### Phase Boundary Check

Before moving to the next phase, confirm the three core files exist and contain the evidence needed by downstream agents. Do not proceed with undocumented decisions.

## Violation Determination

- a phase completes without a corresponding worklog folder -> Violation
- a delegated multi-step task has no `brief.md` -> Violation
- a phase worklog is missing `references.md`, `findings.md`, or `decisions.md` -> Violation
- a decision has no traceable evidence chain -> Violation
- existing-team work changes runtime or structure without recording surface classification and gap class -> Violation
- runtime-affecting changes close without probe evidence or fresh-context acceptance evidence -> Violation
- the coordinator enters the next phase before checking worklog completeness -> Violation

## Exceptions

For a single-turn maintenance change that produces no design decision, write a brief note in the final response instead of creating a worklog.
