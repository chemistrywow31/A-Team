---
name: Execution Contract
description: Binding runtime contract for reporting, escalation, verification, precedence, and context economy
---

# Execution Contract

## Applicability

- Applies to: all agents (coordinator and every dispatched agent)
- Generated teams: every generated team must include this contract in its `rules/` (see `rules/output-structure.md`)
- Cite clauses by number when resolving disputes or writing dispatches, e.g. "per EC-2.4"
- Directive mapping: EC-1 = §7.1, EC-2 = §7.2, EC-3 = §7.3, EC-4 = §7.4, EC-5 = §7.5

## EC-1 Reporting Contract

- **EC-1.1** Every task return must contain exactly these six fields, in this order:
  1. `STATUS:` DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
  2. `CONCLUSIONS:` max 10 lines — outcomes and decisions, not narrative
  3. `EVIDENCE:` file:line pointers or command outputs that prove each conclusion
  4. `ARTIFACTS:` paths to every file produced or updated, including worklog files — mark newly created files with `(new)`
  5. `RISKS/UNKNOWNS:` issues the coordinator must know; write "none" when none exist
  6. `NEXT:` exactly one recommendation
- **EC-1.2** `STATUS: DONE` with an empty `EVIDENCE` field is invalid. Compliance check: the coordinator rejects any DONE report whose EVIDENCE field cites zero files or commands.
- **EC-1.3** Any product longer than 30 lines — code, analysis, research notes, logs — must be written to a file. The report carries the path plus a summary of at most 3 lines.
- **EC-1.4** Do not paste file contents, diffs, transcripts, or raw tool output into a report or a dispatch. Write the content to a file and send the path.
- **EC-1.5** Status handling by the coordinator: DONE → dispatch verification per EC-3, then proceed. DONE_WITH_CONCERNS → log each concern to the worklog, resolve or accept explicitly, then proceed. BLOCKED → resolve the named blocker before re-dispatch; re-dispatching unchanged is forbidden. NEEDS_CONTEXT → provide the named missing items and re-dispatch.
- **EC-1.6** Bounce protocol: a report violating EC-1.1–EC-1.4 is returned to the producer once, with this schema attached. A second schema violation on the same task counts as a failed attempt under EC-2.4.
- **EC-1.7** NEEDS_CONTEXT is bounded: name every missing item you can identify in a single return — withholding known items for later rounds is a violation. The coordinator re-dispatches only after supplying every named item; re-dispatching with the same items still missing is forbidden — if an item cannot be supplied (no file exists, no user answer available), treat the subtask as BLOCKED instead. Backstop: more than 3 NEEDS_CONTEXT rounds on the same subtask → BLOCKED. QUESTIONS blocks relayed to the user are the designed exception: each relay returns with new user answers and does not count against the cap, but obeys `rules/conversation-protocol.md` interview limits.

### Filled example

```
STATUS: DONE
CONCLUSIONS:
- Generated 5 rule files for teams/demo-team/, including the 4 mandatory rules.
- All files pass the 100-line limit; worklog.md defines the evidence chain.
- One planned rule (api-format) merged into coding-standard to stay within the 8-rule cap.
EVIDENCE: teams/demo-team/.claude/rules/worklog.md:1-62, wc -l output in worklog findings.md
ARTIFACTS: teams/demo-team/.claude/rules/ (5 files), .worklog/202607/demo-team/phase-3-generation/findings.md
RISKS/UNKNOWNS: api-format merge widens coding-standard scope; verifier must check the Applicability line.
NEXT: dispatch a fresh-context verifier per EC-3 against the Phase 2 rules plan.
```

## EC-2 Escalation Ladder

Tier names map to this repo's models per `rules/context-tier.md`: SMALL = `haiku`, MID = `sonnet`, STRONG = `opus`. The ladder is keyed to the model actually running the task — the dispatch-time model override when present, else the agent's `model:` frontmatter — not to the context-tier number. The same task follows EC-2.1 when run on haiku and EC-2.2 when run on sonnet.

- **EC-2.1** haiku-tier task fails its acceptance check → zero retries at haiku. Escalate to the next tier up immediately (haiku → sonnet → opus; skipping straight to opus is permitted only when the failure needs expertise sonnet lacks — the `JUDGMENT.md` J1.3 signal; name that reason in the escalation), attaching the task, the failed check output, and artifact paths.
- **EC-2.2** sonnet-tier task fails → one retry, changed approach only. Re-running the same approach is forbidden. A second consecutive failure on the same subtask → escalate to opus.
- **EC-2.3** Every escalation carries the complete failure trace: the goal, every attempt with its exact error or diff path, hypotheses eliminated, and current file state. Escalating the task without the failure trace is a violation. Compliance check: the receiving tier rejects escalations whose trace lists zero prior attempts.
- **EC-2.4** Global cap: one initial attempt plus at most two retries = three total attempts per subtask, across all tiers. This is the same bound as the existing "3 attempts then BLOCKED" rules in `rules/anti-sycophancy.md` and `rules/context-management.md` — there is no conflict. One exception: when the cap is consumed and a HIGHER tier has not yet attempted, that tier receives exactly one escalation attempt (with the full EC-2.3 trace); after it fails, BLOCKED per EC-2.7.
- **EC-2.5** "Same subtask" = same acceptance criteria. Shrinking the goal to reset the attempt counter is a violation. A shrunk goal is a new subtask only when the coordinator re-issues it in a new dispatch with new acceptance criteria. Criteria may be corrected at most ONCE per deliverable (keyed to the artifact path(s) the criteria target, across all re-issues of that work — a correction cannot reset its own allowance), and only with external evidence (a rule file, spec, or user statement) recorded in the task worklog; the working agent's own claim that the criteria are wrong is not sufficient. Compliance check: the coordinator enforces both bounds against the worklog record (fresh-context verifiers lack dispatch history and do not check this clause).
- **EC-2.6** opus-tier solves an escalated task → extraction is mandatory: write a reusable recipe (preconditions, steps, verification command) to the task worklog before closing. Remaining instances of the same problem are then batch-applied at sonnet or haiku tier using the recipe.
- **EC-2.7** Cap exhausted: if a higher tier remains, escalate. If no higher tier remains, report BLOCKED and stop for user input, per `JUDGMENT.md` J3.4.

