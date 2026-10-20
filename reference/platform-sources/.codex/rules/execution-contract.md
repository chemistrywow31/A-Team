---
name: Execution Contract
description: Bind dispatches and specialist returns to owned paths, bounded escalation, and independent acceptance
---

# Execution Contract

## Applicability

- Applies to: the coordinator, every specialist, and generated multi-agent teams
- Include this contract in the canonical rule family and requested runtimes. Cite EC clauses when resolving disputes; EC-1 through EC-5 map to directives §7.1 through §7.5.

## EC-1 Reporting Contract

- **EC-1.1** Every specialist return contains six fields in order: `STATUS`, `CONCLUSIONS`, `EVIDENCE`, `ARTIFACTS`, `RISKS/UNKNOWNS`, `NEXT`. Status is exactly `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`; conclusions have at most 10 lines, risks say "none" when absent, and NEXT names one recommendation.
- **EC-1.2** Start CONCLUSIONS with the stable task path and whether acceptance criteria are met, partially met, or not met.
- **EC-1.3** DONE requires nonempty EVIDENCE with file:line or command-evidence paths. Verifiers cite evidence for every criterion.
- **EC-1.4** ARTIFACTS lists every produced or updated file, including worklogs and touched owned paths; mark new files `(new)`.
- **EC-1.5** Put products longer than 30 lines in files; return their paths and a summary of at most 3 lines. EC-1.12 is the bounded exception when the host blocks persistence.
- **EC-1.6** Do not paste file contents, diffs, transcripts, or raw tool output into dispatches or returns. Link their files; only EC-1.12 permits bounded inline report evidence.
- **EC-1.7** Coordinator handling: verify DONE under EC-3; resolve or explicitly accept logged concerns; resolve BLOCKED before redispatch; supply all named context for NEEDS_CONTEXT. Do not redispatch an unchanged blocker.
- **EC-1.8** Bounce a malformed report once with the schema. A second schema violation on the task counts as a failed attempt under EC-2.4.
- **EC-1.9** Name all known missing context at once. More than 3 NEEDS_CONTEXT rounds becomes BLOCKED, except user-question relays under the conversation protocol.
- **EC-1.10** Dispatch the stable task path, goal, BRIEF/worklog paths, exact owned and forbidden paths, acceptance criteria, shared-filesystem non-reversion rule, startup inputs, report-persistence owner/destination, and any runtime override or fork choice.
- **EC-1.11** Follow-ups on an existing task path carry only changed assumptions, invalidated evidence, updated criteria, or new paths.
- **EC-1.12** When the live sandbox or host prevents an assigned report write, use `INLINE-FALLBACK` only if the dispatch names the coordinator as persistence owner, the exact report destination, and a finite raised return cap. Keep EC-1 fields and statuses; put the blocker, intended path, and concise evidence in the bounded return. ARTIFACTS must say the report is pending coordinator persistence, not claim a file exists. The coordinator persists it, verifies the path, and records provenance before acceptance. If this handoff is unspecified, return `NEEDS_CONTEXT` for the cap/owner; never bypass the restriction through another tool or broaden permissions.

## EC-2 Escalation Ladder

Use the model actually running the task: MID = `gpt-5.6-terra`/`high`, STRONG = `gpt-6-astra`/`xhigh`, SMALL = an approved lower utility tier. Preserve role pins; root/unpinned defaults are host-selected. Prompt labels do not prove effective routing. On A-Team's observed v2 host, full-history forks inherit the parent model/effort and overrides require `fork_turns = "none"` or a positive bounded fork. For other targets, use their supported lifecycle/profile under `.codex/rules/codex-runtime-config.md` and `.codex/rules/context-isolation.md`.

- **EC-2.1** SMALL failure gets no retry at that tier. Escalate to MID with failed checks and paths; skip to STRONG only for a stated expertise gap under J1.3.
- **EC-2.2** MID failure gets one changed-approach retry. A second consecutive failure escalates to STRONG.
- **EC-2.3** Every escalation includes goal, all attempts with exact error/diff paths, eliminated hypotheses, and current file state. Reject traces with no prior attempt.
- **EC-2.4** One initial attempt plus at most two retries per subtask across all tiers. This clause owns the bound. If a higher tier has not attempted when the cap is spent, it gets exactly one escalation attempt with the full trace; failure then requires BLOCKED.
- **EC-2.5** Same subtask means same acceptance criteria; shrinking the goal cannot reset the counter. A new subtask requires a coordinator dispatch with new criteria. Correct criteria at most once per deliverable across reissues, using external evidence recorded in the worklog; a producer's unsupported claim cannot change the check. The coordinator audits both bounds from the worklog.
- **EC-2.6** STRONG success on escalation writes a reusable recipe with preconditions, steps, and verification before closeout; batch remaining matching instances at an adequate lower tier.
- **EC-2.7** When the cap is spent, escalate if a higher tier remains; otherwise report BLOCKED with the failure trace and specific unblock request per J3.4.

