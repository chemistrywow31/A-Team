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
# so a fresh-context verifier can paste it directly as its evidence.
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
	grep -icE "$1" "$2" 2>/dev/null || echo 0
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

# ---------------------------------------------------------------- team detection

# Prints a skip reason when the directory is not a Claude Code team, else nothing.
not_a_claude_team() {
	_d="$1"
	_n=$(basename "$_d")

	if [ ! -d "$_d/.claude" ]; then
		if [ -f "$_d/AGENTS.md" ] && [ ! -f "$_d/CLAUDE.md" ]; then
			echo "no .claude/ directory; AGENTS.md present (Codex-only tree)"
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
	if [ -f "$_d/CLAUDE.md" ] &&
	   grep -qiE '(reference[- ]only|not a runnable|NOT a runnable|唯讀鏡像|參考用鏡像)' "$_d/CLAUDE.md" 2>/dev/null; then
		echo "charter declares a reference-only mirror: $(firstmatch '(reference[- ]only|not a runnable|NOT a runnable)' "$_d/CLAUDE.md")"
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

	# The entry-point skill is identified by SHAPE, not by filename. Teams name
	# it after their coordinator or identity (callimachus/, ventris/, tongzheng/)
	# and that is preferred over a generic boss/ — see rules/output-structure.md,
	# Entry-Point Skill. A fixed-name check reported 10 such teams as defective
	# when each had in fact shipped a better-named front door.
	_cands=$(grep -rlE '^disable-model-invocation: *true' "$_t/.claude/skills" 2>/dev/null | sort)
	_n=$(printf '%s' "$_cands" | grep -c . 2>/dev/null || echo 0)

	if [ "$_n" -eq 0 ]; then
		fail E1 entry-skill-present "no skill under $_t/.claude/skills declares 'disable-model-invocation: true'"
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

	_h=$(firstmatch '^disable-model-invocation: *true' "$_bs")
	[ -n "$_h" ] && pass E2 entry-disable-model-invocation "$_h" ||
		fail E2 entry-disable-model-invocation "no 'disable-model-invocation: true' in $_bs frontmatter"

	_h=$(grep -nE '^allowed-tools:' "$_bs" 2>/dev/null | grep -i 'agent' | head -1 | cut -c1-120 | oneline)
	[ -n "$_h" ] && pass E3 entry-allowed-tools-agent "$_h" ||
		fail E3 entry-allowed-tools-agent "allowed-tools missing or does not grant Agent: $(firstmatch '^allowed-tools:' "$_bs" | sed 's/^$/absent/')"

	_h=$(firstmatch '^argument-hint:' "$_bs")
	[ -n "$_h" ] && pass E4 entry-argument-hint "$_h" ||
		fail E4 entry-argument-hint "no 'argument-hint:' in $_bs frontmatter"

	# Main-session adoption: a reference to the coordinator .md AND an adopt
	# instruction. The path reference is matched language-neutrally — Chinese
	# teams write "讀取 `.claude/agents/x.md` 並採用為 playbook", which an
	# English-only /read .*agents/ pattern false-FAILs.
	_read=$(grep -inE 'agents/[a-z0-9._-]+\.md' "$_bs" 2>/dev/null | head -1 | cut -c1-100 | oneline)
	_adopt=$(countmatch '(adopt|採納|採用|接管|adopts? (it|its))' "$_bs")
	if [ -n "$_read" ] && [ "$_adopt" -gt 0 ]; then
		pass E5 entry-main-session-adoption "$_read (+$_adopt adopt-mentions)"
	elif [ -n "$_read" ]; then
		fail E5 entry-main-session-adoption "references coordinator .md ($_read) but 0 adopt/採用 instructions"
	else
		fail E5 entry-main-session-adoption "no reference to .claude/agents/{coordinator}.md in $_bs"
	fi

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
	_badmodel=""
	for _f in $(find "$_ad" -type f -name '*.md' 2>/dev/null | sort); do
		_n=$((_n + 1))
		# Frontmatter = lines between the first '---' and the next '---'.
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

	if [ -n "$_missing" ]; then
		fail F1 agent-frontmatter-fields "missing fields in$_missing (of $_n agents)"
	else
		pass F1 agent-frontmatter-fields "all $_n agents declare name+description+model"
	fi

	if [ -n "$_badmodel" ]; then
		fail F2 agent-model-value "model not in opus|sonnet|haiku:$_badmodel"
	else
		pass F2 agent-model-value "all $_n agents use opus|sonnet|haiku"
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
	check_caps "$_team"
	check_frontmatter "$_team"
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
