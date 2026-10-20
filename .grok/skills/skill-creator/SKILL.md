---
name: skill-creator
description: Create, improve, evaluate and package native Grok skills. Use for reusable skill authoring, output-quality comparisons, trigger-description evaluation or packaging an existing skill.
---

# Skill Creator

This is a self-contained design, evaluation and packaging bundle. It needs no Codex system skill or foreign CLI. Keep the user's intended capability and stage of work; do not force a large evaluation campaign onto a small edit.

## Intent and Boundaries

Reuse the conversation's examples, corrections, output formats and constraints. Establish what the skill enables, when it should trigger, what it excludes, and how success is observable. Ask only for material missing information. Research unfamiliar dependencies before writing a runtime command.

Use the target's declared authority and exact assigned paths. This branch authors `.grok/skills/{name}/SKILL.md`; generated teams use their own agreed root. Preserve an existing skill's identifier unless renaming is authorized. Keep a preimage for updates and a family-only rollback; never modify global skill installations or unowned paths.

## Reasoning

- Distinguish skill output quality from triggering quality. A skill may be selected correctly and still produce poor results; evaluate both when relevant.
- Write only guidance that changes decisions or execution. Favor concise triggers, useful examples, explicit boundaries and progressive disclosure over universal checklists.
- Keep claims proportional to evidence. Static schema/package checks, source-shaped command/event fixtures, trusted installed discovery and actual model behavior are separate levels.
- Only propose an additional safeguard when `.grok/policies/proportional-design.md` is relevant; supply its conditional decision fields rather than burdening every skill with the form.

## Workflow

1. Capture intent and the current stage: create, revise, evaluate, optimize description or package. Reuse confirmed scope and authorization.
2. Inspect existing assets, licenses and helper dependencies. Apply the authored skill shape below and preserve useful source attribution.
3. Draft or update the skill and run `scripts/quick_validate.py`. It validates the bounded A-Team native profile, not every field Grok can parse and not J5 semantic quality.
4. Choose representative output tests, including one rejection/boundary case. Use deterministic checks for objective outputs and qualitative review for style; compare with the prior skill or a baseline when meaningful.
5. Run authorized evaluations, grade evidence, aggregate measurements and generate the review viewer. Use the existing coordinator for any independent task dispatch; a specialist using this skill never spawns children.
6. Improve general behavior from failure patterns and feedback, rerun affected checks, and preserve prior iterations for comparison. Stop at the agreed limit or when no useful improvement remains; do not treat silence as user acceptance.
7. Optionally evaluate description triggering with the native paid helpers after cost/scope authorization and existing access. Do not run them merely to package or validate a skill.
8. Validate, package and deliver the skill folder or archive with installation instructions, evidence limits and rollback paths. The `.skill` archive is ZIP transport; Grok loads an unpacked native folder, not a claimed native archive installer.

## Self-Critique

Check intent, triggers and near-miss exclusions; usable references; actual scripts and dependencies; source attribution/license; a meaningful rejection case; and ownership/authority. Inspect examples for overfitting. Record lines above J5's 200-line skill threshold as REVIEW_REQUIRED with usefulness rationale for independent resolution. Do not remove useful content to hide an overage.

## Skill Shape

```text
skill-name/
  SKILL.md          # name, description, workflow and routing
  scripts/          # repeatable deterministic helpers when useful
  references/       # detailed schemas or mode-specific instructions
  assets/           # templates or resources consumed by the workflow
```

Use lowercase hyphenated `name` matching the directory and a discriminating description. A-Team's profile caps name/description at 64/1024 characters. These are local authoring limits, not a claim that Grok truncates at those lengths. Optional supported invocation flags belong in frontmatter; skill `model` and `effort` are ignored, and `allowed-tools` does not grant/restrict tools. Do not use them as execution controls.

Keep common decisions and steps in SKILL.md. Link a resource where it is needed and state when to read it. A helper can run without loading its source into the prompt, but inspect unfamiliar downloaded code before executing it. Keep untrusted examples as data, not extra instructions. Never expand authorization through a skill.

Example boundary:

