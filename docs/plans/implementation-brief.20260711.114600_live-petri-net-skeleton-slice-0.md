```json
{
  "title": "Live Petri-net skeleton slice 0 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-planning-ready",
  "datetime": "20260711.114600Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.petrinet.00.md",
  "source_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "slice_name": "live-petri-net-skeleton-slice-0",
  "target_command": "uv run projectkoios workflow status",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.114600: Live Petri-net skeleton slice 0

## Purpose

Make the existing Petri-net workflow harness visibly inspectable from the CLI with an immediate live command:

```bash
uv run projectkoios workflow status
```

The command should load a static bootstrap workflow-net fixture and print the current net/status in human-readable form: places, token locations, enabled transitions, and whether a user decision is required.

This slice is about **live inspectability**, not another ADR/process expansion.

## Architecture sufficiency

No new ADR is required for this narrow slice.

Existing authority is sufficient because:

- `docs/adr/adr.petrinet.20260705.132740Z.md` already accepts the first-slice separation of Petri-net definition, marking, binding, request, state, executor, and events.
- `docs/architecture/architecture.petrinet.00.md` already defines Petri-net state as explicit and inspectable, with state represented by `(PetriNet, PetriNetMarking)` and enabled transitions determined by the executor/runtime.
- The existing implementation substrate already exists under `src/python/projectkoios/workflow/`.

This brief only asks VULCAN to expose that substrate through a bounded read-only CLI status command backed by a static fixture.

## User-facing goal

As the user/operator, running:

```bash
uv run projectkoios workflow status
```

should show enough live CLI output to answer:

- What workflow net is loaded?
- Which places exist?
- Where are the current tokens?
- Which transitions are enabled right now?
- Is a user decision currently required?

## Target files

Likely implementation scope:

- Add `src/python/projectkoios/cli/workflow.py`.
- Edit `src/python/projectkoios/cli/main.py` to register the top-level `workflow` command group.
- Add `dev/workflow-nets/bootstrap-harness.workflow-net.json` as the static fixture.
- Add `tests/projectkoios/cli/test__workflow_status.py`.

VULCAN may add small helper classes/functions if needed, but should avoid broad runtime redesign.

## Static fixture requirements

Create one static bootstrap workflow-net fixture under:

```text
dev/workflow-nets/bootstrap-harness.workflow-net.json
```

Minimum fixture semantics:

- `net_id`: stable identifier such as `bootstrap-harness.slice-0`.
- places: at least three places representing a small inspectable harness flow.
- transitions: at least one enabled transition and at least one disabled transition if practical.
- arcs: input/output arcs compatible with existing `PetriNetArcKind` values.
- marking: at least one token currently located in a place.
- decision metadata: one explicit field or token color showing whether a user decision is required.

The fixture should be simple enough to map directly into existing `PetriNet`, `PetriNetPlace`, `PetriNetTransition`, `PetriNetArc`, `PetriNetMarking`, and `PetriNetToken` objects without new schema machinery.

## CLI behavior

Add a top-level command group:

```bash
projectkoios workflow status
```

Default behavior:

- load `dev/workflow-nets/bootstrap-harness.workflow-net.json` from the repository root;
- instantiate the existing Petri-net runtime objects;
- validate the net using existing validation/runtime behavior;
- compute enabled bindings using `PetriNetExecutor.enabled_bindings(...)`;
- print deterministic human-readable status.

Suggested output sections:

```text
workflow: bootstrap-harness.slice-0
fixture: dev/workflow-nets/bootstrap-harness.workflow-net.json

places:
  - intake: Intake
  - user_decision: User decision
  - implementation: Implementation

tokens:
  - token current-slice at user_decision color={kind=workflow-slice, requires_user_decision=true}

enabled transitions:
  - approve_next_slice: Approve next slice

user decision required: yes
```

Exact wording may differ, but tests must assert the key user-visible facts.

## Explicit out of scope

Do not implement in this slice:

- transition firing command;
- persistence or mutable workflow state;
- runtime event log persistence;
- Operator Console integration;
- workflow-object integration;
- Petri-net graph UI;
- schema authority under `docs/schemas/`;
- generalized workflow-net JSON loader framework beyond this fixture;
- role/permission model expansion;
- actor identity / firing request authority beyond existing classes;
- live intercom/session adapters;
- product/mothership workflow authority.

## Acceptance criteria

1. `uv run projectkoios workflow status` exists and exits successfully.
2. The command loads the static fixture `dev/workflow-nets/bootstrap-harness.workflow-net.json` by default.
3. The output includes workflow/net id and fixture path.
4. The output lists places with identifiers and labels.
5. The output lists current token locations.
6. The output lists enabled transitions computed using existing Petri-net runtime behavior, not hard-coded output only.
7. The output states whether a user decision is required.
8. The command is read-only: it does not fire transitions or mutate fixture/state.
9. The implementation uses existing `projectkoios.workflow` Petri-net classes rather than creating a parallel workflow model.
10. No Operator Console, workflow-object, backend/API, persistence, or product authority expansion is introduced.
11. Tests cover command registration and output for the static fixture.
12. Validation passes: focused CLI test, existing workflow tests, mypy for touched source/tests if practical, python policy for touched paths, and `git diff --check`.

## Suggested validation commands

From repository root:

```bash
uv run projectkoios workflow status
uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q
uv run mypy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli
git diff --check
```

If mypy or policy scope needs adjustment because `tests/projectkoios/cli/` is new, VULCAN should document the exact command run and result.

## Pause triggers

Pause and request direction if implementation would require:

- mutable workflow state or a transition-firing command;
- persistent runtime storage;
- role/permission or actor identity decisions;
- new workflow schema authority;
- Operator Console integration;
- workflow-object integration;
- live adapter/session/intercom reads;
- product/mothership workflow decisions;
- substantial changes to existing Petri-net runtime semantics.

## Handoff

VULCAN should produce a concise implementation plan and pause for USER/HERMES approval unless USER/HERMES explicitly authorizes direct coding from this brief.
