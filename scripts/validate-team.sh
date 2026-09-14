#!/bin/sh
# validate-team.sh — mechanical validator for A-Team generated teams.
#
# Runs the mechanically checkable half of the quality-validation checklist
# (.claude/skills/quality-validation/SKILL.md) against a generated team.
# Judgment items (responsibility overlap, semantic rule correctness, evidence
# quality) stay in the prose checklist for a model to run — they are NOT faked
# here.
#
# Usage:
#   validate-team.sh <team-path>      validate one team
#   validate-team.sh --all            sweep every directory under teams/
#   validate-team.sh --help
#
# Output: one line per check, in the EC-3.6 verifier verdict format
#   {check-id} {check-name} | PASS|FAIL|SKIP | {evidence}
# Store these lines in verifier-owned evidence files and return the criterion
# lines with those evidence paths in the EC report; do not paste raw output.
#
# Exit: 0 when every check passed, 1 when any check FAILed.
#
# Portability: POSIX sh. JSON is parsed with python3, never with the external
# JSON CLI that .claude/rules/hooks-integration.md forbids depending on (it is
# not preinstalled on stock macOS). No GNU-only flags. Tested under sh and bash
# on Darwin.

set -u

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

TOTAL=0
PASSED=0
FAILED=0
SKIPPED=0
G_TOTAL=0
G_PASSED=0
G_FAILED=0
G_SKIPPED=0
TEAMS_VALIDATED=0
TEAMS_SKIPPED=0

# ---------------------------------------------------------------- bilingual patterns
# Generated teams legitimately write CLAUDE.md in the user's language. Every
# content-section pattern below matches English, Traditional Chinese and
# Japanese variants; an English-only pattern produces false FAILs (prior audit:
# 5 false failures across 3 teams).
P_DEPLOY='^#+ .*([Dd]eployment|[Dd]eploy |部署|デプロイ|運用モード)'
P_PRECED='([Pp]receden|優先序|優先順序|優先順位|優先級|指令衝突|conflict resolution|EC-4)'
P_WORKCTX='([Ww]orklog|[Cc]ontext [Mm]anagement|工作日誌|工作日志|工作紀錄|コンテキスト管理|Context 管理|\.worklog)'
P_MAINSESS='(main[- ]session|current session|this session|top-level session|主會話|主 會話|當前會話|本會話|主工作階段|當前工作階段|本工作階段|頂層會話|主 ?session|メインセッション|現在のセッション|トップレベルセッション)'
P_NEGATION='(never|not |n.t |cannot|do not|without|instead|dead-?lock|prohibit|forbidden|不要|不可|不能|禁止|絕不|永不|勿)'
P_ROLLBACK='([Rr]ollback|auto-mode reset|restore .*\.bak|revert|回滾|還原|復原|ロールバック)'
P_BLUEPRINT='(status: *blueprint|狀態：?設計藍圖|設計藍圖（尚未生成|尚未生成|design blueprint \(not generated)'

# Directories under teams/ that are known not to be Claude Code teams. This is a
# FALLBACK only — it is consulted after the structural test, and never masks a
# directory that structurally is a Claude team.
NON_TEAM_FALLBACK='flutter-app-dev-team-codex forge-team-codex code-warfare-dev ducha teams-index'

# Caps
CAP_RULE_LINES=100
CAP_AGENT_LINES=300
CAP_SKILL_LINES=200
CAP_RULE_COUNT=12
CAP_AGENT_COUNT=14

# Output-mode component mandate cutover (rules/output-structure.md, Output Mode
# Component). Teams stamped before this date SKIP O1/O2 instead of retro-FAILing.
OUTPUT_MODE_SINCE="2026-07-28"

# ---------------------------------------------------------------- emit helpers

emit() {
	# $1=id $2=name $3=verdict $4=evidence
	printf '%s %s | %s | %s\n' "$1" "$2" "$3" "$4"
	TOTAL=$((TOTAL + 1))
	case "$3" in
	PASS) PASSED=$((PASSED + 1)) ;;
	FAIL) FAILED=$((FAILED + 1)) ;;
	SKIP) SKIPPED=$((SKIPPED + 1)) ;;
	esac
}

pass() { emit "$1" "$2" PASS "$3"; }
fail() { emit "$1" "$2" FAIL "$3"; }
skip() { emit "$1" "$2" SKIP "$3"; }

# Collapse a multi-line value into one evidence-safe line.
oneline() {
	tr '\n' ' ' | sed 's/  */ /g; s/^ //; s/ $//'
}

# grep -c that never fails the script under set -u / pipefail-less sh
countmatch() {
	# $1=pattern $2=file  (extended regex, case-insensitive)
	_count=$(grep -icE "$1" "$2" 2>/dev/null) || _count=0
	printf '%s\n' "$_count"
}

firstmatch() {
	# $1=pattern $2=file -> "line:text" of the first hit, truncated
	grep -inE "$1" "$2" 2>/dev/null | head -1 | cut -c1-120 | oneline
}

# Prefer a section HEADING hit; fall back to a body hit. Section-presence checks
# must not report a passing mention buried in prose when a real heading exists —
# the evidence has to show the strongest thing observed.
firstmatch_section() {
	# $1=pattern $2=file
	_fs=$(grep -inE "^#+ .*$1" "$2" 2>/dev/null | head -1 | cut -c1-120 | oneline)
	[ -n "$_fs" ] || _fs=$(firstmatch "$1" "$2")
	printf '%s' "$_fs"
}

