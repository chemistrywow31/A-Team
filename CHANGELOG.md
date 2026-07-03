# CHANGELOG.md — A-Team Hardening Pass (2026-07-03)

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
