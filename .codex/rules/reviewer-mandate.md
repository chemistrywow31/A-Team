---
name: Reviewer Mandate
description: Require a dedicated process reviewer in generated teams
---

# Reviewer Mandate

## Applicability

- Applies to: all generated teams

## Rule Content

### Process Reviewer Must Exist

Every generated team must include a process reviewer, unless the team is small enough for the documented exception below.

### Process Reviewer Is Not QA

QA checks deliverable correctness. The process reviewer checks how the team coordinated:

- handoff quality
- workflow adherence
- coordination efficiency
- information completeness
- missed opportunities

Do not merge QA and process review into one role.

### Process Reviewer Output

The process reviewer must produce a retrospective report with:

- scores or ratings for each evaluation dimension
- evidence for every issue
- actionable recommendations
- positive highlights

### Placement

Place the process reviewer in a dedicated group such as `.codex/agents/review/` or `.codex/agents/quality/`. Do not place it in the same group as the workers it audits.

## Violation Determination

- No process reviewer exists -> Violation
- The reviewer prompt focuses on deliverable QA instead of process quality -> Violation
- The reviewer lives in the same execution group as the workers it reviews -> Violation
- The reviewer prompt lacks evaluation dimensions or report format -> Violation

## Exceptions

- If the generated team has three or fewer total agents, the coordinator may absorb process review duties, but that secondary responsibility must be written explicitly in the coordinator prompt.
