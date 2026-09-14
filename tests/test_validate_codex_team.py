#!/usr/bin/env python3
"""Provider-free registry identity coverage for the Codex team validator."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
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


class ValidateCodexTeamClassificationTests(unittest.TestCase):
    def test_repo_self_classify_emits_only_classification_without_cli_calls(self) -> None:
        output = io.StringIO()
        with (
            contextlib.redirect_stdout(output),
            mock.patch.object(validator, "shutil_which", side_effect=AssertionError("unexpected CLI lookup")),
            mock.patch.object(validator, "run_strict_config", side_effect=AssertionError("unexpected strict inference")),
            mock.patch.object(validator.subprocess, "run", side_effect=AssertionError("unexpected CLI call")),
        ):
            result = validator.main(["--repo-self", "--classify"])
        self.assertEqual(result, 0, output.getvalue())
        criteria = [line.split()[0] for line in output.getvalue().splitlines() if " | " in line]
        self.assertEqual(criteria, ["R0", "STAMP", "CANONICAL_AUTHORITY", "MAPPING_STATE"])

    def test_repo_self_validation_passes_its_root_to_strict_runner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with (
                contextlib.redirect_stdout(io.StringIO()),
                mock.patch.object(validator, "shutil_which", return_value=None),
                mock.patch.object(validator, "run_strict_config", return_value=(True, "CONFIG_OK")) as strict,
            ):
                validator.validate_repo_self(validator.Reporter(), root)
            strict.assert_called_once_with(root)


class ValidateCodexTeamStrictConfigTests(unittest.TestCase):
    def test_exit_zero_config_ok_without_rejected_diagnostics_passes(self) -> None:
        proc = mock.Mock(returncode=0, stdout="CONFIG_OK\n", stderr="")
        with (
            mock.patch.object(validator, "shutil_which", return_value="/usr/bin/codex"),
            mock.patch.object(validator.subprocess, "run", return_value=proc) as run,
        ):
            ok, evidence = validator.run_strict_config(None)

        self.assertTrue(ok)
        self.assertEqual(evidence, "CONFIG_OK")
        self.assertIn("--strict-config", run.call_args.args[0])


class ValidateCodexTeamMcpInheritanceTests(unittest.TestCase):
    def test_child_cannot_prove_subtraction_from_enabled_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "planner.toml"
            path.write_text(
                'name = "planner"\n[mcp_servers.tracker]\nenabled = false\n'
                'enabled_tools = []\ndisabled_tools = ["create"]\n',
                encoding="utf-8",
            )
            cfg = {
                "mcp_servers": {"tracker": {"enabled": True, "enabled_tools": ["create"]}}
            }
            problems = validator.ineffective_child_mcp_override_problems(
                cfg, [("planner", "planner.toml", path)]
            )
            self.assertEqual(len(problems), 1)
            self.assertIn("cannot prove subtraction", problems[0])

    def test_child_cannot_prove_addition_to_disabled_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "coordinator.toml"
            path.write_text(
                'name = "coordinator"\n[mcp_servers.tracker]\nenabled = true\n',
                encoding="utf-8",
            )
            cfg = {"mcp_servers": {"tracker": {"enabled": False}}}
            problems = validator.ineffective_child_mcp_override_problems(
                cfg, [("coordinator", "coordinator.toml", path)]
            )
            self.assertEqual(len(problems), 1)
            self.assertIn("cannot prove addition", problems[0])

    def test_equal_child_posture_or_omission_has_no_override_problem(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            equal = root / "equal.toml"
            omitted = root / "omitted.toml"
            equal.write_text(
                'name = "equal"\n[mcp_servers.tracker]\nenabled = true\n'
                'enabled_tools = ["read"]\n',
                encoding="utf-8",
            )
            omitted.write_text('name = "omitted"\n', encoding="utf-8")
            cfg = {
                "mcp_servers": {"tracker": {"enabled": True, "enabled_tools": ["read"]}}
            }
            problems = validator.ineffective_child_mcp_override_problems(
                cfg,
                [
                    ("equal", "equal.toml", equal),
                    ("omitted", "omitted.toml", omitted),
                ],
            )
            self.assertEqual(problems, [])

    def test_exit_zero_config_ok_with_malformed_ignored_role_diagnostics_fails(self) -> None:
        proc = mock.Mock(
            returncode=0,
            stdout="CONFIG_OK\n",
            stderr=(
                "WARN failed to load custom agent config for role planner: "
                "MCP server linear has invalid transport; token=super-secret\n"
                "WARN role planner ignored because its agent configuration was malformed"
                + " additional-context" * 100
                + "\n"
            ),
        )
        with (
            mock.patch.object(validator, "shutil_which", return_value="/usr/bin/codex"),
            mock.patch.object(validator.subprocess, "run", return_value=proc),
        ):
            ok, evidence = validator.run_strict_config(None)

        self.assertFalse(ok)
        self.assertIn("invalid transport", evidence)
        self.assertIn("role planner", evidence)
        self.assertIn("ignored", evidence)
        self.assertIn("token=<redacted>", evidence)
        self.assertNotIn("super-secret", evidence)
        self.assertLessEqual(len(evidence), validator.STRICT_CONFIG_EVIDENCE_LIMIT)

    def test_intentional_ignore_user_config_notice_is_not_rejected(self) -> None:
        proc = mock.Mock(
            returncode=0,
            stdout="CONFIG_OK\n",
            stderr=(
                "WARN --ignore-user-config is active; "
                "role settings from user configuration were ignored\n"
            ),
        )
        with (
            mock.patch.object(validator, "shutil_which", return_value="/usr/bin/codex"),
            mock.patch.object(validator.subprocess, "run", return_value=proc),
        ):
            ok, evidence = validator.run_strict_config(None)

        self.assertTrue(ok)
        self.assertEqual(evidence, "CONFIG_OK")


class ValidateCodexTeamAuthorityTests(unittest.TestCase):
    def test_consistent_claude_codex_and_shared_authorities_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            for authority in ("claude", "codex", "shared"):
                with self.subTest(authority=authority):
                    root = self._write_authority_fixture(temporary_root / authority, authority)
                    classification = validator.classify_team(root)
                    self.assertEqual(classification.canonical_authority, authority)
                    self.assertEqual(classification.mapping_state, "complete")

    def test_unmapped_single_surface_declarations_do_not_need_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            for authority in ("claude", "codex"):
                root = self._write_authority_fixture(Path(temporary_directory) / authority, authority, dual=False)
                classification = validator.classify_team(root)
                self.assertEqual(classification.canonical_authority, authority)
                self.assertEqual(classification.mapping_state, "not-required")

    def test_a_team_yaml_claude_manifest_shape_is_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "yaml-claude"
            (root / ".codex/docs").mkdir(parents=True)
            canonical_text = "`.claude/` is the canonical source design.\n"
            (root / "CLAUDE.md").write_text(canonical_text, encoding="utf-8")
            (root / "AGENTS.md").write_text(canonical_text, encoding="utf-8")
            (root / ".codex/docs/format-mapping.md").write_text(
                "Canonical authored format: Claude Code; `.claude/` is the maintenance authority.\n",
                encoding="utf-8",
            )
            (root / ".codex/docs/format-mapping.manifest.yaml").write_text(
                """spec_version: 1
