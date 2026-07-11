# AAR 20260712: Workflow status queue overlay hotfix

## Scope

VULCAN implemented a dirty read-only inspectability hotfix for `uv run projectkoios workflow status`.

## What happened

- HERMES/operator was misled because Petri-net status showed `user_decision` and `approve_next_slice` while queue-control context was hidden.
- ATHENA advised a bounded dirty code patch rather than documentation-only warning.
- VULCAN patched status output to include the existing queue fixture state.
- VULCAN added a hard warning when queue `active_item` is set.
- Focused tests, mypy, Python policy, and diff hygiene passed.

## Process issues

- The command exposed only one control plane while operators needed both Petri-net token state and queue control-surface state.
- Prior status output made it too easy to infer queued-item activation from enabled Petri-net transition alone.
- The hotfix was intentionally dirty and bounded; it should not become final workflow architecture by accident.

## Proposed follow-up improvements

- ATHENA should decide whether to produce a formal workflow status/queue consistency brief.
- Future workflow status output should have a designed read-model rather than bolting fixture output into the command.
- Add mismatch reporting if status fixture and queue fixture disagree about active slice/item.

## Candidate ADR or implementation topics

- Workflow status/queue consistency architecture.
- Operator-facing status affordance semantics.
- Queue fixture versus Petri-net token authority boundary.

## Current status

Hotfix implemented and validated as read-only inspectability repair. No `docs/adr`, `docs/schemas`, workflow mutation, activation, migration, or authority cutover was introduced.
