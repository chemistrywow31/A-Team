# JUDGMENT.md — Externalized Judgment Rubrics

Purpose: make judgment calls explicit enough for the selected runtime role to apply from its assigned evidence. Cite criteria by number (e.g. "escalating per J1.2"). The coordinator's dispatch templates in `templates/` reference these sections; read the cited section before acting on it.

Examples distinguish task capability and evidence, not vendor model tiers. Native role model/effort are omitted until a measured profile is authorized; omitted model follows the parent in source, while omitted effort leaves installed session/default behavior unasserted. Do not treat parser acceptance as effective routing.

Format per criterion: SIGNAL (observable condition) → ACTION (single imperative) → one POSITIVE example (signal fires, action is right) → one NEGATIVE example (look-alike where the signal does NOT fire).

## J1 Escalation Triggers

Beyond the mechanical retry counters in `.grok/policies/execution-contract.md` EC-2, escalate when:

### J1.1 Unmappable blast radius
- SIGNAL: The fix requires touching more than 3 files, and the dispatch does not state, for each file, both its purpose and the exact change it needs. Purposes you invent yourself do not count as mapped.
- ACTION: Stop. Report NEEDS_CONTEXT listing the files whose purpose or change is unstated, or request a demonstrably adequate specialist with that list.
- POSITIVE: A deterministic formatter is asked to "align frontmatter across the team" and finds agents, skills, and rules all affected, with no per-file changes stated. Escalate.
- NEGATIVE: The dispatch itself lists 5 files, each with its purpose AND the exact change per file. Proceed — the blast radius is mapped, not unmappable.

### J1.2 Two plausible readings
- SIGNAL: An instruction has two readings, both plausible, and the choice changes the deliverable.
- ACTION: Stop. Report the two readings and ask the coordinator to pick; do not pick silently.
- POSITIVE: "Make the rules match our conventions" — repo conventions and the user's stated conventions differ. Ask.
- NEGATIVE: The dispatch cites the exact convention file to follow. Follow it — one reading survives.

### J1.3 Verification outruns demonstrated capability
- SIGNAL: Checking your own output for correctness requires expertise the assigned role/profile lacks (security review, architecture judgment, domain facts you cannot cite).
- ACTION: Deliver with STATUS DONE_WITH_CONCERNS, name the unverifiable aspect in RISKS, and name the required expert verifier in NEXT. The coordinator must dispatch that verifier before accepting the artifact (EC-3) — the recommendation alone does not complete acceptance.
- POSITIVE: A writer generates a native permission pattern and cannot establish whether it safely bounds an external transfer. Flag it; the coordinator holds acceptance until the security-competent verifier reports.
- NEGATIVE: The check is mechanical (line count, field presence, jq parse). Run it yourself — no expertise gap exists.

## J2 Definition of Done

### J2.1 Generic
- SIGNAL: You are about to report DONE.
- ACTION: Report DONE only when every acceptance criterion in the dispatch is met with evidence you can cite; final acceptance still requires the fresh-context verifier per EC-3.
- POSITIVE: All 4 criteria checked against the actual files, file:line cited for each in EVIDENCE. Report DONE.
- NEGATIVE: "I finished all the steps in my plan" but criterion 3 was never checked against the file. That is not done — check it or report DONE_WITH_CONCERNS naming the gap.

### J2.2 Per artifact type
- SIGNAL: The artifact is one of the standard A-Team types.
- ACTION: Apply the matching floor from J5 as the minimum done-bar, plus the dispatch's own criteria.
- POSITIVE: An agent .md meets every J5.1 check and the dispatch's two extra criteria. Done.
- NEGATIVE: The artifact passes J5 floors but fails a dispatch-specific criterion. Not done — dispatch criteria are additive, not alternative.

## J3 Stop-and-Ask-the-User Triggers

### J3.1 Charter conflict without a resolver
- SIGNAL: Two charter-level instructions conflict, EC-4 puts them at the same level, and neither has narrower Applicability.
- ACTION: Stop work on the affected item. Present both instructions and the conflict to the user; continue unaffected work.
- POSITIVE: AGENTS.md demands a section that another charter rule prohibits at the same precedence level. Ask.
- NEGATIVE: A rule conflicts with a dispatch instruction. Do not ask — EC-4 already resolves it (rules outrank dispatches).

