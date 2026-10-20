# CHANGELOG.md

---

# Context-Engineering Realignment (2026-07-25)

Trigger: Anthropic's 2026-07-24 post "The new rules of context engineering for Claude 5 generation
models" — >80% of Claude Code's system prompt deleted for Opus 5 / Fable 5 with no measurable eval
loss. Method: four context-isolated auditors (article alignment, context budget, dead machinery,
generated-team conformance) + one fresh-context verifier. Registers:
`.worklog/202607/context-engineering-realignment/phase-1-assessment/` (4 files, 963 lines);
decisions with per-item rationale in `phase-3-execution/decisions.md` (D1–D11).

## The finding that drove every decision

**Requirements with a mechanical check are met ~100% of the time; requirements without one, ~1%.**

| Requirement | Grepped by something? | Compliance |
|---|---|---|
| Agent .md carries `## Reasoning` four slots | yes (`quality-validation` 2.3) | 13/13 = 100% |
| Directory placement rules | yes | 32/32 teams = 100% |
| Reasoning slots written out to the worklog | no | 34/2,338 files = 1.5% |
| Five Self-Critique checks in the worklog | no | 2/2,338 = 0.09% |
| Agent .md carries `## Responsibilities` | no | 3/13 |
| Rules ≤100 lines | no (prose only; `wc -l` never run) | 19 violations in 8 teams |
| `docs/RUNTIME-SETUP.md` present | no (0 hits for `docs/` in the 42-item checklist) | **0/37 teams** |

So the correction was not "delete rules". It was: delete what is provably dead, relocate what is
spec-not-context, **make the spec executable**, and wire up what was built but never connected.

## Changes

| # | Change | Defect closed |
|---|---|---|
| 1 | `scripts/validate-team.sh` (NEW, 26 KB, jq-free, bilingual, 37 checks) — replaces the prose checklist's mechanical half, emits EC-3.6 `{item} | PASS/FAIL | {evidence}` | the ~1% compliance rate above |
| 2 | Phase 3.5 wired: Step 3.5 in `team-architect.md` + `runtime-preflight-advisor` added to the Subordinate Agents roster (it was absent) + checklist items 1.8/1.9 | `RUNTIME-SETUP.md` 0/37 — a fully built feature, with agent and script, dispatched by nothing |
| 3 | `skills/` incl. `boss/` reassigned from the coordinator to `skill-writer`; `coordinator-mandate.md` gains an explicit 2-item carve-out list; its violation check re-scoped off a section `team-architect.md` does not have | self-assigned steps have no dispatch record, no EC-1 report, and no producer to bounce — the FAIL path routed to nobody |
| 4 | Entry-point naming freed: identified by SHAPE (`disable-model-invocation` + `allowed-tools: Agent` + adopt instruction), not the filename `boss` | 10 of 11 "missing boss skill" teams had shipped a *better*-named front door (`callimachus/`, `ventris/`, `tongzheng/`). Real defect count: 1 missing (`u-team`) + 2 ambiguous |
| 5 | EC-2.4 made sole owner of the retry bound; `anti-sycophancy` and `context-management` now cite it | three-way contradiction: EC-2.2 bans same-approach retries at sonnet while two rules licensed three of them. `context-management.md:49` was unpatched, inside the section agents read for BLOCKED |
| 6 | "Copy verbatim" → "take the headers, write agent-specific checks"; generic template wording is now the violation | all 13 agents violated the verbatim mandate, and were right to: they share only the 5 headers, and enforcing it would have destroyed the specialization that makes the gates executable |
| 7 | Runtime write-out mandate for Reasoning slots deleted, authoring requirement kept | 1.5% observed compliance on the unverifiable half; 100% on the grepped half |
| 8 | Three-example mandate → one rejection case | 3,331 lines across 332 generated agents, enforced in only 22 of 32 teams, while 11 of A-Team's own 13 agents carry zero |
| 9 | M1 resolved: `.claude/` canonical, `AGENTS.md` rewritten to agree; both entry docs stamped; M4's stamp-diff moved into `team-restructuring-master.md` Step 0 | A-Team violated its own `dual-platform-parity` M1 and M3; the agent M4 names as enforcer contained zero mentions of stamps |
| 10 | `reviewer-mandate.md` and `dual-platform-parity.md` path-scoped (the latter to the platform globs, NOT `teams/**` — A-Team is itself multi-tree) | 108 lines of `teams/**` spec loaded on every session and every dispatch |
| 11 | Size budgets added: ≤12 rules, ≤14 agents, escape hatch = one justification line | the "8-rule cap" existed nowhere as a rule — only inside a *filled example* of an EC-1 report |
| 12 | `.claude/settings.json` hooks de-jq'd; checklist 1.5 switched to `python3 -m json.tool` | A-Team exempted itself from the no-jq portability rule it enforces on output |
| 13 | `skills/continuous-learning-v2/` DELETED from all 3 trees (153+51+51 lines) | documented `MEMORY.md`, `.claude/instincts/`, `/instinct-status` — none exist; zero hooks drove it; zero referrers |
| 14 | `AUDIT.md` staleness banners; `prompt-patterns/SKILL.md` version note | AUDIT.md's cited baseline was 70% above the live value, its four register files have been deleted, and `assets/raw/` is 3,311 lines of 4.x-anchored text with zero Claude 5 references |

