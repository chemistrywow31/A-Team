# JUDGMENT.md — Externalized Judgment Rubrics

Purpose: make judgment calls explicit enough for the selected runtime role to apply from its assigned evidence. Cite criteria by number (e.g. "escalating per J1.2"). The coordinator's dispatch templates in `templates/` reference these sections; read the cited section before acting on it.

Model names in examples illustrate Claude routing; actual dispatches use the selected runtime's current role profile, model, and effort. Do not translate aliases across providers by name.

Format per criterion: SIGNAL (observable condition) → ACTION (single imperative) → one POSITIVE example (signal fires, action is right) → one NEGATIVE example (look-alike where the signal does NOT fire).

## J1 Escalate-Model Triggers

Beyond the mechanical retry counters in `rules/execution-contract.md` EC-2, escalate when:

### J1.1 Unmappable blast radius
- SIGNAL: The fix requires touching more than 3 files, and the dispatch does not state, for each file, both its purpose and the exact change it needs. Purposes you invent yourself do not count as mapped.
- ACTION: Stop. Report NEEDS_CONTEXT listing the files whose purpose or change is unstated, or escalate one tier with that list.
- POSITIVE: A haiku formatter is asked to "align frontmatter across the team" and finds agents, skills, and rules all affected, with no per-file changes stated. Escalate.
- NEGATIVE: The dispatch itself lists 5 files, each with its purpose AND the exact change per file. Proceed — the blast radius is mapped, not unmappable.

### J1.2 Two plausible readings
- SIGNAL: An instruction has two readings, both plausible, and the choice changes the deliverable.
- ACTION: Stop. Report the two readings and ask the coordinator to pick; do not pick silently.
- POSITIVE: "Make the rules match our conventions" — repo conventions and the user's stated conventions differ. Ask.
- NEGATIVE: The dispatch cites the exact convention file to follow. Follow it — one reading survives.

### J1.3 Verification outruns your tier
- SIGNAL: Checking your own output for correctness requires expertise the task tier lacks (security review, architecture judgment, domain facts you cannot cite).
- ACTION: Deliver with STATUS DONE_WITH_CONCERNS, name the unverifiable aspect in RISKS, and name the required higher-tier verifier in NEXT. The coordinator must dispatch that verifier before accepting the artifact (EC-3) — the recommendation alone does not complete acceptance.
- POSITIVE: A sonnet writer generates a permissions block and cannot judge whether `Bash(curl *)` belongs in allow or ask. Flag it; the coordinator holds acceptance until the security-competent verifier reports.
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
- POSITIVE: CLAUDE.md demands a section that another charter rule prohibits at the same precedence level. Ask.
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

### J3.4 Retry budget exhausted with no higher tier
- SIGNAL: Three total attempts consumed (EC-2.4) AND every authorized tier up to the highest available task tier has already attempted (the one-shot escalation attempt in EC-2.4 is spent or unavailable).
- ACTION: Report BLOCKED with the full failure trace and one specific unblock request. Stop.
- POSITIVE: haiku failed once, sonnet twice, opus spent its single escalation attempt; trace complete. Ask the user.
- NEGATIVE: haiku + sonnet consumed all three attempts but opus has not attempted — opus still gets the single EC-2.4 escalation attempt. Escalate with the trace; do not ask the user yet.

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
- POSITIVE: Attempt 1 edits one rule; attempt 2 edits the rule plus three agents; the planned attempt 3 would edit CLAUDE.md too. Stop and escalate.
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

Each floor lists the check that proves it. A verifier runs these checks; a producer runs them before reporting. J5 is the canonical floor definition. `skills/quality-validation/SKILL.md` compiles it into the team-sweep checklist; when the two disagree, J5 wins and quality-validation is updated in the same change.

The floor is small on purpose. It covers what a runtime needs and what a validator can prove. Whether a file is well written is judged against `.claude/rules/writing-quality-standard.md` by the independent reviewer, not by counting sections. Which floors apply depends on the team's work-shape profile, read from `docs/work-shape.json` by `scripts/check_work_shape.py`:

- `skill-workflow`: J5.2, J5.4, J5.7 and J5.8. There are no agents, and rules are optional.
- `agent-group`: all of J5.
- `legacy` (stamped before 2026-11-26, no record): the validator applies the contract the team was built under, including the six-section agent floor, the four mandatory rules and the rule section floor. Do not apply that contract to new teams.

The 300/200/100-line marks for agent, skill and rule files trigger a look, not a cut. An over-mark file is `REVIEW_REQUIRED`: the producer records its size and why the content earns it, and the independent reviewer accepts or rejects the current file.

