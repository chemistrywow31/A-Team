---
name: Grok Hooks
description: Preserve lifecycle bookkeeping with verified optional native hooks and explicit workflow fallbacks
---

# Grok Hooks

## Applicability

- Applies to coordinators, agent/runtime writers, and preflight reviewers considering lifecycle automation.
- Trigger: a target proposes or retains a hook; hook-free teams still perform the bookkeeping below in their workflow.

## Rule Content

### Preserve Bookkeeping Without Inventing Configuration

The coordinator must create the task brief/worklog, record user decisions, checkpoint before losing context, and check phase evidence at completion under `.grok/policies/worklog.md`. Hooks may automate those steps only when the installed event, supported configuration surface, payload, output, and effective behavior are verified.

The pinned native source defines `SessionStart`, `UserPromptSubmit`, `PreCompact`, `Stop`, and tool/subagent events in `xai-grok-hooks/src/event.rs`; agent definitions have a parsed `hooks` field in `xai-grok-agent/src/config.rs`. These source facts establish investigation candidates, not installed activation or permission to emit an untested hook schema. Project `.grok/config.toml` does not supply a hook section.

| Bookkeeping intent | Candidate native event | Safe default |
| --- | --- | --- |
| Establish project worklog | `SessionStart` | Root creates its assigned directories and brief |
| Preserve the user's requirement/answer | `UserPromptSubmit` | Root records only needed decisions and dialogue evidence |
| Preserve continuation state | `PreCompact` | Root updates brief, findings, and decisions |
| Detect missing phase evidence | `Stop` | Root performs an advisory completeness check |
| Audit authorized external effects | Tool lifecycle event | Root records the exact operation/evidence in the worklog |

A first-run presentation preference may be asked through normal user conversation when useful. Do not port a foreign output-style hook or write an unsupported preference setting.

### Evidence Before Emitting A Hook

For each proposed hook, record the installed version, exact native configuration location/schema, event/matcher, input/output contract, trigger condition, timeout, command dependencies, and expected result. Validate with real parsers and an isolated fresh-shell fixture, then exercise the event through the installed runtime before claiming it works. A listed hook or empty error list is insufficient execution evidence.

Keep optional features optional. If effective support is unavailable, report the hook as UNVERIFIED and use the explicit coordinator workflow; do not make hook absence a blocker for otherwise complete native generation. Never relax trust or approvals to activate it.

### Bound Effects And Dependencies

Default bookkeeping hooks to advisory/non-blocking. Blocking requires a credible dangerous action and all five proportional-design fields; do not block ordinary configuration, startup, stop/restart, update, or recovery for a hypothetical integrity concern.

Keep synchronous bookkeeping within a 10-second authoring budget; longer work needs documented native asynchronous support and a tested non-blocking design. Confirm the actual shell and installed dependencies. Do not assume JSON processors or language runtimes exist on the user's machine, and do not use a silent failure suffix to hide required evidence loss.

Anchor every path to the verified target root from a documented native payload/environment contract or an explicitly configured root. Test from a caller cwd outside the project. Do not assume the current directory is the project root or substitute an invented environment variable.

A prompt-capture hook can retain secrets or personal data. Name its consumer, minimum retained fields, storage path, and retention policy; omit raw prompt capture or redact before persistence when sensitive content is plausible. Logs must stay inside exact assigned paths. Hooks never supply authorization for external writes.

### Rejection Example

Reject a generated project TOML with a guessed hook table that silently captures every user prompt and claims `Stop` proves full phase triads exist. Move bookkeeping into the coordinator's explicit workflow; investigate and test only the narrowly required native automation before adding it.

## Violation Determination

- An untested hook schema/event/payload or unsupported project hook table is shipped as effective automation -> Violation.
- Mandatory bookkeeping disappears because no hook is available, or hook absence alone blocks native delivery -> Violation.
- Hook writes depend on caller cwd, unknown variables/dependencies, or paths outside assigned ownership -> Violation.
- Ordinary work is blocked without proportional evidence, timeout exceeds the declared budget, or failures silently discard required evidence -> Violation.
- Raw prompt capture lacks a consumer/privacy boundary, or a hook bypasses authorization/trust -> Violation.

## Exceptions

A non-interactive deterministic pipeline may document a mechanical phase-log profile instead of full phase triads under the worklog policy. It does not need interactive events. Required decision evidence and privacy boundaries still apply.

Tradeoff: Hooks add startup cost and another failure surface. Prefer explicit workflow steps until repeated cost justifies tested native automation; retain manual recovery when automation fails.
