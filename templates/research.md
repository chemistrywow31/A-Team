# Delegation Template: Research

Use for: domain investigation, best-practice synthesis, comparative analysis (domain-researcher work). Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in `.claude/rules/execution-contract.md` (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

## Template

```
TASK ID: {{id}}   TIER: {{haiku|sonnet|opus}}   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: {{the one question this research must answer}}
QUESTION DECOMPOSITION: {{2–5 sub-questions; each gets its own evidence-table rows}}
CONTEXT (paths only): {{BRIEF path}}; {{upstream decisions.md paths}}
SCOPE — IN: {{domains/source types to cover}}
SCOPE — OUT (do not touch): {{out-of-scope topics; no file modifications outside the output file}}
EVIDENCE TABLE (required output format, one row per claim):
  | claim | source (URL + date) | confidence (high: 2+ independent sources / medium: 1 / low: inference) |
CONTRADICTIONS: surface every source disagreement explicitly in a CONTRADICTIONS section;
  resolving one silently = failed attempt. No resolver → list both positions + what would settle it.
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every sub-question has ≥ {{N}} evidence rows or an explicit "no source found: {queries}".
  2. Every claim in CONCLUSIONS appears in the evidence table.
STOP CONDITION: stop after {{K}} sources per sub-question or when marginal sources repeat known claims
VERIFICATION: fresh-context verifier spot-checks {{M}} rows: source resolves and supports the claim, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); full table → {{output file}}, send the path
ESCALATE IF: J1.2 (question ambiguous), J1.3 (verification outruns tier), or J4.1 fires
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: legal-02   TIER: opus   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: What workflow stages do professional legal-review teams use for contract analysis?
QUESTION DECOMPOSITION: (1) standard stages; (2) roles per stage; (3) common failure points; (4) automation precedents
CONTEXT (paths only): .worklog/202607/legal-team/brief.md; .worklog/202607/legal-team/phase-1-discovery/decisions.md
SCOPE — IN: bar-association guides, legal-ops publications, LLM-for-legal case studies
SCOPE — OUT (do not touch): jurisdiction-specific statutes; no file modifications outside the output file
CONTRADICTIONS: surface every source disagreement explicitly; resolving one silently = failed attempt
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Each of the 4 sub-questions has ≥ 3 evidence rows or an explicit "no source found" with queries.
  2. Every claim in CONCLUSIONS appears in the evidence table.
STOP CONDITION: stop after 8 sources per sub-question or when new sources repeat known claims
VERIFICATION: fresh-context verifier spot-checks 4 rows resolve and support the claims, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); full table → .worklog/202607/legal-team/phase-1-discovery/domain-research.md, send the path
ESCALATE IF: J1.2, J1.3, or J4.1 fires
BUDGET: max 40 output lines / 25 tool calls
```
