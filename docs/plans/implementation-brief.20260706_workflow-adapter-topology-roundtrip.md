```json
{
  "title": "Workflow adapter topology round trip implementation brief",
  "artifact_type": "implementation-brief",
  "status": "completed-validated",
  "datetime": "20260706.031950Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "topology-only concrete workflow adapter round-trip acceptance criteria",
  "controlling_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "implementation_report": "docs/implementation/workflow-adapter-contract-hardening.20260706.045501.md",
  "conformance_review": "docs/reviews/architecture-conformance.20260706.023601_workflow-adapter-topology-roundtrip.md",
  "status_note": "Brief materialized after implementation to preserve ATHENA-controlled acceptance criteria that were initially conveyed by intercom."
}
```

# Implementation brief: workflow adapter topology round trip

## Purpose

Preserve the ATHENA-controlled implementation brief and acceptance criteria for the workflow adapter topology-only round-trip slice.

This brief was materialized after VULCAN implementation because the revised acceptance criteria were originally conveyed through intercom in response to user clarification. It records the bounded authority used for the implemented slice and links the resulting evidence.

## Controlling authority

- Controlling ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.
- Architecture decomposition surface: `docs/architecture/architecture.petrinet.00.md`.

The accepted ADR controls the bootstrap-held Petri-net vocabulary/runtime separation. This brief authorizes only a concrete adapter topology round-trip test/conversion slice under that boundary.

## Implementation scope

Implement a topology-only concrete adapter round trip for one backend first:

```text
canonical PetriNet / WorkflowNet
  -> backend representation
  -> canonical topology payload
```

The current implementation uses SNAKES as the first backend.

## Acceptance criteria

The slice is complete when tests prove bidirectional round-trip topology equivalence.

Topology equivalence covers:

- place IDs;
- place labels;
- transition IDs;
- transition labels;
- arc endpoints;
- arc kind/direction;
- arc weights.

The comparison MUST be deterministic and MUST NOT depend on backend object identity or backend-specific ordering.

The adapter MUST preserve normal library-neutral export behavior without importing optional backends.

## Dependency boundary

- Use one backend first.
- Current backend: SNAKES.
- SNAKES MAY be a dev/test dependency for this slice.
- SNAKES MUST NOT become a mandatory runtime dependency through this brief.
- Optional backend imports MUST remain lazy and adapter-owned.
- Executor/runtime modules MUST NOT import adapter backends.

## Files in scope

- `src/python/projectkoios/workflow/adapters.py`
- workflow adapter tests under `tests/projectkoios/workflow/`
- `pyproject.toml` only for dev/test dependency declaration
- implementation report and conformance review documentation

## Non-goals

This brief does not authorize:

- PM4Py conversion;
- token or marking state round trips;
- guard/callable serialization;
- execution history semantics;
- event provenance semantics;
- persistence or restart behavior;
- external event-bus integration;
- handoff/evaluator migration;
- product workflow semantics;
- package extraction into `projectkoios.petrinet`.

## Evidence

- VULCAN implementation report: `docs/implementation/workflow-adapter-contract-hardening.20260706.045501.md`.
- ATHENA conformance review: `docs/reviews/architecture-conformance.20260706.023601_workflow-adapter-topology-roundtrip.md`.
- KOIOS process capture: `docs/process-capture/pc.workflow.document-trace.md`.
- KOIOS process capture snapshot: `docs/process-capture/pc.workflow.document-trace.20260706.025408Z.md`.

## Validation expectations

At minimum:

```bash
uv run pytest tests/projectkoios/workflow -q
uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow
git diff --check
```

If implementation code changes, run full pytest before packaging:

```bash
uv run pytest -q
```

## Completion status

Status: completed and validated by VULCAN, reviewed by ATHENA.

This brief is retained as the durable ATHENA-controlled acceptance-criteria source for the completed slice.
