# Delegation Template: Review

Use for: verification dispatches, decision audits, structure validation, dialogue review. Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in `.claude/rules/execution-contract.md` (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

## Template

```
TASK ID: {{id}}   TIER: {{haiku|sonnet|opus}}   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: {{one sentence — what artifact set gets reviewed against what bar}}
RUBRIC: apply {{JUDGMENT.md J5.x floors and/or rule-file violation lists}} — cite each by number
CONTEXT (absolute paths only): {{acceptance criteria file/list, absolute}}; {{artifact absolute paths}} — DO NOT send producer
  reasoning or history to this reviewer (EC-3.2)
SCOPE — IN: {{exact files to review}}
SCOPE — OUT (do not touch): the reviewer modifies nothing — findings only. Rewrites are a
  separate implementation dispatch (EC-3.1: judging and mutating the same artifact is forbidden)
FINDINGS FORMAT: one line per finding — {severity Critical|Major|Minor} | {file:line} | {issue} | {remedy}
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every reviewed file appears in the report with per-criterion PASS/FAIL + file:line evidence (EC-3.3).
  2. Executable artifacts were executed, output cited (EC-3.4); unexecuted claim = FAIL.
VERDICT: overall PASS only when every criterion on every file is PASS (EC-3.6)
REPORT: EC-1 schema (§7.1); findings over 30 lines → {{output file}}, send the path
HARNESS NOTE: the harness may block subagent Writes of report-shaped .md ("Subagents should
  return findings as text"); do not circumvent via Bash — return findings inline marked
  INLINE-FALLBACK (dispatch states the raised line cap); the dispatcher persists them verbatim
ESCALATE IF: J1.3 (expertise gap) or J3.1 (criteria conflict) fires; budget per EC-2.4
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: demo-15   TIER: opus   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: Verify the 6 generated agent files for teams/demo-team/ meet the agent floor and the Phase 2 plan.
RUBRIC: JUDGMENT.md J5.1 (agent floor) + rules/reasoning-and-self-critique.md violation list
CONTEXT (absolute paths only): /Users/{user}/{repo}/.worklog/202607/demo-team/phase-2-planning/decisions.md (criteria source);
  teams/demo-team/.claude/agents/ — DO NOT send producer reasoning (EC-3.2)
SCOPE — IN: all .md under teams/demo-team/.claude/agents/
SCOPE — OUT (do not touch): the reviewer modifies nothing; findings only
FINDINGS FORMAT: one line per finding — {severity} | {file:line} | {issue} | {remedy}
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every agent file has per-criterion PASS/FAIL with file:line evidence (EC-3.3).
  2. Section-order checks were executed via grep -n '^## ', output cited (EC-3.4).
VERDICT: overall PASS only when every criterion on every file is PASS (EC-3.6)
REPORT: EC-1 schema (§7.1); findings → .worklog/202607/demo-team/phase-3-generation/verification.md, send the path
ESCALATE IF: J1.3 or J3.1 fires
BUDGET: max 40 output lines / 30 tool calls
```