canonical_authored_format: claude-native
canonical_authority: claude
mapping_retained: true
canonical_roots:
  - CLAUDE.md
  - .claude/rules
root_relations:
  - source: CLAUDE.md
    target: AGENTS.md
    relation: semantic-adaptation
""" ,
                encoding="utf-8",
            )
            classification = validator.classify_team(root)
            self.assertEqual(classification.canonical_authority, "claude")
            self.assertEqual(classification.mapping_state, "complete")

    def test_indented_yaml_shared_declaration_is_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "yaml-shared"
            (root / ".codex/docs").mkdir(parents=True)
            for entry in ("CLAUDE.md", "AGENTS.md"):
                (root / entry).write_text("canonical_authority: shared\ncanonical_root: shared/\n", encoding="utf-8")
            (root / "shared").mkdir()
            (root / "shared/team.yaml").write_text(
                """canonical_authority:
  root: shared/
  policy: platform-neutral
roles:
  - architect
rules:
  - proportional-design
skills:
  - delivery
""",
                encoding="utf-8",
            )
            (root / ".codex/docs/format-mapping.md").write_text(
                "canonical_authority: shared\ncanonical_root: shared/\n", encoding="utf-8"
            )
            (root / ".codex/docs/format-mapping.manifest.yaml").write_text(
                """canonical_authority: shared/
