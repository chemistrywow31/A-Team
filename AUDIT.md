# AUDIT.md — A-Team Hardening Defect Register (2026-07-03)

## §0 Parameter resolution (recorded per directive)

- `A_TEAM_ROOT` = this repository root — charter: `CLAUDE.md` + `.claude/rules/`; orchestrator: `.claude/agents/team-architect.md`; subagents: `.claude/agents/**`; config: `.claude/settings.json`; Codex tree: `.codex/` + `AGENTS.md` + `agents/**.toml` + `.agents/skills/`. (Paths in this document are repo-relative; the original recorded an absolute local path, which does not belong in a checked-in file.)

> **Counts and byte figures in this document are as-of 2026-07-03 and have since changed.** At the time of writing: 16 rules, 12 subagents, 82,200 B always-loaded. As of 2026-07-25: **18 rules (7 always-on), 13 subagents, 48,429 B always-loaded.** Do not cite this file's numbers as a current baseline — the 82,200 B figure is 70% above the live value. Current measurements: `.worklog/202607/context-engineering-realignment/phase-1-assessment/context-budget.md`.
- `OUTPUT_ROOT` = edit in place. Audit artifacts (`AUDIT.md`, `CHANGELOG.md`, `VERIFICATION.md`), `JUDGMENT.md`, `templates/` at repo root. Canonical RULES file at `.claude/rules/execution-contract.md` — the only auto-loaded location; a repo-root copy would be dead weight (phase-1 decisions D1).
- `STRONG`/`MID`/`SMALL` = `opus`/`sonnet`/`haiku` (the identifiers this repo's frontmatter uses).
- Repo conventions: none found — no package.json anywhere (node_modules is an orphan of the deleted "a-team-draft-system"); no test/lint command. Mechanical checks: `jq`, `wc`, `grep`, `head`.

## Method

Four context-isolated auditors (Cartographer, Token Economist, Failure Analyst, Layer-2 Auditor) + one runtime probe. Full registers with per-defect file:line evidence:

> **These four register files no longer exist.** `.worklog/202607/a-team-hardening/` was deleted at some point after 2026-07-03; the paths below are retained as a record of what was produced, not as working references. Consequence worth stating plainly: this pass's own evidence base is gone, so its findings can no longer be re-verified against their sources. That is the concrete cost of not tracking work products, and it is why the 2026-07-25 pass keeps its registers under `.worklog/202607/context-engineering-realignment/`.
- `.worklog/202607/a-team-hardening/phase-1-cartography/inventory.md` (171-row file table)
- `.worklog/202607/a-team-hardening/phase-2-audit/defects-token-waste.md` (TW-1..15)
- `.worklog/202607/a-team-hardening/phase-2-audit/defects-failure.md` (FL-1..9, EP-1..11, 3 failure traces)
- `.worklog/202607/a-team-hardening/phase-2-audit/defects-layer2.md` (L2-1..19)

Baseline: always-loaded set = 82,200 B ≈ 20,550 tok, injected into every session AND every subagent dispatch; typical run = 12–15 dispatches → 247k–308k tok of pure boilerplate per run (6–7× the actual agent definitions). Runtime probe result: a `paths:`-scoped rule is ABSENT from subagent startup context and INJECTS on matching file read (control string confirmed the method).

## Consolidated ranked register (severity × frequency; Layer-2 first)

| Rank | X-ID | Merges | Sev | Layer | Finding | Location (canonical) |
|------|------|--------|-----|-------|---------|----------------------|
| 1 | X-1 | L2-12, EP-11, TW-4 | S1 | L2+L1 | Coordinator-as-subagent dead-locks: spawned coordinator has no dispatch tool and no user channel; interview gets simulated; O(n²) re-dispatch ≈160k tok/run. Production evidence: toeic hand-patch vs cnn still broken. | output-structure.md:121-145; a-team/SKILL.md:21-34; team-architect.md:75; requirements-analyst.md:139-145 |
| 2 | X-2 | EP-2, EP-1, L2-13 | S1 | L2+L1 | Success accepted on claim; gates test shape not evidence; producer/architect self-validates (Step 3 + Phase 5); documented 2026-04-22 false-PASS in ground truth. | team-architect.md:100,152-183,203-213 |
| 3 | X-3 | L2-11 | S1 | L2 | Generator mandates advisory in practice: 0/26 ground-truth agents carry mandated sections; 16 rules vs ≤8 cap; no version stamp; no backport loop for production fixes. | reasoning-and-self-critique.md → teams/{toeic,cnn} greps |
| 4 | X-4 | TW-3, TW-7, TW-13, L2-1, L2-2 | S3×freq | L1+L2 | Always-loaded tax: 10/16 rules apply only to writers yet load on every dispatch (~113k tok/run); canonical gate blocks duplicated (~34k); filler ~11.6k; generated teams inherit the same architecture (15–22k tok/dispatch). | rules/* Applicability headers |
| 5 | X-5 | FL-8, L2-9, EP-5 | S1 | L1+L2 | No precedence order anywhere; live conflicts: CLAUDE.md/settings.json double-vs-zero ownership (architect Step 0 vs agent-writer.md:336-350); inline Output Formats vs 500-word return rule. | team-architect.md:122 vs agent-writer.md:336-350 |
| 6 | X-6 | FL-1, FL-9, L2-7 | S1 | L1+L2 | No acceptance criteria or definition of done in any dispatch protocol — dispatches carry only worklog path + scope summary. | context-management.md:18-20 |
| 7 | X-7 | EP-7, TW-6, EP-6, L2-10 | S1/S2 | L1+L2 | Unbounded correction loop, no counter/log; Phase 4/7 mutate files after validation with no re-validation. | team-architect.md:181,191-201,223 |
| 8 | X-8 | EP-10, L2-16 | S1/S2 | L1+L2 | Environment assumptions: jq not on stock macOS (silent hook death), relative paths built nested .worklog trees (disk evidence), write-only PII ledger 166KB/month, Stop hook that can never fail, /skill-creator invoked where unavailable. | hooks-integration.md:39-92; settings.json:64-109; skill-writer.md:39 |
| 9 | X-9 | TW-5, EP-9 | S1 | L1 | Phase 6 "complete transcript" and the 20-item checklist exist only in compactable memory → fabricated reviews post-compaction; transcript double-cost ≈40k tok/run. | team-architect.md:152-179,229-231 |
| 10 | X-10 | EP-8, L2-15 | S2 | L1+L2 | Return schema exists but no bounce protocol; malformed reports drive phase transitions silently. | context-management.md:36-88 |
| 11 | X-11 | L2-14, L2-5, EP-3/4 | S2 | L2 | No escalation ladder; 26/26 generated agents are opus (no tier headroom); escalations lose failure history; silent retries. | context-tier.md; anti-sycophancy.md:53 |
| 12 | X-12 | TW-10, TW-14 | S3 | L1 | Entry-point/fork contract triplicated across 3 rules; validation checklist duplicated (architect vs quality-validation skill, already drifted). | yaml-frontmatter.md:77; output-structure.md:119; frontmatter-optional-patterns.md:96 |
| 13 | X-13 | L2-8 | S3 | L2 | No batch-sizing rule for generated coordinators: per-item dispatch ≈1.08M tok/day measured in toeic. | agent-writer.md coordinator template |
| 14 | X-14 | L2-18 | S3 | L2 | Code reviewer mandated for non-code teams — mandate silently violated (market-research ships none). | CLAUDE.md:65-66; reviewer-mandate.md |
| 15 | X-15 | L2-19 | S3 | L2 | 3-file evidence-chain worklog replicates into mechanical pipeline phases (30 boilerplate files/day in toeic). | worklog.md:29-31 |
| 16 | X-16 | TW-15, L2-17 | S3 | maint | Codex tree is a drifted hand-rewrite (26–54% smaller, diverges from line 3); generated teams ship 2–3 skill copies with no sync check. | .codex/rules/* |

## Charter amendments proposed (per §5; each gets a case file + Guardian ruling)

- AMD-1 (§5b, from X-1): entry-point skills must instruct the main session to adopt the coordinator playbook instead of spawning the coordinator as a subagent. Evidence: toeic production dead-lock + hand-patch; probe of runtime capabilities.
- AMD-2 (§5c, from X-1): user dialogue happens only in the main session; subagents return NEEDS_CONTEXT question blocks relayed by the coordinator; every exchange appended to `dialogue-log.md`.
- AMD-3 (§5c, from X-14): code reviewer required only for teams whose deliverables include executable artifacts; other teams require a deliverable-QA reviewer instead.
- AMD-4 (§5c, from X-15): generated teams may declare per-phase worklog profiles — decision phases keep the 3-file chain; mechanical phases log one `phase-log.jsonl` line.

## Hygiene notes (out of hardening scope; user decision)

- Stale registered git worktree `.claude/worktrees/dazzling-ellis-43891f` (930,517 B duplicate of the harness at commit 6327257).
- Orphans: `node_modules/` (~63 MB) + `coverage/` (from deleted a-team-draft-system), `teams-index/` (stale 2026-05-02 scan), `local-ai-work-harness/` (generated team misplaced at root), `xxxteam.md` (scratch).
- `teams/` = 51 teams, ~4.15 GB, only `life-partners` git-tracked. *(As of 2026-07-25: 37 directories — 32 Claude teams, 3 Codex mirrors, 1 design blueprint `ducha`, 1 build artifact `teams-index`. `git ls-files teams/` returns 0; `.gitignore:29` excludes them all. The user reviewed this on 2026-07-25 and chose to keep both the ignore rule and `teams-index` as they are.)*
