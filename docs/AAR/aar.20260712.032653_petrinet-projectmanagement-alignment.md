```json
{
  "title": "AAR: Petri-net project management alignment",
  "artifact_type": "after-action-report",
  "status": "draft-aar",
  "datetime": "20260712.032653Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "filesystem-backed Petri-net/Gantt project-management alignment note and role-boundary clarification",
  "related_artifacts": [
    "docs/plans/petrinet-projectmanagement.20260712.project-alignment.md"
  ]
}
```

# AAR: Petri-net project management alignment

## Scope

This AAR covers the HERMES-led initial alignment interview for a filesystem-backed project-management system using Petri-net state and transition payloads as source/control authority with Gantt projections.

Primary durable artifact:

```text
docs/plans/petrinet-projectmanagement.20260712.project-alignment.md
```

## What happened

USER introduced a need for a filesystem-only project-management system, initially described as Gantt-based and eventually Petri-net workflow-based.

HERMES asked KOIOS for provenance/terminology input and VULCAN for implementation-reality input before creating a durable artifact.

KOIOS cautioned that the idea should be preserved as user intent/alignment first, not architecture or implementation authority. KOIOS emphasized distinctions among filesystem-only project management, Gantt planning/projection, and eventual Petri-net workflow/runtime.

VULCAN cautioned that implementation should not begin before source/control files, projection boundaries, validation, concurrency, and mutation semantics are defined.

USER corrected the term `spec-intake`, clarified that HERMES is responsible for interviewing the user to create initial project alignment, and provided alignment answers.

HERMES created a project-alignment note, got KOIOS provenance/terminology review, updated the note with KOIOS review/watchpoints, committed it, then renamed it to the USER-preferred filename convention.

Final artifact path:

```text
docs/plans/petrinet-projectmanagement.20260712.project-alignment.md
```

## Process issues

- HERMES initially suggested a `spec-intake` artifact, but USER objected. The term was inappropriate because initial alignment is not yet specification.
- Existing role policy says ATHENA owns both specification and architecture, but USER stated that specification and architecture should not be owned by the same role.
- HERMES clarified a new workflow expectation: HERMES owns initial project-alignment interviewing before specification or architecture work begins.
- File naming convention was corrected after artifact creation. HERMES handled this with a rename commit and reference updates, but earlier confirmation of the filename pattern would have avoided churn.
- The current artifact model in root policy does not explicitly include `project-alignment-note` as a first-class artifact type, even though the workflow now needs it.

## Proposed follow-up improvements

- Add or promote a durable artifact type for `project-alignment-note` or equivalent HERMES-owned alignment artifact.
- Clarify role boundaries so HERMES owns initial user interview/alignment, ATHENA owns architecture, VULCAN owns implementation/validation, and KOIOS owns provenance/knowledge grounding.
- Revisit whether specification should remain under ATHENA or be separated into a distinct owner/domain.
- Establish filename convention for project-alignment notes. USER-preferred pattern from this session:

```text
<topic>.<datetime>.project-alignment.md
```

Example:

```text
petrinet-projectmanagement.20260712.project-alignment.md
```

- When HERMES proposes a new durable artifact type, ask the USER about naming before writing if the convention is not already established.

## Candidate ADR or implementation topics

- Workflow/policy decision: separate initial project alignment, specification, architecture, implementation, and provenance ownership.
- Artifact model update: add `project-alignment-note` as a HERMES-owned artifact.
- Naming convention policy: define stable filename patterns for project-alignment notes.
- Architecture-framing request: route `docs/plans/petrinet-projectmanagement.20260712.project-alignment.md` to ATHENA after HERMES/USER approval.
- Future architecture question: evaluate USER's current mental model that Gantt tasks map to Petri-net places, because conventional Petri-net modeling may map tasks to transitions instead.

## Current status

The project-alignment note exists, has KOIOS provenance/terminology review, and is committed under the USER-requested filename.

No architecture authority, specification authority, implementation authorization, database/runtime decision, schema decision, or Petri-net workflow cutover was created by the alignment note.

Next coherent action is HERMES/USER decision on whether to route the alignment note to ATHENA for bounded architecture framing.