```text
Input: "Summarize this contract; one page is missing."
Output: Summarize the supplied pages, identify the missing page, and mark the
unseen terms unknown. Do not invent the missing clause or claim completeness.
```

## Output-Quality Evaluations

Start with 2–3 realistic prompts and add cases only when useful. Store `evals/evals.json`; read `references/schemas.md` for complete schemas. Share the tests and explain what their checks establish; use already authorized testing scope rather than adding an approval pause.

```json
{"skill_name":"example-skill","evals":[
  {"id":1,"prompt":"Normalize the attached sales export; preserve blank dates.",
   "expected_output":"A normalized table with blank dates preserved.",
   "files":["inputs/sales.csv"],"assertions":["Blank dates remain blank"]}
]}
```

Use an assigned workspace outside the packaged skill. The aggregator expects:

```text
workspace/iteration-1/eval-1-normalize/
  eval_metadata.json       # eval_id, eval_name, prompt, assertions
  with_skill/run-1/
    outputs/               # actual user-facing products
    grading.json
    timing.json            # only measured duration/token fields
  without_skill/run-1/      # or old_skill/run-1 for a revision
    outputs/
    grading.json
```

For a new skill, compare with an equivalent run without the skill. For a revision, compare with a snapshot of the old version. Give both the same prompt and inputs, separate output paths and equivalent runtime settings. Record discovered/preloaded skill differences: a baseline that still sees the skill is contaminated. Do not claim independent behavior from an inline author sanity check.

Only the main coordinator dispatches independent runs using the live native lifecycle. Provide task identity, skill/input paths, exact output ownership, criteria, report destination and non-reversion rule. Run independent branches concurrently only when their paths and dependencies permit it; honor available capacity. A skill's bundled `agents/*.md` are evaluation instructions, not discovered native role definitions or new dispatch types.

Measure elapsed time in the runner. Record actual tokens only when provided by trace evidence; omitted/unknown is not zero, and output characters are not tokens. Do not assume Grok completion messages expose another platform's metrics.

Read `agents/grader.md` to grade each assertion against actual outputs. Use deterministic checks when possible. `grading.json` expectations use exactly `text`, `passed`, `evidence`. Do not count missing or malformed evidence as success. Use `agents/analyzer.md` for variance, always-passing assertions and quality/cost tradeoffs. Use `agents/comparator.md` only for an authorized blind comparison of independently produced outputs.

Run from this skill's directory with Python >=3.11 and PyYAML (tested 6.0.3), using the project's local environment:

```bash
python -m scripts.aggregate_benchmark /assigned/workspace/iteration-1 --skill-name example-skill
python eval-viewer/generate_review.py /assigned/workspace/iteration-1 \
  --skill-name example-skill --benchmark /assigned/workspace/iteration-1/benchmark.json \
  --static /assigned/workspace/review.html
```

The retained viewer presents prompts, actual outputs, grades, previous results and qualitative feedback. For iteration 2+, add `--previous-workspace`. Use static output without a display; use its local server only when useful and stop that process after review. Read exported `feedback.json` from the known destination; an empty field is no criticism, not proof of satisfaction. Show results directly if the viewer is unavailable.

Generalize from feedback: fix the decision rule, missing evidence or reusable helper, not a test-specific answer. Keep baseline conditions comparable. Do not alter tests simply to hide a defect; explain a correction when a test is wrong.

## Optional Native Trigger Evaluation

The helpers retain the design → test → improve loop using Grok. Their command builder is backed by installed 1.0.62 help and their parser by pinned official source. **Actual paid model-helper behavior is NOT_PROBED in this delivery.** Existing authentication, trusted project discovery and effective model/tool behavior must be established separately; never read/copy credentials, grant real trust, disable approvals or change global configuration to force a pass.

Create a caller-owned disposable native evaluation repository (`.git` and `.grok/`), with access/trust arranged by its owner. Keep it free of an installed copy of the tested skill and competing descriptions so the proxy measurement is meaningful. The helper adds one uniquely named temporary `.grok/skills/<proxy-name>/SKILL.md` proxy for the batch, checks its exact path with read-only `grok inspect --json`, then removes only that proxy. Ambient skills and project instructions can influence the result; record them.