root_relations:
  - source: shared/team.yaml
    target: CLAUDE.md
  - source: shared/team.yaml
    target: AGENTS.md
""",
                encoding="utf-8",
            )
            classification = validator.classify_team(root)
            self.assertEqual(classification.canonical_authority, "shared")
            self.assertEqual(classification.mapping_state, "complete")

    def test_missing_declaration_and_runnable_disagreement_are_ambiguous(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self._write_authority_fixture(Path(temporary_directory), "claude")
            (root / "CLAUDE.md").unlink()
            authority, evidence = validator.detect_canonical_authority(root)
            self.assertEqual(authority, "ambiguous")
            self.assertIn("missing team declaration", evidence)

            root = self._write_authority_fixture(Path(temporary_directory) / "disagreement", "claude")
            (root / "AGENTS.md").write_text("canonical_authority: codex\ncanonical_root: .codex/\n", encoding="utf-8")
            authority, evidence = validator.detect_canonical_authority(root)
            self.assertEqual(authority, "ambiguous")
            self.assertIn("conflicting declarations", evidence)

    def test_manifest_disagreement_and_unsupported_authority_are_ambiguous(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self._write_authority_fixture(Path(temporary_directory), "codex")
            manifest_path = root / ".codex/docs/format-mapping.manifest.yaml"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["canonical_authority"] = "claude"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(validator.detect_canonical_authority(root)[0], "ambiguous")

            root = self._write_authority_fixture(Path(temporary_directory) / "unsupported", "codex")
            manifest_path = root / ".codex/docs/format-mapping.manifest.yaml"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["canonical_authority"] = "arbitrary/"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            authority, evidence = validator.detect_canonical_authority(root)
            self.assertEqual(authority, "ambiguous")
            self.assertIn("unsupported manifest", evidence)

    def test_directory_and_shared_escape_are_not_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temp_root = Path(temporary_directory)
            directory_only = temp_root / "directory-only"
            (directory_only / "shared").mkdir(parents=True)
            self.assertEqual(validator.detect_canonical_authority(directory_only)[0], "ambiguous")

            root = self._write_authority_fixture(temp_root / "shared", "shared")
            shared = root / "shared"
            external_shared = temp_root / "external-shared"
            shutil.copytree(shared, external_shared)
            shutil.rmtree(shared)
            shared.symlink_to(external_shared, target_is_directory=True)
            authority, evidence = validator.detect_canonical_authority(root)
            self.assertEqual(authority, "ambiguous")
            self.assertIn("must not be a symlink", evidence)

    def test_parent_and_absolute_shared_roots_are_rejected(self) -> None:
        for invalid_root in ("/shared/", "../shared/"):
            with self.subTest(invalid_root=invalid_root), tempfile.TemporaryDirectory() as temporary_directory:
                root = self._write_authority_fixture(Path(temporary_directory), "shared")
                declaration = root / "shared/team.yaml"
                team = json.loads(declaration.read_text(encoding="utf-8"))
                team["canonical_authority"]["root"] = invalid_root
                declaration.write_text(json.dumps(team), encoding="utf-8")
                authority, evidence = validator.detect_canonical_authority(root)
                self.assertEqual(authority, "ambiguous")
                self.assertIn("canonical_authority.root", evidence)

    @staticmethod
    def _write_authority_fixture(root: Path, authority: str, dual: bool = True) -> Path:
        (root / ".codex/docs").mkdir(parents=True)
        entries = ["CLAUDE.md", "AGENTS.md"] if dual or authority == "shared" else ["CLAUDE.md" if authority == "claude" else "AGENTS.md"]
        root_name = {"claude": ".claude/", "codex": ".codex/", "shared": "shared/"}[authority]
        for entry in entries:
            (root / entry).write_text(
                f"canonical_authority: {authority}\ncanonical_root: {root_name}\n", encoding="utf-8"
            )
        if authority == "shared":
            (root / "shared").mkdir()
            (root / "shared/team.yaml").write_text(json.dumps({
                "canonical_authority": {"root": "shared/", "policy": "platform-neutral"},
                "roles": [], "rules": [], "skills": [],
            }), encoding="utf-8")
        if dual or authority == "shared":
            (root / ".codex/docs/format-mapping.md").write_text(
                f"canonical_authority: {authority}\ncanonical_root: {root_name}\n", encoding="utf-8"
            )
            source = {"runtime": authority, "path": f"{root_name}team.yaml" if authority == "shared" else f"{root_name}rules/base.md"}
            targets = [{"runtime": "claude", "path": "CLAUDE.md"}, {"runtime": "codex", "path": "AGENTS.md"}]
            (root / ".codex/docs/format-mapping.manifest.yaml").write_text(json.dumps({
                "canonical_authority": "shared/" if authority == "shared" else authority,
                "artifacts": [{"canonical": True, "source": source, "targets": targets}],
            }), encoding="utf-8")
        return root


class ValidateCodexTeamProportionalContractTests(unittest.TestCase):
    def test_marked_future_team_requires_structure_not_risk_scoring(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = ValidateCodexTeamAuthorityTests._write_authority_fixture(Path(temporary_directory), "claude")
            manifest_path = root / ".codex/docs/format-mapping.manifest.yaml"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.update({
                "generation_contract": "proportional-design-v1",
                "requested_runtimes": ["claude", "codex"],
                "approved_role_count": 2,
                "generated_role_count": 2,
                "proportional_design_cases": [
                    {"kind": "unsupported-blocker", "verdict": "REJECT"},
                    {"kind": "high-impact-control", "verdict": "ACCEPT", "evidence": "confirmed corruption incident"},
                ],
            })
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            for runtime in ("claude", "codex"):
                (root / f".{runtime}/rules").mkdir(parents=True, exist_ok=True)
                (root / f".{runtime}/rules/proportional-design.md").write_text("rule\n", encoding="utf-8")
                (root / f".{runtime}/agents").mkdir(parents=True, exist_ok=True)
            (root / ".claude/agents/producer.md").write_text("safeguard_decision: conditional-v1\n", encoding="utf-8")
            (root / ".codex/agents/reviewer.md").write_text("proportional_design_verdict: criterion-level-v1\n", encoding="utf-8")
            self.assertEqual(validator.validate_generated_proportional_contract(root)[0], "PASS")

            manifest["proportional_design_cases"] = [{"kind": "unsupported-blocker", "verdict": "ACCEPT"}]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            verdict, evidence = validator.validate_generated_proportional_contract(root)
            self.assertEqual(verdict, "FAIL")
            self.assertIn("unsupported-blocker rejection", evidence)

    def test_yaml_future_contract_cases_are_structurally_recognized(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "yaml-contract"
            (root / ".codex/docs").mkdir(parents=True)
            canonical_text = "`.claude/` is the canonical source design.\n"
            (root / "CLAUDE.md").write_text(canonical_text, encoding="utf-8")
            (root / "AGENTS.md").write_text(canonical_text, encoding="utf-8")
            (root / ".codex/docs/format-mapping.md").write_text(
                "Canonical authored format: Claude Code; `.claude/` is the maintenance authority.\n",
                encoding="utf-8",
            )
            (root / ".codex/docs/format-mapping.manifest.yaml").write_text(
                "\n".join((
                    "canonical_authority: claude", "generation_contract: proportional-design-v1",
                    "requested_runtimes:", "  - claude", "  - codex", "approved_role_count: 2",
                    "generated_role_count: 2", "root_relations:", "  - source: CLAUDE.md",
                    "    target: AGENTS.md", "proportional_design_cases:",
                    "  - kind: unsupported-blocker", "    verdict: REJECT",
                    "  - kind: high-impact-control", "    verdict: ACCEPT",
                    "    evidence: confirmed corruption incident", "",
                )),
                encoding="utf-8",
            )
            for runtime in ("claude", "codex"):
                (root / f".{runtime}/rules").mkdir(parents=True, exist_ok=True)
                (root / f".{runtime}/rules/proportional-design.md").write_text("rule\n", encoding="utf-8")
                (root / f".{runtime}/agents").mkdir(parents=True, exist_ok=True)
            (root / ".claude/agents/producer.md").write_text("safeguard_decision: conditional-v1\n", encoding="utf-8")
            (root / ".codex/agents/reviewer.md").write_text("proportional_design_verdict: criterion-level-v1\n", encoding="utf-8")
            self.assertEqual(validator.validate_generated_proportional_contract(root)[0], "PASS")


class ValidateCodexTeamJ5AgentMetadataTests(unittest.TestCase):
    def test_codex_agent_type_and_paired_toml_model_are_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            agent = root / ".codex/agents/planner.md"
            agent.parent.mkdir(parents=True)
            (root / "agents").mkdir()
            (root / ".codex/rules").mkdir(parents=True)
            agent.write_text(self._agent_text(), encoding="utf-8")
            paired = root / "agents/planner.toml"
            paired.write_text('name = "planner"\nmodel = "gpt-5"\n', encoding="utf-8")
            (root / ".codex/rules/example.md").write_text(
                "--" + "-\nname: Example\ndescription: Example rule\n" + "--" + "-\n"
                "## Violation Determination\n- missing field -> violation\n## Exceptions\n- none\n",
                encoding="utf-8",
            )
            self.assertEqual(validator.validate_generated_j5_markdown(root)[0], "PASS")

            agent.write_text(self._agent_text().replace("agent_type: default\n", ""), encoding="utf-8")
            verdict, evidence = validator.validate_generated_j5_markdown(root)
            self.assertEqual(verdict, "FAIL")
            self.assertIn("missing nonempty agent_type", evidence)

            agent.write_text(self._agent_text(), encoding="utf-8")
            paired.write_text('name = "planner"\n', encoding="utf-8")
            verdict, evidence = validator.validate_generated_j5_markdown(root)
            self.assertEqual(verdict, "FAIL")
            self.assertIn("paired TOML missing model", evidence)

    @staticmethod
    def _agent_text() -> str:
        return (
            "--" + "-\nname: Planner\ndescription: Plans work\nagent_type: default\n" + "--" + "-\n"
            "## Reasoning\nUse evidence.\n## Workflow\nFollow steps.\n## Self-Critique\nCheck output.\n"
            "## Boundaries\nStay scoped.\n## Uncertainty Protocol\nEscalate missing facts.\n"
            "## Examples\n### Rejection Case\nReject unsupported work.\n"
        )


class ValidateCodexTeamAdaptationInputTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.temporary_path = Path(temporary_directory.name)
        self.root = self.temporary_path / "repo"
        self.inputs = [
            ".codex/rules/codex-runtime-config.md",
            ".codex/rules/codex-agent-config-patterns.md",
            ".codex/rules/context-isolation.md",
        ]
        self.rows = [
            {"path": path, "scope": f"Bounded runtime purpose {index}",
             "targets": ["AGENTS.md", ".codex/agents/writer.md"]}
            for index, path in enumerate(self.inputs)
        ]
        for path in [*self.inputs, "AGENTS.md", ".codex/agents/writer.md", ".claude/source.md"]:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("fixture\n", encoding="utf-8")
        (self.root / ".codex/docs").mkdir()
        self.data = {"platform_only": [{"path": path} for path in self.inputs],
                     "deliberately_not_copied": [], "adaptation_inputs": self.rows}
        self.write_manifest()
        self.write_audit()

    def write_manifest(self) -> None:
        lines = []
        for key, rows in self.data.items():
            if not isinstance(rows, list) or not rows:
                lines.append(f"{key} = {json.dumps(rows)}")
        for key, rows in self.data.items():
            if isinstance(rows, list):
                for row in rows:
                    lines.extend([f"[[{key}]]", *[f"{field} = {json.dumps(value)}" for field, value in row.items()]])
        (self.root / ".codex/docs/claude-adaptation-manifest.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_audit(self, rows: list[dict] | None = None) -> None:
        lines = ["## Codex-Only Inventory", "| Path | Why |", "|---|---|"]
        lines.extend(f"| `{row['path']}` | fixture |" for row in self.data["platform_only"])
        lines.extend(["## Deliberately Not Copied", "## Runtime Adaptation Inputs",
                      "| Input | Bounded scope | Projections |", "|---|---|---|"])
        for row in self.rows if rows is None else rows:
            targets = "<br>".join(f"`{target}`" for target in row["targets"])
            lines.append(f"| `{row['path']}` | {row['scope']} | {targets} |")
        (self.root / ".codex/docs/claude-adaptation-audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def assert_invalid(self, expected: str) -> None:
        verdict, evidence = validator.validate_m5_inventory(self.root)
        self.assertEqual(verdict, "FAIL", evidence)
        self.assertIn(expected, evidence)

    def test_three_known_inputs_and_matching_scope_target_sets_pass(self) -> None:
        reversed_targets = [{**row, "targets": list(reversed(row["targets"]))} for row in self.rows]
        self.write_audit(reversed_targets)
        verdict, evidence = validator.validate_m5_inventory(self.root)
        self.assertEqual(verdict, "PASS", evidence)
        self.assertIn("3 bounded adaptation inputs", evidence)

    def test_missing_unknown_duplicate_and_noninventoried_inputs_fail(self) -> None:
        original = json.loads(json.dumps(self.data))
        for rows, expected in (
            ([], "missing [[adaptation_inputs]]"),
            (self.rows[:2], "all three known"),
            ([*self.rows, self.rows[0]], "duplicate adaptation input"),
            ([*self.rows, {"path": ".codex/rules/unapproved.md"}], "unknown adaptation input"),
        ):
            with self.subTest(expected=expected):
                self.data = {**original, "adaptation_inputs": rows}
                self.write_manifest()
                self.assert_invalid(expected)
        self.data = {**original, "platform_only": original["platform_only"][1:]}
        self.write_manifest()
        self.write_audit()
        self.assert_invalid("not platform-only")

    def test_empty_scope_and_invalid_duplicate_or_unsafe_targets_fail(self) -> None:
        original = json.loads(json.dumps(self.data))
        mutations = [("scope", value, "empty/invalid scope") for value in ("", " ", 42)]
        mutations += [("targets", value, expected) for value, expected in (
            ([], "empty/invalid targets"), ("AGENTS.md", "empty/invalid targets"),
            ([""], "invalid target"), ([42], "invalid target"),
            (["AGENTS.md", "AGENTS.md"], "duplicate adaptation target"),
            ([str(self.root / "AGENTS.md")], "unsafe or missing Codex projection"),
            ([".codex/../AGENTS.md"], "unsafe or missing Codex projection"),
            ([".codex/missing.md"], "unsafe or missing Codex projection"),
            ([".claude/source.md"], "unsafe or missing Codex projection"),
            ([".codex/agents/"], "unsafe or missing Codex projection"),
        )]
        for key, value, expected in mutations:
            with self.subTest(key=key, value=value):
                self.data = json.loads(json.dumps(original))
                self.data["adaptation_inputs"][0][key] = value
                self.write_manifest()
                self.assert_invalid(expected)

    def test_symlink_escape_in_input_or_target_fails(self) -> None:
        outside = self.temporary_path / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        link = self.root / ".codex/agents/escape.md"
        link.symlink_to(outside)
        self.data["adaptation_inputs"][0]["targets"] = [".codex/agents/escape.md"]
        self.write_manifest()
        self.write_audit()
        self.assert_invalid("unsafe or missing Codex projection")
        self.data["adaptation_inputs"][0]["targets"] = ["AGENTS.md", ".codex/agents/writer.md"]
        source = self.root / self.inputs[0]
        source.unlink()
        source.symlink_to(outside)
        self.write_manifest()
        self.write_audit()
        self.assert_invalid("unsafe or missing adaptation input")

    def test_audit_scope_target_duplicate_and_malformed_rows_fail(self) -> None:
        for rows, expected in (
            ([{**self.rows[0], "scope": "Different scope"}, *self.rows[1:]], "scope/targets differ"),
            ([{**self.rows[0], "targets": ["AGENTS.md"]}, *self.rows[1:]], "scope/targets differ"),
            ([*self.rows, self.rows[0]], "duplicate audit adaptation input"),
            ([{**self.rows[0], "targets": ["AGENTS.md", "AGENTS.md"]}, *self.rows[1:]], "duplicate audit adaptation target"),
        ):
            with self.subTest(expected=expected):
                self.write_audit(rows)
                self.assert_invalid(expected)
        self.write_audit()
        audit = self.root / ".codex/docs/claude-adaptation-audit.md"
        original = audit.read_text(encoding="utf-8")
        for text, expected in (
            (original.replace("## Runtime Adaptation Inputs", "## Other"), "requires one Runtime Adaptation Inputs"),
            (original.replace("| Input | Bounded scope | Projections |", "| Input | Scope | Projections |"), "requires one Runtime Adaptation Inputs"),
            (original.replace("`AGENTS.md`<br>", "AGENTS.md<br>", 1), "malformed audit"),
            (original + "## Runtime Adaptation Inputs\n", "requires one Runtime Adaptation Inputs"),
        ):
            with self.subTest(expected=expected):
                audit.write_text(text, encoding="utf-8")
                self.assert_invalid(expected)


class ValidateCodexTeamJ5ContractTests(unittest.TestCase):
    def validate_agent(self, text: str, runtime: str = "codex") -> tuple[str, str]:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        agent_root = root / ("shared/agents" if runtime == "shared" else f".{runtime}/agents")
        agent_root.mkdir(parents=True)
        if runtime == "claude":
            text = text.replace("agent_type: default", "model: opus")
        elif runtime == "shared":
            text = text.replace("agent_type: default\n", "")
        (agent_root / "planner.md").write_text(text, encoding="utf-8")
        (root / "agents").mkdir()
        (root / "agents/planner.toml").write_text('name = "planner"\nmodel = "gpt-6-astra"\n', encoding="utf-8")
        (root / ".codex/rules").mkdir(parents=True)
        (root / ".codex/rules/fixture.md").write_text(
            "---\nname: Fixture\ndescription: Fixture rule\n---\n"
            "## Violation Determination\n- missing field -> violation\n## Exceptions\n- none\n",
            encoding="utf-8",
        )
        return validator.validate_generated_j5_markdown(root)

    def test_compact_specific_contract_and_nested_workflow_checks_pass(self) -> None:
        text = ValidateCodexTeamJ5AgentMetadataTests._agent_text().replace(
            "Use evidence.", "Identify the requested runtime and approved role coverage."
        ).replace(
            "Follow steps.", "Map each approved role to its owned paths.\n### Verification\nCheck runtime paths resolve."
        ).replace("Check output.", "Verify every approved role appears once in the role map.")
        for runtime in ("codex", "claude", "shared"):
            with self.subTest(runtime=runtime):
                verdict, evidence = self.validate_agent(text, runtime)
                self.assertEqual(verdict, "PASS", evidence)

    def test_missing_duplicate_reordered_and_separated_contract_sections_fail(self) -> None:
        base = ValidateCodexTeamJ5AgentMetadataTests._agent_text()
        cases = [
            (base.replace(f"## {heading}\n", "", 1), "missing H2")
            for heading in ("Reasoning", "Workflow", "Self-Critique")
        ] + [
            (base + f"## {heading}\nDuplicate.\n", "duplicate H2")
            for heading in ("Reasoning", "Workflow", "Self-Critique", "Boundaries", "Uncertainty Protocol", "Examples")
        ] + [
            (base.replace("## Workflow", "## Self-Critique", 1).replace("## Self-Critique\nCheck output.", "## Workflow\nCheck output."), "order failed"),
            (base.replace("## Workflow", "## Unrelated\nExtra block.\n## Workflow"), "adjacent H2"),
        ]
        for text, expected in cases:
            with self.subTest(expected=expected, text=text):
                verdict, evidence = self.validate_agent(text)
                self.assertEqual(verdict, "FAIL", evidence)
                self.assertIn(expected, evidence)

    def test_duplicate_preflight_and_verification_gate_aliases_fail(self) -> None:
        for heading in ("Preflight", "Verification", "Preflight Gate", "Verification Gate"):
            with self.subTest(heading=heading):
                text = ValidateCodexTeamJ5AgentMetadataTests._agent_text() + f"## {heading}\nRepeat the contract.\n"
                verdict, evidence = self.validate_agent(text)
                self.assertEqual(verdict, "FAIL", evidence)
                self.assertIn(f"duplicate contract gates: {heading}", evidence)

    def test_rejection_only_examples_remain_required(self) -> None:
        base = ValidateCodexTeamJ5AgentMetadataTests._agent_text()
        for text in (
            base.replace("### Rejection Case\n", ""),
            base + "### Rejection Case\nDuplicate.\n",
            base + "### Normal Case\nSurplus.\n",
            base + "### Edge Case\nSurplus.\n",
        ):
            with self.subTest(text=text):
                verdict, evidence = self.validate_agent(text)
                self.assertEqual(verdict, "FAIL", evidence)
                self.assertIn("Examples rejection=", evidence)


if __name__ == "__main__":
    unittest.main()
