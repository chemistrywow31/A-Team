#!/usr/bin/env python3
"""Portable preflight regressions with hand-built installed-inspect fixtures."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

import test_validate_grok_team as fixtures
from test_validate_grok_team import REPO_ROOT, validator, write


class PreflightTests(unittest.TestCase):
    setUp = fixtures.NativeContractTests.setUp
    tearDown = fixtures.NativeContractTests.tearDown

    def evidence(self):
        # Installed contract: inspect exposes identity/source, no effective tools,
        # model, effort, context, or permission enforcement evidence.
        return {"grokVersion": "1.0.62", "projectRoot": str(self.root), "projectTrusted": True,
                "agents": [{"name": name, "description": "fixture", "source": {"type": "project", "path": str(self.root / f".grok/agents/{name}.md")}} for name in ("coordinator", "checker")],
                "skills": [{"name": "check", "source": {"type": "project", "path": str(self.root / ".grok/skills/check/SKILL.md")}}],
                "projectInstructions": [{"path": str(self.root / p), "scope": "project"} for p in ("AGENTS.md", ".grok/rules/core.md")]}

    def binary(self, evidence=None, exit_code=0):
        # Emits inspect fixture only. Captures argv/cwd/env to prove the wrapper
        # preserves process state and does not pass --trust or a model prompt.
        path = Path(self.temp.name) / "fake grok"
        record = Path(self.temp.name) / "invocation.json"
        payload = json.dumps(evidence if evidence is not None else self.evidence())
        script = f'''#!{sys.executable}
import json, os, pathlib, sys
pathlib.Path({str(record)!r}).write_text(json.dumps({{"argv":sys.argv[1:],"cwd":os.getcwd(),"grok_home":os.environ.get("GROK_HOME")}}))
print({payload!r})
raise SystemExit({exit_code})
'''
        path.write_text(script); path.chmod(0o755)
        return path, record

    def test_explicit_root_from_arbitrary_cwd_and_python_override(self):
        binary, record = self.binary()
        home = Path(self.temp.name) / "isolated-home"
        home.mkdir(); sentinel = write(home, "config.toml", "# unchanged fixture\n")
        env = {**os.environ, "PYTHON": sys.executable, "GROK_HOME": str(home)}
        process = subprocess.run(["bash", str(REPO_ROOT / "scripts/preflight-grok-runtime.sh"), str(self.root), "--grok-bin", str(binary), "--json"], cwd=home, env=env, capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
        report = json.loads(process.stdout)
        self.assertEqual(report["status"], "DISCOVERY_READY")
        self.assertEqual(report["effective_runtime"], "UNVERIFIED")
        self.assertEqual(report["model_access"], "NOT_PROBED")
        call = json.loads(record.read_text())
        self.assertEqual(call["argv"], ["inspect", "--json"])
        self.assertEqual(Path(call["cwd"]), self.root)
        self.assertEqual(call["grok_home"], str(home))
        self.assertEqual(sentinel.read_text(), "# unchanged fixture\n")
        self.assertEqual(sorted(p.name for p in home.iterdir()), ["config.toml"])

    def test_validate_wrapper_from_arbitrary_cwd(self):
        process = subprocess.run(["bash", str(REPO_ROOT / "scripts/validate-team.sh"), str(self.root), "--json"], cwd=self.temp.name, env={**os.environ, "PYTHON": sys.executable}, capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
        self.assertEqual(json.loads(process.stdout)["status"], "STATIC_VALID")

    def test_missing_binary_is_distinct_without_running_any_command(self):
        with mock.patch.object(validator.subprocess, "run", side_effect=AssertionError("must not execute")):
            code, report = validator.preflight(self.root, grok_bin=str(self.root / "missing-grok"))
        self.assertEqual((code, report["status"]), (2, "MISSING_BINARY"))

    def test_unknown_metadata_fails_before_inspect_permissive_loader(self):
        p = self.root / ".grok/agents/checker.md"
        p.write_text(p.read_text().replace("name: checker", "name: checker\nmax_turns: 0"))
        with mock.patch.object(validator.subprocess, "run", side_effect=AssertionError("must validate before inspect")):
            code, report = validator.preflight(self.root, grok_bin="unused")
        self.assertEqual((code, report["status"]), (1, "INVALID_METADATA"))

    def test_untrusted_is_distinct_and_never_auto_grants_trust(self):
        evidence = self.evidence(); evidence["projectTrusted"] = False
        evidence["skills"] = []; evidence["projectInstructions"] = []
        binary, record = self.binary(evidence)
        code, report = validator.preflight(self.root, grok_bin=str(binary))
        self.assertEqual((code, report["status"]), (3, "UNTRUSTED_PROJECT"))
        self.assertEqual(json.loads(record.read_text())["argv"], ["inspect", "--json"])

    def test_inspect_failure_does_not_guess_authentication_failure(self):
        binary, _ = self.binary(exit_code=9)
        code, report = validator.preflight(self.root, grok_bin=str(binary))
        self.assertEqual((code, report["status"]), (5, "INSPECT_UNAVAILABLE"))
        self.assertEqual(report["model_access"], "NOT_PROBED")
        self.assertEqual(report["inspect_exit_code"], 9)

    def test_missing_role_even_zero_inspect_exit_is_not_a_pass(self):
        evidence = self.evidence(); evidence["agents"].pop()
        binary, _ = self.binary(evidence)
        code, report = validator.preflight(self.root, grok_bin=str(binary))
        self.assertEqual((code, report["status"]), (4, "DISCOVERY_MISMATCH"))
        self.assertIn("missing agents", report["diagnostic"])

    def test_wrong_source_or_same_name_user_override_is_not_native_pass(self):
        evidence = self.evidence()
        evidence["agents"][0]["source"] = {"type": "user", "path": str(self.root / ".grok/agents/coordinator.md")}
        binary, _ = self.binary(evidence)
        code, report = validator.preflight(self.root, grok_bin=str(binary))
        self.assertEqual((code, report["status"]), (4, "DISCOVERY_MISMATCH"))
        self.assertIn("wrong source", report["diagnostic"])

    def test_foreign_project_agent_and_instruction_are_not_ambient(self):
        for field, item in (("agents", {"name": "foreign", "source": {"type": "project", "path": str(self.root / ".claude/agents/foreign.md")}}),
                            ("projectInstructions", {"scope": "project", "path": str(self.root / "CLAUDE.md")})):
            with self.subTest(field=field):
                evidence = self.evidence(); evidence[field].append(item)
                binary, _ = self.binary(evidence)
                code, report = validator.preflight(self.root, grok_bin=str(binary))
                self.assertEqual((code, report["status"]), (4, "DISCOVERY_MISMATCH"))

    def test_user_sources_reported_separately_without_changing_them(self):
        evidence = self.evidence()
        evidence["agents"].append({"name": "user-helper", "source": {"type": "user", "path": "/fixture-user/agents/helper.md"}})
        binary, _ = self.binary(evidence)
        code, report = validator.preflight(self.root, grok_bin=str(binary))
        self.assertEqual(code, 0)
        self.assertEqual(report["ambient_sources"]["agents"][0]["name"], "user-helper")

    def test_missing_rule_and_wrong_root_fail(self):
        for mutation in ("rule", "root"):
            with self.subTest(mutation=mutation):
                evidence = self.evidence()
                if mutation == "rule": evidence["projectInstructions"].pop()
                else: evidence["projectRoot"] = str(self.root.parent)
                binary, _ = self.binary(evidence)
                code, report = validator.preflight(self.root, grok_bin=str(binary))
                self.assertEqual((code, report["status"]), (4, "DISCOVERY_MISMATCH"))

    def test_inspect_cannot_upgrade_fabricated_model_tool_claims(self):
        evidence = self.evidence()
        evidence["effectiveTools"] = ["Task"]
        evidence["effectiveModel"] = "made-up-observation"
        binary, _ = self.binary(evidence)
        code, report = validator.preflight(self.root, grok_bin=str(binary))
        self.assertEqual(code, 0)
        self.assertEqual(report["effective_runtime"], "UNVERIFIED")
        self.assertEqual(report["model_access"], "NOT_PROBED")

    def test_malformed_output_returns_probe_unavailable(self):
        binary = Path(self.temp.name) / "broken-grok"
        binary.write_text("#!/bin/sh\nprintf 'not JSON'\n"); binary.chmod(0o755)
        code, report = validator.preflight(self.root, grok_bin=str(binary))
        self.assertEqual((code, report["status"]), (5, "INSPECT_UNAVAILABLE"))


if __name__ == "__main__":
    unittest.main()
