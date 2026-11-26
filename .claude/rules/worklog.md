---
name: Worklog
description: Phase-level evidence in .worklog/ for A-Team's own design tasks
paths:
  - ".worklog/**"
  - "teams/**"
---

# Worklog

## Applicability

- Applies to: A-Team's own design tasks, where every agent reads from and writes to the worklog
- Generated teams: a worklog is not part of every team. Add one, sized to the need, when a flow must be resumable across sessions or audited afterwards. Do not copy this rule into a team.

## Rule Content

### Every Task Must Have a Worklog

Every task executed by the team must maintain a worklog under the `.worklog/` directory. The worklog records reference information, key findings, and decision rationale for each phase, ensuring all work is verifiable, traceable, and continuable.

### Directory Structure and Naming

```
.worklog/{yyyymm}/{task-name}/
  ├── brief.md          ← task BRIEF: goal, constraints, key paths (rules/execution-contract.md EC-5.1)
  ├── dialogue-log.md   ← every user Q&A exchange, appended when it happens
  └── phase-{n}-{label}/
      ├── references.md    ├── findings.md    ├── decisions.md    └── audit.md (optional)
```

- `{yyyymm}`: Year-month of task start (e.g., `202603`)
- `{task-name}`: kebab-case (e.g., `english-teaching-team`)
- `phase-{n}-{label}`: numbered sequentially, kebab-case label (e.g., `phase-1-discovery`)

### Required Files Per Phase

Each phase folder must contain three core files:

#### references.md

Record all information sources consulted during this phase:
- URLs to documentation, articles, or tools evaluated
- File paths to internal documents referenced
- Conversation segments or user statements that informed decisions
- Domain Researcher reports (when investigation was conducted)

Each reference must include: source identifier, brief description of content, and how it was used.

#### findings.md

Record key discoveries and analysis derived from the references:
- Facts established from research
- Patterns identified across multiple sources
- Constraints or limitations discovered
- Comparative analysis results (e.g., tool A vs tool B)

Each finding must trace back to at least one entry in `references.md`.

#### decisions.md

Record every decision made during this phase:
- The decision statement (what was decided)
- The rationale (why this option was chosen)
- Alternatives considered and why they were rejected
- Supporting evidence (references to `findings.md` and `references.md`)
- Impact assessment (what this decision affects downstream)

Each decision must be defensible — a reader who disagrees must be able to identify which specific evidence or reasoning to challenge.

### Evidence Chain Requirement

The three files form an evidence chain: **references → findings → decisions**. Every decision must trace back through findings to references. A decision with no traceable evidence chain is a violation.

When no external reference exists for a decision, `references.md` must explicitly state: "No established reference found for {topic}." The corresponding `decisions.md` entry must document the first-principles reasoning used instead.

### Worklog Creation Timing

- The coordinator creates the worklog directory structure at the start of each task, before dispatching any phase work — including `brief.md` and an EMPTY `dialogue-log.md` (created even when no dialogue has happened yet: Phase 6 reads this file, and an absent file blocks the dialogue review)
- Each agent writes to the worklog during and at the end of their phase work
- The coordinator verifies worklog completeness at each phase boundary before proceeding

Once something is in the worklog, pass its path instead of its content; `.claude/rules/context-management.md` covers dispatch and resume.

## Violation Determination

- Task completes a phase with no corresponding worklog directory → Violation
- Phase worklog missing any of the three core files (references.md, findings.md, decisions.md) → Violation
- `decisions.md` contains a decision with no traceable evidence (no reference to findings or references) → Violation
- `findings.md` contains a finding with no source reference → Violation
- Coordinator proceeds to next phase without verifying worklog completeness → Violation
- Worklog directory or file names do not follow kebab-case convention → Violation

## Exceptions

- Phases that produce no decisions (e.g., a phase that only collects user input without making design choices) may have an empty `decisions.md` with a note: "No decisions made in this phase — input collection only."
- For tasks with a single phase, the phase folder is still required (e.g., `phase-1-execution/`).
- A generated team that keeps a worklog chooses its own format. A-Team's own design phases use the full triad.
