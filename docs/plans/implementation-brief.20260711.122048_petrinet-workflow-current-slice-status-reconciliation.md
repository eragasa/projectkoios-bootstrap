```json
{
  "title": "Petri-net workflow current-slice status reconciliation implementation brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-planning-ready-pending-user-hermes-approval",
  "datetime": "20260711.122048Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "Petri-net workflow harness / workflow inspectability",
  "previous_slice": "petrinet-workflow-agent-status-skill-slice-1",
  "slice_name": "petrinet-workflow-current-slice-status-reconciliation-slice-2",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.122048: Petri-net workflow current-slice status reconciliation

## Purpose

Continue the Petri-net workflow harness / workflow inspectability effort by reconciling the static live-status fixture with the current active Petri-net workflow slice.

The current inspectability command works:

```bash
uv run projectkoios workflow status
```

But it still reports:

```text
active_slice=live-petri-net-skeleton-slice-0
```

while the active Petri-net workflow work has advanced through `petrinet-workflow-agent-status-skill-slice-1` and is now selecting the next Petri-net slice. This slice closes that control-surface gap without changing runtime semantics.

## Scope

In scope:

```text
dev/workflow-nets/bootstrap-harness.workflow-net.json
tests/projectkoios/cli or tests/projectkoios/workflow focused status-output test, if needed
docs/implementation/<implementation-report>.md
docs/AAR/<aar-if-useful>.md
```

Expected fixture target:

```text
active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2
place=user_decision
requires_user_decision=true
enabled transition=approve_next_slice
```

## Required behavior

1. `uv run projectkoios workflow status` must report the active token as the current slice, not `live-petri-net-skeleton-slice-0`.
2. The workflow remains in `user_decision` with `user decision required: yes` until USER/HERMES explicitly approves an implementation transition.
3. The command remains read-only.
4. The static fixture remains explicitly non-canonical workflow authority.
5. The slice must not add transition firing, persistence, live adapter/session reads, runtime mutation, schema authority, Operator Console integration, workflow-object runtime coupling, role/permission expansion, or product/mothership workflow authority.
6. If tests are added, they should validate the visible status output or fixture content narrowly and should not turn the fixture into durable completion authority.

## Acceptance criteria

1. The static bootstrap workflow-net fixture no longer reports `active_slice=live-petri-net-skeleton-slice-0`.
2. The fixture reports the selected/current slice as `petrinet-workflow-current-slice-status-reconciliation-slice-2` unless USER/HERMES selects a different exact slice name before implementation.
3. `uv run projectkoios workflow status` still reports:
   - workflow id;
   - fixture path;
   - current token/place;
   - enabled transitions;
   - user decision requirement.
4. The command behavior remains read-only and uses existing runtime enabledness checks.
5. Tests, if touched, remain focused on status inspectability and do not introduce broad workflow-runtime assertions.
6. No source outside the narrow fixture/status-test/report scope is changed without pausing for USER/HERMES.

## Suggested validation

From repository root:

```bash
uv run projectkoios workflow status
uv run pytest tests/projectkoios/workflow tests/projectkoios/cli -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow tests/projectkoios/cli
python -m json.tool dev/workflow-nets/bootstrap-harness.workflow-net.json >/dev/null
git diff --check
```

If no CLI test package exists or the focused test path differs, VULCAN may narrow the pytest command to the relevant existing workflow/status tests and report the exact command used.

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- changing Petri-net runtime logic;
- changing `projectkoios workflow status` command semantics beyond displayed fixture content;
- adding transition firing or dry-run behavior;
- introducing persistence or canonical workflow-state storage;
- adding live intercom/session adapters;
- adding Operator Console integration;
- broad workflow schema/authority changes;
- changing the selected slice name.

## Handoff

VULCAN should produce a concise implementation plan and pause for USER/HERMES approval before coding unless USER/HERMES explicitly approves direct implementation from this brief.
