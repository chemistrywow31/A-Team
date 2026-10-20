#!/usr/bin/env python3
"""Optional paid Grok trigger evaluation; opt-in, bounded, no trust/auth changes.

Uses one native proxy skill per batch and native read_file completion events.
This measures description-triggered reads, not the quality of the skill's output.
Command/event fixtures are tested; effective installed model behavior NOT_PROBED.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import yaml
from scripts.utils import grok_command, parse_native_stream, parse_skill_md


def find_project_root() -> Path:
    current = Path.cwd().resolve()
    for parent in (current, *current.parents):
        if (parent / ".git").exists():
            return parent
    return current


def require_discovered_skill(project_root: Path, name: str, skill_file: Path):
    """Read-only inspect: untrusted/missing/wrong-source never becomes a negative pass."""
    command = [os.environ.get("GROK_SKILL_CLI", "grok"), "inspect", "--json"]
    result = subprocess.run(command, cwd=project_root, capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise RuntimeError("Grok inspect failed; no model calls were started")
    report = json.loads(result.stdout)
    if report.get("projectTrusted") is not True:
        raise RuntimeError("Evaluation project is untrusted; arrange trust separately, then rerun")
    if Path(report.get("projectRoot", "")).resolve() != project_root.resolve():
        raise RuntimeError("Inspect projectRoot does not match the explicit evaluation root")
    found = [s for s in report.get("skills", []) if s.get("name") == name]
    if len(found) != 1 or Path(found[0].get("source", {}).get("path", "")).resolve() != skill_file.resolve():
        raise RuntimeError("Native evaluation skill missing or wrong-source in inspect")


def run_single_query(query: str, skill_file: Path, timeout: int,
                     project_root: Path, model: str | None = None) -> bool:
    result = subprocess.run(grok_command(query=query, model=model), cwd=project_root,
                            capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"Grok process failed (exit {result.returncode}); result unverified")
    return parse_native_stream(result.stdout, skill_file, project_root)["triggered"]


def validate_eval_set(eval_set):
    if not isinstance(eval_set, list) or not eval_set:
        raise ValueError("Evaluation set must be a nonempty list")
    queries = set()
    for item in eval_set:
        if not isinstance(item, dict) or not isinstance(item.get("query"), str) or not item["query"].strip() or type(item.get("should_trigger")) is not bool:
            raise ValueError("Each item requires nonempty query and boolean should_trigger")
        if item["query"] in queries:
            raise ValueError("Duplicate queries would corrupt train/test separation")
        queries.add(item["query"])


def run_eval(eval_set: list[dict], skill_name: str, description: str, num_workers: int,
             timeout: int, project_root: Path, runs_per_query: int = 1,
             trigger_threshold: float = 0.5, model: str | None = None,
             allow_model_calls: bool = False) -> dict:
    if not allow_model_calls:
        raise ValueError("Paid model calls require explicit allow_model_calls/--allow-model-calls")
    validate_eval_set(eval_set)
    if min(num_workers, timeout, runs_per_query) < 1 or not 0 < trigger_threshold <= 1:
        raise ValueError("Invalid evaluation bounds")
    project_root = Path(project_root).resolve()
    # Require a caller-chosen evaluation repository; never install in global skills.
    if not (project_root / ".git").exists() or not (project_root / ".grok").is_dir():
        raise ValueError("Choose an existing native evaluation repository with .git and .grok")
    name = f"eval-{uuid.uuid4().hex[:12]}"
    skill_dir = project_root / ".grok" / "skills" / name
    if not skill_dir.resolve().is_relative_to(project_root):
        raise ValueError("Evaluation skill parent escapes project root")
    skill_dir.mkdir(parents=True, exist_ok=False)
    skill_file = skill_dir / "SKILL.md"
    triggers = {item["query"]: [] for item in eval_set}
    errors = {item["query"]: [] for item in eval_set}
    try:
        skill_file.write_text("---\n" + yaml.safe_dump({"name": name, "description": description}, sort_keys=False) + "---\n\n# " + skill_name + "\n\nThis is a trigger-only evaluation proxy. Report that the matching skill was consulted.\n", encoding="utf-8")
        require_discovered_skill(project_root, name, skill_file)
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = {executor.submit(run_single_query, item["query"], skill_file, timeout, project_root, model): item["query"]
                       for item in eval_set for _ in range(runs_per_query)}
            for future in as_completed(futures):
                query = futures[future]
                try:
                    triggers[query].append(future.result())
                except Exception as exc:
                    errors[query].append(f"{type(exc).__name__}: {exc}")
    finally:
        # Only this invocation's uniquely created proxy, never another skill.
        shutil.rmtree(skill_dir)
    results = []
    for item in eval_set:
        query = item["query"]
        runs = triggers[query]
        rate = sum(runs) / len(runs) if runs else None
        valid = not errors[query] and len(runs) == runs_per_query
        passed = valid and ((rate >= trigger_threshold) if item["should_trigger"] else (rate < trigger_threshold))
        results.append({**item, "trigger_rate": rate, "triggers": sum(runs), "runs": len(runs),
                        "requested_runs": runs_per_query, "pass": bool(passed),
                        "status": "MEASURED" if valid else "UNVERIFIED", "errors": errors[query]})
    passed = sum(r["pass"] for r in results)
    unverified = sum(r["status"] == "UNVERIFIED" for r in results)
    return {"skill_name": skill_name, "description": description, "results": results,
            "summary": {"total": len(results), "passed": passed, "failed": len(results)-passed, "unverified": unverified},
            "measurement": "completed native read_file of description-only proxy; not output quality",
            "model_requested": model, "effective_model": "NOT_OBSERVED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-set", required=True)
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--project-root", required=True, help="Explicit native evaluation repository, already trusted")
    parser.add_argument("--description")
    parser.add_argument("--num-workers", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--runs-per-query", type=int, default=1)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--model", help="Optional verified target model ID; omission preserves client default")
    parser.add_argument("--allow-model-calls", action="store_true", help="Explicit opt-in to paid calls")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if not args.allow_model_calls:
        parser.error("--allow-model-calls is required; no model calls were made")
    name, description, _ = parse_skill_md(Path(args.skill_path))
    output = run_eval(json.loads(Path(args.eval_set).read_text()), name, args.description or description,
                      args.num_workers, args.timeout, Path(args.project_root), args.runs_per_query,
                      args.trigger_threshold, args.model, allow_model_calls=True)
    print(json.dumps(output, indent=2))
    return 2 if output["summary"]["unverified"] else (0 if not output["summary"]["failed"] else 1)


if __name__ == "__main__":
    sys.exit(main())
