#!/usr/bin/env python3
"""Regression coverage for target-context Codex runtime probes."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = REPO_ROOT / "scripts" / "preflight-codex-runtime.sh"


class PreflightCodexRuntimeTests(unittest.TestCase):
    def test_team_live_probes_use_target_context_and_repo_self_uses_caller(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            caller_path = temporary_path / "caller"
            target_path = temporary_path / "target"
            fake_bin = temporary_path / "bin"
            log_path = temporary_path / "codex.log"
            for path, marker in ((caller_path, "caller-config"), (target_path, "target-config")):
                path.mkdir()
                (path / "config-marker").write_text(marker, encoding="utf-8")
            fake_bin.mkdir()

            fake_codex = fake_bin / "codex"
            fake_codex.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    import os
                    from pathlib import Path
                    import sys

                    arguments = sys.argv[1:]
                    context = Path.cwd()
                    if arguments[:1] == ["-C"]:
                        context = Path(arguments[1]).resolve()
                        arguments = arguments[2:]
                    marker = (context / "config-marker").read_text(encoding="utf-8").strip()
                    if arguments == ["--version"]:
                        print("codex fake 1.0")
                        raise SystemExit(0)
                    operation = "exec" if arguments[:1] == ["exec"] else " ".join(arguments)
                    with open(os.environ["FAKE_CODEX_LOG"], "a", encoding="utf-8") as log:
                        log.write(f"{operation}|{context}|{marker}\\n")
                    if arguments[:1] == ["doctor"]:
                        print(f"  ✓ sandbox {marker}")
                        print(f"      config.toml {marker}")
                    elif arguments[:2] == ["features", "list"]:
                        print(f"multi_agent {marker}")
                    else:
                        print(f"CONFIG_OK {marker}")
                    """
                ),
                encoding="utf-8",
            )
            fake_codex.chmod(0o755)

            fake_python = fake_bin / "python3"
            fake_python.write_text(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env sh
                    if [ "${{2:-}}" = "{REPO_ROOT / 'scripts' / 'validate_codex_team.py'}" ]; then
                      printf 'P0 fake-validator | PASS | isolated regression validator\\n'
                      exit 0
                    fi
                    exec "{sys.executable}" "$@"
                    """
                ),
                encoding="utf-8",
            )
            fake_python.chmod(0o755)

            environment = os.environ.copy()
            environment.update(
                {
                    "PATH": f"{fake_bin}{os.pathsep}{environment['PATH']}",
                    "FAKE_CODEX_LOG": str(log_path),
                    "CODEX_HOME": str(temporary_path / "codex-home"),
                }
            )

            team_run = subprocess.run(
                [str(PREFLIGHT), "--team-dir", str(target_path)],
                cwd=caller_path,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(team_run.returncode, 0, team_run.stdout + team_run.stderr)
            self.assertIn("multi_agent target-config", team_run.stdout)

            repo_self_run = subprocess.run(
                [str(PREFLIGHT), "--repo-self"],
                cwd=caller_path,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(repo_self_run.returncode, 0, repo_self_run.stdout + repo_self_run.stderr)
            self.assertIn("multi_agent caller-config", repo_self_run.stdout)

            observed = [line.split("|", 2) for line in log_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(
                observed,
                [
                    ["doctor", str(target_path.resolve()), "target-config"],
                    ["features list", str(target_path.resolve()), "target-config"],
                    ["exec", str(target_path.resolve()), "target-config"],
                    ["doctor", str(caller_path.resolve()), "caller-config"],
                    ["features list", str(caller_path.resolve()), "caller-config"],
                    ["exec", str(caller_path.resolve()), "caller-config"],
                ],
            )


if __name__ == "__main__":
    unittest.main()
