```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "live-petri-net-skeleton-slice-0-planned-awaiting-approval",
  "datetime": "20260711.114700Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md",
    "docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md",
    "docs/architecture/architecture.petrinet.00.md",
    "docs/adr/adr.petrinet.20260705.132740Z.md",
    "src/python/projectkoios/workflow/",
    "src/python/projectkoios/cli/"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": "docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md",
  "latest_report": null,
  "latest_aar": null
}
```

# Vulcan active work

## Current priority stack

1. `live-petri-net-skeleton-slice-0`: planned and awaiting USER/HERMES approval before coding.
2. Target command: `uv run projectkoios workflow status`.
3. Boundaries: read-only CLI status; static fixture only; use existing `projectkoios.workflow` Petri-net runtime; no firing, persistence, Operator Console integration, workflow-object integration, schema/product expansion, or live adapters.

## Latest working material

- Brief: `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`.
- Plan: `docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md`.
- Source architecture: `docs/architecture/architecture.petrinet.00.md`.
- Source ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.

## Planned outputs

- Add static fixture: `dev/workflow-nets/bootstrap-harness.workflow-net.json`.
- Add CLI command adapter: `src/python/projectkoios/cli/workflow.py`.
- Register command in `src/python/projectkoios/cli/main.py`.
- Add focused CLI tests: `tests/projectkoios/cli/test__workflow_status.py`.

## Required behavior

- Print workflow/net id and fixture path.
- List places with identifiers and labels.
- List current token locations and token color.
- List enabled transitions computed via `PetriNetExecutor.enabled_bindings(...)`.
- Print whether a user decision is required.
- Exit successfully and remain read-only.

## Validation plan

From repository root:

```bash
uv run projectkoios workflow status
uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q
uv run mypy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
git diff --check
```

## Dirty tree caution

Current dirty tree includes ATHENA/KOIOS handoff and proposal files outside VULCAN implementation ownership. Do not include unrelated workspace/provenance/schema-proposal changes in a VULCAN implementation commit unless explicitly requested.

## Next expected artifact

- USER/HERMES approval to implement the plan, or requested edits to the plan.