## EC-3 Verification Protocol

- **EC-3.1** No self-verification. The agent that produced an artifact must not perform its acceptance, and the coordinator that dispatched it must not be the sole acceptor. Producer Self-Critique per `rules/reasoning-and-self-critique.md` remains mandatory, may be logged, and never counts toward acceptance.
- **EC-3.2** Acceptance is performed by a fresh-context verifier dispatched via Task. The verifier receives only: the acceptance criteria and the artifact paths. Do not send the producer's reasoning, drafts, or conversation history.
- **EC-3.3** Files: the verifier opens the actual file and checks each criterion, citing file:line evidence per criterion. A criterion with no cited evidence is unverified and therefore FAIL.
- **EC-3.4** Executable artifacts (settings.json, hooks, scripts, code): the verifier executes — `jq` parse for JSON, run the hook command in a fresh shell, run the test or code path. A pass claim without execution output is FAIL.
- **EC-3.5** A judgment is high-risk when it matches ANY ONE of: charter or rule amendment, deployment-mode choice, deleting or overwriting a file the current task did not create, external network write. Every high-risk judgment requires a second independent opinion or best-of-N adjudication by a separate judge agent. "Files the current task did not create" is determined from the worklog: a file is task-created only when a prior EC-1 ARTIFACTS entry of this task marks it `(new)` — an entry recording an update to a pre-existing file does not count. When ambiguous, treat the file as NOT task-created (the safer default: second opinion required). The coordinator supplies the `(new)` list to the judge. Scope exception: files inside a Phase 7 restructuring target that are named in the user-approved restructuring plan count as task scope — one second opinion covers the plan, not each file individually.
- **EC-3.6** Verifier verdict format: one line per criterion — `{criterion} | PASS or FAIL | {evidence}` — then an overall verdict. Overall PASS requires every criterion PASS.

## EC-4 Precedence Order

When two instructions conflict, the higher source wins. Resolve by citing this order — never by judgment:

1. Safety: `settings.json` deny rules and destructive-action guards
2. Charter: `CLAUDE.md` and this contract
3. EC-3 verification requirements
4. EC-1 reporting requirements
5. EC-2 escalation requirements
6. Other rules in `rules/`
7. Task-specific dispatch instructions
8. Style preferences (tone, formatting, length aesthetics)

Two conflicting rules at the same level: the rule with the narrower Applicability wins. Still tied → report BLOCKED and ask the coordinator (agents) or the user (coordinator), per `JUDGMENT.md` J3.1.

## EC-5 Context Economy

- **EC-5.1** The coordinator creates one BRIEF file per task at `.worklog/{yyyymm}/{task-name}/brief.md` before the first dispatch: goal (max 5 lines), constraints, key paths, and pointers to each phase's `decisions.md`. Update it at every phase boundary. Every dispatch passes this path — never the BRIEF's contents.
- **EC-5.2** Dispatches follow the same path rule as reports (EC-1.4): paths in, paths out.
- **EC-5.3** Two caps, the stricter wins: task reports max 40 lines (EC-1.1 fields with EC-1.3 applied); all other output max 60 lines per message per agent. A dispatch may raise either cap only by stating the new number explicitly.
- **EC-5.4** Coordinator session only (dispatched subagents start fresh and read files directly): before re-reading a file over 200 lines already read this task, read its worklog summary instead. If no summary exists yet, write one to the worklog after this read.

## Violation Determination

- Task return missing any EC-1.1 field, or fields out of order → violation (bounce per EC-1.6)
- DONE status with empty EVIDENCE → violation
- File contents, diffs, or transcripts pasted into a report or dispatch → violation
- Retry of the same approach after failure at sonnet tier, or any retry at haiku tier → violation
- Fourth attempt on the same acceptance criteria → violation, with exactly one exception: the single EC-2.4 escalation attempt at a higher tier that has not yet attempted. A fifth attempt is never legal
- Escalation delivered without the failure trace → violation
- Artifact accepted with no fresh-context verifier verdict → violation
- Producer or dispatching coordinator acting as sole acceptor → violation
- Dispatch missing the BRIEF path (once the task's BRIEF exists) → violation
- Dispatch missing the BRIEF path (once the task's BRIEF exists) → violation
- Message exceeding 60 lines, or task report exceeding 40 lines, without a dispatch-raised cap → violation (bounce per EC-1.6)

## Exceptions

- Phase 1 interactive conversation turns with the user are conversation, not task returns; EC-1 format does not apply to them. It applies to every artifact-producing dispatch in any phase.
- Micro-dispatches whose full context is under 200 words may pass context inline (matches the existing exception in `rules/context-management.md`); the report format still applies.
- The BRIEF file is not required for single-dispatch tasks with no phases; the dispatch then carries the goal and paths directly.

Tradeoff: EC-3 adds one verifier dispatch per accepted deliverable and EC-5.1 adds one file per task. This costs roughly one extra agent invocation per deliverable; it buys detection of false "done" claims before they propagate downstream, which historically costs more than the verifier dispatch (re-dispatch + rework + audit findings).
