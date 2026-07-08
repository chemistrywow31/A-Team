# Delegation Template: Implementation

Use for: generating files (agent/skill/rule .md, CLAUDE.md, settings.json) or writing code. Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in `.claude/rules/execution-contract.md` (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

## Template

```
TASK ID: {{id}}   TIER: {{haiku|sonnet|opus}}   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: {{one sentence, one deliverable}}
CONTEXT (absolute paths only): {{BRIEF absolute path}}; {{upstream decisions.md absolute paths}}; {{template/spec absolute paths to read first}}
SCOPE — IN: {{exact files to create or edit}}
SCOPE — OUT (do not touch): {{dirs/files owned by other agents this phase}}
CONSTRAINTS: {{length limits, mandatory sections, naming rules — cite the rule file}}
ACCEPTANCE CRITERIA (mechanically checkable):
  1. {{e.g. file passes the J5 floor for its artifact type}}
  2. {{e.g. grep/wc check specific to this task}}
CHECKS TO RUN BEFORE REPORTING: {{exact commands, e.g. head -1, grep -n '^## ', wc -l, jq .}}
NO PLACEHOLDERS: delivered files contain zero TODO/TBD/{{...}} markers
EXECUTION EVIDENCE: paste nothing — run the checks, cite their output location in EVIDENCE
VERIFICATION: fresh-context verifier re-runs the checks and reads back each criterion, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); anything over 30 lines → file under {{worklog path}}, send the path
ESCALATE IF: J1.1, J1.2, J4.2 (fix keeps growing), or J4.3 (weakened check) fires
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: demo-11   TIER: opus   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: Generate the 4 mandatory rule files for teams/demo-team/.claude/rules/.
CONTEXT (paths only): .worklog/202607/demo-team/brief.md; .worklog/202607/demo-team/phase-2-planning/decisions.md; .claude/rules/execution-contract.md (adapt as the team's execution contract)
SCOPE — IN: teams/demo-team/.claude/rules/{worklog,context-management,reasoning-and-self-critique,execution-contract}.md
SCOPE — OUT (do not touch): teams/demo-team/.claude/agents/, skills/, CLAUDE.md (agent-writer owns these)
CONSTRAINTS: each rule ≤ 100 lines with Violation Determination + Exceptions, per rules/writing-quality-standard.md
ACCEPTANCE CRITERIA (mechanically checkable):
  1. All 4 files exist, pass the J5.3 floor (frontmatter, both sections, ≤ 100 lines).
  2. execution-contract.md keeps EC-1..EC-5 clause numbering so agents can cite it.
CHECKS TO RUN BEFORE REPORTING: head -1 each file; grep -n '^## Violation' each; wc -l each
NO PLACEHOLDERS: delivered files contain zero TODO/TBD markers
VERIFICATION: fresh-context verifier re-runs the checks and reads back each criterion, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); check outputs → .worklog/202607/demo-team/phase-3-generation/findings.md, send the path
ESCALATE IF: J1.1, J1.2, J4.2, or J4.3 fires
BUDGET: max 40 output lines / 30 tool calls
```
