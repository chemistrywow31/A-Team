# Delegation Template: Research

Use for: domain investigation, best-practice synthesis, comparative analysis (domain-researcher work). Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in the selected runtime's execution contract (`.grok/policies/execution-contract.md`) (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

Assign context tier by decision scope. Omit model/effort unless a measured native override is authorized; preserve existing target pins. Root uses advertised `spawn_subagent` with `background`, and `subagent_type` only when its live enum contains the selected role. A new acceptance reviewer never receives `resume_from`. These are dispatch templates, not executable tool argument objects.

## Template

```
TASK ID: {{id}}   CONTEXT TIER / PROFILE: {{decision scope; supported measured override or default omission}}   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: {{the one question this research must answer}}
QUESTION DECOMPOSITION: {{2–5 sub-questions; each gets its own evidence-table rows}}
CONTEXT (absolute paths only): {{BRIEF absolute path}}; {{upstream decisions.md absolute paths}}
SCOPE — IN: {{domains/source types; exact evidence files to create}}
SCOPE — OUT (do not touch): {{out-of-scope topics; no file modifications outside the output file}}
EVIDENCE TABLE (required output format, one row per claim):
  | claim | source (URL + date) | confidence (state source quality, corroboration, and inference limits) |
CONTRADICTIONS: surface every source disagreement explicitly in a CONTRADICTIONS section;
  resolving one silently = failed attempt. No resolver → list both positions + what would settle it.
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every sub-question has ≥ {{N}} evidence rows or an explicit "no source found: {queries}".
  2. Every claim in CONCLUSIONS appears in the evidence table.
STOP CONDITION: stop after {{K}} sources per sub-question or when marginal sources repeat known claims
VERIFICATION: fresh-context verifier spot-checks {{M}} rows: source resolves and supports the claim, per EC-3 (§7.3)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); full table → {{output file}}, send the path
ESCALATE IF: J1.2 (question ambiguous), J1.3 (verification exceeds demonstrated expertise), or J4.1 fires
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: research_legal_workflow   CONTEXT TIER / PROFILE: 3; model and effort omitted; effective values unverified   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: What workflow stages do professional legal-review teams use for contract analysis?
QUESTION DECOMPOSITION: (1) standard stages; (2) roles per stage; (3) common failure points; (4) automation precedents
CONTEXT (paths only): .worklog/202607/legal-team/brief.md; .worklog/202607/legal-team/phase-1-discovery/decisions.md
SCOPE — IN: bar-association guides, legal-ops publications, relevant case studies;
  .worklog/202607/legal-team/phase-1-discovery/domain-research.md (only write path)
SCOPE — OUT (do not touch): jurisdiction-specific statutes; no file modifications outside the output file
CONTRADICTIONS: surface every source disagreement explicitly; resolving one silently = failed attempt
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Each of the 4 sub-questions has ≥ 3 evidence rows or an explicit "no source found" with queries.
  2. Every claim in CONCLUSIONS appears in the evidence table.
STOP CONDITION: stop after 8 sources per sub-question or when new sources repeat known claims
VERIFICATION: fresh-context verifier spot-checks 4 rows resolve and support the claims, per EC-3 (§7.3)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); full table → .worklog/202607/legal-team/phase-1-discovery/domain-research.md, send the path
ESCALATE IF: J1.2, J1.3, or J4.1 fires
BUDGET: max 40 output lines / 25 tool calls
```
