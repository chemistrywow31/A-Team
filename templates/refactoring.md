# Delegation Template: Refactoring

Use for: restructuring existing files while preserving behavior (prompt optimization, rule consolidation, team restructuring execution). Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in the selected runtime's execution contract (`.grok/policies/execution-contract.md`) (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

Assign context tier by decision scope. Omit model/effort unless a measured native override is authorized; preserve existing target pins. Root uses advertised `spawn_subagent` with `background`, and `subagent_type` only when its live enum contains the selected role. A new acceptance reviewer never receives `resume_from`. These are dispatch templates, not executable tool argument objects.

## Template

```
TASK ID: {{id}}   CONTEXT TIER / PROFILE: {{decision scope; supported measured override or default omission}}   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: {{one sentence — what gets restructured, what must not change}}
CONTEXT (absolute paths only): {{BRIEF absolute path}}; {{upstream decisions.md absolute paths}}
SCOPE — IN: {{exact files to refactor; exact report/preimage/check-evidence files}}
SCOPE — OUT (do not touch): {{files that stay frozen, e.g. frontmatter fields, other agents' files}}
BEHAVIOR-PRESERVATION PROOF: run {{check commands}} BEFORE editing, save output; run the same
  commands AFTER; both outputs go to {{exact owned evidence paths}}; any regression = failed attempt
FORBIDDEN CHANGES: {{list, e.g. no requirement deleted, no Violation Determination weakened}}
DIFF-SIZE CAP: at most {{N}} lines changed per file; about to exceed it = stop at the cap and report per J4.4
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Before/after check outputs are identical for every preserved behavior.
  2. {{observable improvement; preserve useful contracts rather than impose a cosmetic size cut}}
VERIFICATION: fresh-context verifier re-runs the before/after checks from the worklog, per EC-3 (§7.3)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); report → {{exact owned report path}}; diffs/check outputs → {{exact owned evidence paths}}; send paths
ESCALATE IF: J4.1, J4.2, J4.3, or J4.4 fires; budget per EC-2.4
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: refactor_reasoning_contract   CONTEXT TIER / PROFILE: 3; model and effort omitted; effective values unverified   RETRY BUDGET: per EC-2 (§7.2)
NON-REVERSION: shared filesystem; preserve concurrent edits and never revert work you did not make.
OBJECTIVE: Consolidate the native reasoning template reference while preserving every effective decision and critique requirement.
CONTEXT (paths only): .worklog/202607/a-team-hardening/brief.md; .worklog/202607/a-team-hardening/phase-2-audit/defects-token-waste.md
SCOPE — IN: .grok/policies/reasoning-and-self-critique.md; .grok/templates/reasoning-self-critique-blocks.md;
  .worklog/202607/a-team-hardening/phase-3-design/refactor-report.md
SCOPE — OUT (do not touch): .grok/agents/*.md; every other rule file
BEHAVIOR-PRESERVATION PROOF: capture exact preimages and enumerate each clause BEFORE editing;
  map each to its actual AFTER text and check heading/reference validity in the assigned report.
FORBIDDEN CHANGES: no violation-determination item deleted; no canonical slot name renamed
DIFF-SIZE CAP: at most 120 lines changed per file; about to exceed it = stop at the cap and report per J4.4
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every pre-edit decision, workflow, critique, violation, and exception clause has a substantive destination.
  2. The template preserves adjacent Reasoning/Workflow/Self-Critique and no duplicate mandatory form is introduced.
VERIFICATION: fresh-context verifier reads the before/after clauses and re-runs the structural checks, per EC-3 (§7.3)
REPORT PERSISTENCE: assigned specialist writes the exact REPORT output below; root owns only an explicitly bounded fallback.
REPORT: EC-1 schema (§7.1); report and preimage/check evidence → .worklog/202607/a-team-hardening/phase-3-design/refactor-report.md
ESCALATE IF: J4.1, J4.2, J4.3, or J4.4 fires
BUDGET: max 40 output lines / 25 tool calls
```
