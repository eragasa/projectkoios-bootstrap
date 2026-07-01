# AAR 20260701.153038: Delegated identity resolution

## Scope

ATHENA debugging of `AGENTS.md` identity instructions after a delegated Codex
session identified itself as HERMES when the user expected ATHENA.

## What happened

The instructions clearly separated harness identity from runtime identity, but
they did not give delegated operators an explicit identity-resolution order.
The prominent migration statement that HERMES has command authority made it too
easy for a delegated operator to select the HERMES session protocol even when
the intended represented role was ATHENA.

## Process issues

Command authority, artifact ownership, represented harness identity, and session
protocol selection were adjacent but not ordered. The missing precedence rule
caused command authority to override the user-specified represented role.

## Proposed follow-up improvements

Keep `AGENTS.md` identity resolution explicit and test future role-protocol
changes against this case: if the user says "you are ATHENA", a delegated
operator must speak as ATHENA and must not run the HERMES session protocol
unless separately asked for HERMES repo/run-control state.

## Candidate ADR or implementation topics

- Delegated-operator identity-resolution tests or examples for harness prompts.
- Review whether `docs/agent-charter.md` should mirror the same precedence rule.

## Current status

`AGENTS.md` now includes a delegated identity resolution section that gives
explicit user role naming first priority and states that command authority is
not identity.
