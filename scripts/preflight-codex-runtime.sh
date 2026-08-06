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
It probes the current Codex host, runs the static Codex validator, and emits a
Markdown advisory to stdout or --out.
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
STRICT_CMD=(codex exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral "Reply with CONFIG_OK only.")
if [ "$MODE" = "team" ]; then
  TARGET_LABEL=$(basename "$TARGET_DIR")
  TARGET_PATH=$(cd "$TARGET_DIR" && pwd)
  VALIDATOR_CMD=(python3 -B "$SCRIPT_DIR/validate_codex_team.py" "$TARGET_DIR")
  STRICT_CMD=(codex -C "$TARGET_DIR" exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral "Reply with CONFIG_OK only.")
fi

STRICT_DISPLAY_CMD="codex exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral 'Reply with CONFIG_OK only.'"
if [ "$MODE" = "team" ]; then
  STRICT_DISPLAY_CMD="codex -C \"$TARGET_DIR\" exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral 'Reply with CONFIG_OK only.'"
fi

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
STRICT_EXIT=0

if command -v codex >/dev/null 2>&1; then
  codex --version >"$VERSION_FILE" 2>&1 || true
  if [ "$MODE" = "team" ]; then
    codex -C "$TARGET_PATH" doctor >"$DOCTOR_FILE" 2>&1 || true
    codex -C "$TARGET_PATH" features list >"$FEATURES_FILE" 2>&1 || true
  else
    codex doctor >"$DOCTOR_FILE" 2>&1 || true
    codex features list >"$FEATURES_FILE" 2>&1 || true
  fi
  if [ -n "$LIVE_TOOLS" ]; then
    CODEX_PREFLIGHT_LIVE_TOOLS="$LIVE_TOOLS" "${VALIDATOR_CMD[@]}" >"$VALIDATOR_FILE" 2>&1 || VALIDATOR_EXIT=$?
  else
    "${VALIDATOR_CMD[@]}" >"$VALIDATOR_FILE" 2>&1 || VALIDATOR_EXIT=$?
  fi
  "${STRICT_CMD[@]}" >"$STRICT_FILE" 2>&1 || STRICT_EXIT=$?
else
  printf 'codex binary not found in PATH\n' >"$VERSION_FILE"
  printf 'codex binary not found in PATH\n' >"$DOCTOR_FILE"
  printf 'codex binary not found in PATH\n' >"$FEATURES_FILE"
  if [ -n "$LIVE_TOOLS" ]; then
    CODEX_PREFLIGHT_LIVE_TOOLS="$LIVE_TOOLS" "${VALIDATOR_CMD[@]}" >"$VALIDATOR_FILE" 2>&1 || VALIDATOR_EXIT=$?
  else
    "${VALIDATOR_CMD[@]}" >"$VALIDATOR_FILE" 2>&1 || VALIDATOR_EXIT=$?
  fi
  printf 'codex binary not found in PATH\n' >"$STRICT_FILE"
  STRICT_EXIT=127
fi

# Preserve only EC-3.6 criterion records in the advisory, never raw validator logs.
awk '/^[A-Za-z0-9_]+ [^|]+ \| (PASS|FAIL|SKIP) \| /' "$VALIDATOR_FILE" >"$CRITERIA_FILE"

VERSION=$(head -1 "$VERSION_FILE" | tr '\n' ' ' | sed 's/  */ /g; s/^ //; s/ $//')
HOST_LINE=$(awk '/^  ✓ sandbox /{sub(/^  /,""); print; exit}' "$DOCTOR_FILE")
CONFIG_LINE=$(awk '/^      config\.toml/{sub(/^      /,""); print; exit}' "$DOCTOR_FILE")
FEATURE_LINES=$(grep '^multi_agent' "$FEATURES_FILE" 2>/dev/null || true)
STRICT_SUMMARY=$(head -5 "$STRICT_FILE" | tr '\n' ' ' | sed 's/  */ /g; s/^ //; s/ $//')
STATIC_RESULT="PASS"
[ "$VALIDATOR_EXIT" -eq 0 ] || STATIC_RESULT="FAIL"
STRICT_RESULT="PASS"
[ "$STRICT_EXIT" -eq 0 ] || STRICT_RESULT="FAIL"

LIVE_CLASS="not-probed"
LIVE_EVIDENCE="No live tool list supplied. Pass --live-tools or set CODEX_PREFLIGHT_LIVE_TOOLS to record the active session tool surface."
if [ -n "$LIVE_TOOLS" ]; then
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

OVERALL_RESULT="PASS (static and strict config valid; host tools not probed)"
PREFLIGHT_EXIT=0
if [ "$STATIC_RESULT" = "FAIL" ] || [ "$STRICT_RESULT" = "FAIL" ]; then
  OVERALL_RESULT="FAIL (static=$STATIC_RESULT; strict-config=$STRICT_RESULT; host-tools=$LIVE_CLASS)"
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

OUTPUT="$TMP_DIR/output.md"
{
  echo "# Codex Runtime Setup — $TARGET_LABEL"
  echo
  echo "> Probed: \`$VERSION\` on $(uname -s) at $(date +%Y-%m-%d)."
  echo "> Re-run \`scripts/preflight-codex-runtime.sh $([ "$MODE" = "repo-self" ] && printf -- '--repo-self' || printf -- '--team-dir %s' "$TARGET_DIR")\` after any Codex upgrade or runtime-config change."
  echo
  echo "## What Was Probed"
  echo
  echo "| Item | Value |"
  echo "|---|---|"
  echo "| Target | \`$TARGET_PATH\` |"
  echo "| Codex | \`$VERSION\` |"
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
  printf 'P1 strict-config | %s | command exit %s\n' "$STRICT_RESULT" "$STRICT_EXIT"
  echo '```'
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
  echo "- Rule: host-tool readiness cannot override static target or strict-config failures."
  echo
  echo "## Protected-Path Posture"
  echo
  echo "- Static scope only: this preflight records whether the target owns runtime metadata under \`.codex/\` or \`.agents/\`; it does not perform a write probe."
  echo "- Consequence: keep live host-tool readiness separate from the static validator output. Do not claim autonomous protected-metadata rewrites from config text alone."
  echo
  echo "## Setup"
  echo
  echo '```sh'
  echo "codex --version"
  echo "codex features list | rg '^multi_agent'"
  printf '%s\n' "$STRICT_DISPLAY_CMD"
  echo '```'
  echo
  echo "## Verify"
  echo
  echo '```sh'
  printf '%s\n' "${VALIDATOR_CMD[*]}"
  printf '%s\n' "$STRICT_DISPLAY_CMD"
  echo '```'
  echo
  echo "## Rollback"
  echo
  echo "- This probe is read-only, so it has no config rollback step."
  echo "- If you changed repo or team runtime files before re-running validation, restore those files from version control or an untouched generated copy."
  echo "- Never use this lane to edit \`~/.codex/config.toml\`."
} >"$OUTPUT"

if [ -n "$OUT_FILE" ]; then
  mkdir -p "$(dirname "$OUT_FILE")"
  cp "$OUTPUT" "$OUT_FILE"
fi

cat "$OUTPUT"
exit "$PREFLIGHT_EXIT"
