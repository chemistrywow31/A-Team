# Delegation Template: Implementation

Use for: generating files (agent/skill/rule .md, CLAUDE.md, settings.json) or writing code. Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in the selected runtime's execution contract (`.claude/rules/execution-contract.md` or `.codex/rules/execution-contract.md`) (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

Select a runtime-native tier and effective model/effort from the target profile. Claude aliases in filled examples are illustrative; preserve explicit target pins and use the current host's delegation tool.

## Template

```
TASK ID: {{id}}   TIER: {{selected runtime tier; explicit model/effort or supported inheritance}}   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: {{one sentence, one deliverable}}
CONTEXT (absolute paths only): {{BRIEF absolute path}}; {{upstream decisions.md absolute paths}}; {{template/spec absolute paths to read first}}
SCOPE — IN: {{exact files to create or edit}}
SCOPE — OUT (do not touch): {{dirs/files owned by other agents this phase}}
CONSTRAINTS: {{size review targets or explicit task caps, mandatory sections, native metadata — cite the rule file}}
ACCEPTANCE CRITERIA (mechanically checkable):
  1. {{e.g. file passes the J5 floor for its artifact type}}
  2. {{e.g. grep/wc check specific to this task}}
CHECKS TO RUN BEFORE REPORTING: {{exact commands, e.g. head -1, grep -n '^## ', wc -l, jq .}}
NO PLACEHOLDERS: delivered files contain zero TODO/TBD/{{...}} markers
EXECUTION EVIDENCE: paste nothing — run the checks, cite their output location in EVIDENCE
VERIFICATION: fresh-context verifier re-runs the checks and reads back each criterion, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); anything over 30 lines → file under {{worklog path}}, send the path
HARNESS NOTE: if the host blocks the assigned report write, preserve the sandbox. Return
  INLINE-FALLBACK under EC-1.12 with at most {{finite fallback line cap}} lines; coordinator
  persists the report to {{exact report path}} before acceptance. This covers report evidence
  only; blocked production writes still require escalation.
ESCALATE IF: J1.1, J1.2, J4.2 (fix keeps growing), or J4.3 (weakened check) fires
BUDGET: max {{lines}} normal report lines or the explicit INLINE-FALLBACK cap / {{count}} tool calls
```

## Filled example

```
TASK ID: demo-11   TIER: strong; Claude opus example, preserve the selected runtime profile   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: Generate the 4 mandatory rule files for teams/demo-team/.claude/rules/.
CONTEXT (absolute paths only): /Users/{user}/{repo}/.worklog/202607/demo-team/brief.md; /Users/{user}/{repo}/.worklog/202607/demo-team/phase-2-planning/decisions.md; /Users/{user}/{repo}/.claude/rules/execution-contract.md (Claude example; use the target runtime contract)
SCOPE — IN: teams/demo-team/.claude/rules/{worklog,context-management,reasoning-and-self-critique,execution-contract}.md
SCOPE — OUT (do not touch): teams/demo-team/.claude/agents/, skills/, CLAUDE.md (agent-writer owns these)
CONSTRAINTS: each rule has Violation Determination + Exceptions; >100 lines triggers independent usefulness review, per JUDGMENT.md J5.3
ACCEPTANCE CRITERIA (mechanically checkable):
  1. All 4 files exist and pass J5.3 (frontmatter, both sections, and any size review explicitly resolved).
  2. execution-contract.md keeps EC-1..EC-5 clause numbering so agents can cite it.
CHECKS TO RUN BEFORE REPORTING: head -1 each file; grep -n '^## Violation' each; wc -l each
NO PLACEHOLDERS: delivered files contain zero TODO/TBD markers
VERIFICATION: fresh-context verifier re-runs the checks and reads back each criterion, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); check outputs → .worklog/202607/demo-team/phase-3-generation/findings.md, send the path
INLINE-FALLBACK: report-write block only; max 100 lines; coordinator persists the REPORT path before acceptance
ESCALATE IF: J1.1, J1.2, J4.2, or J4.3 fires
BUDGET: max 40 normal report lines or 100 INLINE-FALLBACK lines / 30 tool calls
```
