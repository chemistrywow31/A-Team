---
name: Proportional Design
description: Require evidence and ordinary-path safety before adding or retaining non-obvious safeguards
---

# Proportional Design

## Applicability

- Applies to: architecture, design, implementation, packaging, deployment, migration, recovery, and independent review work
- Trigger condition: a proposal or existing design adds or retains a non-obvious safeguard

## Rule Content

### Prefer The Cheapest Adequate Design

Use the simplest mechanism that satisfies observed requirements and credible, likely failure modes. Treat an unsupported rare hypothetical as an assumption or monitoring trigger, not as code, a special protocol, or a release blocker.

### Record A Short Safeguard Decision

Only when the trigger condition applies, record these five fields:

1. `Evidence and likelihood:` cite the requirement, incident, measurement, or credible scenario.
2. `Protected impact:` name what fails and the practical consequence.
3. `Cheapest adequate alternative:` compare the proposed safeguard with the least complex sufficient control.
4. `Ordinary-path cost and new failure modes:` identify effects on configuration, updates, deployment, recovery, maintenance, and comprehension.
5. `Removal, override, or monitoring trigger:` state how the control is escaped, retired, or revisited.

Reject or remove the safeguard when evidence and protected impact do not outweigh its ordinary-path cost and new failure modes.

### Preserve Ordinary Operation

Absent proportionate contrary evidence, keep mutable configuration, package copy-and-start, intentional stop-and-restart, routine updates, and recovery usable. Do not let whole-tree integrity locks, stale-work checks, or similar gates block those paths solely for hypothetical protection.

### Preserve Justified High-Impact Controls

Keep narrowly scoped controls justified by concrete corruption, security, privacy, compatibility, data-loss, compliance, or irreversible-mutation risk. Bound each control to the evidenced risk and preserve a usable recovery or authorized override when the requirement permits one.

## Violation Determination

- A non-obvious safeguard is proposed or retained without all five decision fields -> Violation
- A rare unsupported hypothetical becomes code, a special protocol, or a release blocker -> Violation
- A safeguard blocks an ordinary configuration, update, deployment, restart, or recovery path without evidence that its protected impact outweighs the added cost and failure modes -> Violation
- A less complex adequate control is identified but rejected without evidence -> Violation
- A safeguard has no bounded scope or removal, override, or monitoring trigger -> Violation

## Exceptions

- A law, contract, platform constraint, or confirmed high-impact risk may require a blocking control. Record the exact requirement or evidence in the five fields, limit the control to that boundary, and document any permitted recovery or override.
