```json
{
  "title": "Live Petri-net skeleton slice 0 implementation plan",
  "artifact_type": "implementation-plan",
  "status": "awaiting-user-hermes-approval",
  "datetime": "20260711.114700Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_brief": "docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md",
  "slice_name": "live-petri-net-skeleton-slice-0",
  "target_command": "uv run projectkoios workflow status",
  "next_owner": "USER_HERMES_APPROVAL"
}
```

# Implementation plan 20260711.114700: Live Petri-net skeleton slice 0

## Scope boundary

Implement the approved read-only CLI status surface only:

```bash
uv run projectkoios workflow status
```

The command will load one static fixture from `dev/workflow-nets/bootstrap-harness.workflow-net.json`, instantiate existing `projectkoios.workflow` Petri-net classes, validate the net, compute enabled transitions through `PetriNetExecutor.enabled_bindings(...)`, and print deterministic human-readable status.

Out of scope remains firing, persistence, Operator Console integration, workflow-object integration, schema/product authority, live adapters, and broad JSON loader/framework work.

## Planned file changes

1. Add `dev/workflow-nets/bootstrap-harness.workflow-net.json`
   - Fixture fields: `net_id`, `places`, `transitions`, `arcs`, `marking`, and small `decision` metadata.
   - Include at least three places, one token at a user-decision place, one enabled transition, and one disabled transition.
   - Use existing `PetriNetArcKind` string values: `input`, `output`.
   - Keep token color string-valued for current `PetriNetToken.from_color(...)`, e.g. `requires_user_decision: "true"`.

2. Add `src/python/projectkoios/cli/workflow.py`
   - Register `workflow status` under argparse.
   - Add small CLI-local DataObject/ActionObject-style helpers, likely:
     - `WorkflowStatusFixture`: loaded fixture path, net id, `PetriNetState`, and decision metadata.
     - `WorkflowStatusFixtureLoader`: narrow fixture-to-runtime mapper for this one static JSON shape.
     - `WorkflowStatusReporter`: deterministic human-readable formatter.
     - `Command`: argparse adapter.
   - Use `json` and `Path` only; no persistence, mutation, live reads beyond the static fixture file.
   - Validate through `WorkflowValidator` or `PetriNetExecutor.enabled_bindings(...)` before output.
   - Determine user-decision-required from fixture decision metadata and/or token color, without adding permission/actor semantics.

3. Edit `src/python/projectkoios/cli/main.py`
   - Import and register the new `workflow` command group alongside existing top-level command groups.

4. Add `tests/projectkoios/cli/test__workflow_status.py`
   - Cover command registration through the public CLI entrypoint or command adapter.
   - Assert output includes:
     - `workflow: bootstrap-harness.slice-0`;
     - fixture path;
     - place identifiers/labels;
     - token id and current place;
     - enabled transition from runtime computation;
     - disabled transition absent from enabled list;
     - `user decision required: yes`.
   - Include a focused assertion that `PetriNetExecutor.enabled_bindings(...)` is the source of enabled transition reporting, not just hard-coded fixture output.

## Output shape

Exact copy can vary, but intended output is close to:

```text
workflow: bootstrap-harness.slice-0
fixture: dev/workflow-nets/bootstrap-harness.workflow-net.json

places:
  - intake: Intake
  - user_decision: User decision
  - implementation: Implementation

Tokens:
  - current-slice at user_decision color={kind=workflow-slice, requires_user_decision=true}

enabled transitions:
  - approve_next_slice: Approve next slice

user decision required: yes
```

## Validation plan

Run from repository root:

```bash
uv run projectkoios workflow status
uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q
uv run mypy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
git diff --check
```

If mypy or policy scope needs narrowing due to new `tests/projectkoios/cli/`, record the exact command and result in the implementation report.

## Pause/approval state

Paused for USER/HERMES approval before coding, per brief. Direct implementation can proceed if USER/HERMES authorizes this plan or explicitly authorizes direct coding from the brief.
