#!/usr/bin/env bash
# preflight-permissions.sh — probe the live Claude Code permission runtime and emit
# a per-team RUNTIME-SETUP.md advisory. READ-ONLY: this script never writes to any
# settings file. It writes only its report and a paste-ready snippet under --out.
#
# Usage: scripts/preflight-permissions.sh --team-dir teams/{name} [--out {dir}]
#
# Why advisory-only: Claude Code blocks an agent from writing autoMode rules into
# user settings (Self-Modification / Auto-Mode Bypass classifier rules). Verified
# 2026-07-25 against claude 2.1.220 — two blocked attempts. The user must apply.

set -euo pipefail

TEAM_DIR=""
OUT_DIR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --team-dir) TEAM_DIR="${2:-}"; shift 2 ;;
    --out)      OUT_DIR="${2:-}"; shift 2 ;;
    -h|--help)  sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -n "$TEAM_DIR" ] || { echo "--team-dir is required" >&2; exit 2; }
[ -d "$TEAM_DIR" ] || { echo "team dir not found: $TEAM_DIR" >&2; exit 2; }
TEAM_NAME="$(basename "$TEAM_DIR")"
OUT_DIR="${OUT_DIR:-$TEAM_DIR/docs}"
mkdir -p "$OUT_DIR"

# ---------------------------------------------------------------- probe: host
OS_RAW="$(uname -s 2>/dev/null || echo unknown)"
case "$OS_RAW" in
  Darwin)                     OS_KIND="posix"; OS_LABEL="macOS" ;;
  Linux)                      OS_KIND="posix"; OS_LABEL="Linux" ;;
  MINGW*|MSYS*|CYGWIN*)       OS_KIND="windows"; OS_LABEL="Windows" ;;
  *)                          OS_KIND="posix"; OS_LABEL="$OS_RAW (assuming POSIX)" ;;
esac

if [ "$OS_KIND" = "windows" ]; then
  USER_SETTINGS='%USERPROFILE%\.claude\settings.json'
else
  USER_SETTINGS="$HOME/.claude/settings.json"
fi

HAVE_JQ=no; command -v jq >/dev/null 2>&1 && HAVE_JQ=yes
CLAUDE_BIN="$(command -v claude 2>/dev/null || true)"
CLAUDE_VERSION="not found"
[ -n "$CLAUDE_BIN" ] && CLAUDE_VERSION="$("$CLAUDE_BIN" --version 2>/dev/null | head -1 || echo unknown)"

# ------------------------------------------------- probe: auto mode capability
# Never assume auto mode exists. Older Claude Code has no `auto-mode` subcommand,
# and the whole recommendation below is wrong for those versions.
AUTOMODE_SUPPORTED=no
AM_CONFIG=""
AM_DEFAULTS=""
if [ -n "$CLAUDE_BIN" ] && AM_CONFIG="$("$CLAUDE_BIN" auto-mode config 2>/dev/null)"; then
  AUTOMODE_SUPPORTED=yes
  AM_DEFAULTS="$("$CLAUDE_BIN" auto-mode defaults 2>/dev/null || true)"
fi

# ------------------------------------------- probe: is auto mode actually live?
# `permissionMode` is recorded per session in the project transcript. This is the
# only way to tell an installed-but-inactive auto mode from an active one.
ACTIVE_MODE="unknown"
PROJ_KEY="$(printf '%s' "$PWD" | sed 's|/|-|g')"
PROJ_DIR="$HOME/.claude/projects/$PROJ_KEY"
if [ -d "$PROJ_DIR" ] && [ "$HAVE_JQ" = yes ]; then
  NEWEST="$(ls -t "$PROJ_DIR"/*.jsonl 2>/dev/null | head -1 || true)"
  if [ -n "$NEWEST" ]; then
    ACTIVE_MODE="$(jq -r 'select(.permissionMode!=null) | .permissionMode' "$NEWEST" 2>/dev/null \
      | tail -1 || echo unknown)"
    [ -n "$ACTIVE_MODE" ] || ACTIVE_MODE="unknown"
  fi
