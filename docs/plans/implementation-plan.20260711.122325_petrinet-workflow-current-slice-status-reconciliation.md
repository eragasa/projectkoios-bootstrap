```json
{
  "title": "Petri-net workflow current-slice status reconciliation implementation plan",
  "artifact_type": "implementation-plan",
  "status": "awaiting-user-hermes-approval",
  "datetime": "20260711.122325Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_brief": "docs/plans/implementation-brief.20260711.122048_petrinet-workflow-current-slice-status-reconciliation.md",
  "slice_name": "petrinet-workflow-current-slice-status-reconciliation-slice-2",
  "target_command": "uv run projectkoios workflow status",
  "next_owner": "USER_HERMES_APPROVAL"
}
```

# Implementation plan 20260711.122325: Petri-net workflow current-slice status reconciliation

## Scope boundary

Reconcile the existing static bootstrap workflow-net fixture so the visible status command reports the current Petri-net workflow slice:

```bash
uv run projectkoios workflow status
```

This is fixture/status-output reconciliation only. The workflow remains read-only and at `user_decision` with `user decision required: yes`.

No Petri-net runtime logic, transition firing, persistence, live adapter/session reads, Operator Console integration, workflow-object runtime coupling, schema authority, role/permission semantics, or product/mothership authority will be changed.

## Planned file changes

1. Edit `dev/workflow-nets/bootstrap-harness.workflow-net.json`
   - Replace token color `active_slice=live-petri-net-skeleton-slice-0` with `active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2`.
   - Keep token at `user_decision`.
   - Keep `requires_user_decision=true`.
   - Keep enabled transition behavior unchanged: `approve_next_slice` remains enabled through existing runtime enabledness checks.
   - Preserve static bootstrap fixture / non-canonical authority wording.

2. Update focused status test if needed
   - Likely update `tests/projectkoios/cli/test__workflow_status.py` assertion from the old active-slice token color to the new slice name.
   - Do not add broad runtime assertions or turn the fixture into durable completion authority.

3. Add implementation report
   - `docs/implementation/petrinet-workflow-current-slice-status-reconciliation-slice-2.<timestamp>.md`.
   - Record changed files, validation output, and preserved boundaries.

4. Add AAR only if useful
   - This is a small fixture reconciliation; write a short AAR if process lessons or handoff notes need durable capture.

5. Update VULCAN workspace state
   - `workspaces/vulcan/active.md` and `workspaces/vulcan/state.md`.

## Expected output after implementation

`uv run projectkoios workflow status` should still print workflow id, fixture path, places, token location/color, enabled transition, and user decision status, with the token color showing:

```text
active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2
```

and still showing:

```text
current-slice at user_decision
user decision required: yes
```

## Validation plan

From repository root:

```bash
uv run projectkoios workflow status
uv run pytest tests/projectkoios/workflow tests/projectkoios/cli -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow tests/projectkoios/cli
python -m json.tool dev/workflow-nets/bootstrap-harness.workflow-net.json >/dev/null
git diff --check
```

If the full focused pytest scope is unnecessarily broad or unavailable, VULCAN may narrow to the existing workflow/status tests and record the exact command and result in the implementation report.

## Pause/approval state

Paused for USER/HERMES approval before coding, per brief. Direct implementation can proceed only if USER/HERMES explicitly approves this plan or explicitly authorizes direct implementation from the brief.
