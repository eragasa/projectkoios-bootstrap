# ADR 20260703.000001: ADR-Driven Implementation Kernel

## Status

draft

## Context

The repository needs a minimal control-plane kernel for ADR-driven implementation. The kernel exists to prevent implementation work from being mistaken for approval and to keep implementation behavior bounded by explicit USER authority.

The USER is the human terminal operator and the final authority.

## Decision

This kernel defines the minimum machine-enforceable rules for ADR-driven implementation.

### Normative rules

- The USER MUST be treated as the final authority for approval.
- A generated plan MUST NOT be treated as approval.
- A proposal MUST NOT be treated as approval.
- An implementation record MUST NOT be treated as approval unless it records explicit USER approval.
- VULCAN MUST NOT treat its own implementation plan as approval.
- VULCAN MUST NOT expand scope while implementing.
- VULCAN MUST NOT invent architecture.
- VULCAN MUST NOT mix `DataObject` and `ActionObject`.
- VULCAN MUST NOT move implementation code into production without explicit USER approval.
- Any implementation surface MAY include validation records only if they are traceable to the governing ADR and the USER approval state.
- Rules in this kernel SHOULD be read as enforcement constraints, not as architecture guidance.

### Promotion path

| Stage | State | Surface |
|---|---|---|
| 1 | `draft` | `adr.<name>.draft.md` |
| 2 | `draft` | `adr.<name>.draft.md` + `spike/<name>/` |
| 3 | `proposed` | `adr.<name>.proposed.md` + `implementation.<name>.md` + `implementation.<name>.json` |
| 4 | `proposed` | `implementation/<name>/` |
| 5 | `active` | `adr.<name>.md` + `src/python/projectkoios/bootstrap/*` |

### Enforcement notes

- Stage transitions MUST be explicit.
- A stage MAY advance only when the surface for that stage exists.
- USER approval MUST be recorded before any active implementation promotion.
- An implementation artifact without explicit USER approval MUST remain non-authoritative.

## Consequences

- Implementation work stays subordinate to explicit USER authority.
- Plan generation cannot self-authorize implementation.
- Control-plane checks can reject scope drift, approval drift, and object-type mixing.
