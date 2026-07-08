```json
{
  "title": "Workflow adapter topology round trip",
  "artifact_type": "implementation-report",
  "status": "validated",
  "datetime": "20260706.045501",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "workflow adapter topology-only SNAKES round-trip and dependency-boundary tests",
  "source_brief": "ATHENA intercom guidance revised by user clarification for bidirectional round-trip topology equivalence",
  "controlling_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "validation_status": "pass"
}
```

# Workflow adapter topology round trip

## Summary

VULCAN implemented the revised ATHENA-authorized workflow adapter slice: topology-only bidirectional adapter conversion for one concrete backend, using SNAKES as the lower-risk backend. The slice keeps conversion limited to canonical Petri-net topology and preserves optional backend dependency boundaries.

## Changes

- Added SNAKES as a non-runtime dev dependency in `pyproject.toml`; `uv sync --dev` verified the lock/install state without leaving `uv.lock` dirty.
- Added SNAKES topology conversion methods to `SnakesColoredNetAdapter`:
  - `export_backend_topology()` converts canonical `PetriNet` topology to a SNAKES backend net.
  - `import_backend_topology_payload()` converts SNAKES backend topology back to deterministic `PetriNetPayload`.
  - helper methods lazily load `snakes.nets`, preserve weighted topology arcs, and canonicalize backend ordering.
- Strengthened always-on adapter payload tests for stable topology shape and weighted arcs without optional backend access.
- Added concrete SNAKES round-trip topology test: canonical `PetriNet` -> SNAKES backend net -> canonical `PetriNetPayload`.
- Preserved dependency-boundary tests that prove normal adapter `export()` remains library-neutral and does not import optional backends.

## Files changed

- `pyproject.toml`
- `src/python/projectkoios/workflow/adapters.py`
- `tests/projectkoios/workflow/test__WorkflowAdapters__encapsulate_dependencies.py`

## Topology equivalence covered

The SNAKES round-trip test compares canonical payload data rather than backend object identity or backend ordering. It covers:

- place IDs and labels;
- transition IDs and labels;
- arc endpoints;
- arc kind/direction;
- arc weights.

## Explicit non-changes

- No PM4Py conversion was implemented.
- No marking/token state round trip was implemented.
- No transition guard/callable serialization was implemented.
- No executor/runtime/event changes were made.
- No handoff/evaluator migration was attempted.
- No persistence, restart, external event-bus, or product workflow semantics were introduced.

## Validation

- `uv sync --dev` => installed `snakes==0.9.33`; `uv.lock` was already satisfied and is not part of the final diff.
- `uv run pytest tests/projectkoios/workflow -q` => `13 passed in 0.03s`.
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 11 file(s)`.
- `uv run pytest -q` => `228 passed in 1.27s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `uv run mypy src/python tests` => `Success: no issues found in 118 source files`.
- `git diff --check` => clean.
- `graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `8129 nodes, 9172 edges, 764 communities`.

## Acceptance evidence

- Always-on topology payload tests pass without using backend imports.
- Concrete SNAKES round-trip test passes with the dev dependency installed.
- Adapter round-trip assertion compares canonicalized topology payload data, not backend object identity/order.
- Optional backend access remains lazy; normal adapter `export()` does not import SNAKES or PM4Py.
- Concrete PM4Py conversion remains deferred.

## Residual risks

- SNAKES mapping is topology-only and does not decide colored-token, marking, guard, execution, or runtime semantics.
- Optional dependency policy is limited to the dev/test dependency added here; runtime mandatory dependency remains avoided.
- PM4Py mapping remains undefined and may need separate dependency/license review before implementation.