### J3.2 Irreversible or outward action without authorization
- SIGNAL: The next step performs an irreversible mutation, deletes user data, pushes to a remote, or writes to an external API without existing user authorization for that operation and target. A broad request does not authorize unrelated destructive/external actions. Routine reversible edits inside the requested scope are authorized; declared-authority, exact-path, confinement, and independent-review requirements still apply.
- ACTION: Stop before the unauthorized action. Prepare a concrete reviewable result, then ask with the exact operation and target; continue authorized independent work.
- POSITIVE: Restructuring suggests deleting `teams/old-team/`. The dispatch never mentioned deletion. Ask.
- NEGATIVE: The user requested optimization of the named repository, and the reviewed plan identifies reversible edits within that scope. Proceed under existing authorization; do not ask again at each phase or file.

### J3.3 Contradictory requirements
- SIGNAL: The user asked for X and Y, and X and Y cannot both be true of the same artifact at the same time (not merely "Y gets harder when X holds").
- ACTION: Stop. Present the contradiction with one concrete consequence per branch; ask which wins.
- POSITIVE: "Keep all 16 rules always-loaded" and "cut always-loaded tokens by half." Ask.
- NEGATIVE: X and Y are merely in tension and the user stated a priority order. Follow the order — tension with a tiebreaker is not contradiction.

### J3.4 Retry budget exhausted with no justified escalation
- SIGNAL: Three total attempts consumed (EC-2.4) AND every authorized escalation option up to the highest evidenced available task capability has already attempted (the one-shot escalation attempt in EC-2.4 is spent or unavailable).
- ACTION: Report BLOCKED with the full failure trace and one specific unblock request. Stop.
- POSITIVE: A utility failed once, an execution role twice, and the justified expert spent its single escalation attempt; trace complete. Ask the user.
- NEGATIVE: Utility and execution roles consumed all three attempts but an evidenced adequate expert has not attempted — that expert still gets the single EC-2.4 escalation attempt. Escalate with the trace; do not ask the user yet.

## J4 Wrong-Direction Signals

Wrong direction means the approach is wrong, not the effort. Retrying into a wrong direction is forbidden.

### J4.1 Same error class after an approach change
- SIGNAL: You changed approach once, and the new attempt fails with the same error class as the first.
- ACTION: Stop. Mark WRONG-DIRECTION. Escalate per EC-2 with the full failure trace. Do not retry.
- POSITIVE: Two different frontmatter fixes both fail the same loader validation — the schema model is wrong, not the patch. Escalate.
- NEGATIVE: The second attempt fails with a different error. That is progress — continue within the EC-2.4 budget.

### J4.2 The fix keeps growing
- SIGNAL: Each attempt touches more files or more lines than the previous attempt (lines touched = max(lines added, lines deleted) per attempt).
- ACTION: Stop expanding. Return only this task's delta to the smallest failing state after checking for intervening edits; preserve all user/other-writer work. Write the trace and escalate per EC-2.
- POSITIVE: Attempt 1 edits one rule; attempt 2 edits the rule plus three agents; the planned attempt 3 would edit AGENTS.md too. Stop and escalate.
- NEGATIVE: Attempt 2 is smaller and passes more checks than attempt 1. Shrinking with progress is convergence — continue.

### J4.3 Checks pass only because they were weakened
- SIGNAL: A previously failing check now passes, and the diff shows the check itself (criteria, test, threshold, cap) was modified.
- ACTION: Revert the weakening. Count the attempt as failed. Escalate or fix the artifact, not the check.
- POSITIVE: A 60-line template limit was failing, so the limit was edited to 80 and now "passes." Revert; the artifact must shrink.
- NEGATIVE: The coordinator re-issued the dispatch with corrected criteria, citing external evidence (a rule file, spec, or user statement — recorded in the worklog) that the original criterion was factually wrong. New criteria = new subtask per EC-2.5 — legitimate. The working agent's own testimony that the criterion is wrong never qualifies; that path is the laundering exploit this rubric exists to block.

