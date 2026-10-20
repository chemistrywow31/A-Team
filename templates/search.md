# Delegation Template: Search

Use for: external skill discovery, tool lookup, finding existing solutions. Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in the selected runtime's execution contract (`.grok/policies/execution-contract.md`) (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

Assign context tier by decision scope. Omit model/effort unless a measured native override is authorized; preserve existing target pins. Root uses advertised `spawn_subagent` with `background`, and `subagent_type` only when its live enum contains the selected role. A new acceptance reviewer never receives `resume_from`. These are dispatch templates, not executable tool argument objects.

## Template

```
TASK ID: {{id}}   CONTEXT TIER / PROFILE: {{decision scope; supported measured override or default omission}}   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: {{one sentence, one deliverable}}
CONTEXT (absolute paths only): {{BRIEF absolute path}}; {{upstream decisions.md absolute paths}}
SCOPE — IN: {{search topics; exact evidence files to create}}
SCOPE — OUT (do not touch): {{topics/dirs; every path except exact assigned evidence outputs}}
ACCEPTANCE CRITERIA (mechanically checkable):
  1. {{e.g. every candidate has name, source URL, license, last-update date}}
  2. {{e.g. at least N candidates or an explicit "none found" with queries listed}}
SOURCES REQUIRED: {{source types + quality bar, e.g. official docs; repos updated < 12 months}}
CITATION FORMAT: every finding carries source URL + retrieval date
DEDUPLICATION: same-tool findings merge (only when versions match or the query is version-agnostic); keep the richer citation
STOP CONDITION: stop when {{N}} independent sources agree, or after {{K}} queries, whichever first
BUDGET SHORTFALL: query budget exhausted before the candidate floor → report DONE_WITH_CONCERNS
  with the shortfall and the queries run — not DONE, not BLOCKED
VERIFICATION: fresh-context verifier spot-checks {{M}} citations resolve and support the claim, per EC-3 (§7.3)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); findings over 30 lines → write to {{output file}} and send the path
ESCALATE IF: J1.1 (unmappable scope), J1.2 (ambiguous instruction), or J4.1 (same error class twice) fires
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: search_toeic_skills   CONTEXT TIER / PROFILE: 2; model and effort omitted; effective values unverified   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: Find reusable external skills for TOEIC question generation to avoid writing custom ones.
CONTEXT (absolute paths only): /Users/you/repo/.worklog/202607/toeic-team/brief.md; /Users/you/repo/.worklog/202607/toeic-team/phase-2-planning/decisions.md
SCOPE — IN: native skill catalogs and maintained source repositories; reusable language-quiz workflows;
  .worklog/202607/toeic-team/phase-2-planning/skill-candidates.md (only write path)
SCOPE — OUT (do not touch): paid marketplaces; every file except the exact REPORT path
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every candidate row has: name, source URL, license, last-update date, Pattern A/B/C fit.
  2. At least 5 candidates, or "none found" with the exact queries listed.
STOP CONDITION: stop when 3 independent sources agree the field is covered, or after 12 queries, whichever first
VERIFICATION: fresh-context verifier spot-checks 3 citations resolve and support the claim, per EC-3 (§7.3)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); findings over 30 lines → write to .worklog/202607/toeic-team/phase-2-planning/skill-candidates.md and send the path
ESCALATE IF: J1.1, J1.2, or J4.1 fires
BUDGET: max 40 output lines / 20 tool calls
```
