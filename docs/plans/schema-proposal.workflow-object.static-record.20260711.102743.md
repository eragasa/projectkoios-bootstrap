```json
{
  "title": "Workflow object static record schema proposal",
  "artifact_type": "schema-proposal",
  "status": "record-shape-candidate",
  "datetime": "20260711.102743Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.workflow-object.md",
  "source_brief": "docs/plans/implementation-brief.20260711.102123_workflow-object-static-operator-console-record.md",
  "authority_boundary": "candidate only; not docs/schemas authority"
}
```

# Schema proposal 20260711.102743: Workflow object static record

## Status

Record-shape candidate for the first static workflow-object JSON record.

This document is not repository-wide schema authority. It must not be treated as an accepted `docs/schemas/` JSON Schema, database model, CLI contract, UI contract, Petri-net runtime contract, or product/mothership authority.

## Purpose

Define the concrete JSON shape VULCAN should use when planning the first static workflow-object record for the accepted Operator Console P0/P1/readability bundle.

This proposal translates `docs/architecture/architecture.workflow-object.md` into a deterministic static JSON record shape while preserving the architecture distinction:

- artifacts/documents are durable referenced records with status, provenance, owner/domain, authority boundary, and hash/version/ref where required;
- Petri-net places are workflow states, not documents;
- tokens reference work items and artifact versions/records;
- gates evaluate typed evidence/status predicates;
- workflow objects are projection/index records, not source artifact authority or completion authority.

## Candidate example skeleton

A tiny representative example skeleton exists at:

- `docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json`

The skeleton is a candidate/non-authoritative guardrail for VULCAN planning. It intentionally uses a minimum representative artifact set, placeholders for hashes, and explicit deferred extensions so the first implementation does not become a quasi-bulk index.

## Placement guidance

The first static JSON record should live under an explicitly non-authoritative dev/fixture path, for example:

- `dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json`

Do not create `docs/schemas/workflow-object.schema.json` in the first slice unless USER/HERMES explicitly changes the authority boundary.

## Top-level JSON shape

```json
{
  "record_type": "workflow_object",
  "record_shape_version": "candidate-0",
  "record_id": "workflow-object.operator-console-bootstrap-bundle.20260711",
  "title": "Operator Console bootstrap P0/P1/readability bundle",
  "status": "accepted-static-projection",
  "shape_authority": "candidate-only-not-schema-authority",
  "authority_boundary": {
    "mode": "projection-index-only",
    "non_authority_statement": "This record indexes and summarizes source artifacts. It does not replace source artifacts, decide completion, create storage authority, or execute workflow transitions.",
    "source_authorities_preserved": true,
    "completion_authority": "HERMES/user or owning domain artifact only",
    "not_authority_for": [
      "source-artifacts",
      "completion",
      "petri-net-runtime",
      "storage",
      "product-ui"
    ]
  },
  "non_authority_markers": [
    "projection-index-only",
    "static-record",
    "bootstrap-incubation",
    "fixture-only",
    "non-live",
    "stale-by-design",
    "not-source-authority",
    "not-product-authority",
    "not-completion-authority",
    "not-petri-net-runtime",
    "not-schema-authority",
    "not-storage-authority"
  ],
  "source_architecture_refs": [],
  "work_item": {},
  "artifact_records": [],
  "workflow_tokens": [],
  "workflow_places": [],
  "transition_gates": [],
  "gate_evaluations": [],
  "validation_evidence": [],
  "preview_evidence": [],
  "process_links": [],
  "deferred_extensions": [],
  "open_questions": []
}
```

## Required top-level fields for candidate-0

Required:

- `record_type`
- `record_shape_version`
- `record_id`
- `title`
- `status`
- `authority_boundary`
- `non_authority_markers`
- `work_item`
- `artifact_records`
- `gate_evaluations`
- `validation_evidence`
- `process_links`

Required for the Operator Console proving case:

- `preview_evidence`

Optional/minimal for candidate-0:

- `source_architecture_refs`
- `workflow_tokens`
- `workflow_places`
- `transition_gates`
- `deferred_extensions`
- `open_questions`

If `workflow_places` is omitted or minimal, the record must not imply that artifact paths are place ids.

## Work item object

Required fields:

```json
{
  "work_item_id": "workflow-object.operator-console-bootstrap-bundle.20260711",
  "title": "Operator Console bootstrap P0/P1/readability bundle",
  "slice_names": [
    "operator-console-review-one-proposal-fixture",
    "operator-console-fixture-interaction-visibility",
    "operator-console-readability-navigation-fixture"
  ],
  "repository": "projectkoios-bootstrap",
  "workspace_or_package_path": "src/typescript/projectkoios/ui/operator-console/",
  "initiating_source_summary": "Accepted Operator Console bootstrap-incubation slices with implementation, review, validation, and preview evidence.",
  "status": "accepted-static-projection",
  "status_evidence_refs": [],
  "created_at": "YYYYMMDD.HHMMSSZ",
  "observed_at": "YYYYMMDD.HHMMSSZ",
  "producer_role": "VULCAN"
}
```

`producer_role` is the role producing the static record. Source artifacts retain their own owner/domain in `artifact_records`.

## DataObject / ActionObject.method mapping

JSON field names stay snake_case, but each top-level collection maps to DataObject vocabulary:

- `artifact_records` => `ArtifactRecord[]`
- `workflow_tokens` => `WorkflowTokenRecord[]`
- `workflow_places` => `WorkflowPlaceRecord[]`
- `transition_gates` => `TransitionGateRecord[]`
- `gate_evaluations` => `GateEvaluationRecord[]`
- `validation_evidence` => `ValidationEvidenceRecord[]`
- `preview_evidence` => `PreviewEvidenceRecord[]`
- `process_links` => `ProcessLinkRecord[]`
- `deferred_extensions` => `DeferredExtensionRecord[]`

Behavior belongs in ActionObject methods such as `WorkflowObjectValidator.validateRecord(...)`, `ContentRefHasher.hashFile(...)`, `ContentRefHasher.summarizeDirectory(...)`, `TransitionGateEvaluator.evaluate(...)`, and future `WorkflowObjectProjector.projectToPetriNetAdapterPayload(...)`.

Candidate-0 does not require reusable implementation classes; these names are architecture/schema-proposal vocabulary unless separately approved.

## ArtifactRecord DataObject

Implementation-facing JSON must use `artifact_records`, not `nodes`.

Required fields:

```json
{
  "artifact_id": "artifact:architecture.operator-console",
  "locator": "docs/architecture/architecture.operator-console.md",
  "artifact_type": "architecture-note",
  "owner_role": "ATHENA",
  "owner_domain": "architecture",
  "lifecycle_status": "accepted",
  "status_evidence_refs": ["artifact:review.operator-console-p2"],
  "source_report_ref": "artifact:review.operator-console-p2",
  "authority_boundary": "source-authority",
  "content_ref": {
    "ref_type": "sha256",
    "value": "...",
    "availability": "present"
  },
  "provenance_summary": "ATHENA architecture/control-surface artifact referenced by workflow object.",
  "created_at": null,
  "updated_at": null,
  "observed_at": "YYYYMMDD.HHMMSSZ",
  "produced_by_transition_ids": [],
  "consumed_by_transition_ids": [],
  "related_artifact_ids": [],
  "freshness": "current-at-observation",
  "transformation_notes": []
}
```

Hash/ref rule:

- `content_ref` is required for generated, fixture-backed, projection, validation-output, and immutable review evidence artifacts unless explicitly unavailable.
- For files, use `content_ref.ref_type: "sha256"`; do not add a separate `hash_algorithm` field.
- For large directories, use `content_ref.ref_type: "directory-summary"`, `content_ref.value: "path-only:<path>"` or a deterministic summary hash when cheap, `content_ref.availability: "present"`, and `content_ref.limitations` explaining that candidate-0 does not compute a recursive tree hash.
- For optional or unavailable artifacts, keep `content_ref` present with `availability: "explicitly-unavailable"` and `unavailable_reason`; do not silently omit it.
- A hash/ref identifies the referenced source version. It does not make the workflow object source authority.

Allowed `content_ref.availability` values:

- `present`
- `explicitly-unavailable`
- `not-applicable`

When unavailable, include `unavailable_reason`.

## WorkflowTokenRecord DataObject

Candidate-0 may include one projection-only token for the bounded work item.

```json
{
  "token_id": "token:operator-console-bootstrap-bundle",
  "work_item_id": "workflow-object.operator-console-bootstrap-bundle.20260711",
  "current_place_ref": "place:accepted-static-projection",
  "observed_place_refs": ["place:architecture-accepted", "place:implementation-reviewed"],
  "artifact_record_refs": [],
  "status": "projection-only",
  "authority_boundary": "not-runtime-token"
}
```

The token is not a live Petri-net runtime token.

## WorkflowPlaceRecord DataObject

Candidate-0 may include local place vocabulary only when useful for readability.

```json
{
  "place_id": "place:implementation-reviewed",
  "label": "Implementation reviewed",
  "meaning": "Source implementation report and architecture review indicate the implementation evidence was reviewed.",
  "source_vocabulary_ref": "local-first-record-vocabulary",
  "not_a_document": true
}
```