fi

# ------------------------- probe: which shipped rules gate config-shaped writes
# Do NOT hardcode "Self-Modification" — rule labels are version-specific. Recover
# the labels that actually mention agent-config surfaces from the live defaults.
CONFIG_RULES="(could not probe)"
CUSTOM_RULES="none — shipped defaults only"
if [ "$AUTOMODE_SUPPORTED" = yes ] && [ "$HAVE_JQ" = yes ]; then
  CONFIG_RULES="$(printf '%s' "$AM_DEFAULTS" \
    | jq -r '.soft_deny[]? , .hard_deny[]?' 2>/dev/null \
    | grep -iE '\.claude/(settings|agents|skills|rules|hooks)|CLAUDE\.md' \
    | sed -E 's/ *\[.*//' | sort -u | paste -sd',' - | sed 's/,/, /g' || true)"
  [ -n "$CONFIG_RULES" ] || CONFIG_RULES="(none matched — rule labels may have changed)"
  if [ "$(printf '%s' "$AM_CONFIG" | jq -S . 2>/dev/null)" != "$(printf '%s' "$AM_DEFAULTS" | jq -S . 2>/dev/null)" ]; then
    CUSTOM_RULES="present — user settings already extend the shipped rules"
  fi
fi

# ------------------------------------------------- probe: the generated team
TEAM_SETTINGS="$TEAM_DIR/.claude/settings.json"
N_AGENTS=$(find "$TEAM_DIR/.claude/agents" -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
N_RULES=$(find "$TEAM_DIR/.claude/rules" -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
N_SKILLS=$(find "$TEAM_DIR/.claude/skills" -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ')

INERT_AUTOMODE=no
ASK_ENTRIES=""
INERT_ALLOWS=""
if [ -f "$TEAM_SETTINGS" ] && [ "$HAVE_JQ" = yes ]; then
  jq -e 'has("autoMode")' "$TEAM_SETTINGS" >/dev/null 2>&1 && INERT_AUTOMODE=yes
  ASK_ENTRIES="$(jq -r '.permissions.ask[]? // empty' "$TEAM_SETTINGS" | paste -sd',' - | sed 's/,/, /g' || true)"
  INERT_ALLOWS="$(jq -r '.permissions.allow[]? // empty
                         | select(test("^(Write|Edit|Agent|Bash)$"))' "$TEAM_SETTINGS" \
                  | paste -sd',' - | sed 's/,/, /g' || true)"
fi

# ------------------------------------------------------------ emit: the snippet
SNIPPET="$OUT_DIR/automode-snippet.json"
# NOTE — deliberately NO "environment" key. Route B merges with `jq -s '.[0] * .[1]'`, and jq's `*`
# REPLACES arrays instead of concatenating them. `claude auto-mode defaults` ships a 20-entry
# `environment` with no "$defaults" sentinel to self-extend, so emitting even a 2-entry environment
# here would silently drop 18 shipped entries from the user's resolved config. Reproduce:
#   echo '{"autoMode":{"environment":["A","B"]}}' > a.json
#   echo '{"autoMode":{"environment":["C"]}}'     > b.json
#   jq -s '.[0] * .[1]' a.json b.json   # => ["C"]
# `allow` is safe because "$defaults" is its first entry and the resolver expands it. Trust context
# that would have gone in `environment` is folded into the allow carve-out prose below instead.
cat > "$SNIPPET" <<JSON
{
  "autoMode": {
    "allow": [
      "\$defaults",
      "$TEAM_NAME Trusted Workspace: The workspace holding the '$TEAM_NAME' team, and the A-Team repo that generated it, are local git workspaces owned by the user.",
      "$TEAM_NAME Config Authoring: Creating or editing agent, skill, rule, hook, CLAUDE.md and settings.json files under the 'teams/$TEAM_NAME/' subtree of the A-Team repo — including the permission lists and hooks inside those generated files — is that repo's product output, not agent self-modification: the running session does not load those files, and the user launches the generated team deliberately in a separate session. This does NOT cover the running session's own config or ~/.claude/.",
      "$TEAM_NAME Worklog Bookkeeping: Creating, appending to, and pruning files under '.worklog/' and 'output/' inside this team's workspace is routine per-run bookkeeping and deliverable production."
    ]
  }
}
JSON

# ------------------------------------------------------------- emit: the report
REPORT="$OUT_DIR/RUNTIME-SETUP.md"
{
cat <<HDR
# Runtime Setup — $TEAM_NAME

> Probed: \`$CLAUDE_VERSION\` on $OS_LABEL at $(date +%Y-%m-%d).
> Re-run \`scripts/preflight-permissions.sh --team-dir $TEAM_DIR\` after any Claude Code
> upgrade — the commands below are version-specific and go stale silently.

## What was probed

| Item | Value |
|---|---|
| Claude Code | \`$CLAUDE_VERSION\` |
| Host | $OS_LABEL |
| \`jq\` available | $HAVE_JQ |
| Auto mode supported | $AUTOMODE_SUPPORTED |
| Permission mode in last session | \`$ACTIVE_MODE\` |
| Custom autoMode rules in user settings | $CUSTOM_RULES |
| Team inventory | $N_AGENTS agents, $N_RULES rules, $N_SKILLS skills |

HDR

if [ "$AUTOMODE_SUPPORTED" != yes ]; then
cat <<'OLD'
## Finding — auto mode not available on this install

This Claude Code build has no `auto-mode` subcommand, so the permission gate is the
classic deny/ask/allow rule set. The team's own `.claude/settings.json` fully controls
prompting; nothing needs to go into user settings. Stop here.
OLD
elif [ "$ACTIVE_MODE" != "auto" ]; then
cat <<NOTAUTO
## Finding — auto mode supported but not active

The last recorded session ran in \`$ACTIVE_MODE\` mode, so deny/ask/allow rules are the
live gate. The team's \`.claude/settings.json\` controls prompting. Apply the snippet below
only if you switch this workspace to auto mode.
NOTAUTO
else
cat <<AUTO
## Finding — auto mode is the live gate

The last session ran in \`auto\` mode. Under auto mode an AI classifier decides each tool
call; deterministic \`permissions.allow\` entries are consulted but bare tool grants
(\`Write\`, \`Edit\`, \`Agent\`) and shell wildcards are ignored at runtime. Adding more
allow entries will NOT reduce prompting.

The rules that gate writes to agent-config-shaped paths on this version:

> $CONFIG_RULES

A team whose deliverables ARE agent config files trips these on every generated file.
That is the prompt storm. The only lever is an \`autoMode\` carve-out, and it is honored
**only from user settings** — \`autoMode\` in a team's own \`settings.json\` or in
\`settings.local.json\` is inert.
AUTO
fi

cat <<'FIX'

## Apply the carve-out

Claude Code deliberately blocks an agent from writing these rules, so this is a manual
step. Two supported routes — pick one.

### Route A — first-party flow (recommended)

Run `/auto-mode-setup` in this workspace. It does its own repo recon and proposes rules
through a review UI. Use `automode-snippet.json` (next to this file) as a checklist for
what the proposal should cover. Afterwards run `claude auto-mode critique` for an AI
review of whatever ended up in your settings.

### Route B — apply the snippet directly
FIX

if [ "$OS_KIND" = "windows" ]; then
cat <<PS

PowerShell:

\`\`\`powershell
\$s = "\$env:USERPROFILE\\.claude\\settings.json"
Copy-Item \$s "\$s.bak"
\$cur = Get-Content \$s -Raw | ConvertFrom-Json
\$new = Get-Content "$SNIPPET" -Raw | ConvertFrom-Json
\$cur | Add-Member -NotePropertyName autoMode -NotePropertyValue \$new.autoMode -Force
\$cur | ConvertTo-Json -Depth 100 | Set-Content \$s
claude auto-mode config
\`\`\`

Rollback: \`claude auto-mode reset\` (or restore \`\$s.bak\`).
PS
else
cat <<SH

Requires \`jq\`. Paste into the Claude Code prompt with a leading \`!\` to run it here:

\`\`\`sh
S="$USER_SETTINGS"; B="\$S.bak-\$(date +%Y%m%d%H%M%S)"
claude auto-mode config | jq '{allow:(.allow|length),soft_deny:(.soft_deny|length),environment:(.environment|length)}'
cp "\$S" "\$B" && jq -s '.[0] * .[1]' "\$B" "$SNIPPET" > "\$S" \\
  && claude auto-mode config | jq '{allow:(.allow|length),soft_deny:(.soft_deny|length),environment:(.environment|length)}'
\`\`\`

Compare the two lines it prints. \`allow\` should grow by the number of carve-outs;
\`soft_deny\` and \`environment\` must be UNCHANGED. If \`environment\` shrank, the merge
replaced an array instead of extending it — restore \`\$B\` immediately and report it.
This snippet omits \`environment\` precisely so that cannot happen; the check is here in
case a future edit reintroduces it. \`allow\` is safe to extend because \`"\$defaults"\`
is its first entry and the resolver expands it in place.

Rollback: \`claude auto-mode reset\`, or restore \`\$B\`.
SH
fi

cat <<'VER'

Verify afterwards with `claude auto-mode critique` — the first-party review of custom
rules. It flags rules that are too broad, ambiguous, or mutually conflicting.
VER

echo
echo "## Team settings findings"
echo
FOUND=no
if [ "$INERT_AUTOMODE" = yes ]; then
  echo "- **INERT** — \`$TEAM_SETTINGS\` contains an \`autoMode\` key. Auto mode ignores it; only user settings count. Remove it and use this document instead."; FOUND=yes
fi
if [ -n "$INERT_ALLOWS" ]; then
  echo "- **IGNORED UNDER AUTO MODE** — bare grants in \`permissions.allow\`: $INERT_ALLOWS. Harmless, but they buy nothing; the classifier decides regardless."; FOUND=yes
fi
if [ -n "$ASK_ENTRIES" ]; then
  echo "- **UNCONDITIONAL PROMPTS** — every \`permissions.ask\` entry prompts on every match, classifier or not: $ASK_ENTRIES. Keep only what genuinely warrants a human decision each time; let the classifier judge the rest."; FOUND=yes
fi
[ "$FOUND" = no ] && echo "- No issues found in \`$TEAM_SETTINGS\`."

if [ "$HAVE_JQ" != yes ]; then
  echo
  echo "> \`jq\` was not found, so team-settings analysis and the Route B command are unavailable. Install jq, or apply the snippet by hand."
fi

cat <<'STALE'

## Where this document goes stale first

The next Claude Code upgrade. The classifier rule names, the `auto-mode` subcommand set, and the
settings schema are all version-bound, and none of them announce a change. The `Probed:` stamp at
the top is the staleness signal: once it no longer matches `claude --version`, re-run the probe
before trusting any command below it.
STALE
} > "$REPORT"

# Localization note: this report is emitted in English. When the team's own CLAUDE.md is written in
# another language, a hand-localized version reads better for that team's user and is permitted —
# see teams/tongzhengsi/docs/RUNTIME-SETUP.md for a Traditional Chinese reference. Re-running this
# script OVERWRITES such a version, so re-localize after any re-probe. Teaching this script to
# switch heading sets on the team's detected language is a logged follow-up.

echo "$REPORT"
echo "$SNIPPET"
