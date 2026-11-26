# Canonical Reasoning and Self-Critique Blocks

An optional skeleton for an agent whose work has real decisions and failure modes (`.claude/rules/reasoning-and-self-critique.md`). When you use it, keep the three headers in this order and replace the bullets with role-specific instructions; leave it out when the sections would hold nothing specific to the role. Do not copy generic bullets into the finished agent or add duplicate Preflight/Verification forms.

```markdown
## Reasoning

- Confirm {material input and authority needed for this role's decision}.
- Choose {approach} from {relevant evidence}; state only material assumptions or gaps.

## Workflow

1. {Perform the assigned work within exact owned paths and authority.}
2. {Produce the requested artifact and evidence.}

## Self-Critique

- Check {role-specific acceptance criteria} against the actual artifact and cite evidence.
- Challenge {likely failure or rejection boundary}; fix gaps before submission.
- After a correction, rerun every criterion citing a changed file and dependent mapping/parity checks; revisit other criteria when affected by new evidence.
```

The sections are instructions, not a required output form. Return concise decisions, material assumptions, unresolved gaps, and verification evidence through EC-1 or the worklog; do not request private reasoning transcripts or nine labeled slots.

For coordinators, add the bounded outcome, owner, ready inputs, exact path ownership, and acceptance criteria to the existing Reasoning/Workflow contract. Preserve useful parallel work and sequential producer-freeze/review gates. A separate pre-dispatch form is unnecessary.

For deterministic Tier 1 utilities, keep the same headers with brief input-validity, format, and input-coverage checks; document the zero-judgment justification. Producer Self-Critique never replaces independent EC-3 acceptance.