## Always-on context

| | 2026-07-03 pass | 2026-07-25 pass |
|---|---:|---:|
| Always-on rules | 9 | **7** |
| Lines (CLAUDE.md + unscoped rules) | 782 | **687** |
| Bytes | 53,539 | **48,429** |
| Est. tokens | 13,384 | **12,107** |

−95 lines / ≈−1,280 tokens, paid on the main session and on every subagent dispatch (up to 13 per
run). Deliberately modest: 108 lines came out by scoping and ~26 lines of load-bearing content went
back in. The large scoping win was already taken in 2026-07-03 (−41%); what remains always-on is
mostly load-bearing, and the remaining reductions land in on-demand and generated output instead.

## Three premises the audit refuted

Recorded because they were the coordinator's own starting assumptions and were wrong:

1. **"Generated teams are bloated."** `presentation-studio` is 8,231 lines of structure that produced
   3,704,584 lines of deliverable. Structure is 2.7% of team text; deliverables are 94.2%. Verbatim
   boilerplate in large teams is 3.6–6.5% of rules+agents, and agent files are 0.0–12.8%
   generator-derived — the specialists are genuinely written per team.
2. **"EC-2's escalation ladder is dead code."** True of A-Team's own tree (13/13 opus), false of its
   output: 195 opus / 116 sonnet / 11 haiku across 332 agents, mixed rosters in 20 of 32 teams. EC-2
   was kept and its all-opus case documented instead of cut.
3. **"16 teams are missing their entry-point skill."** 10 of them had themed entry points that were
   better than the mandated name. The mandate was the defect.

## Rejected

- **R-1 Split EC-2.1/2.2/2.3/2.6 into a path-scoped rule** (auditor recommendation, ~6 always-on
  lines): REJECTED — six lines does not justify fragmenting a numbered contract across two files with
  different loading conditions. Fixed the underlying defect instead: EC-2 cited `context-tier.md` as
  its tier authority while that rule is path-scoped and never loads where EC-2 applies. Mapping now
  inline.
- **R-2 Path-scope `coordinator-mandate.md`** (both auditors): REJECTED — the carve-out list added in
  change 3 governs A-Team's own main-session coordinator, making the file load-bearing outside
  `teams/**`.
- **R-3 Delete `prompt-patterns/assets/raw/`** (3,311 lines, zero readers, zero Claude 5 references):
  user declined 2026-07-25. Staleness note added to `prompt-patterns/SKILL.md` instead.
- **R-4 Track `teams/` structure in git; remove `teams-index/`**: user declined 2026-07-25. Consequence
  logged — no output-to-generator feedback loop can be verified, and this assessment cannot be
  repeated as a diff.
- **R-5 Mandatory-rules templates** (the 4 rules are independently rewritten in every team: 3,132
  lines across 103 files, one team's execution contract sharing 0.0% with A-Team's): NOT DONE this
  pass. Dormant, not broken; queued as follow-up.

## Retrofit (16 teams with run records; scope approved by the user)

