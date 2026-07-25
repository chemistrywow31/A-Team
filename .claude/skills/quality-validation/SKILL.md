---
name: Quality Validation
description: Canonical validation checklist for generated team structures, executed by a fresh-context verifier
disable-model-invocation: true
---

# Quality Validation

## Description

The single checklist source for validating a generated team. Team Architect does NOT execute this checklist itself — per `rules/execution-contract.md` EC-3.1, the orchestrator of production never accepts the production. The architect dispatches a fresh-context verifier (built from `templates/review.md`) with: this file's path, the team directory, and the Phase 1–2 `decisions.md` paths. The verifier runs every check with commands and returns per-item PASS/FAIL with evidence (EC-3.6).

## Belongs To

Used by the fresh-context verifier dispatched by `agents/team-architect.md` (Phase 3 Step 3, re-validation after Phase 4/7 mutations, Phase 5 confirmation).

## How to Execute

**Run `bash scripts/validate-team.sh {team}` FIRST.** It executes every mechanical check in this file and emits the required `{item} | PASS/FAIL | {evidence}` lines directly. Paste its output as your evidence. Then run only the judgment items below that the script marks SKIP or does not cover — the ones needing a model to read for meaning (Level 4 overlap and coverage analysis, semantic correctness of rules, whether the single rejection-case example names a concrete refusal boundary rather than a vague one).

Do not hand-run a check the script already performs. Prose checklists in this repo were measured at ~1% compliance where nothing executed them; the script exists so that number is not the checklist's fate.

- Level 2 items apply the per-artifact floors canonically defined in `JUDGMENT.md` J5. When this file and J5 disagree, J5 wins — update this file AND `scripts/validate-team.sh` in the same change (single-source rule).
- Run each remaining check's command from the repo root; `{team}` = `teams/{team-name}`.
- Record one line per item: `{item} | PASS or FAIL | {file:line or command output}`.
- Overall PASS requires every applicable item PASS. Return per EC-1 with the full item table INLINE (the harness blocks subagent report-file writes); the dispatching coordinator lands the table at the phase worklog as `verification.md`.

## Level 1: Structural Completeness

- 1.1 `{team}/CLAUDE.md` exists — `test -f`
- 1.2 Coordinator .md sits in `agents/` root; every non-coordinator agent sits in a subfolder — `ls -R {team}/.claude/agents/`
- 1.3 Every skill is `skills/{name}/SKILL.md` (uppercase filename) — `find {team}/.claude/skills -name SKILL.md`
- 1.4 `rules/` contains .md files — `ls {team}/.claude/rules/`
- 1.5 `settings.json` exists and parses — `python3 -m json.tool {team}/.claude/settings.json` (not `jq` — absent on stock macOS)
- 1.6 All file and folder names kebab-case — `find {team} -name '*_*' -o -name '* *'` returns nothing
- 1.7 Entry-point skill exists, identified by SHAPE not filename — `grep -rl '^disable-model-invocation: *true' {team}/.claude/skills` returns exactly ONE file. The folder name is the team's choice (`callimachus/`, `tongzheng/`, `ventris/` are all valid); a `boss/`-only test false-FAILs the majority of teams. Zero hits → no front door; two or more → ambiguous front door. Both FAIL.
- 1.8 Runtime advisory exists — `test -f {team}/docs/RUNTIME-SETUP.md`. Produced by `runtime-preflight-advisor` at Phase 3.5. It was absent from 37 of 37 teams because no checklist item looked for it and no dispatch step produced it; both gaps are now closed, and this item is what keeps them closed.
- 1.9 Advisory is not stale boilerplate — `grep -c 'Probed:' {team}/docs/RUNTIME-SETUP.md` ≥ 1 AND the file names a rollback command (`grep -iE 'rollback|restore|revert'`). Do not anchor the stamp pattern to line start: the generator emits it inside a blockquote as `> Probed: ...`, and `^Probed:` false-FAILs every correct file.
- 1.10 Size budgets — rule count ≤ 12 and agent count ≤ 14, or the phase `decisions.md` carries a justification line. `ls {team}/.claude/rules/*.md | wc -l`; `find {team}/.claude/agents -name '*.md' | wc -l`

## Level 2: Content Completeness

