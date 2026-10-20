#!/usr/bin/env bash
# Read-only Codex runtime preflight for repo-self and generated-team surfaces.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

MODE=""
TARGET_DIR=""
OUT_FILE=""
LIVE_TOOLS="${CODEX_PREFLIGHT_LIVE_TOOLS:-}"

usage() {
  cat <<'EOF'
Usage:
  scripts/preflight-codex-runtime.sh --repo-self [--live-tools a,b,c] [--out path]
  scripts/preflight-codex-runtime.sh --team-dir teams/{name} [--live-tools a,b,c] [--out path]

Read-only: this script never edits runtime config or user-scope files.
It probes the current Codex host, runs the Codex validator (including one strict
config execution), and emits a Markdown advisory to stdout or --out.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --repo-self)
      MODE="repo-self"
      shift
      ;;
    --team-dir)
      MODE="team"
      TARGET_DIR="${2:-}"
      shift 2
      ;;
    --live-tools)
      LIVE_TOOLS="${2:-}"
      shift 2
      ;;
    --out)
      OUT_FILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

[ -n "$MODE" ] || { usage >&2; exit 2; }
if [ "$MODE" = "team" ]; then
  [ -n "$TARGET_DIR" ] || { echo "--team-dir requires a path" >&2; exit 2; }
  [ -d "$TARGET_DIR" ] || { echo "team dir not found: $TARGET_DIR" >&2; exit 2; }
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 2
fi

TARGET_LABEL="A-Team repo-self"
TARGET_PATH="$REPO_ROOT"
VALIDATOR_CMD=(python3 -B "$SCRIPT_DIR/validate_codex_team.py" --repo-self)
STRICT_CRITERION="R2"
STRICT_NAME="strict-config"
if [ "$MODE" = "team" ]; then
  TARGET_LABEL=$(basename "$TARGET_DIR")
  TARGET_PATH=$(cd "$TARGET_DIR" && pwd)
  VALIDATOR_CMD=(python3 -B "$SCRIPT_DIR/validate_codex_team.py" "$TARGET_PATH")
  STRICT_CRITERION="G2"
  STRICT_NAME="target-strict-config"
fi

printf -v STRICT_DISPLAY_CMD "codex -C %q exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral 'Reply with CONFIG_OK only.'" "$TARGET_PATH"

TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/codex-preflight.XXXXXX")
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

VERSION_FILE="$TMP_DIR/version.txt"
DOCTOR_FILE="$TMP_DIR/doctor.txt"
FEATURES_FILE="$TMP_DIR/features.txt"
VALIDATOR_FILE="$TMP_DIR/validator.txt"
STRICT_FILE="$TMP_DIR/strict.txt"
CRITERIA_FILE="$TMP_DIR/criteria.txt"
VALIDATOR_EXIT=0

if command -v codex >/dev/null 2>&1; then
  codex -C "$TARGET_PATH" --version >"$VERSION_FILE" 2>&1 || true
  codex -C "$TARGET_PATH" doctor >"$DOCTOR_FILE" 2>&1 || true
  codex -C "$TARGET_PATH" features list >"$FEATURES_FILE" 2>&1 || true
else
  printf 'codex binary not found in PATH\n' >"$VERSION_FILE"
  printf 'codex binary not found in PATH\n' >"$DOCTOR_FILE"
  printf 'codex binary not found in PATH\n' >"$FEATURES_FILE"
fi
if [ -n "$LIVE_TOOLS" ]; then
  CODEX_PREFLIGHT_LIVE_TOOLS="$LIVE_TOOLS" "${VALIDATOR_CMD[@]}" >"$VALIDATOR_FILE" 2>&1 || VALIDATOR_EXIT=$?
else
  "${VALIDATOR_CMD[@]}" >"$VALIDATOR_FILE" 2>&1 || VALIDATOR_EXIT=$?
fi

# Preserve only EC-3.6 criterion records in the advisory, never raw validator logs.
# Strict evidence is already redacted by the validator. Require exactly one
# record for this target and never turn SKIP, absent, or malformed evidence into PASS.
awk '$1 != "R2" && $1 != "G2" && /^[A-Za-z0-9_]+ [^|]+ \| (PASS|FAIL|SKIP|REVIEW_REQUIRED) \| /' "$VALIDATOR_FILE" >"$CRITERIA_FILE"
awk -v id="$STRICT_CRITERION" -v name="$STRICT_NAME" '
  $1 == id {
    count++
    if ($0 ~ ("^" id " " name " [|] (PASS|FAIL) [|] [^[:space:]]")) {
      record=$0
    }
  }
  END {
    if (count == 1 && record != "") {
      sub("^" id " " name, "P1 strict-config", record)
      sub(/ [|] (PASS|FAIL) [|] /, "&reused validator " id ": ", record)
      print record
    } else {
      print "P1 strict-config | FAIL | validator " id " evidence missing, malformed, skipped, or duplicated"
    }
  }