Do not use document paths as place ids.

## TransitionGateRecord DataObject

Gate definitions describe expected predicates. Gate evaluations record observed results.

```json
{
  "gate_id": "gate:p2-readability-navigation-implemented-reviewed-previewed",
  "name": "P2 readability/navigation implemented, reviewed, and previewed",
  "from_place_ref": "place:implementation-planned",
  "to_place_ref": "place:accepted-static-projection",
  "required_predicates": [
    {
      "predicate_type": "artifact_status",
      "target_ref": "artifact:implementation.operator-console-readability-navigation",
      "expected": "implemented"
    },
    {
      "predicate_type": "review_acceptance",
      "target_ref": "artifact:review.operator-console-readability-navigation",
      "expected": "accepted"
    },
    {
      "predicate_type": "user_preview",
      "target_ref": "preview:p2-readability-navigation",
      "expected": "observed"
    }
  ],
  "authority_boundary": "evaluation-template-only"
}
```

`from_place_ref` and `to_place_ref` are optional for candidate-0 when not evidenced.

## GateEvaluationRecord DataObject

Required fields:

```json
{
  "evaluation_id": "evaluation:p2-readability-navigation-implemented-reviewed-previewed",
  "gate_id": "gate:p2-readability-navigation-implemented-reviewed-previewed",
  "observed_result": "passed",
  "evaluated_predicates": [
    {
      "predicate_type": "artifact_status",
      "target_ref": "artifact:implementation.operator-console-readability-navigation",
      "expected": "implemented",
      "observed": "implemented",
      "result": "passed",
      "evidence_refs": ["artifact:implementation.operator-console-readability-navigation"]
    }
  ],
  "evidence_refs": [],
  "evaluator_role": "ATHENA",
  "source_artifact_ref": "artifact:review.operator-console-readability-navigation",
  "observed_at": "YYYYMMDD.HHMMSSZ",
  "completion_authority_created": false,
  "notes": []
}
```

`completion_authority_created` must be `false` in the first static record.

## ValidationEvidenceRecord DataObject

Required fields:

```json
{
  "validation_id": "validation:p2.npm-test",
  "source_report_ref": "artifact:implementation.operator-console-readability-navigation",
  "reported_command": "npm test",
  "working_directory": "src/typescript/projectkoios/ui/operator-console/",
  "target_scope": "operator-console package",
  "reported_result": "passed",
  "status": "passed",
  "limitations": [],
  "observed_at": "YYYYMMDD.HHMMSSZ",
  "reported_by_source_artifact": true
}
```

If validation was copied from a source report or review, preserve `reported_by_source_artifact: true`. Do not imply the workflow object reran validation.

## PreviewEvidenceRecord DataObject

Required for the Operator Console first static record:

```json
{
  "preview_id": "preview:p2-readability-navigation",
  "source_report_ref": "artifact:review.operator-console-readability-navigation",
  "preview_command": "npm run preview -- --host 127.0.0.1",
  "preview_url_or_method": "http://127.0.0.1:4173/",
  "inspected_surface": "Operator Console static fixture UI",
  "user_visible_question": "Can the user inspect readability/navigation affordances in the local browser preview?",
  "observed_feedback_summary": "User inspected local preview; ATHENA accepted review evidence.",
  "changed_scope": false,
  "authority_boundary": "preview-evidence-only-not-product-activation"
}
```

Preview evidence is review evidence, not product activation authority.

## ProcessLinkRecord DataObject

```json
{
  "process_link_id": "process:aar.operator-console-readability-navigation",
  "locator": "docs/AAR/aar.20260711.092524_operator-console-readability-navigation-fixture.md",
  "link_type": "aar",
  "owner_role": "VULCAN",
  "authority_boundary": "process-provenance"
}
```

## Deferred extensions

Candidate-0 should explicitly list deferred areas rather than silently omitting them:

```json
{
  "extension_id": "extension:dirty-tree-package-boundary",
  "status": "deferred",
  "reason": "Full closeout and packaging model is out of scope for first static record.",
  "related_requirement": "R7"
}
```

Required deferred extensions for candidate-0:

- full dirty-tree/package-boundary model (`R7`);
- full fixture/sidecar omitted-field provenance model (`R9` depth);
- skill/reusable-procedure lifecycle model (`R13`);
- schema authority;
- storage/database authority;
- Petri-net runtime integration;
- Operator Console UI display.

## Controlled values for candidate-0

