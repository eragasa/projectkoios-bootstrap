```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "live-petri-net-skeleton-slice-0-implemented-validated",
  "datetime": "20260711.114916Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md",
    "docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md",
    "docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md",
    "dev/workflow-nets/bootstrap-harness.workflow-net.json",
    "src/python/projectkoios/cli/workflow.py",
    "src/python/projectkoios/cli/main.py",
    "tests/projectkoios/cli/test__workflow_status.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": "docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md",
  "latest_report": "docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md",
  "latest_aar": "docs/AAR/aar.20260711.114916_live-petri-net-skeleton-slice-0.md"
}
```

# Vulcan active work

## Current priority stack

1. `live-petri-net-skeleton-slice-0`: implemented and validated.
2. Target command: `uv run projectkoios workflow status`.
3. Boundaries preserved: read-only CLI status; static fixture only; existing `projectkoios.workflow` Petri-net runtime; no firing, persistence, Operator Console integration, workflow-object integration, schema/product expansion, or live adapters.

## Latest working material

- Brief: `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`.
- Plan: `docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md`.
- Implementation report: `docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md`.
- AAR: `docs/AAR/aar.20260711.114916_live-petri-net-skeleton-slice-0.md`.
- Source architecture: `docs/architecture/architecture.petrinet.00.md`.
- Source ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.

## Implemented outputs

- Static fixture: `dev/workflow-nets/bootstrap-harness.workflow-net.json`.
- CLI adapter/loader/reporter: `src/python/projectkoios/cli/workflow.py`.
- Top-level command registration in `src/python/projectkoios/cli/main.py`.
- Focused CLI tests: `tests/projectkoios/cli/test__workflow_status.py`.

## Validation results

From repository root:

```bash
uv run projectkoios workflow status
```

Passed; printed workflow id, fixture path, places, current token location/color, enabled transition, and user decision status.

```bash
uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q
```

Passed: `15 passed in 0.06s`.

```bash
uv run mypy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
```

Passed: `Success: no issues found in 12 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
```

Passed: `summary: 0 finding(s), 12 file(s)`.

```bash
git diff --check
```

Passed with no output.

## Next expected artifact

- USER/HERMES/ATHENA review or closeout/commit direction.
