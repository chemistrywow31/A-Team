# VERIFICATION.md — Fresh-Context Acceptance Evidence (2026-07-03)

Method: every acceptance below was performed per `rules/execution-contract.md` EC-3 — fresh-context verifier agents receiving ONLY acceptance criteria and artifact paths (no producer reasoning), executing checks with commands and citing file:line evidence. Producer self-critique never counted toward acceptance. Full verifier transcripts: `.worklog/202607/a-team-hardening/phase-5-verification/`.

## Verifier reports

| Verifier | Scope | Result | Report |
|----------|-------|--------|--------|
| V1 mechanical (fresh, sonnet) | 14 command-executed checks: template line caps, JSON parses, JUDGMENT format integrity, contract clause presence, byte budget, paths-scoping frontmatter, stale-pattern sweep, architect sections | **14/14 PASS** | phase-5-verification/mechanical-checks.md |
| V2 read-back (fresh, sonnet) | 10-criterion §13 read-back with file:line per criterion | **10/10 PASS** (R10 failed once → fixed → re-verified by fresh micro-check + V2's independent re-read; FAIL history preserved) | phase-5-verification/readback-checks.md |
| V3 lens re-run (fresh, sonnet) | §4 lenses applied to the pass's own output (§12.7) | 4 MATERIAL + 5 minor found → **all closed same-session** (2 accepted with logged rationale) | phase-5-verification/final-lens-audit.md |
| Runtime probe (fresh) | paths-scoped rule injection behavior | STARTUP ABSENT / CONTROL PRESENT / POST-READ PRESENT — scoping mechanism confirmed | phase-2-audit/references.md |
| Haiku advocates ×2 (fresh, haiku) | §6.7 paraphrase-back on contract, JUDGMENT, templates, architect protocol sections | Contract 26/26 clauses unambiguous; 3 ambiguities elsewhere → fixed pre-round-2 | phase-4-adversarial/advocate-*.md |

## §13 done-criteria, item by item

1. **Both layers audited, register complete with file:line** — PASS. AUDIT.md (X-1..X-16 consolidating 49 raw defects: TW-15, FL-9, EP-11, L2-19); V2-R1.
2. **Every merged change survived the adversarial protocol with zero open material objections** — PASS. Round 1: 27 MATERIAL + 9 minor across three bundles → every one revised or rebutted with evidence (2 rebuttals sustained). Round 2 (structural bundle, per §11.5): 11/11 round-1 findings CLOSED, rebuttal accepted, 3 new MATERIAL + 6 minors from the revisions themselves → all closed. Non-structural bundles: one attack round + revision + fresh-context verification (per §11.5, two rounds bind structural changes only). Guardian: zero hidden amendments, zero contract-vs-charter conflicts.
3. **Charter intact except documented §5 amendments; rejects logged** — PASS. AMD-1..4 all APPROVED with independently verified production evidence (guardian-rulings.md); 5 rejected proposals logged with reasons (CHANGELOG.md); V2-R6/R7.
4. **§7.1–7.5 in the canonical RULES file, restated at points of use, no {{slots}}** — PASS. `.claude/rules/execution-contract.md` EC-1.1–EC-5.4 (V1-M6); restatements verified in context-management.md, team-architect.md, CLAUDE.md, all templates (V1-M10, V2-R2/R3); zero placeholders (V2-R2).
5. **JUDGMENT.md: five areas, exactly one positive + one negative per criterion, cold read passed** — PASS. 20 criteria × exactly one SIGNAL/ACTION/POSITIVE/NEGATIVE (V1-M5); five areas + same-error-class signal (V2-R4); haiku cold-read paraphrase-back passed with fixes applied (advocate-judgment.md).
6. **Five templates, each ≤60 lines with filled example, citing §7.1/§7.2/§7.3 + JUDGMENT by number** — PASS. V1-M1/M2/M3; V2-R5.
7. **Always-loaded tokens ≤ original, or justified line-by-line** — PASS with margin: 48,243 B vs 82,200 B baseline (−41%), measured by fresh verifier (V1-M7); the contract's own additions justified in CHANGELOG token accounting.
8. **VERIFICATION.md shows fresh-context acceptance per deliverable** — this file.
9. **§4 lenses re-run on own output, findings closed** — PASS. V3: 9 findings → 7 fixed, 2 accepted with rationale (CHANGELOG follow-ups + accepted-duplication note); closure evidence in phase-5-verification/findings.md.

## Residual items (documented, out of this pass's scope)

- 51 pre-existing generated teams predate the hardening (no version stamps; market-research remains AMD-3 non-compliant) — retrofit path: `/A-Team --restructure teams/{name}`.
- Codex tree parity beyond the contract mirror (drifted hand-condensed rules) — follow-up in CHANGELOG.
- Re-run the paths-scoping probe after Claude Code upgrades (the ~113k tok/run saving rests on verified-today runtime behavior).

## Process disclosure

The first adversary/guardian wave (4 top-tier agents in parallel) hit a platform session limit after completing reads but before writing outputs; all four were re-run sequentially on sonnet with write-early instructions and completed fully. Haiku-tier agents were unaffected throughout. Disclosed in CHANGELOG.md.