Use controlled string values in JSON. Do not require generated enum classes or JSON Schema enums yet.

### artifact_type

- `architecture-note`
- `implementation-plan`
- `implementation-brief`
- `implementation-report`
- `architecture-review`
- `aar`
- `process-capture`
- `source-directory`
- `source-file`
- `package-manifest`
- `lockfile`
- `fixture`
- `validation-output`

### owner_role

- `ATHENA`
- `VULCAN`
- `KOIOS`
- `HERMES`
- `USER`
- `MIXED`
- `UNKNOWN`

### owner_domain

- `architecture`
- `implementation`
- `review`
- `process-provenance`
- `source`
- `orchestration`
- `user-decision`
- `mixed`
- `unknown`

### authority_boundary

- `source-authority`
- `evidence-authority`
- `provenance-only`
- `projection-only`
- `projection-index-only`
- `fixture-only`
- `non-authoritative`
- `generated`
- `advisory`
- `process-provenance`
- `evaluation-template-only`
- `not-runtime-token`
- `preview-evidence-only-not-product-activation`

### lifecycle/status values

- `draft`
- `planned`
- `approved`
- `implemented`
- `validated`
- `reviewed`
- `accepted`
- `captured`
- `superseded`
- `not-applicable`
- `unknown`
- `accepted-static-projection`
- `projection-only`

### observed_result / predicate result

- `passed`
- `failed`
- `warning`
- `not-applicable`
- `not-yet-evaluated`

### predicate_type

- `artifact_status`
- `validation_result`
- `review_acceptance`
- `user_preview`
- `approval_record`
- `non_authority_marker`
- `path_hash_present`

## Adapter-library mapping

The candidate JSON shape should be compatible with adapter-library boundaries without making adapter libraries authoritative for workflow-object content.

Current workflow adapter surfaces such as `src/python/projectkoios/workflow/adapters.py` expose adapter-neutral Petri-net payload concepts for places, transitions, and arcs. Workflow-object JSON should map to those surfaces only through a projection layer:

- `workflow_places` may project to adapter-neutral place payloads because places are workflow states.
- `transition_gates` may project to transition/topology metadata when a later slice explicitly defines how gate names/predicates relate to Petri-net transitions.
- `workflow_tokens` may project to token payloads or colored-token metadata only in a later adapter extension; candidate-0 is not a runtime token format.
- `artifact_records` must not project to Petri-net places. Artifact refs may be token payload/evidence metadata, never adapter topology nodes.
- `gate_evaluations` remain evidence/read-model records. They are not executable adapter guards unless a later slice defines a compiler/projection and preserves source authority.
- `validation_evidence`, `preview_evidence`, and `process_links` are provenance/evidence inputs for operator/read-model surfaces, not Petri-net topology.

A future adapter slice should define an explicit `WorkflowObjectAdapterPayload` or projection contract rather than passing raw workflow-object JSON directly into Petri-net backend adapters.

## Candidate-0 acceptance expectations

The first static JSON record should satisfy these expectations:

1. Top-level identity, status, authority boundary, and non-authority markers are explicit.
2. Work item identity references the Operator Console P0/P1/readability bundle.
3. Artifact records cover controlling architecture, plans/briefs, implementation reports, reviews, AARs/process links, and exactly one minimal package/source ref (`src/typescript/projectkoios/ui/operator-console/package.json`) unless a stronger evidence need is explicitly justified.
4. Artifact lifecycle/status claims cite status evidence refs where feasible; if a status is taken from the artifact's own frontmatter/body, the record should say so rather than leaving an unsupported assertion.
5. Hashes/refs are present where required, or unavailability is explicit.
6. Gate evaluations record observed evidence and set `completion_authority_created: false`.
7. Validation evidence is marked as reported by source artifacts when not rerun by the workflow-object implementation.
8. Preview evidence is present for the Operator Console UI slices and marked as non-activation evidence.
9. `workflow_tokens`, `workflow_places`, and `transition_gates` remain present-but-minimal or explicitly omitted/deferred; rich `gate_evaluations` carry the main proof for candidate-0.
10. Deferred extensions are explicit.
11. No schema/storage/CLI/UI/Petri-net runtime/live adapter/bulk generation authority is introduced.

## Promotion path

Candidate-0 can be promoted only after evidence from implementation/review shows the shape is stable enough.

Possible future promotions:

1. Static example record only.
2. Static record plus local validator.
3. Second static record for a non-UI work item.
4. Consolidated vocabulary update.
5. Draft JSON Schema proposal.
6. Accepted `docs/schemas/` schema only if USER/HERMES and domain owners explicitly authorize schema authority.
