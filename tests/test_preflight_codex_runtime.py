#!/usr/bin/env python3
"""Provider-free coverage for preflight context and strict evidence reuse."""

from __future__ import annotations

import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = REPO_ROOT / "scripts" / "preflight-codex-runtime.sh"
VALIDATOR = REPO_ROOT / "scripts" / "validate_codex_team.py"
LIVE_TOOLS = "spawn_agent,send_message,followup_task,wait_agent,interrupt_agent,list_agents"


class PreflightCodexRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.temporary_path = Path(temporary_directory.name)
        self.caller_path = self.temporary_path / "caller"
        self.target_path = self.temporary_path / "target with spaces"
        self.fake_bin = self.temporary_path / "bin"
        self.log_path = self.temporary_path / "codex.log"
        for path in (self.caller_path, self.target_path, self.fake_bin):
            path.mkdir()

        fake_codex = self.fake_bin / "codex"
        fake_codex.write_text(
            f"#!{sys.executable}\n" + textwrap.dedent(
                """\
                import os
                from pathlib import Path
                import sys

                arguments = sys.argv[1:]
                context = Path.cwd()
                if arguments[:1] == ["-C"]:
                    context = Path(arguments[1]).resolve()
                    arguments = arguments[2:]
                operation = "exec" if arguments[:1] == ["exec"] else " ".join(arguments)
                with open(os.environ["FAKE_CODEX_LOG"], "a", encoding="utf-8") as log:
                    log.write(f"{operation}|{context}\\n")
                if arguments == ["--version"]:
                    print("codex fake 1.0")
                elif arguments[:1] == ["doctor"]:
                    print(f"  ✓ sandbox {context}")
                    print(f"      config.toml {context}")
                elif arguments[:2] == ["features", "list"]:
                    print(f"multi_agent_v2 stable true {context}")
                else:
                    print("CONFIG_OK")
                    if os.environ.get("FAKE_CODEX_DIAGNOSTIC"):
                        print(os.environ["FAKE_CODEX_DIAGNOSTIC"], file=sys.stderr)
                    raise SystemExit(int(os.environ.get("FAKE_CODEX_EXIT", "0")))
                """
            ),
            encoding="utf-8",
        )
        fake_codex.chmod(0o755)

        # Keep shell probes real, isolating unrelated team checks while using
        # the production strict runner against our fake Codex binary.
        fake_python = self.fake_bin / "python3"
        fake_python.write_text(
            f"#!{sys.executable}\n" + textwrap.dedent(
                f"""\
                import importlib.util
                import os
                from pathlib import Path
                import sys

                if sys.argv[1:3] != ["-B", {str(VALIDATOR)!r}]:
                    os.execv({sys.executable!r}, [{sys.executable!r}, *sys.argv[1:]])
                print("P0 fake-validator | PASS | isolated regression validator")
                if "FAKE_VALIDATOR_RECORDS" in os.environ:
                    print(os.environ["FAKE_VALIDATOR_RECORDS"])
                    raise SystemExit(int(os.environ.get("FAKE_VALIDATOR_EXIT", "0")))
                spec = importlib.util.spec_from_file_location("fixture_validator", {str(VALIDATOR)!r})
                module = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)
                repo_self = "--repo-self" in sys.argv
                target = module.REPO_ROOT if repo_self else Path(sys.argv[3])
                ok, evidence = module.run_strict_config(target)
                criterion, name = ("R2", "strict-config") if repo_self else ("G2", "target-strict-config")
                verdict = "PASS" if ok else "FAIL"
                print(f"{{criterion}} {{name}} | {{verdict}} | {{evidence}}")
                raise SystemExit(0 if ok else 1)
                """
            ),
            encoding="utf-8",
        )
        fake_python.chmod(0o755)
        self.environment = os.environ.copy()
        self.environment.pop("CODEX_PREFLIGHT_LIVE_TOOLS", None)
        self.environment.update({
            "PATH": f"{self.fake_bin}{os.pathsep}{self.environment['PATH']}",
            "FAKE_CODEX_LOG": str(self.log_path),
            "PYTHONDONTWRITEBYTECODE": "1",
        })

    def run_preflight(self, repo_self: bool = False, **environment: str) -> subprocess.CompletedProcess[str]:
        target_arguments = ["--repo-self"] if repo_self else ["--team-dir", str(self.target_path)]
        return subprocess.run(
            [str(PREFLIGHT), *target_arguments],
            cwd=self.caller_path,
            env={**self.environment, **environment},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_team_and_repo_self_probe_their_target_with_one_fresh_strict_call(self) -> None:
        for repo_self, target, criterion in ((False, self.target_path, "G2"), (True, REPO_ROOT, "R2")):
            with self.subTest(repo_self=repo_self):
                result = self.run_preflight(repo_self)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f"reused validator {criterion}: CONFIG_OK", result.stdout)
                self.assertIn(f"multi_agent_v2 stable true {target.resolve()}", result.stdout)
        observed = [line.split("|", 1) for line in self.log_path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(
            observed,
            [[operation, str(target)] for target in (self.target_path.resolve(), REPO_ROOT)
             for operation in ("--version", "doctor", "features list", "exec")],
        )
        # Each subsequent run must consume fresh strict evidence, including failure.
        failed = self.run_preflight(FAKE_CODEX_EXIT="9")
        self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
        self.assertIn("P1 strict-config | FAIL | reused validator G2:", failed.stdout)
        strict_calls = [line for line in self.log_path.read_text(encoding="utf-8").splitlines() if line.startswith("exec|")]
        self.assertEqual(len(strict_calls), 3)

    def test_emitted_setup_and_verify_use_one_quoted_preflight_and_scoped_rollback(self) -> None:
        quoted_target = self.temporary_path / "target 'quoted'; $(exit 73)"
        self.target_path.rename(quoted_target)
        self.target_path = quoted_target
        for repo_self, target in ((False, self.target_path), (True, REPO_ROOT)):
            with self.subTest(repo_self=repo_self):
                result = self.run_preflight(repo_self)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                setup = re.search(r"## Setup\n\n```sh\n(.*?)```", result.stdout, re.DOTALL)
                verify = re.search(r"## Verify\n\n```sh\n(.*?)```", result.stdout, re.DOTALL)
                self.assertIsNotNone(setup)
                self.assertIsNotNone(verify)
                self.assertEqual(
                    [shlex.split(line) for line in setup[1].splitlines()],
                    [["codex", "-C", str(target), "--version"],
                     ["codex", "-C", str(target), "features", "list"]],
                )
                arguments = ["--repo-self"] if repo_self else ["--team-dir", str(target)]
                self.assertEqual(
                    [shlex.split(line) for line in verify[1].splitlines()],
                    [[str(PREFLIGHT), *arguments]],
                )
                self.assertIn("includes the validator and one strict-config execution", result.stdout)
                rollback = result.stdout.split("## Rollback\n", 1)[1]
                self.assertIn("Preserve the current worktree and concurrent edits", rollback)
                self.assertIn("scoped preimages", rollback)
                self.assertNotIn("restore those files from version control", rollback)

    def test_redacted_failure_is_reused_and_raw_diagnostics_are_not_emitted(self) -> None:
        result = self.run_preflight(
            FAKE_CODEX_DIAGNOSTIC="WARN malformed agent configuration token=super-secret",
            CODEX_PREFLIGHT_LIVE_TOOLS=LIVE_TOOLS,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("P1 strict-config | FAIL | reused validator G2:", result.stdout)
        self.assertIn("malformed agent configuration token=<redacted>", result.stdout)
        self.assertNotIn("super-secret", result.stdout + result.stderr)
        self.assertIn("host-tools=v2-ready", result.stdout)

    def test_missing_malformed_skipped_and_duplicate_strict_records_fail_closed(self) -> None:
        for repo_self, criterion, name in ((False, "G2", "target-strict-config"), (True, "R2", "strict-config")):
            valid = f"{criterion} {name} | PASS | CONFIG_OK"
            for records in (
                "raw log token=do-not-emit",
                f"{criterion} {name} | PASS | ",
                f"{criterion} {name} | MAYBE | CONFIG_OK",
                f"{criterion} wrong-name | PASS | CONFIG_OK",
                f"{criterion} {name} | SKIP | not applicable",
                valid + "\n" + valid,
            ):
                with self.subTest(repo_self=repo_self, records=records):
                    result = self.run_preflight(repo_self, FAKE_VALIDATOR_RECORDS=records)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(f"P1 strict-config | FAIL | validator {criterion} evidence", result.stdout)
                    self.assertNotIn("do-not-emit", result.stdout + result.stderr)

    def test_validator_exit_and_strict_failure_each_override_live_tool_success(self) -> None:
        for records, validator_exit in (
            ("G2 target-strict-config | PASS | CONFIG_OK", "7"),
            ("G2 target-strict-config | FAIL | rejected config", "0"),
        ):
            with self.subTest(records=records):
                result = self.run_preflight(
                    FAKE_VALIDATOR_RECORDS=records,
                    FAKE_VALIDATOR_EXIT=validator_exit,
                    CODEX_PREFLIGHT_LIVE_TOOLS=LIVE_TOOLS,
                )
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("host-tools=v2-ready", result.stdout)

    def test_missing_codex_binary_preserves_failure_evidence(self) -> None:
        (self.fake_bin / "codex").unlink()
        for command in ("bash", "dirname", "basename", "mktemp", "rm", "awk", "head", "tr", "sed", "grep", "uname", "date", "cat"):
            path = shutil.which(command)
            self.assertIsNotNone(path, command)
            (self.fake_bin / command).symlink_to(path)
        result = self.run_preflight(PATH=str(self.fake_bin))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("P1 strict-config | FAIL | reused validator G2: codex binary not found in PATH", result.stdout)


if __name__ == "__main__":
    unittest.main()