### J4.4 Absolute cap about to be breached
- SIGNAL: A dispatch-stated absolute limit (diff-size cap, file-count cap, tool-call or line budget) is about to be exceeded by the work in progress.
- ACTION: Stop at the cap. Report DONE_WITH_CONCERNS (partial work within the cap) or BLOCKED, stating the estimated overage and what the cap prevented. Never exceed a stated cap silently.
- POSITIVE: The refactoring dispatch caps changes at 120 lines per file; the correct fix needs ~180. Stop at a coherent boundary under 120, report the overage estimate, let the coordinator re-scope.
- NEGATIVE: The work fits within every stated cap but feels large. Feelings are not signals — finish within the caps and report normally.

## J5 Quality Floor Per Artifact Type

Each floor lists the exact check that proves it. A verifier runs these checks; a producer runs them before reporting. J5 is the CANONICAL floor definition — `.grok/skills/quality-validation/SKILL.md` compiles these floors into its team-sweep checklist; when the two disagree, J5 wins and quality-validation must be updated in the same change.

Prioritize task effectiveness using current official platform/model guidance. Preserve useful XML structure, examples, concrete steps, and checks; concision is secondary. Use one role-specific Reasoning/Workflow/Self-Critique contract; the headings below do not require fixed four/five slots, duplicate Preflight/Verification forms, or private reasoning transcripts. One independent review may cover a coherent frozen artifact batch. After corrections, invalidate and rerun every criterion citing a changed file plus dependent mapping/parity criteria; preserve only unaffected current evidence.

The existing 300/200/100-line targets for authored agent/skill/rule files are review triggers, not permission to discard useful instructions. An over-target file is `REVIEW_REQUIRED`: the producer records its size and concrete usefulness rationale; an independent reviewer accepts or rejects the current file in the criterion report. An author-only marker or shorter file is not evidence of quality. Keep EC report caps separately bounded. Retain at least one meaningful rejection/defer/escalation example in authored agents and skills; add positive or contrast examples when they clarify behavior or a testable boundary. Do not force a universal example count.

### J5.1 Agent .md
- SIGNAL: Artifact is a native agent file.
- ACTION: Enforce flat `.grok/agents/{name}.md` with matching unique kebab-case name; line-1 YAML `name`/`description`; one adjacent `## Reasoning` → `## Workflow` → `## Self-Critique`; `## Boundaries`, `## Uncertainty Protocol`, input/output and completion contracts, exact ownership, and `## Examples` with a meaningful rejection/defer/escalation case. Validate supported keys/types and runtime posture under `.grok/policies/grok-agent-config.md`; specialists deny Task, execution-check roles retain Execute, coordinator tools are omitted. New roles omit model/effort unless a measured profile is declared; preserve supported target pins outside migration. Check with actual YAML parsing, ordered headers, reference resolution, line count, and native source inventory. Above 300 lines requires independent usefulness review; discovery alone does not prove tools/model/context.
- POSITIVE: A 240-line flat specialist has all sections and a meaningful rejection case, native metadata with Task denial, exact startup paths, and current discovery evidence; effective-runtime gaps are separately labeled.
- NEGATIVE: All headings exist but Self-Critique precedes Workflow, or a shell-check auditor uses an execution-excluding profile. Floor failed.

### J5.2 Skill SKILL.md
- SIGNAL: Artifact is a native skill file.
- ACTION: Enforce `.grok/skills/{name}/SKILL.md`, line-1 name/description, resolvable assets, an ordered executable workflow, and at least one meaningful rejection/defer/escalation example. Above 200 lines requires independent usefulness review. Identify coordinator-entry candidates by workflow purpose/main-session adoption, independent of folder/name or already-valid metadata. A multi-agent team has exactly one; verify its explicit-invocation intent (`disable-model-invocation: true`), useful `argument-hint`, and resolvable coordinator playbook adopted by the current session without spawning it. Ordinary manual-only utilities are exempt from entry-only checks. Native skill model/effort and allowed-tools are not effective routing/permission controls; inspect and session evidence remain separate.
- POSITIVE: A renamed entry plus a manual review utility produces one entry candidate; its metadata and current-session adoption pass, and referenced scripts are present and checked.
- NEGATIVE: A genuine workflow entry tells root to spawn the coordinator. It remains an entry candidate and fails; metadata omissions cannot hide it from the check.