# Surface-specific detector for Claude mirrors that are intentionally non-runnable.
# Accept only a labelled declaration such as `Claude surface: reference-only`
# (surface/runtime/mirror are accepted labels).  A general authority paragraph
# can legitimately mention both Claude and a reference-only projection, so it
# must not decide whether this runnable surface is skipped.
claude_reference_only_declared() {
	# $1=file -> emits the first matching declaration line, else nothing
	[ -f "$1" ] || return 1
	awk '
	{
		raw = $0
		clean = tolower($0)
		gsub(/\r/, "", clean)
		gsub(/[`*]/, "", clean)
		gsub(/^[[:space:]]*#+[[:space:]]*/, "", clean)
		if (clean ~ /^claude[[:space:]_-]+(surface|runtime|mirror)[[:space:]]*:[[:space:]]*(reference[- ]only|not[[:space:]]+runnable|non[- ]runnable|compatibility[[:space:]]+mirror)[[:space:]]*([.;].*)?$/) {
			gsub(/[[:space:]]+/, " ", raw)
			print substr(raw, 1, 160)
			found = 1
			exit
		}
	}
	END { exit(found ? 0 : 1) }
	' "$1"
}

# ---------------------------------------------------------------- team detection

# Prints a skip reason when the directory is not a Claude Code team, else nothing.
not_a_claude_team() {
	_d="$1"
	_n=$(basename "$_d")

	if [ ! -d "$_d/.claude" ]; then
		if [ -f "$_d/AGENTS.md" ] && [ ! -f "$_d/CLAUDE.md" ]; then
			echo "no .claude/ directory; AGENTS.md present (Codex-only tree; validate with scripts/validate_codex_team.py)"
			return 0
		fi
		echo "no .claude/ directory"
		return 0
	fi

	# .claude/ exists but neither an entry document nor an agent registry ->
	# a mirror or build artifact, not a Claude team.
	if [ ! -f "$_d/CLAUDE.md" ] && [ ! -d "$_d/.claude/agents" ]; then
		echo "no CLAUDE.md and no .claude/agents/ (not a Claude team tree)"
		return 0
	fi

	# Pre-generation design blueprint.
	for _f in "$_d/README.md" "$_d/CLAUDE.md"; do
		[ -f "$_f" ] || continue
		if grep -qE "$P_BLUEPRINT" "$_f" 2>/dev/null; then
			echo "blueprint marker in $(basename "$_f"): $(firstmatch "$P_BLUEPRINT" "$_f")"
			return 0
		fi
	done

	# Declared reference-only mirror: a Claude tree that exists to be READ, whose
	# charter says it is not runnable under Claude Code. Such a tree deliberately
	# omits an entry-point skill, settings.json, and model/effort frontmatter, so
	# the runnable-team checks would FAIL it forever and re-provoke a retrofit that
	# breaks its stated contract. Verified case: teams/u-team.
	_ref=$(
		claude_reference_only_declared "$_d/CLAUDE.md" 2>/dev/null || true
	)
	if [ -n "$_ref" ]; then
		echo "charter declares a Claude-specific reference-only mirror: $(printf '%s' "$_ref" | oneline)"
		return 0
	fi

	# Name-based fallback, only for directories that already lack CLAUDE.md.
	if [ ! -f "$_d/CLAUDE.md" ]; then
		for _known in $NON_TEAM_FALLBACK; do
			if [ "$_n" = "$_known" ]; then
				echo "no CLAUDE.md; name matches known non-Claude-team list"
				return 0
			fi
		done
	fi

	return 1
}

# ---------------------------------------------------------------- checks

check_structure() {
	_t="$1"
	_cd="$_t/.claude"

	if [ -f "$_t/CLAUDE.md" ]; then
		pass S1 claude-md-present "$_t/CLAUDE.md ($(wc -l <"$_t/CLAUDE.md" | tr -d ' ') lines)"
	else
		fail S1 claude-md-present "no CLAUDE.md at team root $_t/"
	fi

	if [ -f "$_cd/CLAUDE.md" ]; then
		fail S2 claude-md-not-in-dot-claude "found $_cd/CLAUDE.md — must live at team root"
	else
		pass S2 claude-md-not-in-dot-claude "no CLAUDE.md inside $_cd/"
	fi

	if [ -d "$_cd/agents" ]; then
		_root_agents=$(find "$_cd/agents" -maxdepth 1 -type f -name '*.md' 2>/dev/null | sort)
		_root_n=$(printf '%s\n' "$_root_agents" | grep -c . || true)
		_root_names=$(printf '%s\n' "$_root_agents" | sed 's#.*/##' | oneline)
		_all_n=$(find "$_cd/agents" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
		_sub_n=$((_all_n - _root_n))

		if [ "$_root_n" -eq 1 ]; then
			pass S3 coordinator-single-in-agents-root "1 file in agents/ root: $_root_names"
		elif [ "$_root_n" -eq 0 ]; then
			fail S3 coordinator-single-in-agents-root "0 .md files in agents/ root; coordinator must sit there"
		else
			fail S3 coordinator-single-in-agents-root "$_root_n .md files in agents/ root: $_root_names"
		fi

		if [ "$_all_n" -le 1 ]; then
			pass S4 specialists-in-subfolders "$_all_n agent file(s) total; no specialists to group"
		elif [ "$_sub_n" -eq $((_all_n - 1)) ]; then
			pass S4 specialists-in-subfolders "$_sub_n of $_all_n agents in subfolders, 1 in root"
		else
			fail S4 specialists-in-subfolders "$_sub_n of $_all_n agents in subfolders; $_root_n in root: $_root_names"
		fi
	else
		fail S3 coordinator-single-in-agents-root "no $_cd/agents/ directory"
		fail S4 specialists-in-subfolders "no $_cd/agents/ directory"
	fi

	if [ -d "$_cd/skills" ]; then
		_missing=""
		_skill_n=0
		for _sd in "$_cd"/skills/*/; do
			[ -d "$_sd" ] || continue
			_skill_n=$((_skill_n + 1))
			[ -f "$_sd/SKILL.md" ] || _missing="$_missing $(basename "$_sd")"
		done
		_stray=$(find "$_cd/skills" -maxdepth 1 -type f -name '*.md' 2>/dev/null | sed 's#.*/##' | oneline)
		if [ -n "$_missing" ] || [ -n "$_stray" ]; then
			fail S5 skills-have-skill-md "$_skill_n skill dirs; missing SKILL.md:${_missing:- none}; loose .md in skills/: ${_stray:-none}"
		else
			pass S5 skills-have-skill-md "$_skill_n skill dirs, each with SKILL.md"
		fi
	else
		skip S5 skills-have-skill-md "no $_cd/skills/ directory"
	fi

	# Kebab-case: scoped to design artifacts (agent .md, rule .md, skill folder
	# names). Vendored bundle scripts and macOS .DS_Store are out of scope.
	# NOTE: `find -name '*[A-Z]*'` is useless here — macOS filesystems are
	# case-insensitive, so the glob matches everything. Case is compared in awk.
	_bad=""
	for _f in $(find "$_cd/agents" "$_cd/rules" -type f -name '*.md' 2>/dev/null); do
		_b=$(basename "$_f" .md)
		if ! printf '%s' "$_b" | LC_ALL=C awk '/^[a-z0-9]+(-[a-z0-9]+)*$/{ok=1} END{exit !ok}'; then
			_bad="$_bad $(basename "$_f")"
		fi
	done
	for _d in $(find "$_cd/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null); do
		_b=$(basename "$_d")
		if ! printf '%s' "$_b" | LC_ALL=C awk '/^[a-z0-9]+(-[a-z0-9]+)*$/{ok=1} END{exit !ok}'; then
			_bad="$_bad $_b/"
		fi
	done
	if [ -n "$_bad" ]; then
		fail S6 kebab-case-names "non-kebab-case:$_bad"
	else
		_scanned=$(find "$_cd/agents" "$_cd/rules" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
		_sdirs=$(find "$_cd/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
		pass S6 kebab-case-names "$_scanned agent/rule files + $_sdirs skill dirs all kebab-case"
	fi

	_rule_n=$(find "$_cd/rules" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
	if [ "$_rule_n" -gt 0 ]; then
		pass S7 rules-dir-populated "$_rule_n rule .md files in $_cd/rules/"
	else
		fail S7 rules-dir-populated "no rule .md files under $_cd/rules/"
	fi
}

# A mandatory rule matches on filename OR frontmatter `name:`.
find_rule() {
	# $1=rules-dir $2=filename-pattern $3=frontmatter-name-pattern
	_rd="$1"
	[ -d "$_rd" ] || return 1
	_hit=$(find "$_rd" -type f -name '*.md' 2>/dev/null | grep -iE "$2" | head -1)
	if [ -n "$_hit" ]; then
		printf '%s\n' "$_hit"
		return 0
	fi
	for _f in $(find "$_rd" -type f -name '*.md' 2>/dev/null); do
		if head -20 "$_f" | grep -iqE "^name: *$3"; then
			printf '%s\n' "$_f"
			return 0
		fi
	done
	return 1
}

check_mandatory_rules() {
	_rd="$1/.claude/rules"

	_h=$(find_rule "$_rd" 'worklog' 'work.?log') && pass R1 rule-worklog "$_h" ||
		fail R1 rule-worklog "no rule matching filename/name 'worklog' under $_rd/"

	_h=$(find_rule "$_rd" 'context.?management|context.?econom' 'context.?(management|econom)') &&
		pass R2 rule-context-management "$_h" ||
		fail R2 rule-context-management "no rule matching 'context-management' under $_rd/"

	_h=$(find_rule "$_rd" 'reasoning.*(critique|self)|self.?critique' 'reasoning.*(critique|self)|self.?critique') &&
		pass R3 rule-reasoning-self-critique "$_h" ||
		fail R3 rule-reasoning-self-critique "no rule matching 'reasoning-and-self-critique' under $_rd/"

	_h=$(find_rule "$_rd" 'execution.?contract' 'execution.?contract') &&
		pass R4 rule-execution-contract "$_h" ||
		fail R4 rule-execution-contract "no rule matching 'execution-contract' under $_rd/"
}

check_claude_md() {
	_f="$1/CLAUDE.md"
	if [ ! -f "$_f" ]; then
		skip C1 claude-md-deployment-mode "no CLAUDE.md to read (see S1)"
		skip C2 claude-md-main-session-statement "no CLAUDE.md to read (see S1)"
		skip C3 claude-md-worklog-context "no CLAUDE.md to read (see S1)"
		skip C4 claude-md-precedence-order "no CLAUDE.md to read (see S1)"
		skip C5 claude-md-generator-stamp "no CLAUDE.md to read (see S1)"
		return
	fi

	_h=$(firstmatch "$P_DEPLOY" "$_f")
	[ -n "$_h" ] && pass C1 claude-md-deployment-mode "$_h" ||
		fail C1 claude-md-deployment-mode "no heading matching /$P_DEPLOY/ in $_f"

	_h=$(firstmatch "$P_MAINSESS" "$_f")
	[ -n "$_h" ] && pass C2 claude-md-main-session-statement "$_h" ||
		fail C2 claude-md-main-session-statement "no main-session statement in $_f (searched EN/zh-TW/ja variants)"

	_h=$(firstmatch_section "$P_WORKCTX" "$_f")
	[ -n "$_h" ] && pass C3 claude-md-worklog-context "$_h" ||
		fail C3 claude-md-worklog-context "no worklog/context-management content in $_f"

	_h=$(firstmatch_section "$P_PRECED" "$_f")
	[ -n "$_h" ] && pass C4 claude-md-precedence-order "$_h" ||
		fail C4 claude-md-precedence-order "no precedence order in $_f (searched EN/zh-TW/ja variants)"

	_h=$(firstmatch 'Generated by A-Team on' "$_f")
	[ -n "$_h" ] && pass C5 claude-md-generator-stamp "$_h" ||
		fail C5 claude-md-generator-stamp "no 'Generated by A-Team on {date}' stamp in $_f"
}

check_entry_skill() {
	_t="$1"

	# J5.2: identify declared purpose or coordinator-adoption intent first.
	# Manual-only is an invocation setting, not an entry identity test. Missing
	# fields, broken coordinator paths, and invalid adoption must not hide entries.
	_cands=$(python3 - "$_t" <<'PY'
from pathlib import Path
import re
import sys

adopt = r"\badopt(?:s|ing)?\b|採納|採用|接管"
negated_adopt = r"(?:do not|don.t|never|cannot|not|不要|禁止|不可|勿).{0,20}(?:" + adopt + r")"
directive = r"^\s*(?:[-*]|\d+[.)])?\s*(?:read\b|load\b|adopt\b|in\b|inside\b|within\b|(?:the )?(?:current|main|this)\b|讀取|載入|採用|接管)"
inspect_entry = r"\b(?:verify|check|inspect|review|validate)\b.{0,80}\b(?:entry|skill)\b"
for skill in sorted((Path(sys.argv[1]) / ".claude/skills").glob("*/SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    description = re.search(r"^description:[ \t]*(.*(?:\n[ \t]+[^\n]+)*)", text, re.MULTILINE)
    purpose_section = re.search(r"^## (?:Description|Purpose)\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    purpose = "\n".join(part.group(1) for part in (description, purpose_section) if part)
    declared = re.search(
        r"\b(?:entry[- ](?:point|command)|front[- ]door|coordinator[- ]entry)\b"
        r"|\b(?:enter|start|starts|launch|launches)\b.{0,100}\bcoordinator\b"
        r"|\b(?:run|runs)\b.{0,100}\b(?:coordinator workflow|coordination workflow)\b"
        r"|(?:入口|進入|啟動).{0,50}(?:協調|團隊流程)",
        purpose, re.IGNORECASE | re.MULTILINE,
    ) and not re.search(inspect_entry, purpose, re.IGNORECASE)
    coordinator = re.search(r"agents/[a-z0-9._-]+\.md|\bcoordinator\b|協調者|協調員", text, re.IGNORECASE)
    intent = coordinator and any(
        re.search(directive, line, re.IGNORECASE) and re.search(adopt, line, re.IGNORECASE)
        and not re.search(negated_adopt, line, re.IGNORECASE)
        and not re.search(inspect_entry, line, re.IGNORECASE)
        for line in text.splitlines()
    )
    if declared or intent:
        print(skill)
PY
	)
	# grep -c always prints exactly one count line (even "0" on no match, exit 1);
	# an `|| echo 0` fallback here double-printed "0\n0" and broke every numeric
	# comparison below for trees with no entry-skill candidate.
	_n=$(printf '%s' "$_cands" | grep -c . 2>/dev/null)
	[ -n "$_n" ] || _n=0

	if [ "$_n" -eq 0 ]; then
		fail E1 entry-skill-present "no coordinator entry declared by purpose or adoption intent under $_t/.claude/skills"
		for _i in E2 entry-disable-model-invocation E3 entry-allowed-tools-agent E4 entry-argument-hint \
		          E5 entry-main-session-adoption E6 entry-no-coordinator-spawn; do :; done
		skip E2 entry-disable-model-invocation "no entry-point skill (see E1)"
		skip E3 entry-allowed-tools-agent "no entry-point skill (see E1)"
		skip E4 entry-argument-hint "no entry-point skill (see E1)"
		skip E5 entry-main-session-adoption "no entry-point skill (see E1)"
		skip E6 entry-no-coordinator-spawn "no entry-point skill (see E1)"
		return
	fi

	if [ "$_n" -gt 1 ]; then
		fail E1 entry-skill-present "$_n entry-point-shaped skills — the front door is ambiguous: $(printf '%s' "$_cands" | sed "s#.*/skills/##" | oneline)"
		# Still validate the first one so E2-E6 produce evidence rather than a
		# cascade of SKIPs that hides a second, unrelated defect.
	fi

	_bs=$(printf '%s\n' "$_cands" | head -1)
	[ "$_n" -eq 1 ] && pass E1 entry-skill-present "$(printf '%s' "$_bs" | sed "s#.*/skills/##") ($(wc -l <"$_bs" | tr -d ' ') lines)"

	# Read required metadata only from closed, line-1 frontmatter; body examples
	# cannot supply missing fields or conceal malformed entry metadata.
	_fm=$(awk 'NR==1 && $0!="---" { exit } NR==1 { next } /^---[[:space:]]*$/ { closed=1; exit } { body=body $0 "\n" } END { if (closed) printf "%s", body }' "$_bs")
	_h=$(printf '%s\n' "$_fm" | grep -nE '^disable-model-invocation:[[:space:]]*true[[:space:]]*(#.*)?$' | head -1 | oneline)
	_count=$(printf '%s\n' "$_fm" | grep -c '^disable-model-invocation:' || true)
	[ "$_count" -eq 1 ] && [ -n "$_h" ] && pass E2 entry-disable-model-invocation "$_h" ||
		fail E2 entry-disable-model-invocation "no 'disable-model-invocation: true' in $_bs frontmatter"

	# Parse the bounded allowed-tools forms, not mentions in YAML comments or
	# partial names. A sequence item is one tool; scalar grants may use commas
	# or spaces. Malformed/duplicate metadata cannot grant Agent accidentally.
	_h=$(python3 - "$_fm" <<'PY'
import json
import re
import sys

quoted = r"\"(?:\\.|[^\"\\])*\"|'(?:''|[^'])*'"
tool = r"[A-Za-z][A-Za-z0-9_.:-]*(?:\([^()\r\n]*\))?"
item = rf"(?:{quoted}|{tool})"

def uncomment(line):
    return re.sub(rf"({quoted})|(?<!\S)#.*", lambda match: match.group(1) or "", line).rstrip()

def decode(value):
    if value.startswith('"'):
        return json.loads(value)
    if value.startswith("'"):
        if not re.fullmatch(quoted, value):
            raise ValueError("malformed quoted tool")
        return value[1:-1].replace("''", "'")
    return value

def grants_agent(lines):
    fields = [index for index, line in enumerate(lines) if line.startswith("allowed-tools:")]
    if len(fields) != 1:
        return False
    index = fields[0]
    value = uncomment(lines[index].partition(":")[2]).strip()
    children = []
    for line in lines[index + 1:]:
        line = uncomment(line)
        if not line.strip():
            continue
        if not line[0].isspace() and not line.startswith("- "):
            break
        children.append(line)
    if not value:
        # YAML permits indented or indentless block sequences, but all items
        # here must be scalar tools at one indentation level.
        matches = [re.fullmatch(r"( *)- +(.+)", line) for line in children]
        if not matches or any(match is None for match in matches):
            return False
        if len({match.group(1) for match in matches}) != 1:
            return False
        values = [match.group(2).strip() for match in matches]
        if any(not re.fullmatch(item, part) for part in values):
            return False
        tokens = [decode(part) for part in values]
    elif children:
        return False
    elif value.startswith("["):
        if not re.fullmatch(rf"\[\s*(?:{item}(?:\s*,\s*{item})*\s*,?)?\s*\]", value):
            return False
        tokens = [decode(match.group()) for match in re.finditer(item, value[1:-1])]
    else:
        scalar = decode(value)
        if not re.fullmatch(rf"{tool}(?:(?:\s*,\s*|\s+){tool})*", scalar):
            return False
        tokens = re.findall(tool, scalar)
    return all(re.fullmatch(tool, token) for token in tokens) and "Agent" in tokens

try:
    if grants_agent(sys.argv[1].splitlines()):
        print("allowed-tools grants complete Agent tool token")
except (ValueError, TypeError):
    pass
PY
	)
	[ -n "$_h" ] && pass E3 entry-allowed-tools-agent "$_h" ||
		fail E3 entry-allowed-tools-agent "allowed-tools missing or does not grant Agent: $(firstmatch '^allowed-tools:' "$_bs" | sed 's/^$/absent/')"

	# The UI hint is a nonempty plain/quoted scalar, not a YAML comment, null,
	# collection, or malformed scalar. Body text cannot supply its value.
	_h=$(python3 - "$_fm" <<'PY'
import json
import re
import sys

def argument_hint(lines):
    fields = [index for index, line in enumerate(lines) if line.startswith("argument-hint:")]
    if len(fields) != 1:
        return None
    index = fields[0]
    raw = lines[index].partition(":")[2].strip()
    for line in lines[index + 1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace() or line.startswith("- "):
            return None
        break
    if raw.startswith(('"', "'")):
        quoted = r"\"(?:\\.|[^\"\\])*\"|'(?:''|[^'])*'"
        match = re.fullmatch(rf"({quoted})(?:[ \t]+#.*)?", raw)
        if not match:
            return None
        value = match.group(1)
        value = json.loads(value) if value.startswith('"') else value[1:-1].replace("''", "'")
    else:
        value = re.split(r"(?<!\S)#", raw, maxsplit=1)[0].strip()
        if (not value or value.lower() in ("null", "~")
                or value[0] in "[]{}&*!|>,%@" or value[0] == chr(96)
                or re.search(r"^[-?:](?:\s|$)|:(?:\s|$)", value)):
            return None
    return value if value.strip() else None

try:
    hint = argument_hint(sys.argv[1].splitlines())
    if hint is not None:
        print(json.dumps(hint, ensure_ascii=False))
except (ValueError, TypeError):
    pass
PY
	)
	[ -n "$_h" ] && pass E4 entry-argument-hint "$_h" ||
		fail E4 entry-argument-hint "no 'argument-hint:' in $_bs frontmatter"

	_adoption=$(python3 - "$_t" "$_bs" "$P_MAINSESS" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
text = Path(sys.argv[2]).read_text(encoding="utf-8")
body = re.sub(r"\A---\n.*?\n---(?:\n|$)", "", text, count=1, flags=re.DOTALL)
refs = set(re.findall(r"(?<![\w./-])(?:\.claude/)?agents/([a-z0-9._-]+)\.md", body, re.IGNORECASE))
resolved = [name for name in refs if (root / f".claude/agents/{name}.md").is_file()
            and (root / f".claude/agents/{name}.md").resolve().is_relative_to(root)]
adopt = r"\badopt(?:s|ing)?\b|採納|採用|接管"
negated = r"(?:do not|don.t|never|cannot|not|不要|禁止|不可|勿).{0,20}(?:" + adopt + r")"
directive = r"^\s*(?:[-*]|\d+[.)])?\s*(?:read\b|load\b|adopt\b|in\b|inside\b|within\b|(?:the )?(?:current|main|this)\b|讀取|載入|採用|接管)"
inspect_entry = r"\b(?:verify|check|inspect|review|validate)\b.{0,80}\b(?:entry|skill)\b"
adoptions = [line for line in body.splitlines() if re.search(directive, line, re.IGNORECASE)
             and re.search(adopt, line, re.IGNORECASE) and not re.search(negated, line, re.IGNORECASE)
             and not re.search(inspect_entry, line, re.IGNORECASE)]
wrong_session = any(re.search(r"(?:in|inside|from|as) (?:a |the )?(?:subagent|child|worker|dispatched)|(?:子代理|子會話|子工作階段).{0,20}(?:採用|接管)", line, re.IGNORECASE)
                    for line in adoptions)
main_session = re.search(sys.argv[3] + r"|current Claude Code session", body, re.IGNORECASE)
if len(refs) != 1 or len(resolved) != 1:
    print("FAIL|entry must reference one existing confined coordinator playbook in .claude/agents/")
elif not adoptions or not main_session or wrong_session:
    print("FAIL|entry must affirmatively adopt its coordinator in the main session")
else:
    print(f"PASS|.claude/agents/{resolved[0]}.md resolves; affirmative main-session adoption")
PY
	)
	emit E5 entry-main-session-adoption "${_adoption%%|*}" "${_adoption#*|}"

	# Affirmative spawn-the-coordinator instruction.
	# A naive grep for /spawn|subagent_type/ false-FAILs every correct team —
	# they all carry a "Why Main-Session Adoption, Not Spawning" section. The
	# scan therefore: strips markdown emphasis (a bolded "Do **not** spawn"
	# otherwise reads as affirmative), joins wrapped lines into sentences, keeps
	# only sentences naming the ACTUAL coordinator, then drops negated ones.
	_coord=""
	_croot=$(find "$_t/.claude/agents" -maxdepth 1 -type f -name '*.md' 2>/dev/null | head -1)
	[ -n "$_croot" ] && _coord=$(basename "$_croot" .md)
	if [ -z "$_coord" ]; then
		skip E6 entry-no-coordinator-spawn "cannot identify coordinator (no .md in agents/ root)"
	else
		_hits=$(awk 'BEGIN{RS="";FS="\n"}{gsub(/\n/," "); gsub(/[*`]/,""); gsub(/\. /,".\n"); print}' "$_bs" |
			grep -iE '(spawn|subagent_type|Agent\(|Task\()' |
			grep -iE "$_coord" |
			grep -viE "$P_NEGATION" | head -1 | cut -c1-120 | oneline)
		if [ -n "$_hits" ]; then
			fail E6 entry-no-coordinator-spawn "affirmative spawn instruction naming '$_coord': $_hits"
		else
			pass E6 entry-no-coordinator-spawn "0 non-negated spawn sentences naming '$_coord' in $_bs"
		fi
	fi
}

