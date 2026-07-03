# Execution Contract (Codex)

Codex condensation of `.claude/rules/execution-contract.md`. Clause numbers are shared across platforms — cite as EC-n.n. Tiers map to Codex model choices: SMALL = fastest tier, MID = standard, STRONG = strongest available.

## EC-1 Reporting
- Every specialist return: `STATUS` (DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT), `CONCLUSIONS` (max 10 lines), `EVIDENCE` (file:line), `ARTIFACTS` (paths), `RISKS/UNKNOWNS`, `NEXT` (one item). DONE with empty EVIDENCE is invalid.
- Products over 30 lines go to files; reports carry paths plus a 3-line summary. Never paste file contents, diffs, or transcripts.
- Malformed report → bounce once with schema; second violation = failed attempt.

## EC-2 Escalation
- SMALL tier: zero retries — escalate on first failed check with task + failure + paths.
- MID tier: one retry, changed approach only; second failure → escalate with the complete failure trace (goal, attempts, errors, eliminated hypotheses, file state).
- Global cap: 3 total attempts per subtask (initial + 2 retries). Same subtask = same acceptance criteria; shrinking the goal to reset the counter is a violation.
- STRONG tier solves an escalated task → write a reusable recipe to the worklog, then batch-apply at a lower tier.
- Cap exhausted, no higher tier → BLOCKED, ask the user.

## EC-3 Verification
- No self-verification: the producer never accepts its own work; the dispatching coordinator is never the sole acceptor.
- A fresh-context verifier receives only acceptance criteria + artifact paths. Files: read back, cite file:line per criterion. Executables/config: run them; a claim without execution output is FAIL.
- High-risk judgments (charter changes, deployment mode, deleting non-task files, external writes) need a second independent opinion.

## EC-4 Precedence
safety > charter (AGENTS.md + this contract) > EC-3 > EC-1 > EC-2 > other rules > task instructions > style. Same level → narrower applicability wins; still tied → BLOCKED and ask.

## EC-5 Context Economy
- One BRIEF per task at `.worklog/{yyyymm}/{task-name}/brief.md`; dispatches pass its path, never contents.
- Output cap 60 lines per message unless the dispatch raises it explicitly. Reports ≤ 40 lines.

## Violations
Missing report field; DONE without evidence; pasted contents; retry past cap; escalation without trace; acceptance without fresh-context verdict; dispatch without BRIEF path.
