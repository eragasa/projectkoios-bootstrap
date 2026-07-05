```json
{
  "title": "Workflow adapter dependency encapsulation AAR",
  "artifact_type": "after-action-report",
  "status": "captured",
  "datetime": "20260705.105604",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "workflow adapter dependency-boundary follow-up"
}
```

# Workflow adapter dependency encapsulation AAR

## Scope

Follow-up implementation after the workflow first slice to make optional external library boundaries more explicit and testable.

## What happened

- User asked how external libraries were encapsulated, then approved continuing.
- VULCAN added library-neutral adapter payload DataObjects, a payload-builder ActionObject, and lazy optional dependency loading methods.
- VULCAN split reusable Petri-net behavior from workflow-specific specialization with `PetriNet` and `WorkflowNet(PetriNet)`.
- VULCAN applied Athena/user `PetriNetMarking` rename while preserving the handoff alias.
- VULCAN applied Athena/user consistent generic primitive names such as `PetriNetPlace`, `PetriNetTransition`, `PetriNetArc`, and `PetriNetToken`.
- VULCAN applied Athena/user `KoiosHandoff` rename for the domain handoff token concept.
- Added tests proving adapter export does not require SNAKES/PM4Py and that missing optional dependencies fail clearly.
- Ran focused and whole-repository validation.

## Process issues

- The source workflow ADR is still draft, so this remains a user-authorized implementation refinement rather than architecture promotion.
- Initial helper-function shape was corrected during review into the repository's DataObject/ActionObject pattern.
- Initial `PetriNet` rename was refined during review into separate `petrinet.py` and `workflownet.py` boundaries for future extraction.
- Bare `Marking` naming was corrected to `PetriNetMarking` for maintainer clarity.
- Generic Petri-net primitive names were consistently prefixed while preserving domain-specific token names.
- Domain handoff token naming was corrected from `HandoffArtifact` to `KoiosHandoff` for maintainer clarity.
- Concrete third-party conversion remains intentionally deferred because dependency/version/API choices need clearer acceptance criteria.

## Proposed follow-up improvements

- Add a brief specifying exact SNAKES/PM4Py conversion contracts before adding dependencies.
- Consider optional dependency groups in `pyproject.toml` only when concrete adapters are implemented.
- Continue handoff/evaluator migration in a separate bounded slice.

## Candidate ADR or implementation topics

- Optional dependency policy for workflow adapters.
- Concrete SNAKES/PM4Py conversion acceptance tests.

## Current status

- Adapter dependency encapsulation is implemented and validated with explicit payload DataObjects and a builder ActionObject.
- Petri-net substrate and workflow specialization are split and validated.
- `PetriNetMarking` rename is implemented and validated across harness and workflow surfaces.
- Generic Petri-net primitive naming is implemented and validated across workflow surfaces.
- `KoiosHandoff` rename is implemented and validated across harness handoff surfaces.
- No external Petri-net libraries are required for normal workflow package import or tests.