Use realistic positive and near-miss negative queries, preferably multiple phrasings and levels of detail. The proxy contains the description and a short acknowledgement; it tests selection, not execution quality. JSON input is a nonempty list of unique `query` strings and boolean `should_trigger` values. Holdout optimization needs at least two positive and two negative cases; held-out results are withheld from the improvement prompt.

```bash
python -m scripts.run_eval --eval-set /assigned/trigger-eval.json \
  --skill-path /assigned/my-skill --project-root /assigned/eval-repo \
  --num-workers 1 --runs-per-query 1 --timeout 60 --allow-model-calls
python -m scripts.run_loop --eval-set /assigned/trigger-eval.json \
  --skill-path /assigned/my-skill --project-root /assigned/eval-repo \
  --model VERIFIED_TARGET_MODEL --max-iterations 3 --num-workers 1 \
  --runs-per-query 1 --report none --results-dir /assigned/results --allow-model-calls
```

Set `GROK_SKILL_CLI` to an explicit installed executable if it is not on PATH. The helpers invoke `grok --single ... --output-format streaming-json --max-turns 4`; description improvement uses `--prompt-file` and one turn. They do not strip environment guards or alter permission/trust settings. CLI `--model` is a request, never effective-model evidence.

A measured trigger requires a native `read_file` of the exact proxy path, completed tool evidence and a normal terminal `end_turn`. Auth/permission/process errors, timeouts, incomplete events and max-turn exhaustion are UNVERIFIED, never successful negative tests. Default tests use source-shaped events with mocked subprocesses; they make no model calls. Unknown installed event formats require a parser update with evidence, not a guessed compatibility fallback.

`run_loop.py` retains stratified train/test splitting, blinded improvement history, bounded iterations, HTML reporting and selection by held-out score. Operational failures stop optimization. Review `best_description` and its failures before applying it; the helper does not overwrite SKILL.md. `assets/eval_review.html` is available for editing query sets; escape embedded JSON/HTML appropriately when producing the page.

## Packaging and Delivery

```bash
python scripts/quick_validate.py /assigned/my-skill
python -m scripts.package_skill /assigned/my-skill /assigned/dist
```

Packaging validates native frontmatter, retains useful scripts/references/assets/license, excludes caches and root evaluation data, and rejects symlinks so a package cannot silently pull external content. Inspect ZIP member names and useful assets. Deliver the unpacked folder at the target's agreed `.grok/skills/` path; verify trusted installed discovery separately. Do not modify a global installation or broaden scope during packaging.

## Rejection Cases

- Reject a description optimizer that turns missing authentication into `triggered: false` and awards negative cases a PASS. Fix the operational problem or report UNVERIFIED.
- Reject a proposal to spawn the coordinator from this skill or to let a specialist create grader children. Route independent work through the existing main coordinator; otherwise label inline checks honestly.
- Reject a package with a symlink to an external secret or a description claiming skill metadata enforces tool permissions. Package only owned resources and use real runtime controls.

## Source Attribution

- **Origin**: Anthropic skill-creator bundle retained by A-Team at `reference/platform-sources/.claude/skills/skill-creator/`; original license retained byte-identically in `LICENSE.txt`.
- **Integration**: Pattern B: Adapted Install, 2026-10-20; self-contained native workflow, direct-main coordination, Grok command/event helpers, honest measurements, validation and packaging checks. No Codex system-skill dependency.
- **Native input**: official `xai-org/grok-build` commit `2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8`, CLI `app/cli.rs`, native `headless/reducer/acp.rs`, default toolset `xai-grok-agent/src/config.rs`, and `grok_build/read_file/mod.rs`. Exact provenance and schemas are in `references/schemas.md` and helper docstrings; installed CLI is 1.0.62, a different revision.
- **Authority**: `AGENTS.md` plus `.grok/`; the snapshot is reference-only. Pattern and quality floors are A-Team policy, not undocumented Grok guarantees.