' "$VALIDATOR_FILE" >"$STRICT_FILE"

VERSION=$(head -1 "$VERSION_FILE" | tr '\n' ' ' | sed 's/  */ /g; s/^ //; s/ $//')
HOST_LINE=$(awk '/^  ✓ sandbox /{sub(/^  /,""); print; exit}' "$DOCTOR_FILE")
CONFIG_LINE=$(awk '/^      config\.toml/{sub(/^      /,""); print; exit}' "$DOCTOR_FILE")
FEATURE_LINES=$(grep '^multi_agent' "$FEATURES_FILE" 2>/dev/null || true)
STATIC_RESULT="PASS"
[ "$VALIDATOR_EXIT" -eq 0 ] || STATIC_RESULT="FAIL"
# An over-target authored file is pending an independent usefulness verdict.
# Keep that state visible even if a producer exits zero or supplies live tools.
if [ "$VALIDATOR_EXIT" -le 1 ] && grep -q ' | REVIEW_REQUIRED | ' "$CRITERIA_FILE"; then
  STATIC_RESULT="REVIEW_REQUIRED"
fi
if grep -q ' | FAIL | ' "$CRITERIA_FILE"; then
  STATIC_RESULT="FAIL"
fi
RUNTIME_PROFILE="unknown"
[ "$MODE" != "repo-self" ] || RUNTIME_PROFILE="v2"
if grep -q '^G9 target-runtime-profile | PASS | profile=portable-cli;' "$CRITERIA_FILE"; then
  RUNTIME_PROFILE="portable-cli"
elif grep -q '^G9 target-runtime-profile | PASS | profile=v2;' "$CRITERIA_FILE"; then
  RUNTIME_PROFILE="v2"
fi
STRICT_RESULT=$(awk -F ' [|] ' '{print $2}' "$STRICT_FILE")

LIVE_CLASS="not-probed"
LIVE_EVIDENCE="No live tool list supplied. Pass --live-tools or set CODEX_PREFLIGHT_LIVE_TOOLS to record the active session tool surface."
if [ -n "$LIVE_TOOLS" ] && [ "$RUNTIME_PROFILE" = "v2" ]; then
  LIVE_CLASS="unsupported for v2"
  LIVE_EVIDENCE="provided: $LIVE_TOOLS"
  HAVE_ALL=yes
  HAVE_CORE=yes
  for _tool in spawn_agent send_message followup_task wait_agent interrupt_agent list_agents; do
    case ",$LIVE_TOOLS," in
      *,"$_tool",*) : ;;
      *)
        HAVE_ALL=no
        [ "$_tool" = "send_message" ] || HAVE_CORE=no
        ;;
    esac
  done
  if [ "$HAVE_ALL" = yes ]; then
    LIVE_CLASS="v2-ready"
    LIVE_EVIDENCE="all required collaboration tools supplied: $LIVE_TOOLS"
  elif [ "$HAVE_CORE" = yes ]; then
    LIVE_CLASS="legacy-compatible only"
    LIVE_EVIDENCE="core orchestration tools supplied but send_message is missing: $LIVE_TOOLS"
  fi
fi
if [ "$RUNTIME_PROFILE" != "v2" ]; then
  LIVE_CLASS="not-probed"
  LIVE_EVIDENCE="Profile=$RUNTIME_PROFILE; this check implements observed-host v2 lifecycle only. Record target-native lifecycle evidence separately; supplied v2 tools do not establish portable readiness."
fi

OVERALL_RESULT="PASS (static and strict config valid; host tools not probed)"
PREFLIGHT_EXIT=0
if [ "$STATIC_RESULT" = "FAIL" ] || [ "$STRICT_RESULT" = "FAIL" ]; then
  OVERALL_RESULT="FAIL (static=$STATIC_RESULT; strict-config=$STRICT_RESULT; host-tools=$LIVE_CLASS)"
  PREFLIGHT_EXIT=1
elif [ "$STATIC_RESULT" = "REVIEW_REQUIRED" ]; then
  OVERALL_RESULT="REVIEW_REQUIRED (independent usefulness verdict pending; strict-config=$STRICT_RESULT; host-tools=$LIVE_CLASS)"
  PREFLIGHT_EXIT=1
elif [ "$LIVE_CLASS" = "v2-ready" ]; then
  OVERALL_RESULT="V2-READY (static=PASS; strict-config=PASS; host-tools=v2-ready)"
elif [ "$LIVE_CLASS" = "unsupported for v2" ]; then
  OVERALL_RESULT="FAIL (static=PASS; strict-config=PASS; host-tools=unsupported for v2)"
  PREFLIGHT_EXIT=1