`docs/RUNTIME-SETUP.md` + `docs/automode-snippet.json` for 15 teams, and version stamps for 7 that
had none (dates inferred from the oldest `.claude/` file mtime, marked approximate in an HTML comment
because these teams predate stamping). `u-team` was excluded on discovery — its charter declares its
Claude tree a reference-only mirror. Validator: `passed=973 failed=131` → `passed=974 failed=94`,
zero regressions. D1/D2/D3 and C5 now PASS on all 15; three teams are fully green
(`alexandria`, `obsidian-pkm-team`, `tongzhengsi`).

The remaining 94 failures are deliberately out of the approved scope: 15 are `docs/RUNTIME-SETUP.md`
in the 14 never-run teams, and the rest (12 R4, 12 C4, 11 R3, 11 C2, 5 C5, plus cap violations) are
pre-hardening-cohort rule defects. Retrofitting those is a per-team Phase 7 decision, not a batch fix.

## Corrections caught by verification, not by the author

Five, recorded in `phase-3-execution/decisions.md` D12 with reproduction steps. Two are worth naming
here because they are defect *classes*, not instances:

- **A rule change is not done until every EMITTER is swept.** The example-mandate change landed in 3
  of 12 sites on the first pass. The miss that mattered was the `## Examples` skeleton inside
  `agent-writer.md` and `skill-writer.md`, copied verbatim into every generated agent — and
  `prompt-optimizer.md:200`, which told Phase 4 to "add missing cases" and would have re-added on
  every optimization what the rule had just removed. Emitters include templates, writers, optimizers,
  and checklists.
- **`scripts/preflight-permissions.sh` silently destroyed user settings.** Its Route B merge used
  `jq -s '.[0] * .[1]'`; jq's `*` replaces arrays. The snippet carried a 2-entry
  `autoMode.environment` against a shipped 20 with no `"$defaults"` sentinel, so following the
  generated instructions dropped 18 entries. Fixed by omitting `environment` entirely; Route B now
  prints before/after lengths for all three arrays. Verified 20 → 20, 65 → 65. Found by a subagent
  auditing the tool it had been told to use — the single highest-value finding of the retrofit.

Also: `u-team` was misdiagnosed from a validator FAIL before its charter was read, nearly triggering
a retrofit that would have broken a documented contract; `context-tier.md`'s mandated section was
contradictory and was shrunk rather than satisfied; and the dangling decision-record citation in
`teams/u-team/CLAUDE.md` (the cited file exists nowhere) was removed.

## Follow-ups

- Ship `.claude/templates/mandatory-rules/` so the four mandatory rules stop forking 32 ways (R-5).
- Teach `scripts/preflight-permissions.sh` to switch heading sets on the team's detected language.
  15 of the 16 retrofit advisories are hand-localized and a re-probe overwrites them;
  `teams/tongzhengsi/docs/RUNTIME-SETUP.md` is the Traditional Chinese reference implementation.
- Generated teams should carry their own `reasoning-self-critique-blocks.md` — the gates occupy
  22–30% of every generated agent file because the skeleton lives only in A-Team's tree.
- `flutter-app-dev-team` and `muybridge-motion-studio` each ship two entry-point-shaped skills;
  pick one front door per team.
- Re-run the paths-scoping probe after any Claude Code upgrade — the scoping saving rests on it.
- `JUDGMENT.md` reaches 0 generated teams while 127 of their agents are sonnet or haiku, which is the
  tier the rubrics were written for. Propagate it or a team-local equivalent.

---

# A-Team Hardening Pass (2026-07-03)

Every change cites its defect IDs from `AUDIT.md` (X-n consolidated; TW/FL/EP/L2 raw registers under `.worklog/202607/a-team-hardening/phase-2-audit/`). Adversary rulings from `.worklog/202607/a-team-hardening/phase-4-adversarial/`.

## Token budget accounting (§13)

