# Delegation Template: Refactoring

Use for: restructuring existing files while preserving behavior (prompt slimming, rule consolidation, team restructuring execution). Fill every {{slot}}; keep all other lines verbatim. EC-* clauses live in `.claude/rules/execution-contract.md` (EC-1 = directive §7.1, EC-2 = §7.2, EC-3 = §7.3). J-* rubrics live in `JUDGMENT.md`.

## Template

```
TASK ID: {{id}}   TIER: {{haiku|sonnet|opus}}   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: {{one sentence — what gets restructured, what must not change}}
CONTEXT (paths only): {{BRIEF path}}; {{upstream decisions.md paths}}
SCOPE — IN: {{exact files to refactor}}
SCOPE — OUT (do not touch): {{files that stay frozen, e.g. frontmatter fields, other agents' files}}
BEHAVIOR-PRESERVATION PROOF: run {{check commands}} BEFORE editing, save output; run the same
  commands AFTER; both outputs go to {{worklog path}}; any regression = failed attempt
FORBIDDEN CHANGES: {{list, e.g. no requirement deleted, no Violation Determination weakened}}
DIFF-SIZE CAP: at most {{N}} lines changed per file; about to exceed it = stop at the cap and report per J4.4
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Before/after check outputs are identical for every preserved behavior.
  2. {{the improvement target, e.g. file shrinks ≥ 20% by wc -c}}
VERIFICATION: fresh-context verifier re-runs the before/after checks from the worklog, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); diffs and check outputs → files under {{worklog path}}, send paths
ESCALATE IF: J4.1, J4.2, J4.3, or J4.4 fires; budget per EC-2.4
BUDGET: max {{lines}} output lines / {{count}} tool calls
```

## Filled example

```
TASK ID: harden-07   TIER: opus   RETRY BUDGET: per EC-2 (§7.2)
OBJECTIVE: Slim rules/reasoning-and-self-critique.md by extracting canonical blocks; every requirement must survive.
CONTEXT (paths only): .worklog/202607/a-team-hardening/brief.md; .worklog/202607/a-team-hardening/phase-2-audit/defects-token-waste.md
SCOPE — IN: .claude/rules/reasoning-and-self-critique.md; .claude/templates/reasoning-self-critique-blocks.md (new)
SCOPE — OUT (do not touch): .claude/agents/*.md; every other rule file
BEHAVIOR-PRESERVATION PROOF: run grep -c 'Violation' and grep -n '^### ' on the rule BEFORE editing,
  save output; run the same AFTER; outputs to .worklog/202607/a-team-hardening/phase-3-design/
FORBIDDEN CHANGES: no violation-determination item deleted; no canonical slot name renamed
DIFF-SIZE CAP: at most 120 lines changed per file; about to exceed it = stop at the cap and report per J4.4
ACCEPTANCE CRITERIA (mechanically checkable):
  1. Every pre-edit violation item still greps in the post-edit rule or the extracted template.
  2. Rule file shrinks ≥ 2,000 bytes by wc -c; extracted file contains both canonical blocks verbatim.
VERIFICATION: fresh-context verifier re-runs the before/after greps from the worklog, per EC-3 (§7.3)
REPORT: EC-1 schema (§7.1); outputs → .worklog/202607/a-team-hardening/phase-3-design/, send paths
ESCALATE IF: J4.1, J4.2, J4.3, or J4.4 fires
BUDGET: max 40 output lines / 25 tool calls
```
