```json
{
  "title": "Workflow object AAR synthesis architecture intake review",
  "artifact_type": "architecture-intake-review",
  "status": "reviewed-next-architecture-slice-recommended",
  "datetime": "20260711.092400Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_process_capture": "docs/process-capture/pc.aar-consolidation.20260711.091607Z.md",
  "source_requirements": "docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md"
}
```

# Architecture intake review 20260711.092400: workflow object from AAR synthesis

## Verdict

The KOIOS candidate requirements are suitable intake for a bounded workflow-object architecture/spec surface.

They are not implementation authority. They should first be promoted into an ATHENA-owned architecture note that defines the first workflow-object boundary, vocabulary, and minimum record shape before any VULCAN implementation brief or code.

## Recommended next architecture step

Create an ATHENA architecture note first:

- recommended path: `docs/architecture/architecture.workflow-object.md`
- status: working-draft / bootstrap-incubation architecture
- source: KOIOS AAR consolidation and requirements draft

Do not start with an ADR or implementation brief.

Reason:

- The candidate requirements contain several architecture vocabulary decisions, not just implementation tasks.
- Open questions remain about JSON vs Markdown, canonical transition names, mandatory gates, relation to `state.md`/`active.md`, and completion authority.
- An implementation brief would force VULCAN to invent architecture boundaries.
- An ADR may be appropriate later, after the architecture note stabilizes one bounded first slice decision.

## Requirement triage

### Accept into architecture draft for first modeling pass

- R1 Work item identity and source packet.
- R2 Artifact node model.
- R3 Transition/gate model.
- R4 Role-domain guard.
- R5 Approval and pause state.
- R6 Validation evidence record.
- R8 Non-authority and lifecycle markers.
- R10 User-preview validation record.
- R11 Ephemeral-message promotion rule.
- R12 Dependency/tooling decision record.
- R14 Process-capture observation link.

These should be included as architecture concepts, with minimal first-slice fields only.

### Split or defer before implementation

- R7 Dirty-tree/package boundary record: split into a later closeout/packaging extension. It is important, but it can bloat the first workflow-object record.
- R9 Fixture/sidecar provenance record: include minimal source/hash/authority fields in first slice, defer full sidecar/omitted-field modeling to a provenance extension.
- R13 Skill/reusable-procedure stability record: defer to a skill/procedure workflow-object extension. It crosses into skill lifecycle and multi-owner promotion.

### Reject for first slice only, not permanently

None of R1-R14 should be rejected outright. The issue is staging, not invalidity.

## Recommended next bounded slice

Slice name:

- `workflow-object-architecture-first-record`

Scope:

- Draft `docs/architecture/architecture.workflow-object.md`.
- Define the workflow object as a durable summary/projection of bounded work, not a replacement for source artifacts.
- Define a minimal first workflow-object record for one completed slice.
- Use the accepted Operator Console P0/P1 work as the example/proving case because it has architecture, plan/brief, implementation report, conformance reviews, AAR, validation, preview, and user acceptance artifacts.
- Decide only enough vocabulary for a first record: work item identity, artifact nodes, transitions/gates, approvals/pauses, validation evidence, preview evidence, authority boundaries, and process-capture links.
- State explicitly that the workflow object is not live orchestration, not a database, not a Petri-net runtime, and not a replacement for `state.md`, `active.md`, ADRs, plans, reports, or AARs.

Out of scope:

- VULCAN implementation.
- JSON schema or storage adapter.
- Bulk backfill of historical AARs.
- Live intercom/session integration.
- Operator Console support.
- Petri-net execution.
- Database persistence.
- Skill lifecycle implementation.
- Cross-repo product authority.

## Acceptance criteria for the architecture slice

1. `docs/architecture/architecture.workflow-object.md` exists and cites the KOIOS consolidation and requirements draft as non-authoritative intake.
2. The architecture note defines the workflow object's purpose and non-purpose.
3. The note defines the first minimal record boundary and explicitly marks it as a projection/index of source artifacts, not replacement authority.
4. The note defines core concepts for work item identity, artifact nodes, transitions/gates, role-domain guards, approval/pause state, validation evidence, preview evidence, non-authority markers, dependency/tooling decision references, and process-capture links.
5. The note classifies R1-R14 as first-slice, extension, or deferred.
6. The note names the first implementation candidate but does not authorize implementation.
7. The note states that implementation requires a separate VULCAN plan after user/HERMES approval.
8. The note preserves KOIOS provenance: AAR synthesis remains advisory until promoted.

## Likely implementation candidate after architecture approval

After the architecture note is accepted, the first implementation slice should be a fixture/projection generator for exactly one work item, probably Operator Console P0/P1:

- produce a static JSON workflow-object example under `dev/` or another explicitly non-authoritative fixture path;
- validate that it references existing source artifacts by path/hash;
- do not mutate source artifacts;
- do not create repository-wide workflow state or storage authority.

That implementation should wait for the architecture note and an explicit implementation brief/plan.

## Authority/provenance watchpoints

- KOIOS process-capture artifacts are provenance/advisory, not architecture or implementation authority.
- Candidate requirements R1-R14 are not accepted requirements until promoted by ATHENA/user.
- A workflow object must not become hidden completion authority or silently supersede `state.md`, `active.md`, ADRs, plans, reports, reviews, or AARs.
- HERMES remains responsible for cross-domain completion/closeout authority if workflow objects affect orchestration.
- VULCAN must not implement schema/storage/CLI/UI from the KOIOS draft alone.
- Historical AARs must not be bulk-backfilled in the first slice.
