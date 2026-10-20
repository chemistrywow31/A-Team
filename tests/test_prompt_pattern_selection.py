#!/usr/bin/env python3
"""Exercise the real selector and the instructions it makes reachable."""

from pathlib import Path
import subprocess
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SELECTOR = REPO_ROOT / ".grok/skills/prompt-patterns/select.py"


class PromptPatternSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payloads: dict[str, str] = {}
        # The three generation routes plus tags covering long-running/coding
        # templates exercise loaded contents, not just metadata declarations.
        cls.selections: dict[str, list[str]] = {}
        queries = [
            ("--scenario", "generating-research-agent"),
            ("--scenario", "generating-coordinator"),
            ("--scenario", "writing-skill-prompts"),
            ("--tags", "coding,thinking,multi-window,testing"),
        ]
        for flag, value in queries:
            result = subprocess.run(
                [sys.executable, "-B", str(SELECTOR), flag, value],
                cwd=REPO_ROOT, text=True, capture_output=True, check=False,
            )
            if result.returncode:
                raise AssertionError(result.stdout + result.stderr)
            paths = result.stdout.splitlines()
            cls.selections[value] = paths
            for path in paths:
                cls.payloads[path] = (REPO_ROOT / path).read_text(encoding="utf-8")

    def payload(self, suffix: str) -> str:
        matches = [text for path, text in self.payloads.items() if path.endswith(suffix)]
        self.assertEqual(len(matches), 1, f"expected selected payload {suffix}")
        return matches[0]

    def test_default_scenarios_and_tags_exclude_historical_advice(self) -> None:
        for route, paths in self.selections.items():
            with self.subTest(route=route):
                self.assertTrue(paths)
                self.assertEqual(len(paths), len(set(paths)))
                self.assertFalse(any("/claude-4-patterns/" in path or "/raw/" in path for path in paths))
        # The archive is retained; default exclusion must not mean deletion.
        self.assertTrue((REPO_ROOT / "reference/platform-sources/.claude/skills/prompt-patterns/assets/claude-4-patterns/adaptive-thinking.md").is_file())

    def test_selected_instructions_remove_reproduced_conflicts(self) -> None:
        obsolete_directives = (
            "the reasoning must be externalized",
            "Include a `<thinking>` or `<reasoning>` step before every decision output",
            "Show the scratchpad work, not just the final answer",
            "all execution goes through Task dispatch",
            "yields ~30% quality improvement",
            "Query at end = 30% quality improvement",
            "must wrap every variable input section",
            "must use XML tags in all SKILL.md examples",
            "exactly one rejection-case example",
            "allowing you to continue working indefinitely",
            "Never artificially stop any task early regardless of the context remaining",
            "Do not create helper scripts or workarounds",
            "It is unacceptable to remove or edit tests",
            "For haiku-based agents, this block is less necessary since haiku naturally uses minimal thinking",
        )
        for path, payload in self.payloads.items():
            with self.subTest(path=path):
                for obsolete in obsolete_directives:
                    self.assertNotIn(obsolete, payload)

    def test_useful_structures_grounding_and_native_thinking_distinctions_remain(self) -> None:
        thinking = self.payload("advanced-techniques/chain-of-thought.md")
        self.assertRegex(thinking.lower(), r"native.*thinking|adaptive thinking")
        self.assertRegex(thinking.lower(), r"thinking (?:disabled|is disabled)")
        self.assertIn("240 / 20 = 12", thinking)  # public, checkable worked result
        xml = self.payload("advanced-techniques/xml-tag-separation.md")
        self.assertRegex(xml, r"<document(?:\s[^>]*)?>")
        self.assertIn("</document>", xml)
        self.assertRegex(xml.lower(), r"data|untrusted")
        examples = self.payload("advanced-techniques/few-shot-patterns.md")
        self.assertRegex(examples.lower(), r"positive|success|accepted")
        self.assertRegex(examples.lower(), r"boundary|reject|defer")
        grounding = self.payload("advanced-techniques/anti-hallucination.md")
        self.assertRegex(grounding.lower(), r"missing|insufficient|unavailable")
        self.assertRegex(grounding.lower(), r"citation|cite|source")
        dispatch = self.payload("context-strategies/sub-agent-dispatch.md")
        self.assertIn("spawn_subagent", dispatch)
        self.assertIn(".grok/policies/context-isolation.md", dispatch)
        self.assertIn("without `resume_from`", dispatch)
        self.assertNotIn(".codex/rules/", dispatch)
        self.assertRegex(dispatch.lower(), r"owned|ownership")
        self.assertRegex(dispatch.lower(), r"acceptance|completion")

    def test_selected_long_running_and_action_templates_preserve_real_limits(self) -> None:
        context = self.payload("templates/context-awareness.md").lower()
        self.assertRegex(context, r"budget|limit")
        self.assertRegex(context, r"stop|pause|handoff|handover")
        safety = self.payload("templates/autonomy-safety.md").lower()
        self.assertRegex(safety, r"already authorized|existing authorization|prior authorization|authorization already supplied")
        self.assertRegex(safety, r"uncovered|not covered by that authorization|outside.*scope|scope expansion")
        multi_window = self.payload("context-strategies/multi-window-workflow.md").lower()
        self.assertRegex(multi_window, r"test|verification")
        self.assertRegex(multi_window, r"proportion|relevant|meaningful|applicable|affected files")


if __name__ == "__main__":
    unittest.main()
