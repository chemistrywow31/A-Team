"""The shape decision: one agent that loads skills, or an agent group.

A-Team records the decision per user flow in docs/work-shape.json before it
builds a team. These tests fail when the heavy path is chosen for a
single-context flow, when the skill path is chosen for a flow the rule says
needs a group, and when the generated tree does not match the record.

Two real flows anchor the tests:
- the README's weekly teacher newsletter (tests/fixtures/newsletter-team), a
  single-context flow built as one skill workflow;
- A-Team's own text-only optimization lane (docs/work-shape.json at the repo
  root), which needs a check isolated from the author and is a group.
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_work_shape as shape  # noqa: E402
import validate_codex_team as codex_validator  # noqa: E402

NEWSLETTER = REPO_ROOT / "tests/fixtures/newsletter-team"
CLAUDE_VALIDATOR = REPO_ROOT / "scripts/validate-team.sh"

AGENT = "---\nname: {name}\ndescription: {description}\nmodel: sonnet\n---\n\n# {name}\n\n{body}\n"
ENTRY_SKILL = (
    "---\nname: newsletter\ndescription: Entry command that launches the editor coordinator workflow\n"
    "disable-model-invocation: true\nallowed-tools: [Read, Agent]\nargument-hint: '[issue request]'\n---\n\n"
    "Read `.claude/agents/editor.md` and adopt its workflow in the current session.\n"
    "Do not spawn editor as a subagent.\n"
)
HANDOFF_RULE = (
    "---\nname: Handoff Contract\ndescription: What the source checker receives and returns\n---\n\n"
    "The editor sends the draft path and the source list, nothing about how the draft was written.\n"
    "The source checker returns one line per claim: claim, source, supported or not.\n"
)


def flow(name: str, chosen: str, **triggers: str) -> dict:
    record = {"name": name, "shape": chosen, "parallel": "", "isolated_check": "", "overflow": "", "why": "test"}
    record.update(triggers)
    return record


class TeamCase(unittest.TestCase):
    def copy_newsletter(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "newsletter-team"
        shutil.copytree(NEWSLETTER, root)
        return root

    @staticmethod
    def write_record(root: Path, *flows: dict) -> None:
        (root / "docs").mkdir(exist_ok=True)
        (root / "docs/work-shape.json").write_text(json.dumps({"flows": list(flows)}), encoding="utf-8")

    @staticmethod
    def verdicts(root: Path, surface: str = "claude") -> dict[str, tuple[str, str]]:
        _, checks = shape.evaluate(root, surface)
        return {check_id: (verdict, evidence) for check_id, _, verdict, evidence in checks}

    @staticmethod
    def run_claude_validator(root: Path) -> tuple[int, dict[str, str]]:
        result = subprocess.run(["sh", str(CLAUDE_VALIDATOR), str(root)], capture_output=True, text=True, check=False)
        lines = {line.split()[0]: line for line in result.stdout.splitlines() if " | " in line}
        return result.returncode, lines

    @staticmethod
    def run_codex_validator(root: Path) -> tuple[int, dict[str, str]]:
        output = io.StringIO()
        with (
            contextlib.redirect_stdout(output),
            # Never shell out to a Codex CLI from tests; a team with no config has nothing to check.
            mock.patch.object(codex_validator, "run_strict_config", return_value=(False, "codex CLI not run in tests")),
        ):
            code = codex_validator.main([str(root)])
        lines = {line.split()[0]: line for line in output.getvalue().splitlines() if " | " in line}
        return code, lines

    def make_group(self, root: Path) -> None:
        """Turn the newsletter into the smallest group: an editor and a fresh-context source checker."""
        agents = root / ".claude/agents"
        (agents / "review").mkdir(parents=True)
        (agents / "editor.md").write_text(
            AGENT.format(name="Editor", description="Write the issue and hand it to the source checker.",
                         body="Draft the issue with the weekly-newsletter skill, then dispatch the source checker."),
            encoding="utf-8",
        )
        (agents / "review/source-checker.md").write_text(
            AGENT.format(name="Source Checker", description="Check each claim against its source from fresh context.",
                         body="Open every source. Report claims the source does not support."),
            encoding="utf-8",
        )
        entry = root / ".claude/skills/newsletter/SKILL.md"
        entry.parent.mkdir(parents=True)
        entry.write_text(ENTRY_SKILL, encoding="utf-8")
        (root / ".claude/rules").mkdir()
        (root / ".claude/rules/handoff-contract.md").write_text(HANDOFF_RULE, encoding="utf-8")
        claude_md = root / "CLAUDE.md"
        claude_md.write_text(
            claude_md.read_text(encoding="utf-8").replace(
                "## Gotchas",
                "## Deployment\n\nThe editor runs in the main session and dispatches the source checker.\n\n## Gotchas",
            ),
            encoding="utf-8",
        )


class ShapeRuleTests(TeamCase):
    def test_no_trigger_means_one_skill_workflow(self) -> None:
        self.assertEqual(shape.expected_shape(flow("f", "skill-workflow")), "skill-workflow")
        for trigger in shape.TRIGGERS:
            with self.subTest(trigger=trigger):
                self.assertEqual(shape.expected_shape(flow("f", "agent-group", **{trigger: "evidence"})), "agent-group")

    def test_heavy_path_for_a_single_context_flow_fails(self) -> None:
        root = self.copy_newsletter()
        self.make_group(root)
        self.write_record(root, flow("weekly-newsletter", "agent-group"))

        verdict, evidence = self.verdicts(root)["W2"]
        self.assertEqual(verdict, "FAIL")
        self.assertIn("agent-group chosen for a single-context flow", evidence)
        code, lines = self.run_claude_validator(root)
        self.assertEqual(code, 1)
        self.assertIn("| FAIL |", lines["W2"])

    def test_skill_path_for_a_flow_that_needs_a_group_fails(self) -> None:
        for trigger in shape.TRIGGERS:
            with self.subTest(trigger=trigger):
                root = self.copy_newsletter()
                self.write_record(root, flow("weekly-newsletter", "skill-workflow", **{trigger: "evidence that the trigger applies"}))

                verdict, evidence = self.verdicts(root)["W2"]
                self.assertEqual(verdict, "FAIL")
                self.assertIn("skill-workflow chosen for a flow that needs a group", evidence)
                self.assertIn(trigger, evidence)
                code, lines = self.run_claude_validator(root)
                self.assertEqual(code, 1)
                self.assertIn("| FAIL |", lines["W2"])

    def test_one_group_flow_makes_the_team_a_group(self) -> None:
        flows = [flow("draft", "skill-workflow"), flow("fact-check", "agent-group", isolated_check="checker must not see the draft notes")]
        self.assertEqual(shape.team_profile(flows), "agent-group")
        self.assertEqual(shape.rule_problems(flows), [])

    def test_malformed_record_fails_instead_of_passing_as_legacy(self) -> None:
        root = self.copy_newsletter()
        bad = flow("weekly-newsletter", "agent-group")
        bad["parallel"] = True
        self.write_record(root, bad)
        verdict, evidence = self.verdicts(root)["W1"]
        self.assertEqual(verdict, "FAIL")
        self.assertIn("parallel must be evidence text", evidence)

        (root / "docs/work-shape.json").write_text("{not json", encoding="utf-8")
        self.assertEqual(self.verdicts(root)["W1"][0], "FAIL")

    def test_record_is_required_from_the_cutover_stamp(self) -> None:
        root = self.copy_newsletter()
        (root / "docs/work-shape.json").unlink()
        verdict, evidence = self.verdicts(root)["W1"]
        self.assertEqual(verdict, "FAIL")
        self.assertIn(shape.RECORD_REQUIRED_SINCE, evidence)

        claude_md = root / "CLAUDE.md"
        claude_md.write_text(claude_md.read_text(encoding="utf-8").replace("2026-11-26", "2026-10-06"), encoding="utf-8")
        profile, checks = shape.evaluate(root)
        self.assertEqual(profile, "legacy")
        self.assertEqual([verdict for _, _, verdict, _ in checks], ["SKIP", "SKIP", "SKIP"])


class TreeMatchesRecordTests(TeamCase):
    def test_skill_workflow_record_with_a_roster_fails(self) -> None:
        root = self.copy_newsletter()
        self.make_group(root)

        verdict, evidence = self.verdicts(root)["W3"]
        self.assertEqual(verdict, "FAIL")
        self.assertIn("the tree defines 2 agents", evidence)

    def test_group_record_without_a_group_fails(self) -> None:
        root = self.copy_newsletter()
        self.write_record(root, flow("weekly-newsletter", "agent-group", isolated_check="no owner approval before sending"))

        verdict, evidence = self.verdicts(root)["W3"]
        self.assertEqual(verdict, "FAIL")
        self.assertIn("a group needs a coordinator and at least one more agent", evidence)

    def test_skill_workflow_record_without_a_skill_fails(self) -> None:
        root = self.copy_newsletter()
        shutil.rmtree(root / ".claude/skills")
        self.assertIn("no skill to load", self.verdicts(root)["W3"][1])


class RealFlowTests(TeamCase):
    def test_newsletter_is_one_skill_workflow_and_ships_without_the_rule_pack(self) -> None:
        code, lines = self.run_claude_validator(NEWSLETTER)
        self.assertEqual(code, 0, "\n".join(lines.values()))
        for check in ("W1", "W2", "W3", "C5", "D1", "J3", "O1", "O2"):
            self.assertIn("| PASS |", lines[check])
        # The old pack is not required and is not there.
        for check in ("R1", "R2", "R3", "R4", "E1", "F3", "F4", "X1"):
            self.assertIn("| SKIP |", lines[check])
        self.assertFalse((NEWSLETTER / ".claude/rules").exists())
        self.assertFalse((NEWSLETTER / ".claude/agents").exists())

    def test_newsletter_keeps_the_safety_baseline(self) -> None:
        settings = json.loads((NEWSLETTER / ".claude/settings.json").read_text(encoding="utf-8"))
        baseline = json.loads((REPO_ROOT / ".claude/templates/settings-baseline.json").read_text(encoding="utf-8"))
        self.assertEqual(settings["permissions"]["deny"], baseline["permissions"]["deny"])
        self.assertEqual(settings["permissions"]["ask"], baseline["permissions"]["ask"])
        self.assertEqual(
            (NEWSLETTER / ".claude/output-styles/adhd-friendly.md").read_bytes(),
            (REPO_ROOT / ".claude/output-styles/adhd-friendly.md").read_bytes(),
        )

    def test_newsletter_is_recognised_by_the_codex_validator_as_a_claude_team(self) -> None:
        code, lines = self.run_codex_validator(NEWSLETTER)
        self.assertEqual(code, 0, "\n".join(lines.values()))
        self.assertIn("class=Claude-only", lines["G1"])
        self.assertIn("| PASS |", lines["W2"])

    def test_a_team_optimization_lane_is_a_group_because_of_the_isolated_check(self) -> None:
        flows, error = shape.load_record(REPO_ROOT)
        self.assertIsNone(error)
        lane = next(item for item in flows if item["name"] == "text-only-optimization")
        self.assertEqual(lane["shape"], "agent-group")
        self.assertEqual(shape.triggers_of(lane), ["isolated_check"])
        for surface in ("claude", "codex"):
            with self.subTest(surface=surface):
                self.assertEqual({verdict for verdict, _ in self.verdicts(REPO_ROOT, surface).values()}, {"PASS"})

        # Choosing the skill path for it is caught.
        lane["shape"] = "skill-workflow"
        self.assertIn("skill-workflow chosen for a flow that needs a group", shape.rule_problems(flows)[0])


class LeanPackTests(TeamCase):
    def test_smallest_group_needs_only_a_handoff_contract(self) -> None:
        root = self.copy_newsletter()
        self.make_group(root)
        self.write_record(root, flow("weekly-newsletter", "agent-group", isolated_check="the owner no longer reads drafts before they are sent"))

        code, lines = self.run_claude_validator(root)
        self.assertEqual(code, 0, "\n".join(lines.values()))
        for check in ("W2", "W3", "S3", "C2", "E1", "E5", "F1", "R4", "R5"):
            self.assertIn("| PASS |", lines[check])
        # Worklog, context-management and reasoning rules, the CLAUDE.md worklog
        # and precedence sections, and the agent section floor are not copied forward.
        for check in ("R1", "R2", "R3", "C3", "C4", "F3", "F4", "X1"):
            self.assertIn("| SKIP |", lines[check])

    def test_group_without_a_handoff_contract_fails(self) -> None:
        root = self.copy_newsletter()
        self.make_group(root)
        self.write_record(root, flow("weekly-newsletter", "agent-group", isolated_check="unreviewed sending"))
        (root / ".claude/rules/handoff-contract.md").unlink()

        code, lines = self.run_claude_validator(root)
        self.assertEqual(code, 1)
        self.assertIn("| FAIL |", lines["R4"])

    def test_team_without_a_record_is_still_checked_against_the_contract_it_was_built_under(self) -> None:
        root = self.copy_newsletter()
        self.make_group(root)
        (root / "docs/work-shape.json").unlink()
        claude_md = root / "CLAUDE.md"
        claude_md.write_text(claude_md.read_text(encoding="utf-8").replace("2026-11-26", "2026-10-06"), encoding="utf-8")

        code, lines = self.run_claude_validator(root)
        self.assertEqual(code, 1)
        for check in ("R1", "F3"):
            self.assertIn("| FAIL |", lines[check])

    def test_codex_skill_workflow_team_needs_no_registry(self) -> None:
        root = self.copy_newsletter()
        skill = root / ".claude/skills/weekly-newsletter"
        for target in (".agents/skills", ".codex/skills"):
            shutil.copytree(skill, root / target / "weekly-newsletter")
        shutil.rmtree(root / ".claude")
        text = (root / "CLAUDE.md").read_text(encoding="utf-8")
        (root / "CLAUDE.md").unlink()
        (root / "AGENTS.md").write_text(
            text.replace("`.claude/` is the canonical source design; there is no Codex surface.",
                         "Codex is the canonical authored format. canonical_roots: .codex/"),
            encoding="utf-8",
        )

        code, lines = self.run_codex_validator(root)
        self.assertEqual(code, 0, "\n".join(lines.values()))
        self.assertIn("class=Codex-only", lines["G1"])
        for check in ("W1", "W2", "W3", "G3", "G8"):
            self.assertIn("| PASS |", lines[check])
        self.assertIn("| SKIP |", lines["G4"])

        # The same Codex tree with a group record and no registry is not runnable.
        self.write_record(root, flow("weekly-newsletter", "agent-group", parallel="three researchers at once"))
        code, lines = self.run_codex_validator(root)
        self.assertEqual(code, 1)
        self.assertIn("| FAIL |", lines["W3"])
        self.assertIn("| FAIL |", lines["G1"])


if __name__ == "__main__":
    unittest.main()