- 2.1 Every .md starts with `---` on line 1 — `head -1` each
- 2.2 Every agent frontmatter has `name`, `description`, `model` (+ `effort`) — grep each
- 2.3 Section order in every agent: `## Reasoning` before `## Workflow` before `## Self-Critique` — `grep -n '^## '`
- 2.4 Reasoning has the 4 canonical slots; Self-Critique has the 5 canonical checks (Tier 1 agents: reduced 2-check form allowed only with a Tier 1 justification) — grep slot headers
- 2.5 Every agent has `## Boundaries`, `## Uncertainty Protocol`, and an `## Examples` section carrying one rejection case and no normal/edge cases — grep
- 2.6 Coordinator additionally has: Pre-Dispatch Reasoning, Team Overview, Subordinate Agent List, Task Assignment Strategy, Quality Control Mechanism, Parallelism Strategy (with the >5-items batch rule), Compaction Strategy, Verification Protocol, Correction Loop Bound, User Relay — grep
- 2.7 Every skill per J5.2: lives at `skills/{name}/SKILL.md`, frontmatter `name` + `description`, one rejection-case example, ≤200 lines or progressive-disclosure bundle; entry-point extras are checked in 5.4 — path test + grep + `wc -l`
- 2.8 Every rule has Applicability, Rule Content, Violation Determination, Exceptions; ≤100 lines — grep + `wc -l`
- 2.8b Every agent declares `## Context Tier: {1-4}`, and any Tier 1 agent carries a Tier 1 justification — `grep -c '^## Context Tier' ` per agent; then for Tier 1 hits, grep `Tier 1 justification`. Nothing checked this before, so generated agents omitted the section while items 2.4 and 5.10 silently PRESUMED a declared tier when granting Tier 1 exemptions
- 2.9 Every external skill (Pattern A/B) has Source Attribution with Origin, Integration, Retrieved, Modifications — grep
- 2.10 Every agent .md ≤300 lines — `wc -l`
- 2.11 Generation-artifact hygiene — `grep -rn '</content>\|</invoke>\|</parameter>' {team}` returns nothing; `grep -rn 'TODO\|TBD' {team}` hits only lines that are demonstrably content (e.g., a rule discussing TODO conventions), never unfinished slots (ground truth: alexandria 2026-07 — 14 stray closing tags shipped past producer Self-Critique AND this checklist's verifier; only the design-fidelity auditor caught them)

## Level 3: Reference Consistency

- 3.1 Every skill path referenced in an agent file exists — extract refs, `test -f` each
- 3.2 Every rule path referenced in an agent file exists — same
- 3.3 Where a skill declares a Users/Belongs To section, its list ↔ actual agents (the section itself is optional per 2.7/J5.2); rule Applicability ↔ actual agents
- 3.4 Coordinator's subordinate list covers all non-coordinator agents
- 3.5 Source Attribution URLs and Pattern types match the Phase 2 plan — read Phase 2 `decisions.md`
- 3.6 The same concept uses the same name across all files

## Level 4: Logical Consistency

- 4.1 No two agents have overlapping responsibilities (unless designed as a review relationship)
- 4.2 Combined responsibilities cover the Phase 1 scope with no vacuum — read Phase 1 `decisions.md`
- 4.3 No agent appears in two groups; collaboration relationships are bidirectionally consistent
- 4.4 Coordinator's Responsibilities contain only coordination work (planning, assignment, tracking, quality control)
- 4.5 (judgment expected) Each rule's loading mode is sensible: file-type rules path-scoped, process rules unconditional; flag misclassifications with reasoning — this item may use judgment, unlike Level 5

## Level 5: Mandate Compliance

- 5.1 CLAUDE.md contains: deployment mode section with the coordinator-runs-in-main-session statement, worklog + context management section, precedence order, and the generator version stamp `Generated by A-Team on` — grep each
- 5.2 `rules/` contains the four mandatory rules: worklog, context-management, reasoning-and-self-critique, execution-contract — `ls`
- 5.3 The team's execution contract keeps EC-1..EC-5 clause numbering — `grep -c 'EC-'`
- 5.4 The entry-point skill found in 1.7 declares `disable-model-invocation: true`, `allowed-tools: ["Agent"]`, `argument-hint`, and uses main-session adoption. The verifier dispatch supplies the coordinator agent's name. Check: `grep -inE 'subagent_type|spawn' {entry-skill-path}` — FAIL if any hit instructs spawning the coordinator (by the supplied name or as "the coordinator"); a negated mention in a "why not to spawn" section is not a hit. PASS additionally requires a line instructing the session to Read the coordinator's .md and adopt its workflow
- 5.5 Process reviewer exists in its own group folder (teams ≤3 agents: coordinator absorbs it, documented in Responsibilities)
- 5.6 Code reviewer exists when deliverables include executable artifacts; otherwise a deliverable-QA reviewer — read CLAUDE.md scope
- 5.7 settings.json has `hooks`, `permissions`, `env`; hook commands anchor paths to `$CLAUDE_PROJECT_DIR`, contain no `jq` dependency, and `permissions.allow` grants nothing destructive and no interpreter/runner wildcards; bare `Write`/`Edit`/`Agent` sit in allow, not ask (permission bands per `rules/settings-json.md`) — `jq` + grep
- 5.8 Mechanical check only: every rule whose Rule Content contains glob tokens (`**/` or `*.`) has `paths` frontmatter — grep the body for glob tokens, cross-check the frontmatter. Rules that read as both file-type and process are NOT judged here: list them under DONE_WITH_CONCERNS (semantic classification lives in 4.5)
- 5.9 No urgency language (CRITICAL / MUST / ALWAYS / NEVER) on non-safety behavioral preferences — grep, judge each hit against the tone table in `rules/prompt-engineering-patterns.md`
- 5.10 Every non-Tier-1 agent has an Uncertainty Protocol with a concrete trigger — grep
- 5.11 Agent Teams mode only: env flag in settings.json + `teammateMode`; File Ownership and Communication Patterns per agent; known-limitations list in CLAUDE.md; messaging pairs bidirectional
- 5.12 Agent Teams mode only: environment readiness was checked, or CLAUDE.md includes the exact setup JSON

## Validation Result Format

```markdown
# Quality Validation Report: {team-name}
| Item | Verdict | Evidence |
|------|---------|----------|
| 1.1  | PASS    | teams/x/CLAUDE.md exists |
| ...  | ...     | ... |
Overall: PASS / FAIL ({n} failures listed above)
```

Deliver the report per EC-1 with the table inline; the coordinator lands it at the phase worklog as `verification.md`.