check_runtime_setup() {
	_rs="$1/docs/RUNTIME-SETUP.md"
	if [ ! -f "$_rs" ]; then
		fail D1 runtime-setup-present "no $_rs (Phase 3.5 output missing)"
		skip D2 runtime-setup-probed-stamp "docs/RUNTIME-SETUP.md absent (see D1)"
		skip D3 runtime-setup-rollback "docs/RUNTIME-SETUP.md absent (see D1)"
		return
	fi
	pass D1 runtime-setup-present "$_rs ($(wc -l <"$_rs" | tr -d ' ') lines)"

	_h=$(firstmatch 'Probed:' "$_rs")
	[ -n "$_h" ] && pass D2 runtime-setup-probed-stamp "$_h" ||
		fail D2 runtime-setup-probed-stamp "no 'Probed:' stamp in $_rs"

	_h=$(firstmatch "$P_ROLLBACK" "$_rs")
	[ -n "$_h" ] && pass D3 runtime-setup-rollback "$_h" ||
		fail D3 runtime-setup-rollback "no rollback command in $_rs"
}

check_settings() {
	_s="$1/.claude/settings.json"
	if [ ! -f "$_s" ]; then
		fail J1 settings-json-parses "no $_s"
		skip J2 settings-required-keys "settings.json absent (see J1)"
		skip J3 settings-no-destructive-allow "settings.json absent (see J1)"
		return
	fi

	# The external JSON CLI is NOT preinstalled on stock macOS
	# (.claude/rules/hooks-integration.md); python3 is. Use python3 only.
	_err=$(python3 -m json.tool "$_s" 2>&1 >/dev/null)
	if [ -n "$_err" ]; then
		fail J1 settings-json-parses "python3 -m json.tool: $(printf '%s' "$_err" | head -1 | cut -c1-100)"
		skip J2 settings-required-keys "settings.json does not parse (see J1)"
		skip J3 settings-no-destructive-allow "settings.json does not parse (see J1)"
		return
	fi
	pass J1 settings-json-parses "python3 -m json.tool exit 0 on $_s"

	_keys=$(python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
miss=[k for k in ("hooks","permissions","env") if k not in d]
print("MISSING:"+",".join(miss) if miss else "OK:"+",".join(sorted(d.keys())))
' "$_s" 2>/dev/null)
	case "$_keys" in
	OK:*) pass J2 settings-required-keys "top-level keys ${_keys#OK:}" ;;
	MISSING:*) fail J2 settings-required-keys "missing top-level keys: ${_keys#MISSING:}" ;;
	*) skip J2 settings-required-keys "python3 key inspection produced no output" ;;
	esac

	_destr=$(python3 -c '
import json,re,sys
d=json.load(open(sys.argv[1]))
allow=(d.get("permissions") or {}).get("allow") or []
pats=[r"rm\s+-\w*[rf]", r"git\s+push\s+.*--force", r"push\s+--force", r"mkfs", r":\(\)\{", r"chmod\s+-R\s+777", r"sudo\s"]
bad=[a for a in allow if isinstance(a,str) and any(re.search(p,a,re.I) for p in pats)]
print(("BAD:"+" ; ".join(bad[:3])) if bad else "CLEAN:%d allow entries"%len(allow))
' "$_s" 2>/dev/null)
	case "$_destr" in
	CLEAN:*) pass J3 settings-no-destructive-allow "permissions.allow scanned, ${_destr#CLEAN:}, 0 destructive" ;;
	BAD:*) fail J3 settings-no-destructive-allow "destructive permissions.allow entries: ${_destr#BAD:}" ;;
	*) skip J3 settings-no-destructive-allow "python3 allow-list inspection produced no output" ;;
	esac
}

