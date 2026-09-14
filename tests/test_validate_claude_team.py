"""Regression tests for Claude surface classification and compact agent contracts."""

from __future__ import annotations

import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate-team.sh"


class ClaudeReferenceOnlyDetectorTests(unittest.TestCase):
    def run_validator(self, claude_md: str) -> subprocess.CompletedProcess[str]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        team_root = Path(temp_dir.name) / "fixture"
        (team_root / ".claude").mkdir(parents=True)
        (team_root / "CLAUDE.md").write_text(claude_md, encoding="utf-8")
        return subprocess.run(
            ["sh", str(VALIDATOR), str(team_root)],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_explicit_claude_surface_reference_only_declaration_skips(self) -> None:
        result = self.run_validator("# Fixture\n\n**Claude surface:** reference-only\n")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("T0 claude-team-detected | SKIP | charter declares", result.stdout)

    def test_general_authority_prose_does_not_skip(self) -> None:
        result = self.run_validator(
            "# Fixture\n\n"
            "Claude authority uses `CLAUDE.md`; a reference-only mirror is never promoted implicitly.\n"
        )

        self.assertIn("T0 claude-team-detected | PASS |", result.stdout)
        self.assertNotIn("T0 claude-team-detected | SKIP |", result.stdout)


class ClaudeEntrySkillTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.root = Path(temporary_directory.name) / "team"
        (self.root / ".claude/agents").mkdir(parents=True)
        (self.root / ".claude/skills").mkdir()
        (self.root / "CLAUDE.md").write_text("# Fixture\n", encoding="utf-8")
        (self.root / ".claude/agents/conductor.md").write_text(ClaudeJ5ContractTests.agent_text(), encoding="utf-8")

    @staticmethod
    def entry_text() -> str:
        return (
            "---\nname: Launch\ndescription: Entry command that launches the conductor coordinator workflow\n"
            "disable-model-invocation: true\nallowed-tools: [Read, Agent]\nargument-hint: '[request]'\n---\n\n"
            "# Launch\n\n## Workflow\n"
            "Read `.claude/agents/conductor.md` and adopt its workflow in the current session.\n"
            "Do not spawn conductor as a subagent.\n"
        )

    def write_skill(self, name: str, text: str) -> Path:
        path = self.root / f".claude/skills/{name}/SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def entry_results(self) -> dict[str, str]:
        result = subprocess.run(["sh", str(VALIDATOR), str(self.root)], capture_output=True, text=True, check=False)
        criteria = {line.split()[0]: line for line in result.stdout.splitlines()
                    if line.startswith(tuple(f"E{index} " for index in range(1, 7)))}
        self.assertEqual(set(criteria), {f"E{index}" for index in range(1, 7)}, result.stdout + result.stderr)
        return criteria

    def assert_entry_passes(self) -> None:
        for criterion in self.entry_results().values():
            self.assertIn("| PASS |", criterion)

    def test_renamed_entry_and_ordinary_manual_review_deploy_are_unambiguous(self) -> None:
        self.write_skill("renamed-front-door", self.entry_text())
        for name in ("review", "deploy"):
            self.write_skill(name, f"---\nname: {name}\ndescription: Manually {name} the artifact\ndisable-model-invocation: true\n---\nPerform the requested {name}.\n")
        self.write_skill("coordinator-checks", "---\nname: Checks\ndescription: Run coordinator checks before release\ndisable-model-invocation: true\n---\nReview the output.\n")
        self.assert_entry_passes()

    def test_actual_a_team_entry_and_quality_checklist_are_unambiguous(self) -> None:
        self.write_skill("renamed-a-team", (REPO_ROOT / ".claude/skills/a-team/SKILL.md").read_text(encoding="utf-8"))
        self.write_skill("renamed-quality-review", (REPO_ROOT / ".claude/skills/quality-validation/SKILL.md").read_text(encoding="utf-8"))
        (self.root / ".claude/agents/conductor.md").unlink()
        shutil.copy2(REPO_ROOT / ".claude/agents/team-architect.md", self.root / ".claude/agents/team-architect.md")
        self.assert_entry_passes()

    def test_checklist_describing_adoption_is_not_itself_an_entry(self) -> None:
        self.write_skill("launch", self.entry_text())
        self.write_skill("manual-checklist", (
            "---\nname: Review\ndescription: Inspect coordinator entry contracts\ndisable-model-invocation: true\n---\n"
            "## Workflow\nRead `.claude/agents/conductor.md` to inspect the entry.\n"
            "Verify that the entry adopts its coordinator in the current session.\n"
            "In this review, check that the skill adopts the coordinator and declares allowed-tools granting Agent.\n"
            "Do not adopt the coordinator yourself.\n"
        ))
        self.assert_entry_passes()

    def test_adoption_intent_identifies_entry_before_metadata_validation(self) -> None:
        text = self.entry_text().replace("Entry command that launches the conductor coordinator workflow", "Run the approved request")
        self.write_skill("intent-only", text)
        self.assert_entry_passes()
        self.write_skill("intent-only", text.replace("allowed-tools: [Read, Agent]\n", ""))
        results = self.entry_results()
        self.assertIn("| PASS |", results["E1"])
        self.assertIn("| FAIL |", results["E3"])

    def test_missing_invalid_and_body_only_metadata_do_not_hide_entries(self) -> None:
        base = self.entry_text()
        cases = [
            (base.replace(field + "\n", "") + "\n" + field + "\n", criterion)
            for field, criterion in (("disable-model-invocation: true", "E2"),
                                     ("allowed-tools: [Read, Agent]", "E3"),
                                     ("argument-hint: '[request]'", "E4"))
        ] + [
            (base.replace("disable-model-invocation: true", "disable-model-invocation: false"), "E2"),
            (base.replace("allowed-tools: [Read, Agent]", "allowed-tools: [Read, NotAgent]"), "E3"),
            (base.replace("allowed-tools: [Read, Agent]", "allowed-tools: [Read, Agent"), "E3"),
            (base.replace("argument-hint: '[request]'", "argument-hint: ''"), "E4"),
            (base.replace("disable-model-invocation: true", "disable-model-invocation: true\ndisable-model-invocation: false"), "E2"),
            (base.replace("---\n\n# Launch", "\n# Launch"), "E2"),
            (base.removeprefix("---\n"), "E2"),
        ]
        for text, failed in cases:
            with self.subTest(failed=failed, text=text):
                self.write_skill("launch", text)
                results = self.entry_results()
                self.assertIn("| PASS |", results["E1"])
                self.assertIn("| FAIL |", results[failed])

    def test_invalid_unresolved_and_non_main_adoption_fail(self) -> None:
        base = self.entry_text()
        for text in (
            base.replace(" and adopt its workflow", " to inspect its workflow"),
            base.replace("conductor.md", "missing.md"),
            base.replace("current session", "a subagent session"),
            base.replace("Read `.claude/agents/conductor.md` and adopt", "Do not adopt"),
            base.replace("Read `.claude/agents/conductor.md` and adopt", "Verify that the entry reads `.claude/agents/conductor.md` and adopts"),
        ):
            with self.subTest(text=text):
                self.write_skill("launch", text)
                results = self.entry_results()
                self.assertIn("| PASS |", results["E1"])
                self.assertIn("| FAIL |", results["E5"])

    def test_agent_grant_ignores_comments_and_partial_tool_names(self) -> None:
        for value in (
            "[Read] # Agent is deliberately not granted",
            "Read # Agent is deliberately not granted",
            "['Read # Agent']",
            '"Read # Agent"',
            '[Read, "Agent # not a tool name"]',
            "[Read, NotAgent, AgentHelper, Agent.Read, Agent-helper]",
            "\n  - Read # Agent is deliberately not granted",
            '\n  - "Read # Agent"',
        ):
            with self.subTest(value=value):
                self.write_skill("launch", self.entry_text().replace("allowed-tools: [Read, Agent]", "allowed-tools: " + value))
                results = self.entry_results()
                self.assertIn("| PASS |", results["E1"])
                self.assertIn("| FAIL |", results["E3"])

    def test_complete_agent_grant_accepts_inline_scalar_and_block_forms(self) -> None:
        for value in (
            "[Read, Agent] # a real grant",
            '["Read", "Agent"]',
            "['Read', 'Agent',]",
            "Read, Agent",
            '"Read Agent"',
            "Bash(git *), Agent",
            "['Bash(echo # literal)', Agent] # comment",
            "\n  - Read # harmless comment\n  - Agent",
            '\n  - "Read"\n  # comment-only line\n  - \'Agent\' # actual grant',
            "\n- Read\n- Agent",
        ):
            with self.subTest(value=value):
                self.write_skill("launch", self.entry_text().replace("allowed-tools: [Read, Agent]", "allowed-tools: " + value))
                self.assert_entry_passes()

    def test_malformed_tool_lists_do_not_grant_agent(self) -> None:
        for value in (
            "[Read, Agent",
            "[Read Agent]",
            '[Read, "Agent]',
            "[Read, 'Agent'junk]",
            "[Read, Agent] trailing",
            "[Read, Agent]\nallowed-tools: [Read]",
            "\n  - Agent\n    - Read",
            "\n  - Agent\n  Read: true",
            "[Agent]\n  - Read",
        ):
            with self.subTest(value=value):
                self.write_skill("launch", self.entry_text().replace("allowed-tools: [Read, Agent]", "allowed-tools: " + value))
                self.assertIn("| FAIL |", self.entry_results()["E3"])

    def test_coordinator_symlink_escape_and_affirmative_spawn_fail(self) -> None:
        outside = self.root.parent / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        coordinator = self.root / ".claude/agents/conductor.md"
        coordinator.unlink()
        coordinator.symlink_to(outside)
        self.write_skill("launch", self.entry_text())
        self.assertIn("| FAIL |", self.entry_results()["E5"])
        coordinator.unlink()
        coordinator.write_text(ClaudeJ5ContractTests.agent_text(), encoding="utf-8")
        self.write_skill("launch", self.entry_text() + "\nSpawn conductor with the Agent tool.\n")
        self.assertIn("| FAIL |", self.entry_results()["E6"])

    def test_argument_hint_requires_an_actual_nonempty_scalar(self) -> None:
        for value in (
            "# no actual hint", "", "null", "NULL # no hint", "~",
            "'' # no hint", '\"\"', "'   '", '\"\\t\"',
            "[request]", "[]", "{request: value}", "{}",
            "\n  - request", "\n  request: value",
            "'unterminated", '\"unterminated', "'request' trailing", '\"request\"#not-separated',
            "request: value", "request\n  - item", "request\nargument-hint: other",
        ):
            with self.subTest(value=value):
                self.write_skill("launch", self.entry_text().replace("argument-hint: '[request]'", "argument-hint: " + value))
                results = self.entry_results()
                self.assertIn("| PASS |", results["E1"])
                self.assertIn("| PASS |", results["E3"])
                self.assertIn("| FAIL |", results["E4"])

    def test_argument_hint_accepts_plain_and_quoted_values_with_comments(self) -> None:
        for value in (
            "request", "request # actual hint", "request#identifier", "user's request",
            "'[request]' # optional argument", '\"[request]\" # optional argument',
            "'request # literal hash'", '\"request # literal hash\"',
            "'user''s request'", r'"say \"request\""', "'null'", "--request",
        ):
            with self.subTest(value=value):
                self.write_skill("launch", self.entry_text().replace("argument-hint: '[request]'", "argument-hint: " + value))
                self.assert_entry_passes()

    def test_two_real_entries_remain_ambiguous_even_when_one_is_malformed(self) -> None:
        self.write_skill("launch-one", self.entry_text())
        self.write_skill("launch-two", self.entry_text().replace("disable-model-invocation: true\n", ""))
        self.assertIn("| FAIL |", self.entry_results()["E1"])

    def test_missing_entry_and_manual_only_checklist_fail(self) -> None:
        self.assertIn("| FAIL |", self.entry_results()["E1"])
        self.write_skill("quality-only", (REPO_ROOT / ".claude/skills/quality-validation/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("| FAIL |", self.entry_results()["E1"])


class ClaudeJ5ContractTests(unittest.TestCase):
    @staticmethod
    def agent_text() -> str:
        return (
            "---\nname: Planner\ndescription: Plans work\nmodel: opus\n---\n"
            "## Reasoning\nIdentify approved role coverage and required runtimes.\n"
            "## Workflow\nMap each role to its owned paths.\n"
            "### Verification\nCheck the mapped runtime paths resolve.\n"
            "## Self-Critique\nVerify every approved role appears once in the role map.\n"
            "## Boundaries\nStay within assigned paths.\n"
            "## Uncertainty Protocol\nEscalate conflicting ownership.\n"
            "## Examples\n### Rejection Case\nReject a role with conflicting owners.\n"
        )

    def run_agent(self, text: str) -> str:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        (root / ".claude/agents").mkdir(parents=True)
        (root / "CLAUDE.md").write_text("# Fixture\n", encoding="utf-8")
        (root / ".claude/agents/planner.md").write_text(text, encoding="utf-8")
        result = subprocess.run(["sh", str(VALIDATOR), str(root)], capture_output=True, text=True, check=False)
        # This fixture isolates agent contract checks; unrelated team checks lack
        # their artifacts and are intentionally outside these assertions.
        return result.stdout

    def test_compact_specific_contract_and_nested_workflow_checks_pass(self) -> None:
        output = self.run_agent(self.agent_text())
        self.assertIn("F3 agent-j5-section-order | PASS |", output)
        self.assertIn("F4 agent-j5-rejection-examples | PASS |", output)

    def test_missing_duplicate_reordered_and_separated_contract_sections_fail(self) -> None:
        base = self.agent_text()
        cases = [
            (base.replace(f"## {heading}\n", "", 1), "missing")
            for heading in ("Reasoning", "Workflow", "Self-Critique")
        ] + [
            (base + f"## {heading}\nDuplicate.\n", "duplicate H2")
            for heading in ("Reasoning", "Workflow", "Self-Critique", "Boundaries", "Uncertainty Protocol", "Examples")
        ] + [
            (base.replace("## Workflow", "## TEMP", 1).replace("## Self-Critique", "## Workflow", 1).replace("## TEMP", "## Self-Critique", 1), "order R="),
            (base.replace("## Workflow", "## Unrelated\nExtra block.\n## Workflow"), "adjacent H2"),
        ]
        for text, expected in cases:
            with self.subTest(expected=expected, text=text):
                output = self.run_agent(text)
                criterion = next(line for line in output.splitlines() if line.startswith("F3 "))
                self.assertIn("| FAIL |", criterion)
                self.assertIn(expected, criterion)

    def test_duplicate_preflight_and_verification_gate_aliases_fail(self) -> None:
        for heading in ("Preflight", "Verification", "Preflight Gate", "Verification Gate"):
            with self.subTest(heading=heading):
                output = self.run_agent(self.agent_text() + f"## {heading}\nRepeat the contract.\n")
                self.assertIn("F3 agent-j5-section-order | FAIL |", output)
                self.assertIn(f"duplicate contract gates ## {heading}", output)

    def test_rejection_only_examples_remain_required(self) -> None:
        base = self.agent_text()
        for text in (
            base.replace("### Rejection Case\n", ""),
            base + "### Rejection Case\nDuplicate.\n",
            base + "### Normal Case\nSurplus.\n",
            base + "### Edge Case\nSurplus.\n",
        ):
            with self.subTest(text=text):
                self.assertIn("F4 agent-j5-rejection-examples | FAIL |", self.run_agent(text))


if __name__ == "__main__":
    unittest.main()
