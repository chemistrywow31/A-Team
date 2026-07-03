# Delegation Template: Search

Use for: external skill discovery, tool lookup, finding existing solutions. Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in `.claude/rules/execution-contract.md` (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

## Template

```
TASK ID: {{id}}   TIER: {{haiku|sonnet|opus}}   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: {{one sentence, one deliverable}}
CONTEXT (paths only): {{BRIEF path}}; {{upstream decisions.md paths}}
SCOPE — IN: {{what to search for}}
SCOPE — OUT (do not touch): {{topics/dirs to leave alone; no file modifications}}
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
REPORT: EC-1 schema (§7.1); findings over 30 lines → write to {{output file}} and send the path
ESCALATE IF: J1.1 (unmappable scope), J1.2 (ambiguous instruction), or J4.1 (same error class twice) fires
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: toeic-04   TIER: sonnet   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: Find reusable external skills for TOEIC question generation to avoid writing custom ones.
CONTEXT (paths only): .worklog/202607/toeic-team/brief.md; .worklog/202607/toeic-team/phase-2-planning/decisions.md
SCOPE — IN: SkillsMP, aitmpl.com, GitHub topic "claude-skills"; skills for language-quiz generation
SCOPE — OUT (do not touch): paid marketplaces; do not modify any repo file
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every candidate row has: name, source URL, license, last-update date, Pattern A/B/C fit.
  2. At least 5 candidates, or "none found" with the exact queries listed.
STOP CONDITION: stop when 3 independent sources agree the field is covered, or after 12 queries, whichever first
VERIFICATION: fresh-context verifier spot-checks 3 citations resolve and support the claim, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); findings over 30 lines → write to .worklog/202607/toeic-team/phase-2-planning/skill-candidates.md and send the path
ESCALATE IF: J1.1, J1.2, or J4.1 fires
BUDGET: max 40 output lines / 20 tool calls
```