elif [ "$LIVE_CLASS" = "legacy-compatible only" ]; then
  OVERALL_RESULT="FAIL (static=PASS; strict-config=PASS; host-tools=legacy-compatible only)"
  PREFLIGHT_EXIT=1
fi

printf -v PREFLIGHT_DISPLAY_CMD '%q' "$SCRIPT_DIR/preflight-codex-runtime.sh"
if [ "$MODE" = "team" ]; then
  printf -v PREFLIGHT_DISPLAY_CMD '%s --team-dir %q' "$PREFLIGHT_DISPLAY_CMD" "$TARGET_PATH"
else
  PREFLIGHT_DISPLAY_CMD="$PREFLIGHT_DISPLAY_CMD --repo-self"
fi

OUTPUT="$TMP_DIR/output.md"
{
  echo "# Codex Runtime Setup — $TARGET_LABEL"
  echo
  echo "> Probed: \`$VERSION\` on $(uname -s) at $(date +%Y-%m-%d)."
  echo "> Re-run \`$PREFLIGHT_DISPLAY_CMD\` after any Codex upgrade or runtime-config change."
  echo
  echo "## What Was Probed"
  echo
  echo "| Item | Value |"
  echo "|---|---|"
  echo "| Target | \`$TARGET_PATH\` |"
  echo "| Codex | \`$VERSION\` |"
  echo "| Configured profile | \`$RUNTIME_PROFILE\` (static selection, not live support) |"
  echo "| Doctor sandbox line | ${HOST_LINE:-not captured} |"
  echo "| Doctor config line | ${CONFIG_LINE:-not captured} |"
  echo "| Feature rows | $(printf '%s' "${FEATURE_LINES:-none}" | tr '\n' '; ' | sed 's/; $//') |"
  echo "| Static validator | \`${VALIDATOR_CMD[*]}\` |"
  echo "| Strict config command | \`$STRICT_DISPLAY_CMD\` |"
  echo
  echo "## Static Validation"
  echo
  echo '```text'
  if [ -s "$CRITERIA_FILE" ]; then
    cat "$CRITERIA_FILE"
  else
    printf 'P0 static-validator | %s | validator exit %s produced no EC-3.6 criterion lines\n' "$STATIC_RESULT" "$VALIDATOR_EXIT"
  fi
  echo '```'
  echo
  echo "## Strict Config"
  echo
  echo '```text'
  cat "$STRICT_FILE"
  echo '```'
  echo "- Source: this invocation's validator criterion \`$STRICT_CRITERION\`; no second strict-config execution."
  echo "- Note: \`codex doctor\` reports the user-scoped base config it loaded; the strict-config command above is the project-surface check."
  echo
  echo "## Live Host Tool Readiness"
  echo
  echo "- Class: \`$LIVE_CLASS\`"
  echo "- Evidence: $LIVE_EVIDENCE"
  echo "- Required v2 collaboration tools: \`spawn_agent\`, \`send_message\`, \`followup_task\`, \`wait_agent\`, \`interrupt_agent\`, \`list_agents\`"
  echo
  echo "## Overall Preflight Result"
  echo
  echo "- Result: \`$OVERALL_RESULT\`"
  echo "- Rule: host-tool readiness cannot override static target failures, pending usefulness review, or strict-config failures."
  echo
  echo "## Protected-Path Posture"
  echo
  echo "- Static scope only: this preflight records whether the target owns runtime metadata under \`.codex/\` or \`.agents/\`; it does not perform a write probe."
  echo "- Consequence: keep live host-tool readiness separate from the static validator output. Do not claim autonomous protected-metadata rewrites from config text alone."
  echo
  echo "## Setup"
  echo
  echo '```sh'
  printf 'codex -C %q --version\n' "$TARGET_PATH"
  printf 'codex -C %q features list\n' "$TARGET_PATH"
  echo '```'
  echo
  echo "## Verify"
  echo
  echo '```sh'
  printf '%s\n' "$PREFLIGHT_DISPLAY_CMD"
  echo '```'
  echo "- This preflight includes the validator and one strict-config execution."
  echo
  echo "## Rollback"
  echo
  echo "- This probe is read-only, so it has no config rollback step."
  echo "- Preserve the current worktree and concurrent edits. To reverse runtime changes, compare the assigned files with their captured scoped preimages and undo only that task's delta."
  echo "- Do not restore whole files from HEAD or reset the worktree."
  echo "- Never use this lane to edit \`~/.codex/config.toml\`."
} >"$OUTPUT"

if [ -n "$OUT_FILE" ]; then
  mkdir -p "$(dirname "$OUT_FILE")"
  cp "$OUTPUT" "$OUT_FILE"
fi

cat "$OUTPUT"
exit "$PREFLIGHT_EXIT"
