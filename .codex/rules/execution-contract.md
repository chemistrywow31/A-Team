---
name: Execution Contract
description: Bind Codex dispatches and specialist returns to stable task paths, acceptance criteria, escalation, and fresh-context verification
---

# Execution Contract

## Applicability

- Applies to: `team-architect`, every A-Team specialist, and every generated Codex multi-agent team
- Cite clauses by number when resolving disputes or writing dispatches.

## EC-1 Reporting And Dispatch

- **EC-1.1** Every specialist return contains exactly these six fields, in this order: `STATUS`, `CONCLUSIONS`, `EVIDENCE`, `ARTIFACTS`, `RISKS/UNKNOWNS`, `NEXT`. `STATUS` accepts exactly `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`; no other value is valid.
- **EC-1.2** The first line under `CONCLUSIONS` restates the stable task path and whether the acceptance criteria were met, partially met, or not met.
- **EC-1.3** `STATUS: DONE` with empty `EVIDENCE` is invalid. Verifier returns cite evidence per acceptance criterion, not only one aggregate claim.
- **EC-1.4** `ARTIFACTS` lists every file produced or updated and identifies which owned write paths were touched. Mark newly created files with `(new)`.
- **EC-1.5** Any product longer than 30 lines goes to a file. The return carries the path plus a summary of at most 3 lines.
- **EC-1.6** Do not paste file contents, diffs, transcripts, or raw tool output into a return or dispatch.
- **EC-1.7** Every dispatch includes the stable task path, goal, worklog or BRIEF paths, owned write paths, forbidden paths, acceptance criteria, and any runtime override or fork choice that changes default behavior.
- **EC-1.8** A follow-up on an existing task path carries only the delta: changed assumptions, invalidated evidence, updated criteria, or new paths.
- **EC-1.9** A malformed return bounces once with the schema attached. A second schema violation on the same task counts as a failed attempt.
- **EC-1.10** `NEEDS_CONTEXT` is bounded: name every known missing item at once. More than 3 `NEEDS_CONTEXT` rounds on the same subtask becomes `BLOCKED`, except user-question relays governed by the conversation protocol.

## EC-2 Escalation

- **EC-2.1** SMALL tier means a project-default utility tier below `gpt-5.6-terra`; it receives zero retries after a failed check and escalates immediately.
- **EC-2.2** MID tier means `gpt-5.6-terra` at `high`; it receives one retry with a changed approach only. A second failure escalates.
- **EC-2.3** STRONG tier means `gpt-5.6-sol` at `xhigh` or a stronger approved project pin.
- **EC-2.4** Every escalation carries the full failure trace: goal, attempts, exact error or diff path, eliminated hypotheses, and current file state.
- **EC-2.5** Global cap: one initial attempt plus at most two retries per subtask across all tiers. Same subtask means same acceptance criteria.
- **EC-2.6** A STRONG-tier success on an escalated task writes a reusable recipe to the worklog before closeout.
- **EC-2.7** Cap exhausted with no higher tier remaining means `BLOCKED`.

## EC-3 Verification

- **EC-3.1** No self-verification: the producer never accepts its own work, and the dispatching coordinator is never the sole acceptor.
- **EC-3.2** A fresh-context verifier receives only acceptance criteria and artifact paths.
- **EC-3.3** File checks cite file:line evidence per criterion.
- **EC-3.4** Executable artifacts such as `.codex/config.toml`, `agents/**/*.toml`, scripts, or tests are actually parsed or run. A pass claim without execution output is FAIL.
- **EC-3.5** High-risk judgments require a second independent opinion: runtime config changes, canonical-authority changes, deleting or overwriting a file the task did not create, or external writes.
- **EC-3.6** Verifier verdict format is one line per criterion: `{criterion} | PASS or FAIL | {evidence}`, then an overall verdict. Overall PASS requires every criterion PASS.

## EC-4 Precedence

Higher source wins in this order:

1. safety and protected-path restrictions
2. `AGENTS.md` and this contract
3. EC-3 verification requirements
4. EC-1 reporting and dispatch requirements
5. EC-2 escalation requirements
6. other rules
7. task-specific instructions
8. style preferences

Same level -> narrower applicability wins. Still tied -> `BLOCKED`.

## EC-5 Context Economy

- **EC-5.1** The coordinator creates one BRIEF per task at `.worklog/{yyyymm}/{task-name}/brief.md` before the first dispatch unless the task is truly single-dispatch.
- **EC-5.2** Dispatches and returns use paths in and paths out.
- **EC-5.3** Reports cap at 40 lines; other messages cap at 60 lines unless the dispatch explicitly raises the cap.
- **EC-5.4** Before re-reading a file over 200 lines already read in the same task, prefer the worklog summary when one exists.

## Violation Determination

- A return is missing any EC-1 field or the fields are out of order -> Violation
- A return uses a `STATUS` value outside `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` -> Violation
- `CONCLUSIONS` does not restate task path plus criteria state -> Violation
- DONE has empty evidence, or verifier evidence does not address each criterion -> Violation
- `ARTIFACTS` omits touched owned paths or created files -> Violation
- A dispatch omits task path, owned paths, forbidden paths, acceptance criteria, or BRIEF path once it exists -> Violation
- A follow-up replays unchanged full context instead of the delta -> Violation
- File contents, diffs, or transcripts are pasted into a dispatch or return -> Violation
- A retry exceeds the cap or reuses the same failed approach at MID tier -> Violation
- An escalation omits the full failure trace -> Violation
- An artifact is accepted without a fresh-context verifier verdict -> Violation

## Exceptions

- Phase 1 user conversation is not a specialist return.
- Micro-dispatches under 200 words may carry inline context when no useful file path exists yet.