### J5.3 Rule .md
- SIGNAL: Artifact is a rule file.
- ACTION: Enforce: frontmatter name/description; `## Violation Determination` present with at least one observable condition; `## Exceptions` present (or states "no exceptions"); lengths above 100 lines require independent usefulness review. Check: grep headers, `wc -l`.
- POSITIVE: 80 lines, both sections, checkable violations. Floor met.
- NEGATIVE: Violation section says "output is low quality" — not observable. Floor failed — rewrite as a checkable condition.

### J5.4 Native Runtime Configuration
- SIGNAL: Artifact is `.grok/config.toml` or a native runtime profile.
- ACTION: Parse TOML/YAML with real parsers; validate only supported project sections (`mcp_servers`, `plugins`, `permission`) and native agent keys/types. Reject broad destructive/arbitrary-execution grants, secret-bearing configuration, unsupported project controls, and any attempt to change trust/global settings for a pass. Confirm exact discovered source paths. Evaluate effective tools, role selection, shell execution, context, model/effort separately through bounded installed-session evidence; record unavailable evidence as UNVERIFIED/activation-gated. Apply `.grok/policies/grok-runtime-config.md` and verify portable setup/rollback.
- POSITIVE: Minimal config parses, source inventory matches, and setup distinctly reports discovery PASS plus PENDING_NATIVE_AUTH for effective execution.
- NEGATIVE: Inspect lists a profile with an ignored unknown key, and the reviewer calls its tool boundary enforced. Floor failed; loading is not enforcement.

### J5.5 Task report
- SIGNAL: Artifact is a task return.
- ACTION: Enforce EC-1.1: six fields, in order, CONCLUSIONS ≤ 10 lines, DONE requires non-empty EVIDENCE. Check: field presence and order by grep; line count; empty-EVIDENCE catch: the line after `EVIDENCE:` (or its same-line remainder) must contain a file, path, or command reference — an empty or whitespace-only value on a DONE report is FAIL.
- POSITIVE: Six fields in order, 3 evidence pointers. Floor met.
- NEGATIVE: Report has rich content but starts with a narrative paragraph before STATUS. Floor failed — bounce once per EC-1.6.

### J5.6 Worklog phase folder
- SIGNAL: Artifact is a phase worklog.
- ACTION: Enforce: `references.md`, `findings.md`, `decisions.md` all present and non-empty — non-empty means at least one substantive entry beyond headers; placeholder text (TBD, TODO, N/A without explanation) counts as empty. Every decision entry names at least one finding or reference. Check: `ls`, `wc -l` per file, grep each decision for a source pointer, grep for placeholder markers.
- POSITIVE: Three populated files; both decisions cite findings. Floor met.
- NEGATIVE: Three files exist but decisions.md contains only "TBD". Floor failed — presence without content is not a populated worklog.

### J5.7 Generated AGENTS.md
- SIGNAL: Artifact is a generated team's root `AGENTS.md`.
- ACTION: Enforce actual team objectives/scope; explicit Grok authority and canonical roots, requested format and runnable/activation states; deployment section placing the coordinator in the main session with target-local roster; worklog/context and precedence contracts; `Generated by A-Team on` stamp. Check exact resolvable native references, complete required policies/skills, and `docs/RUNTIME-SETUP.md` with verify/rollback and evidence limits. Multi-surface/conversion-retained mappings must agree with every runnable entry; a filename alone cannot identify authority. A declared single-agent team may document single-session execution instead of a separate coordinator role.
- POSITIVE: A two-role native team declares its own roster, main-session coordinator, source authority, required policy/skill paths, stamped setup, and separately identified activation gaps.
- NEGATIVE: All headings exist but the deployment section spawns the coordinator or silently promotes an archived surface. Floor failed.
