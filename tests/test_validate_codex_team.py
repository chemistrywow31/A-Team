#!/usr/bin/env python3
"""Provider-free registry identity coverage for the Codex team validator."""

from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_codex_team.py"
SPEC = importlib.util.spec_from_file_location("validate_codex_team", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class ValidateCodexTeamRegistryIdentityTests(unittest.TestCase):
    def test_registry_identity_positive_and_single_name_mutation_negative(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "a-team-fixture"
            (root / ".codex").mkdir(parents=True)
            shutil.copy2(REPO_ROOT / "AGENTS.md", root / "AGENTS.md")
            shutil.copy2(REPO_ROOT / ".codex/config.toml", root / ".codex/config.toml")
            shutil.copytree(REPO_ROOT / "agents", root / "agents")

            config, config_error = validator.parse_toml(root / ".codex/config.toml")
            self.assertIsNone(config_error)
            entries, issues = validator.extract_registry_paths(root, config)
            self.assertEqual(issues, [])
            self.assertEqual(len(entries), 13)
            self.assertEqual(validator.registry_identity_problems(entries), [])
            positive_classification = validator.classify_team(root)
            self.assertTrue(positive_classification.runnable_codex)

            positive_repo_self = self._repo_self_output(root)
            positive_team = self._team_output(root)
            self.assertIn("R4 registry-resolution | PASS | 13 config_file paths resolve from .codex/", positive_repo_self)
            self.assertIn("G4 codex-registry | PASS | registry pattern=explicit; roles=13", positive_team)

            role, _, path = entries[0]
            original = path.read_text(encoding="utf-8")
            self.assertIn(f'name = "{role}"', original)
            path.write_text(original.replace(f'name = "{role}"', 'name = "wrong_identity"', 1), encoding="utf-8")

            negative_repo_self = self._repo_self_output(root)
            negative_team = self._team_output(root)
            expected = f"name 'wrong_identity' does not equal registry id '{role}'"
            negative_classification = validator.classify_team(root)
            self.assertFalse(negative_classification.runnable_codex)
            self.assertEqual(negative_classification.team_class, "incomplete/activation-gated")
            mutated_config, mutated_error, mutated_tomls = validator.load_codex_surface(root)
            runnable, runnable_reason = validator.codex_surface_runnable(root, mutated_config, mutated_error, mutated_tomls)
            self.assertFalse(runnable)
            self.assertIsNotNone(runnable_reason)
            self.assertIn(expected, runnable_reason)
            self.assertIn("R4 registry-resolution | FAIL |", negative_repo_self)
            self.assertIn("G4 codex-registry | FAIL |", negative_team)
            self.assertEqual(self._check_line_count(negative_repo_self, "R4", expected), 1)
            self.assertEqual(self._check_line_count(negative_team, "G4", expected), 1)

    def _repo_self_output(self, root: Path) -> str:
        reporter = validator.Reporter()
        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(validator, "shutil_which", return_value=None):
            validator.validate_repo_self(reporter, root)
        return output.getvalue()

    def _team_output(self, root: Path) -> str:
        reporter = validator.Reporter()
        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(validator, "run_strict_config", return_value=(False, "fake codex unavailable")):
            validator.validate_team(reporter, root, classify_only=False)
        return output.getvalue()

    @staticmethod
    def _check_line_count(output: str, check_id: str, expected: str) -> int:
        return sum(line.startswith(f"{check_id} ") and expected in line for line in output.splitlines())


if __name__ == "__main__":
    unittest.main()