- Always-loaded BEFORE: 82,200 B ≈ 20,550 tok (CLAUDE.md 3,852 + 16 rules 78,348), injected into every session and every dispatch.
- Always-loaded AFTER: **48,243 B ≈ 12,060 tok (−41%)**, final post-adversarial state (fresh-context verifier measurement, mechanical-checks.md M7) — CLAUDE.md + 8 unconditional rules, including the execution contract with its round-1/2 hardening additions (~3.1 KB of adversary-demanded clauses: EC-1.7, escalation-exception mirrors, provenance and correction-cap bounds).
- Moved to on-demand (path-scoped, loads only on `teams/**` reads): 49,034 B across 9 generation rules + spent probe.
- Justification of increases: execution-contract.md (+9,306 B always-loaded) buys the §7 mandate set (report schema, retry caps, verification, precedence, caps) — its per-run cost (~2.3k tok × 12–15 dispatches ≈ 30k) is repaid ~4× by the scoping win alone (~111k–139k/run), before the structural savings (interview O(n²) ~160k, transcript ~40k, correction bound ~50k). CLAUDE.md +1,458 B: deployment-mode correction (X-1), precedence restatement (X-5), AMD-3.

## New artifacts

| Artifact | Defects | Notes |
|----------|---------|-------|
| `.claude/rules/execution-contract.md` (EC-1..EC-5) | X-2, X-6, X-7, X-10, X-11; directive §7.1–7.5 | Canonical RULES file; statuses adapted to repo's four (phase-3 D1) |
| `JUDGMENT.md` (J1–J5) | directive §8 | On-demand; every criterion SIGNAL/ACTION/+ex/−ex |
| `templates/{search,implementation,refactoring,research,review}.md` | X-6; directive §9 | 42–46 lines each incl. filled example; cite EC + J numbers |
| `.claude/templates/reasoning-self-critique-blocks.md` | TW-7 (34k/run duplication) | Single source for canonical gate blocks |
| `.claude/templates/hooks-baseline.json` | X-8 / L2-16 | cat-based capture (no jq), `$CLAUDE_PROJECT_DIR` anchoring, suppression; backports toeic/cnn hand-fixes |
| `.claude/templates/settings-baseline.json` | TW-12 | Extracted from settings-json.md |
| `.codex/rules/execution-contract.md` + AGENTS.md pointer | parity | Condensed Codex mirror; full re-port deferred (see Follow-ups) |

## Changed files (before → after)

