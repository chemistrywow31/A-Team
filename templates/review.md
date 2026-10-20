# Delegation Template: Review

Use for: verification dispatches, decision audits, structure validation, dialogue review. Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in the selected runtime's execution contract (`.grok/policies/execution-contract.md`) (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

Assign context tier by decision scope. Omit model/effort unless a measured native override is authorized; preserve existing target pins. Root uses advertised `spawn_subagent` with `background`, and `subagent_type` only when its live enum contains the selected role. A new acceptance reviewer never receives `resume_from`. These are dispatch templates, not executable tool argument objects.

## Template

```
TASK ID: {{id}}   CONTEXT TIER / PROFILE: {{decision scope; supported measured override or default omission}}   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: {{one sentence — what artifact set gets reviewed against what bar}}
RUBRIC: apply {{JUDGMENT.md J5.x floors and/or rule-file violation lists}} — cite each by number
CONTEXT (absolute paths only): {{acceptance criteria file/list, absolute}}; {{artifact absolute paths}} — DO NOT send producer
  reasoning or history to this reviewer (EC-3.2)
SCOPE — IN: {{exact frozen files to review; exact report path to write}}
SCOPE — OUT (do not touch): reviewed sources remain frozen; only the assigned report may be written.
  Rewrites require a separate owner/dispatch (EC-3.1: do not judge and mutate the same artifact).
FINDINGS FORMAT: one line per finding — {severity Critical|Major|Minor} | {file:line} | {issue} | {remedy}
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every reviewed file appears in the report with per-criterion PASS/FAIL + file:line evidence (EC-3.3).
  2. Relevant executable checks ran with cited evidence (EC-3.4); unavailable effective runtime claims stay UNVERIFIED/FAIL, separate from discovery.
VERDICT: overall PASS only when every criterion on every file is PASS (EC-3.6)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); findings over 30 lines → {{output file}}, send the path
HARNESS NOTE: if the host blocks the assigned report write, preserve the sandbox. Return
  INLINE-FALLBACK under EC-1.12 with at most {{finite fallback line cap}} lines; coordinator
  persists the report to {{exact report path}}. It remains pending until saved. This covers
  report evidence only, not blocked production writes or raw private reasoning/tool dumps.
ESCALATE IF: J1.3 (expertise gap) or J3.1 (criteria conflict) fires; budget per EC-2.4
BUDGET: max {{lines}} normal report lines or the explicit INLINE-FALLBACK cap / {{count}} tool calls
```

## Filled example

```
TASK ID: review_demo_agents   CONTEXT TIER / PROFILE: 3; model and effort omitted; effective values unverified   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: Verify the 6 generated agent files for teams/demo-team/ meet the agent floor and the Phase 2 plan.
RUBRIC: JUDGMENT.md J5.1 (agent floor) + .grok/policies/reasoning-and-self-critique.md violation list
CONTEXT (absolute paths only): /Users/{user}/{repo}/.worklog/202607/demo-team/phase-2-planning/decisions.md (criteria source);
  /Users/{user}/{repo}/teams/demo-team/.grok/agents/ — DO NOT send producer reasoning (EC-3.2)
SCOPE — IN: the six exact frozen agent paths enumerated in the criteria file;
  .worklog/202607/demo-team/phase-3-generation/verification.md (report only)
SCOPE — OUT (do not touch): all reviewed sources; only the exact REPORT path may be written
FINDINGS FORMAT: one line per finding — {severity} | {file:line} | {issue} | {remedy}
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every agent file has per-criterion PASS/FAIL with file:line evidence (EC-3.3).
  2. Section-order checks were executed via grep -n '^## ', output cited (EC-3.4).
VERDICT: overall PASS only when every criterion on every file is PASS (EC-3.6)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); findings → .worklog/202607/demo-team/phase-3-generation/verification.md, send the path
INLINE-FALLBACK: report-write block only; max 100 lines; coordinator persists the REPORT path before acceptance
ESCALATE IF: J1.3 or J3.1 fires
BUDGET: max 40 normal report lines or 100 INLINE-FALLBACK lines / 30 tool calls
```