check_output_mode() {
	_t="$1"
	# Date-gate on the generator stamp: the component is mandated only for teams
	# generated on/after OUTPUT_MODE_SINCE. ISO dates compare numerically once
	# the dashes are stripped; POSIX sh has no string-date comparison.
	_stamp=$(grep -hoE 'Generated by A-Team on [0-9]{4}-[0-9]{2}-[0-9]{2}' "$_t/CLAUDE.md" 2>/dev/null |
		head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
	if [ -z "$_stamp" ]; then
		skip O1 output-style-present "no generator stamp to date-gate the mandate (see C5)"
		skip O2 output-mode-first-run-hook "no generator stamp to date-gate the mandate (see C5)"
		return
	fi
	if [ "$(printf '%s' "$_stamp" | tr -d '-')" -lt "$(printf '%s' "$OUTPUT_MODE_SINCE" | tr -d '-')" ]; then
		skip O1 output-style-present "stamp $_stamp predates output-mode mandate $OUTPUT_MODE_SINCE"
		skip O2 output-mode-first-run-hook "stamp $_stamp predates output-mode mandate $OUTPUT_MODE_SINCE"
		return
	fi

	_sf="$_t/.claude/output-styles/adhd-friendly.md"
	if [ ! -f "$_sf" ]; then
		fail O1 output-style-present "no $_sf (mandated for teams stamped >= $OUTPUT_MODE_SINCE)"
	elif head -5 "$_sf" | grep -qE '^name:'; then
		pass O1 output-style-present "$_sf ($(wc -l <"$_sf" | tr -d ' ') lines, frontmatter name present)"
	else
		fail O1 output-style-present "$_sf exists but frontmatter head has no name: field"
	fi

	_h=$(firstmatch 'outputStyle' "$_t/.claude/settings.json")
	[ -n "$_h" ] && pass O2 output-mode-first-run-hook "$_h" ||
		fail O2 output-mode-first-run-hook "no outputStyle first-run hook in $_t/.claude/settings.json (baseline per rules/hooks-integration.md)"
}

# Emits offenders "name=lines" for every file over the cap.
over_cap() {
	# $1=dir $2=cap $3=find-name-pattern
	[ -d "$1" ] || return 0
	find "$1" -type f -name "$3" 2>/dev/null | while read -r _f; do
		_n=$(wc -l <"$_f" | tr -d ' ')
		if [ "$_n" -gt "$2" ]; then
			printf '%s=%s ' "$(printf '%s' "$_f" | sed "s#^$1/##")" "$_n"
		fi
	done
}

check_caps() {
	_cd="$1/.claude"

	_n=$(find "$_cd/rules" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
	_over=$(over_cap "$_cd/rules" "$CAP_RULE_LINES" '*.md' | oneline)
	if [ "$_n" -eq 0 ]; then
		skip L1 rule-line-cap-100 "no rule files to measure"
	elif [ -n "$_over" ]; then
		fail L1 rule-line-cap-100 "$(printf '%s' "$_over" | wc -w | tr -d ' ') of $_n rules over ${CAP_RULE_LINES}L: $_over"
	else
		pass L1 rule-line-cap-100 "all $_n rules <= ${CAP_RULE_LINES} lines"
	fi

	_n=$(find "$_cd/agents" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
	_over=$(over_cap "$_cd/agents" "$CAP_AGENT_LINES" '*.md' | oneline)
	if [ "$_n" -eq 0 ]; then
		skip L2 agent-line-cap-300 "no agent files to measure"
	elif [ -n "$_over" ]; then
		fail L2 agent-line-cap-300 "$(printf '%s' "$_over" | wc -w | tr -d ' ') of $_n agents over ${CAP_AGENT_LINES}L: $_over"
	else
		pass L2 agent-line-cap-300 "all $_n agents <= ${CAP_AGENT_LINES} lines"
	fi

	_n=$(find "$_cd/skills" -type f -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ')
	_over=$(over_cap "$_cd/skills" "$CAP_SKILL_LINES" 'SKILL.md' | oneline)
	if [ "$_n" -eq 0 ]; then
		skip L3 skill-line-cap-200 "no SKILL.md files to measure"
	elif [ -n "$_over" ]; then
		fail L3 skill-line-cap-200 "$(printf '%s' "$_over" | wc -w | tr -d ' ') of $_n skills over ${CAP_SKILL_LINES}L: $_over"
	else
		pass L3 skill-line-cap-200 "all $_n SKILL.md <= ${CAP_SKILL_LINES} lines"
	fi
}

check_frontmatter() {
	_ad="$1/.claude/agents"
	if [ ! -d "$_ad" ]; then
		skip F1 agent-frontmatter-fields "no agents/ directory"
		skip F2 agent-model-value "no agents/ directory"
		return
	fi

	_n=0
	_missing=""
	_badstart=""
	_badmodel=""
	for _f in $(find "$_ad" -type f -name '*.md' 2>/dev/null | sort); do
		_n=$((_n + 1))
		# Frontmatter = lines between the first '---' and the next '---'.
		[ "$(head -1 "$_f")" = '---' ] || _badstart="$_badstart $(basename "$_f")"
		_fm=$(awk 'NR==1&&$0!="---"{exit} NR==1{next} /^---[[:space:]]*$/{exit} {print}' "$_f")
		_lack=""
		for _k in name description model; do
			printf '%s\n' "$_fm" | grep -qE "^$_k:" || _lack="$_lack$_k,"
		done
		[ -n "$_lack" ] && _missing="$_missing $(basename "$_f"):${_lack%,}"

		_mv=$(printf '%s\n' "$_fm" | grep -E '^model:' | head -1 | sed 's/^model: *//; s/["'"'"']//g; s/ *$//')
		if [ -n "$_mv" ]; then
			case "$_mv" in
			opus | sonnet | haiku) : ;;
			*) _badmodel="$_badmodel $(basename "$_f")=$_mv" ;;
			esac
		fi
	done

	if [ "$_n" -eq 0 ]; then
		skip F1 agent-frontmatter-fields "0 agent .md files found"
		skip F2 agent-model-value "0 agent .md files found"
		return
	fi

	if [ -n "$_missing" ] || [ -n "$_badstart" ]; then
		fail F1 agent-frontmatter-fields "first-line --- missing in:${_badstart:- none}; fields missing in:${_missing:- none} (of $_n agents)"
	else
		pass F1 agent-frontmatter-fields "all $_n agents start with --- and declare name+description+model"
	fi

	if [ -n "$_badmodel" ]; then
		fail F2 agent-model-value "model not in opus|sonnet|haiku:$_badmodel"
	else
		pass F2 agent-model-value "all $_n agents use opus|sonnet|haiku"
	fi
}

# J5.1 requires a deliberately small, fixed agent playbook shape.  These are
# exact English generated headings; do not accept a prose mention as a section.
# Section order uses line numbers, while Examples is bounded at the next H2 so
# a Normal/Edge heading elsewhere in the document cannot cause a false FAIL.
check_agent_j5_sections() {
	_ad="$1/.claude/agents"
	if [ ! -d "$_ad" ]; then
		skip F3 agent-j5-section-order "no agents/ directory"
		skip F4 agent-j5-rejection-examples "no agents/ directory"
		return
	fi

	_n=0
	_structure=""
	_examples=""
	for _f in $(find "$_ad" -type f -name '*.md' 2>/dev/null | sort); do
		_n=$((_n + 1))
		_r=$(grep -nE '^## Reasoning[[:space:]]*$' "$_f" 2>/dev/null | head -1 | cut -d: -f1)
		_w=$(grep -nE '^## Workflow[[:space:]]*$' "$_f" 2>/dev/null | head -1 | cut -d: -f1)
		_s=$(grep -nE '^## Self-Critique[[:space:]]*$' "$_f" 2>/dev/null | head -1 | cut -d: -f1)
		_b=$(grep -nE '^## Boundaries[[:space:]]*$' "$_f" 2>/dev/null | head -1 | cut -d: -f1)
		_u=$(grep -nE '^## Uncertainty Protocol[[:space:]]*$' "$_f" 2>/dev/null | head -1 | cut -d: -f1)
		_x=$(grep -nE '^## Examples[[:space:]]*$' "$_f" 2>/dev/null | head -1 | cut -d: -f1)
		_lack=""
		[ -n "$_r" ] || _lack="$_lack Reasoning"
		[ -n "$_w" ] || _lack="$_lack Workflow"
		[ -n "$_s" ] || _lack="$_lack Self-Critique"
		[ -n "$_b" ] || _lack="$_lack Boundaries"
		[ -n "$_u" ] || _lack="$_lack Uncertainty-Protocol"
		[ -n "$_x" ] || _lack="$_lack Examples"
		if [ -n "$_lack" ]; then
			_structure="$_structure $(basename "$_f"):missing${_lack}"
		elif [ "$_r" -ge "$_w" ] || [ "$_w" -ge "$_s" ]; then
			_structure="$_structure $(basename "$_f"):order R=$_r,W=$_w,S=$_s"
		else
			_between=$(awk -v start="$_r" -v end="$_s" 'NR > start && NR < end && /^##[[:space:]]+/ { count++ } END { print count + 0 }' "$_f")
			[ "$_between" -eq 1 ] || _structure="$_structure $(basename "$_f"):Reasoning/Workflow/Self-Critique must be adjacent H2 sections"
		fi
		for _section in Reasoning Workflow Self-Critique Boundaries "Uncertainty Protocol" Examples; do
			_count=$(grep -cE "^##[[:space:]]+$_section[[:space:]]*$" "$_f" 2>/dev/null || true)
			[ "$_count" -le 1 ] || _structure="$_structure $(basename "$_f"):duplicate H2 $_section"
		done
		_gates=$(grep -E '^##[[:space:]]+(Preflight|Verification)( Gate)?[[:space:]]*$' "$_f" 2>/dev/null | oneline)
		[ -z "$_gates" ] || _structure="$_structure $(basename "$_f"):duplicate contract gates $_gates"

		if [ -z "$_x" ]; then
			_examples="$_examples $(basename "$_f"):missing Examples"
		else
			_example_counts=$(awk '
				$0 == "## Examples" { in_examples=1; next }
				in_examples && /^##[[:space:]]+/ { in_examples=0 }
				in_examples && /^#{3,}[[:space:]]+/ {
					heading=$0
					sub(/^#{3,}[[:space:]]+/, "", heading)
					if (heading == "Rejection Case") rejection++
					lower=tolower(heading)
					if (lower ~ /(^|[[:space:]])(normal|edge)([[:space:]]|$)/) normal_edge++
				}
				END { printf "%d %d", rejection + 0, normal_edge + 0 }
			' "$_f")
			_reject=${_example_counts%% *}
			_normal_edge=${_example_counts#* }
			if [ "$_reject" -ne 1 ] || [ "$_normal_edge" -ne 0 ]; then
				_examples="$_examples $(basename "$_f"):rejection=$_reject,normal-edge=$_normal_edge"
			fi
		fi
	done

	if [ "$_n" -eq 0 ]; then
		skip F3 agent-j5-section-order "0 agent .md files found"
		skip F4 agent-j5-rejection-examples "0 agent .md files found"
		return
	fi
	if [ -n "$_structure" ]; then
		fail F3 agent-j5-section-order "required H2/order failures:$_structure"
	else
		pass F3 agent-j5-section-order "all $_n agents have one adjacent Reasoning < Workflow < Self-Critique contract plus Boundaries, Uncertainty Protocol, Examples; no duplicate Preflight/Verification gates"
	fi
	if [ -n "$_examples" ]; then
		fail F4 agent-j5-rejection-examples "Examples failures:$_examples"
	else
		pass F4 agent-j5-rejection-examples "all $_n Examples sections have exactly one Rejection Case and 0 Normal/Edge headings"
	fi
}

# J5.3 is scoped to runnable Claude rule files.  A section body is the text
# after its exact H2 through the next H2; headings or blank lines alone do not
# count as content.  Exceptions may explicitly say there are none.
check_rule_j5_contract() {
	_rd="$1/.claude/rules"
	if [ ! -d "$_rd" ]; then
		skip R5 rule-j5-frontmatter-and-sections "no rules/ directory"
		return
	fi

	_n=0
	_bad=""
	for _f in $(find "$_rd" -type f -name '*.md' 2>/dev/null | sort); do
		_n=$((_n + 1))
		_fm=$(awk 'NR==1&&$0!="---"{exit} NR==1{next} /^---[[:space:]]*$/{exit} {print}' "$_f")
		_issue=""
		[ "$(head -1 "$_f")" = '---' ] || _issue="$_issue first-line"
		printf '%s\n' "$_fm" | grep -qE '^name:' || _issue="$_issue name"
		printf '%s\n' "$_fm" | grep -qE '^description:' || _issue="$_issue description"
		_v=$(awk '
			$0 == "## Violation Determination" { active=1; next }
			active && /^##[[:space:]]+/ { active=0 }
			active && $0 !~ /^[[:space:]]*$/ && $0 !~ /^#/ {
				found=1
				lower=tolower($0)
				if ($0 ~ /->/ || lower ~ /(^|[[:space:]])(if|when|without|missing|omit|must|fail|forbid|prohibit|violation)([[:space:]]|$)/) observable=1
			}
			END { print found && observable ? "yes" : "no" }
		' "$_f")
		_e=$(awk '
			$0 == "## Exceptions" { active=1; next }
			active && /^##[[:space:]]+/ { active=0 }
			active && $0 !~ /^[[:space:]]*$/ && $0 !~ /^#/ { found=1 }
			END { print found ? "yes" : "no" }
		' "$_f")
		[ "$_v" = yes ] || _issue="$_issue Violation-Determination-observable"
		[ "$_e" = yes ] || _issue="$_issue Exceptions"
		[ -z "$_issue" ] || _bad="$_bad $(basename "$_f"):$_issue"
	done

	if [ "$_n" -eq 0 ]; then
		skip R5 rule-j5-frontmatter-and-sections "0 rule .md files found"
	elif [ -n "$_bad" ]; then
		fail R5 rule-j5-frontmatter-and-sections "J5.3 failures:$_bad"
	else
		pass R5 rule-j5-frontmatter-and-sections "all $_n rules start with name+description frontmatter and have non-empty Violation Determination + Exceptions"
	fi
}

check_counts() {
	_cd="$1/.claude"
	_r=$(find "$_cd/rules" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
	_a=$(find "$_cd/agents" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')

	if [ "$_r" -le "$CAP_RULE_COUNT" ]; then
		pass N1 rule-count-cap-12 "$_r rules (cap $CAP_RULE_COUNT)"
	else
		fail N1 rule-count-cap-12 "$_r rules exceeds cap $CAP_RULE_COUNT"
	fi

	if [ "$_a" -le "$CAP_AGENT_COUNT" ]; then
		pass N2 agent-count-cap-14 "$_a agents (cap $CAP_AGENT_COUNT)"
	else
		fail N2 agent-count-cap-14 "$_a agents exceeds cap $CAP_AGENT_COUNT"
	fi
}

check_execution_contract() {
	_rd="$1/.claude/rules"
	_ec=$(find_rule "$_rd" 'execution.?contract' 'execution.?contract') || {
		skip X1 execution-contract-clause-numbering "no execution-contract rule (see R4)"
		return
	}
	_lack=""
	_found=""
	for _i in 1 2 3 4 5; do
		_c=$(countmatch "EC-$_i" "$_ec")
		if [ "$_c" -eq 0 ]; then
			_lack="$_lack EC-$_i"
		else
			_found="$_found EC-$_i=$_c"
		fi
	done
	if [ -n "$_lack" ]; then
		fail X1 execution-contract-clause-numbering "$_ec missing clause(s):$_lack (found:${_found:- none})"
	else
		pass X1 execution-contract-clause-numbering "$_ec hits:$_found"
	fi
}

# ---------------------------------------------------------------- driver

validate_one() {
	_team="$1"
	TOTAL=0
	PASSED=0
	FAILED=0
	SKIPPED=0

	if [ ! -d "$_team" ]; then
		printf '## %s\n' "$_team"
		emit T0 team-directory-exists FAIL "no such directory: $_team"
		printf 'SUMMARY %s | total=1 passed=0 failed=1 skipped=0\n' "$_team"
		G_TOTAL=$((G_TOTAL + 1))
		G_FAILED=$((G_FAILED + 1))
		return 1
	fi

	printf '## %s\n' "$_team"

	_why=$(not_a_claude_team "$_team")
	if [ -n "$_why" ]; then
		emit T0 claude-team-detected SKIP "$_why"
		printf 'SUMMARY %s | total=1 passed=0 failed=0 skipped=1\n' "$_team"
		G_TOTAL=$((G_TOTAL + 1))
		G_SKIPPED=$((G_SKIPPED + 1))
		TEAMS_SKIPPED=$((TEAMS_SKIPPED + 1))
		return 0
	fi

	emit T0 claude-team-detected PASS "$_team/.claude/ present; validating"
	check_structure "$_team"
	check_mandatory_rules "$_team"
	check_claude_md "$_team"
	check_entry_skill "$_team"
	check_runtime_setup "$_team"
	check_settings "$_team"
	check_output_mode "$_team"
	check_caps "$_team"
	check_frontmatter "$_team"
	check_agent_j5_sections "$_team"
	check_rule_j5_contract "$_team"
	check_counts "$_team"
	check_execution_contract "$_team"

	printf 'SUMMARY %s | total=%s passed=%s failed=%s skipped=%s\n' \
		"$_team" "$TOTAL" "$PASSED" "$FAILED" "$SKIPPED"

	G_TOTAL=$((G_TOTAL + TOTAL))
	G_PASSED=$((G_PASSED + PASSED))
	G_FAILED=$((G_FAILED + FAILED))
	G_SKIPPED=$((G_SKIPPED + SKIPPED))
	TEAMS_VALIDATED=$((TEAMS_VALIDATED + 1))

	[ "$FAILED" -eq 0 ]
}

usage() {
	cat <<'USAGE'
Usage:
  validate-team.sh <team-path>   validate a single generated team
  validate-team.sh --all         validate every directory under teams/
  validate-team.sh --help

Output: {check-id} {check-name} | PASS|FAIL|SKIP | {evidence}   (EC-3.6 format)
Exit:   0 = all checks passed, 1 = at least one FAIL.

Store criterion lines in verifier-owned evidence files; return those paths in
the EC report rather than pasting raw validator output.

Mechanical checks only. Judgment items (responsibility overlap, semantic rule
correctness, example diversity) remain in .claude/skills/quality-validation/
SKILL.md for a model to run — they are deliberately not faked here.
USAGE
}

main() {
	if [ "$#" -eq 0 ]; then
		usage
		exit 2
	fi

	case "$1" in
	-h | --help)
		usage
		exit 0
		;;
	--all)
		_teams_dir="${2:-$REPO_ROOT/teams}"
		if [ ! -d "$_teams_dir" ]; then
			printf 'ERROR | teams directory not found: %s\n' "$_teams_dir" >&2
			exit 2
		fi
		for _d in "$_teams_dir"/*/; do
			[ -d "$_d" ] || continue
			validate_one "${_d%/}" || true
			printf '\n'
		done
		printf 'TOTAL | teams=%s validated=%s team-skipped=%s checks=%s passed=%s failed=%s skipped=%s\n' \
			"$((TEAMS_VALIDATED + TEAMS_SKIPPED))" "$TEAMS_VALIDATED" "$TEAMS_SKIPPED" \
			"$G_TOTAL" "$G_PASSED" "$G_FAILED" "$G_SKIPPED"
		[ "$G_FAILED" -eq 0 ] || exit 1
		exit 0
		;;
	*)
		validate_one "${1%/}" || exit 1
		exit 0
		;;
	esac
}

main "$@"