1. **CLAUDE.md** — X-1, X-5, AMD-3: deployment mode now states the coordinator runs in the main session (never spawned) + NEEDS_CONTEXT relay; new "Execution Contract and Precedence" section (EC-4 restated at point of use); code reviewer scoped to executable-artifact teams; mandatory rules list gains execution-contract + version stamp.
2. **`.claude/agents/team-architect.md`** (rewrite) — X-1, X-2, X-5, X-6, X-7, X-9, TW-5/6/14: Runtime Placement (main-session, relay, dialogue-log); Dispatch Protocol (templates, acceptance criteria, SCOPE-IN/OUT, bounce); Phase 1 interview conducted directly (kills O(n²)); Phase 2 gate now content-based (queries listed); Phase 3 ownership fences, 4 mandatory rules, verification DISPATCHED to fresh-context verifier (never self-run), corrections bounded by EC-2.4, re-validation after any mutation (also Phase 4/7); Phase 6 passes dialogue-log path, never a transcript; Phase 7 gains the generator-backport step; new Parallelism + Compaction strategies; phases renumbered in order.
3. **`.claude/skills/a-team/SKILL.md`** (rewrite) — AMD-1/X-1: main-session adoption of the coordinator playbook; no spawn; 3 examples incl. rejection (J3.2).
4. **9 generation rules** get `paths: ["teams/**"]` — X-4/TW-3 (~113k tok/run): output-structure, yaml-frontmatter, frontmatter-optional-patterns, writing-quality-standard, prompt-engineering-patterns, settings-json, hooks-integration, skill-context-fork (+`.claude/skills/**`), context-tier. Probe evidence: scoped rules absent at subagent startup, inject on matching read. Backstops: writers' "Required Reads Before Writing" + fresh-context verification floors (J5).
5. **settings-json.md / hooks-integration.md** — TW-11/12, X-8/L2-16: embedded JSON replaced by template pointers with read-triggers + compliance checks; Stop-hook table row made honest (dir warn, not "three-file completeness"); guaranteed-tool list drops jq, adds `$CLAUDE_PROJECT_DIR` anchoring + suppression + ledger PII/consumer clauses.
6. **reasoning-and-self-critique.md** — TW-7: four canonical block bodies replaced by slot-name specs + pointer to the blocks template; Tradeoff compressed to charter-required 2 sentences (8,497 → 6,537 B).
7. **context-management.md** — X-6, X-10, AMD-2: dispatch requires acceptance criteria + scope fence + BRIEF path + template read-trigger; return format now points to EC-1 (single source); status handling → EC-1.5 + user-input relay clause; violation list updated.
8. **worklog.md** — EC-5.1, X-9, AMD-4: brief.md + dialogue-log.md added to structure; mechanical-phase `phase-log.jsonl` profile exception for generated teams (A-Team's own phases keep the full triad).
9. **output-structure.md** — AMD-1, X-3: entry-point section rewritten to main-session adoption (with production evidence cited); 4th mandatory rule (execution-contract); generated CLAUDE.md must carry precedence order + `Generated by A-Team on {date}` stamp; violation list extended (incl. spawn-pattern = violation).
10. **skill-context-fork.md** — AMD-1: entry-point wording updated in 3 places.
11. **prompt-engineering-patterns.md** — TW-13, X-13: unsourced effectiveness percentages removed; example-diversity deduped to a cross-ref; parallel-execution guidance gains the >5-items batch rule (~25× measured overhead cited).
12. **anti-sycophancy.md** — X-11: escalation section cross-referenced to EC-2.4 (same 3-attempt bound; EC-2 stricter on approach).
13. **Writers** — X-5, FL-4, EP-10, TW-7: agent-writer loses CLAUDE.md ownership (architect owns it), gains Boundaries + Required Reads + EC-1 return + coordinator-template additions (Verification Protocol, Correction Loop Bound, User Relay, batch rule) + canonical-block pointers replacing embedded copies; rule-writer gains Boundaries + 4-mandatory-rules update + Required Reads; skill-writer gains Boundaries + skill-creator-by-Read fix (slash invocation impossible in subagents).
14. **requirements-analyst.md** — AMD-2/X-1: new Interaction Channel section (question mode / synthesis mode / no user simulation — every summary entry cites a dialogue-log line); completion criterion 6 and Evidence Check retargeted to dialogue-log.md.
15. **prompt-optimizer.md** — AMD-2, EP-10: User Interaction Protocol rewired to NEEDS_CONTEXT relay; `/compact` replaced with worklog summarization.
16. **dialogue-reviewer.md** — X-9: input is the dialogue-log PATH read from disk; inline transcripts refused; BLOCKED when the log is missing (no reconstruction).
17. **skill-planner.md** — TW audit: Applicable Rules gains worklog.md + execution-contract.md.
18. **`.claude/skills/quality-validation/SKILL.md`** (rewrite) — X-2, X-12, TW-14: now the canonical 5-level checklist (49 items) with per-item check commands, absorbing the architect's 20-item list + new mandates (settings.json/hooks check closes failure-trace 2; boss spawn-pattern check; stamp; execution-contract presence); executed only by a dispatched fresh-context verifier.
19. **`.claude/settings.json`** — X-8: all four hook commands anchored to `$CLAUDE_PROJECT_DIR` + suppression; jq retained at L1 (proven working locally — phase-3 D6).
20. **`.claude/rules/zz-paths-probe.md`** — spent probe neutralized (never-matching glob); safe to delete.

## Charter amendments (§5 case files)

| ID | Rule | Class | Evidence | Guardian ruling |
|----|------|-------|----------|-----------------|
| AMD-1 | output-structure entry-point spawn mandate → main-session adoption | (b) demonstrably wrong | toeic boss/SKILL.md:12-20 documents the dead-lock + hand-patch; cnn boss/SKILL.md:68 still broken; runtime probe | APPROVED (guardian-rulings.md) |
| AMD-2 | interview/user-dialogue assumed inside subagents → main-session + relay | (c) blind spot (+b) | EP-11 trace 1 (simulated interview); no relay existed in the original NEEDS_CONTEXT handler | APPROVED |
| AMD-3 | code reviewer mandatory for all teams → scoped to executable-artifact teams | (c) blind spot | teams/market-research/review/ contains only the process reviewer — zero code/QA reviewers | APPROVED |
| AMD-4 | 3-file worklog per phase → mechanical-phase profile for generated pipelines | (c) blind spot | toeic: 30 boilerplate files/day; A-Team's own phases stay full-triad | APPROVED |

Guardian also confirmed: no hidden amendments across the 10 non-AMD changes; no conflicts between execution-contract.md and preserved rules (EC-2.4 ↔ anti-sycophancy bound reconciled by the cross-reference; EC-4 keeps preserved rules in force at level 6). Known gap: market-research itself predates AMD-3 and stays non-compliant until a retrofit (`/A-Team --restructure`).

## Rejected proposals

- R-1 Delete "Boil the Lake" from CLAUDE.md (TW-13#4): REJECTED — user's charter voice with an operative criterion; 330 B not worth intent risk.
- R-2 Full .codex rules re-port (TW-15/X-16): DEFERRED — separate runtime, hand-condensed style; shipped the contract mirror + pointer; follow-up below.
- R-3 Relax the canonical-gate mandate for generated agents (L2-2, ~460 tok/dispatch): REJECTED — structural gates are recent deliberate charter (commit 64a9000); L1 duplication solved by extraction instead.
- R-4 Deep three-file Stop hook in the baseline (cnn's hand-fix): REJECTED for baseline (fragile within 10 s timeout across arbitrary task layouts) — documented as a team-specific addition; table row made honest instead.
- R-5 Delete stale worktree / orphan dirs (~63 MB+): OUT OF SCOPE — not created by this task (J3.2); listed in AUDIT.md hygiene notes for the user.

## Follow-ups (logged, not executed)

- Codex parity: script or checklist to derive `.codex/rules/*` from `.claude/rules/*` with drift detection (X-16); mirror the AMD-1 entry-point change into `.codex` docs.
- L2-17: generated teams ship 2–3 platform copies of each skill with no sync check — generator should emit one canonical tree + derivation step.
- Retrofit: existing 51 generated teams predate this pass (no version stamps); `/A-Team --restructure` per team is the supported path.
- Re-run the paths-scoping probe (a fresh subagent checking startup-absence + inject-on-read) after any Claude Code upgrade — the ~113k tok/run saving rests on that runtime behavior, verified 2026-07-03.
- Accepted duplication (logged, not a defect): context-management.md keeps the four status DEFINITIONS while EC-1.1 enumerates them — point-of-use restatement per the directive's §6.6; the definitions live in exactly one place.

## Adversarial round 1 → revision log

27 MATERIAL + 9 minor findings (registers: `.worklog/202607/a-team-hardening/phase-4-adversarial/`). All revised except two evidence-backed rebuttals (ADV-S7 propagation chain — clarifier added anyway; ADV-R1 jq removal — WARN-on-failure instead, per phase-3 D6). Key post-adversary changes: EC-1.7 (NEEDS_CONTEXT bounding), EC-2.1 (ladder direction, no tier-skipping without J1.3), EC-2.4 (one-shot escalation attempt exception), EC-2.5 (single criteria-correction with external evidence, worklog-enforced), EC-3.5 (provenance = prior ARTIFACTS fields; restructuring-target scope), EC-5.3 (dual caps, stricter wins), EC-5.4 (coordinator-only), J4.4 + J5.7 added, J1.1/J1.3/J3.2/J3.3/J3.4/J4.2/J4.3/J5.1/J5.2/J5.5 tightened, templates review-rewrite-escape removed / search shortfall status / refactoring J4.4 citation, settings-baseline hooks stub `{}`, hooks-baseline event-JSON doc fix, writer CLAUDE.md-absent fallbacks, checklist 5.4 concrete grep + 5.8 mechanical/4.5 judgment split, dialogue-log created empty at task start, `/A-Team` wrong-context guard. Advocate (haiku) fixes: EC-3.5 any-of, J3.2 exact-target authorization, J5.6 non-empty definition, SCOPE-IN/OUT semantics, bounce-per-task.

## Session-limit incident (process note)

The first adversary/guardian wave (4 top-tier agents in parallel) hit a platform session limit after completing their reads but before writing outputs; re-run executed sequentially on sonnet with write-early instructions. Haiku advocates were unaffected; their paraphrase-back findings (EC-3.5 any-of, J3.2 authorization granularity, J5.6 non-empty definition, SCOPE-IN/OUT semantics, bounce-per-task) were applied before round 2.
