---
name: Anti Over-Engineering
category: templates
applies_when:
  - generating-rules
  - generating-architecture-agent
  - generating-execution-agent
  - generating-coding-team
  - generating-packaging-agent
  - generating-deployment-agent
  - generating-migration-agent
  - generating-recovery-agent
  - generating-review-agent
tags: [simplicity, minimal-changes, scope-control, coding, proportionality, safeguards, architecture, implementation, packaging, deployment, migration, recovery, review]
source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/claude-4-best-practices.md
extension_source: .grok/policies/proportional-design.md
---

# Anti Over-Engineering

## When to Use

Inject into rule generation and into relevant architecture, implementation, packaging, deployment, migration, recovery, and review prompts. The baseline below is from the named Anthropic source; the proportional-safeguard extension is the user-approved A-Team addition identified by `extension_source`. Original D6-D9 decision attribution is preserved in the archived source asset; the active path is the native policy, not an unavailable historical worklog.

## Template

```text
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task.

Apply proportional design when proposing or retaining a non-obvious safeguard such as a check, gate, integrity lock, compatibility layer, recovery protocol, or deployment blocker. Only in that case, add a short `Safeguard Decision` with exactly these fields:

- Evidence / likelihood: Cite the observed failure, explicit requirement, or credible likelihood. A rare unsupported hypothetical is an assumption or monitoring trigger, not implementation or a release blocker.
- Protected impact: State the concrete harm the safeguard prevents.
- Cheapest adequate alternative: Compare against the simplest control that covers the evidenced risk.
- Ordinary-path cost / new failures: State effects on routine configuration, copy/start, intentional stop/restart, update, and recovery, plus failure modes introduced by the safeguard.
- Removal / override / monitoring: Define when to remove or bypass the safeguard, or which signal would justify adding it later.

Absent proportionate contrary evidence, keep mutable configuration, package copy/start, intentional stop/restart, update, and recovery usable. Do not let whole-package checksums lock routine configuration changes or let residual-task checks block restart after an intentional stop merely for speculative safety.

Keep narrowly scoped controls when credible corruption, security, privacy, compatibility, data-loss, compliance, or irreversible-mutation risk justifies them. Apply the same five fields and minimize the protected boundary. Use the existing independent reviewer to return a criterion-level verdict; do not add a role, state machine, or approval ladder solely for this contract.
```

## Adaptation Notes

Use the full block for rule generation. For producer prompts, include the `Safeguard Decision` slot only when the role can propose or retain a non-obvious safeguard. For the existing independent reviewer, require a verdict for each of the five fields and for preservation of ordinary paths. Pair with `anti-hard-coding` when both over-engineering and under-engineering are credible failure modes.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/templates/anti-over-engineering.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
