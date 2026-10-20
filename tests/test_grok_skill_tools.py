#!/usr/bin/env python3
"""Native skill regressions: local fixtures only, no model calls or global writes.

Source-shaped events: official xai-org/grok-build commit
2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8,
crates/codegen/xai-grok-pager/src/headless/reducer/acp.rs:29-112,124-141,185-204;
xai-grok-tools/src/implementations/grok_build/read_file/mod.rs:132-138.
Installed 1.0.62 --help corroborates --single, --prompt-file, streaming-json,
--max-turns. These are command/parser fixtures, not observed paid sessions.
"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".grok/skills"
CREATOR = SKILLS / "skill-creator"
SCRATCH = ROOT / ".worklog/202610/grok-native-branch/phase-2-generation/skill_writer/fixtures"
sys.path.insert(0, str(CREATOR))
from scripts.utils import grok_command, parse_native_stream, parse_skill_md
from scripts.quick_validate import validate_skill
from scripts.package_skill import package_skill
from scripts.run_eval import require_discovered_skill, run_eval, run_single_query, validate_eval_set
from scripts.run_loop import split_eval_set, run_loop
from scripts.improve_description import improve_description, _call_grok
from scripts.aggregate_benchmark import load_run_results, aggregate_results, generate_benchmark


def stream(*events):
    return "\n".join(json.dumps(e) for e in events)


def read_event(path, call_id="read-1", status="pending"):
    return {"type": "tool_call", "toolCallId": call_id, "title": "Read file",
            "kind": "read", "status": status, "toolName": "read_file",
            "rawInput": {"target_file": str(path)}, "content": [], "locations": []}


END = {"type": "end", "stopReason": "end_turn", "sessionId": "fixture", "requestId": "fixture"}
DONE = {"type": "tool_call_update", "toolCallId": "read-1", "status": "completed",
        "content": [], "rawOutput": {}, "locations": []}


class SkillToolTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="skills-", dir=SCRATCH)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "fixture-skill"
        self.skill.mkdir()
        (self.skill / "SKILL.md").write_text('---\nname: fixture-skill\ndescription: |\n  Summarize: preserve café and # signs.\n---\n\n# Fixture\n\nDo the task.\n')

    def test_all_eleven_native_skills_validate_and_entry_adopts_main(self):
        files = list(SKILLS.glob("*/SKILL.md"))
        self.assertEqual(len(files), 11)
        for p in files:
            with self.subTest(skill=p.parent.name):
                self.assertTrue(validate_skill(p.parent)[0], validate_skill(p.parent))
        entry = (SKILLS / "a-team/SKILL.md").read_text()
        self.assertIn("current main session", entry)
        self.assertIn("not a request to spawn", entry)
        self.assertIn(".grok/agents/team-architect.md", entry)

    def test_yaml_real_parser_preserves_multiline_unicode(self):
        self.assertTrue(validate_skill(self.skill)[0])
        name, description, _ = parse_skill_md(self.skill)
        self.assertEqual(name, "fixture-skill")
        self.assertIn("café and # signs", description)

    def test_validation_rejects_empty_duplicate_ignored_unknown_and_wrong_type(self):
        invalid = [
            'name: ""\ndescription: x',
            'name: fixture-skill\ndescription: " "',
            'name: fixture-skill\nname: other\ndescription: x',
            'name: fixture-skill\ndescription: x\nmodel: inherit',
            'name: fixture-skill\ndescription: x\neffort: high',
            'name: fixture-skill\ndescription: x\nallowed-tools: [Task]',
            'name: fixture-skill\ndescription: x\nmade_up: true',
            'name: fixture-skill\ndescription: x\nuser-invocable: "false"',
            'name: other-folder\ndescription: x',
        ]
        for metadata in invalid:
            with self.subTest(metadata=metadata):
                (self.skill / "SKILL.md").write_text(f"---\n{metadata}\n---\n# Fixture\nDo work.\n")
                self.assertFalse(validate_skill(self.skill)[0])

    def test_metadata_requires_string_pairs_and_packaging_rejects_malformed(self):
        skill_md = self.skill / "SKILL.md"
        prefix = "---\nname: fixture-skill\ndescription: Useful fixture\n"
        suffix = "\n---\n\n# Fixture\n\nDo the task.\n"
        for metadata in ('metadata: {}', 'metadata: {author: "Example", version: "1", note: "café"}'):
            with self.subTest(valid=metadata):
                skill_md.write_text(prefix + metadata + suffix)
                self.assertTrue(validate_skill(self.skill)[0], validate_skill(self.skill))
        malformed = (
            'metadata: {author: [invalid, list]}',
            'metadata: {author: {nested: value}}',
            'metadata: {version: 1}',
            'metadata: {enabled: true}',
            'metadata: {author: null}',
            'metadata: {1: author}',
            'metadata: [author, version]',
        )
        for metadata in malformed:
            with self.subTest(invalid=metadata):
                skill_md.write_text(prefix + metadata + suffix)
                self.assertFalse(validate_skill(self.skill)[0])
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertIsNone(package_skill(self.skill, self.root / "dist"))
                self.assertFalse((self.root / "dist/fixture-skill.skill").exists())

    def test_package_retains_assets_license_and_excludes_evaluations_cache(self):
        for rel in ["scripts/helper.py", "references/schema.md", "assets/template.txt", "LICENSE.txt", "evals/evals.json", "__pycache__/junk.pyc"]:
            p = self.skill / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("fixture")
        with contextlib.redirect_stdout(io.StringIO()):
            result = package_skill(self.skill, self.root / "dist")
        self.assertIsNotNone(result)
        with zipfile.ZipFile(result) as archive:
            names = archive.namelist()
            self.assertIn("fixture-skill/scripts/helper.py", names)
            self.assertIn("fixture-skill/references/schema.md", names)
            self.assertIn("fixture-skill/assets/template.txt", names)
            self.assertIn("fixture-skill/LICENSE.txt", names)
            self.assertFalse(any("evals/" in n or "__pycache__" in n for n in names))
            self.assertTrue(all(not Path(n).is_absolute() and ".." not in Path(n).parts for n in names))

    def test_package_rejects_symlink_and_bad_frontmatter(self):
        external = self.root / "external.txt"
        external.write_text("not a resource")
        (self.skill / "linked.txt").symlink_to(external)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(package_skill(self.skill, self.root / "dist"))
        (self.skill / "linked.txt").unlink()
        (self.skill / "SKILL.md").write_text("No metadata")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(package_skill(self.skill, self.root / "dist"))

    def test_package_inside_skill_does_not_embed_itself(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = package_skill(self.skill, self.skill)
        with zipfile.ZipFile(result) as archive:
            self.assertNotIn("fixture-skill/fixture-skill.skill", archive.namelist())

    def test_command_uses_actual_grok_flags_without_permission_overrides(self):
        query = "summarize $HOME; `literal`"
        cmd = grok_command(query=query, model="test-model", binary="/installed/grok")
        self.assertEqual(cmd, ["/installed/grok", "--single", query, "--output-format", "streaming-json", "--max-turns", "4", "--model", "test-model"])
        prompt = grok_command(prompt_file=self.root / "prompt.txt", max_turns=1)
        self.assertIn("--prompt-file", prompt)
        self.assertFalse(any(x in prompt for x in ("--trust", "--always-approve", "--permission-mode", "--include-partial-messages")))
        with self.assertRaises(ValueError):
            grok_command(query="x", prompt_file=Path("p"))

    def test_native_completed_exact_read_and_relative_path(self):
        skill_file = self.skill / "SKILL.md"
        events = stream({"type": "thought", "data": "not parsed as output"},
                        read_event(skill_file), DONE, {"type": "text", "data": "done"}, END)
        parsed = parse_native_stream(events, skill_file, self.root)
        self.assertTrue(parsed["triggered"])
        self.assertEqual(parsed["text"], "done")
        self.assertTrue(parse_native_stream(stream(read_event("fixture-skill/SKILL.md"), DONE, END), skill_file, self.root)["triggered"])

    def test_mentions_lookalike_paths_and_uncompleted_reads_do_not_trigger(self):
        expected = self.skill / "SKILL.md"
        for events in [stream({"type": "text", "data": str(expected)}, END),
                       stream(read_event(str(expected) + ".backup"), DONE, END),
                       stream(read_event(expected), END)]:
            self.assertFalse(parse_native_stream(events, expected, self.root)["triggered"])

    def test_native_errors_incomplete_and_foreign_events_are_unverified(self):
        bad = [stream({"type": "error", "message": "unavailable"}),
               stream({"type": "max_turns_reached"}, END),
               stream({"type": "end", "stopReason": "max_turns"}),
               stream(read_event(self.skill / "SKILL.md")),
               stream({"type": "stream_event", "event": {"type": "content_block_start"}}, END),
               stream({"type": "unknown_future_tool_event"}, END),
               stream({**DONE, "status": "failed"}, END), "not-json"]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                parse_native_stream(value, self.skill / "SKILL.md", self.root)

    def test_single_query_subprocess_is_native_and_nonzero_is_error(self):
        fake = subprocess.CompletedProcess([], 0, stream(read_event(self.skill / "SKILL.md"), DONE, END), "")
        with patch("scripts.run_eval.subprocess.run", return_value=fake) as run:
            self.assertTrue(run_single_query("query", self.skill / "SKILL.md", 5, self.root))
            self.assertEqual(run.call_args.args[0][1:3], ["--single", "query"])
            self.assertNotIn("shell", run.call_args.kwargs)
        with patch("scripts.run_eval.subprocess.run", return_value=subprocess.CompletedProcess([], 1, "", "auth unavailable")):
            with self.assertRaises(RuntimeError):
                run_single_query("q", self.skill / "SKILL.md", 5, self.root)

    def test_inspect_rejects_untrusted_missing_and_wrong_source(self):
        for report in [{"projectTrusted": False}, {"projectTrusted": True, "projectRoot": str(self.root), "skills": []},
                       {"projectTrusted": True, "projectRoot": str(self.root), "skills": [{"name": "fixture-skill", "source": {"path": "/wrong/SKILL.md"}}]}]:
            with patch("scripts.run_eval.subprocess.run", return_value=subprocess.CompletedProcess([], 0, json.dumps(report), "")):
                with self.assertRaises(RuntimeError):
                    require_discovered_skill(self.root, "fixture-skill", self.skill / "SKILL.md")

    def test_eval_opt_in_and_invalid_sets_make_no_process_calls(self):
        with patch("scripts.run_eval.subprocess.run") as run:
            with self.assertRaises(ValueError):
                run_eval([{"query": "x", "should_trigger": True}], "x", "d", 1, 5, self.root)
            run.assert_not_called()
        for rows in [[], [{"query": "x", "should_trigger": "false"}], [{"query": "x", "should_trigger": True}] * 2]:
            with self.assertRaises(ValueError):
                validate_eval_set(rows)

    def test_evaluation_failure_cannot_pass_a_negative_case_and_proxy_cleanup(self):
        (self.root / ".git").mkdir()
        (self.root / ".grok").mkdir()
        with patch("scripts.run_eval.require_discovered_skill"), patch("scripts.run_eval.run_single_query", side_effect=RuntimeError("permission unavailable")):
            result = run_eval([{"query": "near miss", "should_trigger": False}], "fixture-skill", "description", 1, 5, self.root, allow_model_calls=True)
        self.assertFalse(result["results"][0]["pass"])
        self.assertEqual(result["results"][0]["status"], "UNVERIFIED")
        self.assertEqual(result["summary"]["unverified"], 1)
        self.assertEqual(list((self.root / ".grok/skills").iterdir()), [])

    def test_holdout_nonempty_disjoint_and_too_small_rejected(self):
        cases = [{"query": f"q{i}", "should_trigger": i % 2 == 0} for i in range(8)]
        train, held = split_eval_set(cases, 0.4)
        self.assertTrue(train and held)
        self.assertFalse({r["query"] for r in train} & {r["query"] for r in held})
        with self.assertRaises(ValueError):
            split_eval_set(cases[:2], 0.4)

    def test_improvement_uses_prompt_file_and_native_text(self):
        with patch("scripts.improve_description.subprocess.run", return_value=subprocess.CompletedProcess([], 0, stream({"type": "text", "data": "new description"}, END), "")) as run:
            self.assertEqual(_call_grok("large prompt", None), "new description")
            self.assertIn("--prompt-file", run.call_args.args[0])
            self.assertNotIn("input", run.call_args.kwargs)
        with self.assertRaises(ValueError):
            improve_description("n", "c", "d", {"results": []}, [], "m")

    def test_unknown_tokens_do_not_become_output_characters(self):
        run_dir = self.root / "eval-1" / "with_skill" / "run-1"
        run_dir.mkdir(parents=True)
        (run_dir / "grading.json").write_text(json.dumps({"summary": {"pass_rate": 1, "passed": 1, "failed": 0, "total": 1}, "expectations": [], "execution_metrics": {"output_chars": 12000}}))
        results = load_run_results(self.root)
        self.assertIsNone(results["with_skill"][0]["tokens"])
        self.assertIsNone(aggregate_results(results)["with_skill"]["tokens"])
        self.assertEqual(aggregate_results(results)["delta"]["tokens"], "NOT_OBSERVED")
        self.assertIsNone(aggregate_results(results)["with_skill"]["time_seconds"])
        benchmark = generate_benchmark(self.root)
        self.assertEqual(benchmark["metadata"]["runs_per_configuration"], 1)
        self.assertEqual(benchmark["metadata"]["executor_model"], "NOT_OBSERVED")

    def test_successful_eval_and_inspect_contract(self):
        (self.root / ".git").mkdir()
        (self.root / ".grok").mkdir()
        report = {"projectTrusted": True, "projectRoot": str(self.root), "skills": [
            {"name": "fixture-skill", "source": {"path": str(self.skill / "SKILL.md")}}]}
        with patch("scripts.run_eval.subprocess.run", return_value=subprocess.CompletedProcess([], 0, json.dumps(report), "")):
            require_discovered_skill(self.root, "fixture-skill", self.skill / "SKILL.md")
        rows = [{"query": "relevant", "should_trigger": True}, {"query": "near miss", "should_trigger": False}]
        with patch("scripts.run_eval.require_discovered_skill"), patch("scripts.run_eval.run_single_query", side_effect=lambda q, *a: q == "relevant"):
            result = run_eval(rows, "fixture-skill", "description", 1, 5, self.root, allow_model_calls=True)
        self.assertEqual(result["summary"]["passed"], 2)
        self.assertEqual(result["summary"]["unverified"], 0)

    def test_loop_stops_on_unverified_and_preserves_heldout_blinding(self):
        rows = [{"query": f"q{i}", "should_trigger": i % 2 == 0} for i in range(8)]
        kwargs = dict(eval_set=rows, skill_path=self.skill, description_override=None,
                      num_workers=1, timeout=5, max_iterations=2, runs_per_query=1,
                      trigger_threshold=0.5, holdout=0.4, model="fixture-model", verbose=False,
                      project_root=self.root, allow_model_calls=True)
        with patch("scripts.run_loop.run_eval", return_value={"summary": {"unverified": 1}}), patch("scripts.run_loop.improve_description") as improve:
            with self.assertRaises(RuntimeError):
                run_loop(**kwargs)
            improve.assert_not_called()
        def measured(**arguments):
            return {"summary": {"unverified": 0}, "results": [
                {**r, "pass": arguments["description"] == "improved", "triggers": 0, "runs": 1, "status": "MEASURED"}
                for r in arguments["eval_set"]]}
        with patch("scripts.run_loop.run_eval", side_effect=measured), patch("scripts.run_loop.improve_description", return_value="improved") as improve:
            result = run_loop(**kwargs)
            self.assertEqual(result["best_description"], "improved")
            history = improve.call_args.kwargs["history"]
            self.assertFalse(any(k.startswith("test_") for h in history for k in h))
            _, held = split_eval_set(rows, 0.4)
            self.assertFalse({r["query"] for r in held} & {r["query"] for r in improve.call_args.kwargs["eval_results"]["results"]})


    def test_retained_viewer_builds_static_artifact(self):
        run_dir = self.root / "eval-1" / "with_skill" / "run-1"
        (run_dir / "outputs").mkdir(parents=True)
        (run_dir / "outputs/result.txt").write_text("Useful fixture output")
        (self.root / "eval-1/eval_metadata.json").write_text(json.dumps({"eval_id": 1, "eval_name": "example", "prompt": "Do the fixture", "assertions": []}))
        result = subprocess.run([sys.executable, "-B", str(CREATOR / "eval-viewer/generate_review.py"), str(self.root), "--skill-name", "fixture-skill", "--static", str(self.root / "review.html")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fixture-skill", (self.root / "review.html").read_text())


if __name__ == "__main__":
    unittest.main()
