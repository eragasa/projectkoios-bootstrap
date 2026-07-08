```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "workflow-adapter-topology-roundtrip-validated",
  "datetime": "20260706.045501",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/workflow-adapter-contract-hardening.20260706.045501.md",
    "docs/AAR/aar.20260706.045501_workflow-adapter-contract-hardening.md"
  ],
  "scratch_directory": "scratch/",
  "controlling_adr": "docs/adr/adr.petrinet.20260705.132740Z.md"
}
```

# Vulcan active work

## Current priority stack

1. Package/commit/push the validated workflow adapter topology round-trip slice if directed.
2. Request ATHENA conformance review if desired before packaging.
3. Do not implement PM4Py conversion, marking/token round trip, guard serialization, or runtime semantics without new ATHENA authority.

## Latest working material

- Controlling ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.
- Source brief: ATHENA intercom guidance revised to require topology-only adapter round trip.
- Latest report: `docs/implementation/workflow-adapter-contract-hardening.20260706.045501.md`.
- Latest AAR: `docs/AAR/aar.20260706.045501_workflow-adapter-contract-hardening.md`.

## Latest validation evidence

- `uv sync --dev` => installed `snakes==0.9.33`; `uv.lock` was already satisfied and is not part of the final diff.
- `uv run pytest tests/projectkoios/workflow -q` => `13 passed in 0.03s`.
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 11 file(s)`.
- `uv run pytest -q` => `228 passed in 1.27s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `uv run mypy src/python tests` => `Success: no issues found in 118 source files`.
- `git diff --check` => clean.
- `graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `8129 nodes, 9172 edges, 764 communities`.

## Implementation notes

- SNAKES is now a dev/test dependency in `pyproject.toml` only.
- `SnakesColoredNetAdapter` converts canonical topology to SNAKES backend topology and imports SNAKES topology back to canonical payload.
- Round-trip test covers place IDs/labels, transition IDs/labels, arc endpoints, direction, and weights.
- Always-on payload tests remain backend-independent.

## Ignore for now

- PM4Py conversion and dependency/license policy.
- Marking/token round-trip semantics.
- Transition guard/callable serialization.
- Executor/runtime/event changes.
- Persistence/restart/event-bus behavior.
- Handoff/evaluator migration.

## Next expected artifact

- Commit/push instruction, optional ATHENA conformance review, or new architecture authority for broader adapter semantics.