### J5.1 Agent .md
- SIGNAL: Artifact is an agent file in a team with a work-shape record.
- ACTION: Enforce: line-1 frontmatter with `name` and `description`; for a Claude-runnable agent, `model`; for a Codex playbook paired with `agents/**/*.toml`, `agent_type` in the playbook and `model` in the paired TOML. The role exists because a trigger in the record justifies it. The body says what this role owns, what it receives and returns, and what stops it; no section is mandatory. Check: `head -1` = `---`; `grep -cE '^(name|description):'` returns 2; inspect the paired runnable artifact for the platform fields; find the role's trigger in `docs/work-shape.json`; `wc -l` and resolve any size review.
- POSITIVE: A 60-line source checker has name, description and model, and the record's `isolated_check` describes its job. Floor met.
- NEGATIVE: A well-written "process reviewer" agent exists, and no flow in the record names an isolated check or a user request for it. Floor failed: the role has no trigger, whatever the file looks like.

### J5.2 Skill SKILL.md
- SIGNAL: Artifact is a skill file.
- ACTION: Enforce: lives at `skills/{name}/SKILL.md`; frontmatter name and a description that says when to load it; lengths above 200 lines require independent review, and detail used only sometimes sits under `references/`. In an agent-group team, identify the Claude coordinator entry from its declared workflow purpose or coordinator-adoption contract, independent of folder name or invocation flag. Exactly one such entry must exist, and it must have `disable-model-invocation: true`, `allowed-tools` granting Agent, `argument-hint`, and a resolvable coordinator playbook that it adopts in the main session without spawning the coordinator. These are A-Team entry requirements, not universal platform metadata. A malformed genuine entry stays a candidate and fails; ordinary manual-only skills are exempt. A skill-workflow team has no entry skill. Source: [Claude Code skill frontmatter](https://code.claude.com/docs/en/skills#frontmatter-reference).
- POSITIVE: A group's renamed coordinator-entry skill plus an ordinary manual-only review skill produce exactly one entry candidate, and it passes its metadata and main-session adoption checks.
- NEGATIVE: A skill declares that it launches the team's coordinator workflow but lacks `allowed-tools` or tells the session to spawn the coordinator. It remains an entry candidate and fails the corresponding check.

### J5.3 Rule .md
- SIGNAL: Artifact is a rule file in a team with a work-shape record.
- ACTION: Enforce: frontmatter name and description; the rule exists because a flow needs it and its content is not stated anywhere else in the team; an agent-group team has exactly one handoff contract rule; lengths above 100 lines require independent review. Check: grep frontmatter; search the team for the rule's key instruction to confirm it has one home; `wc -l`.
- POSITIVE: A group ships one 30-line handoff contract and one path-scoped rule about a billing directory. Floor met.
- NEGATIVE: A team ships worklog, context-management and reasoning rules copied from A-Team, and nothing in its flows uses them. Floor failed: the pack was copied forward.

### J5.4 settings.json
- SIGNAL: Artifact is a settings file.
- ACTION: Enforce: parses with `jq .`; contains `hooks`, `permissions`, `env` keys; no destructive allows (`rm -rf`, `git push --force`). Check: `jq 'has("hooks"), has("permissions"), has("env")'`; grep the deny patterns.
- POSITIVE: Parses, three keys, no destructive allows. Floor met.
- NEGATIVE: Parses and has all keys, but `permissions.allow` contains `Bash(rm -rf *)`. Floor failed — parseability does not excuse unsafe grants.

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

### J5.7 Generated CLAUDE.md
- SIGNAL: Artifact is a generated team's CLAUDE.md.
- ACTION: Enforce: what the project is for; gotchas the tree does not show; the canonical-authority statement; the generator stamp `Generated by A-Team on`. For an agent-group team, also a deployment section stating that the coordinator runs in the main session and is never spawned. No directory listing, role table or copied rule text. Check: grep the stamp and, for a group, the main-session statement; read the file for content the tree already shows.
- POSITIVE: A 14-line CLAUDE.md states the purpose, four gotchas, the authority and the stamp for a skill-workflow team. Floor met.
- NEGATIVE: A group's deployment section says to spawn the coordinator via the Agent tool. Floor failed: the main-session statement is load-bearing (production dead-lock evidence).

### J5.8 Work-shape record
- SIGNAL: Artifact is a team's `docs/work-shape.json`.
- ACTION: Enforce: one entry per user flow; every `agent-group` flow has evidence for at least one trigger and no `skill-workflow` flow has any; the tree matches the record. Check: `python3 scripts/check_work_shape.py <team-root>`; then read each trigger's evidence and judge whether it is true of this flow.
- POSITIVE: A fact-checking flow records `isolated_check: "nobody reads the brief before it is sent"` and ships an author and a checker. Floor met.
- NEGATIVE: The checker passes, and the `parallel` evidence reads "researcher, writer and editor each do their part", three stages that run in sequence. Floor failed: the evidence does not describe parallel work.