## EC-3 Verification Protocol

- **EC-3.1** The producer performs Self-Critique but never accepts its own output; the dispatching coordinator cannot be the sole acceptor.
- **EC-3.2** A fresh-context verifier receives only acceptance criteria and artifact paths, without producer reasoning, drafts, or conversation history. One coherent frozen artifact batch may share a single independent review; do not dispatch a reviewer per file.
- **EC-3.3** Open actual files and cite file:line evidence per criterion. Missing evidence means unverified and FAIL. After a correction, invalidate and rerun every criterion citing a changed file, plus dependent mapping/parity criteria. Carry forward only unaffected passes whose evidence remains current.
- **EC-3.4** Parse or execute relevant runtime configs, hooks, scripts, and code paths; a pass claim without execution evidence is FAIL. Run required checks; add or repeat tests only for changes, failures, or unresolved concerns that justify them.
- **EC-3.5** Charter/rule amendments, deployment or runtime changes, authority changes, deleting/overwriting pre-existing files, and external writes require a second independent opinion. A scoped plan already authorized by the user may receive one opinion covering all named paths and operations. The worklog identifies task-created files with prior `(new)` ARTIFACTS entries; an update is not creation, and ambiguous provenance counts as pre-existing. Preserve required recommendation and artifact gates; obtain new user authority only for actions outside existing authorization.
- **EC-3.6** Return `{criterion} | PASS or FAIL | {evidence}` for each criterion and an overall verdict. Overall PASS requires every criterion PASS. Freeze runtime producers before preflight. Dialogue/process review is a retrospective, not another implementation approval stage.

## EC-4 Precedence Order

System, developer, and explicit user instructions govern this local contract. Within repository guidance, higher wins:

1. Safety: runtime deny rules, destructive-action and protected-path guards
2. Charter: `AGENTS.md` and this contract
3. EC-3 verification requirements
4. EC-1 reporting requirements
5. EC-2 escalation requirements
6. Other rules
7. Task-specific dispatch instructions
8. Style preferences

At the same level, narrower applicability wins. If still tied, stop the affected item and ask the coordinator or user per J3.1; continue unaffected work. Existing authorization is not lost at a phase boundary.

## EC-5 Context Economy

- **EC-5.1** Before the first dispatch, create `.worklog/{yyyymm}/{task-name}/brief.md`: goal (at most 5 lines), constraints, key paths, and phase decision pointers. Update at phase boundaries; pass its path.
- **EC-5.2** Use paths in and paths out. Record concise decisions and verification evidence, not private reasoning transcripts or duplicate forms.
- **EC-5.3** Specialist reports cap at 40 lines; other agent messages cap at 60 unless the dispatch explicitly raises the applicable cap.
- **EC-5.4** Before rereading a file over 200 lines in the coordinator session, use its worklog summary when current and sufficient; otherwise inspect needed source and update the summary. Fresh verifiers inspect actual artifacts.

## Violation Determination

- A return omits/reorders EC-1 fields, uses an invalid status, exceeds its cap, or claims DONE without evidence -> Violation
- A dispatch omits exact scope, criteria, non-reversion, report-persistence ownership, or an existing BRIEF path, or repeats unchanged context -> Violation
- Inline fallback has no dispatch-stated cap/destination/owner, falsely claims persistence, bypasses the host, or is accepted before coordinator persistence -> Violation
- A retry exceeds EC-2 bounds, repeats the failed MID approach, lacks its trace, or weakens criteria without permitted evidence -> Violation
- A producer or dispatching coordinator is sole acceptor, a criterion lacks current evidence, or a changed-file/dependent parity criterion retains stale PASS -> Violation
- Required independent opinion, runtime execution evidence, or runtime freeze is missing -> Violation
- Existing authorization is discarded without a material scope change, or a local preference overrides higher instructions -> Violation

## Exceptions

- EC-1.12 allows a bounded report handoff when persistence is host-blocked; EC statuses, evidence requirements, and independent acceptance remain binding.
- Interactive user conversation is not a specialist return.
- Micro-dispatches under 200 words may carry inline context; report requirements still apply.
- A single-dispatch task with no phases may carry goal and paths directly without a BRIEF.
