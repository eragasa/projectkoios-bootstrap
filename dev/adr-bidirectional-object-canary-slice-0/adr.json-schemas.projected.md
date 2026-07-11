<!-- ADR BIDIRECTIONAL OBJECT CANARY: generated projection evidence only; source Markdown is not ingested or overwritten. -->
<!-- GENERATED PILOT PROJECTION: non-authoritative; do not edit as ADR authority. -->
# ADR Projection: JSON Schemas Namespace

## Projection metadata

- Projection status: generated-projection
- Source record ID: adr.json-schemas
- Canonical slug: json-schemas
- Record status: draft
- Legacy/source path: docs/adr/adr.json-schemas.draft.md
- Schema ID: https://projectkoios.local/schemas/adr.schema.json
- Generation method: projectkoios.bootstrap.control_surface.adr.bidirectional.AdrBidirectionalCanaryRunner.run
- Source-of-truth mode: candidate-evidence-only-not-repository-authority
- Source hash: c95dfb0928ba1398eb058a7bb16b21f2dad77f4116169cbcc8075fb5186c2df5
- JSON checkpoint hash: e5f8c6729ee120ae4a266e6d5d575df3b9ae6f9fb86158c92a29995386a89bfb
- Conflict rule: Generated projection parse-back only; source Markdown remains unmutated and no hand-authored Markdown ingest is implemented.

```json adr-record
{
  "acceptance_criteria": [
    "a reviewer can tell that the namespace holds schemas only",
    "the UI/core concept remains defined elsewhere",
    "workflow UI can consume the namespace without being defined by it",
    "schema/contract validation remains separate from UI architecture decisions"
  ],
  "architecture_spec": "The JSON schemas namespace is a supporting surface for the UI/core family.\n\nIt should define:\n- schema files and contract files only\n- the machine-readable shapes used by the shared UI/core family\n- any constraints needed to validate those shapes\n\nIt should not define:\n- shared UI/core semantics\n- workflow UI behavior\n- rendering internals",
  "consequences": "- schema and contract work stays separate from UI/core design\n- the shared UI/core ADR can remain renderer-agnostic\n- workflow UI can consume schemas without becoming the schema authority\n- future tooling can validate against one schema namespace",
  "context": {
    "acting_as": "user(Eugene)",
    "architecture_domain": "software",
    "delegated_operator": "pi",
    "from": "HERMES",
    "origin": "user request",
    "repository": "projectkoios-bootstrap",
    "scope": "projectkoios-bootstrap"
  },
  "decision": "Adopt a JSON schemas namespace for the UI/core family that holds schemas and contracts only.\n\nThe JSON schemas namespace:\n- defines machine-readable shapes and contracts\n- supports the shared UI/core family without replacing it\n- may be referenced by workflow UI or renderer layers\n- does not define the UI concept itself\n\nThe JSON schemas namespace does not cover:\n- the UI/core domain model\n- rendering implementation\n- marshalling or unmarshalling\n- framework choices\n- transport or runtime internals",
  "id": "adr.json-schemas",
  "implementation_brief": "If accepted, update UI architecture guidance so the JSON schemas namespace is linked as a separate adjacent surface next to `adr.ui-core` and `adr.workflow-ui`.\n\nverification_method: review a proposed schema note and confirm that it defines shapes only, not UI semantics or renderer behavior.",
  "links": {
    "back_to": "architecture.00",
    "superseded_by": null,
    "supersedes": null
  },
  "non_goals": [
    "defining the shared UI/core model itself",
    "choosing renderer implementation details",
    "defining workflow UI behavior",
    "merging schema work into UI core work"
  ],
  "resolved_open_questions": [
    "Which schema files belong in the first version of the namespace?",
    "Should the namespace be flat or grouped by family later?",
    "Which tooling should validate the schema files?"
  ],
  "slug": "json-schemas",
  "status": "draft",
  "title": "JSON Schemas Namespace",
  "validation_expectations": [
    "schema documents can be identified as contracts only",
    "the shared UI/core model remains separate and renderer-agnostic",
    "workflow UI can reference schemas without losing its own boundary"
  ]
}
```

## Status

draft

## Context

{'origin': 'user request', 'from': 'HERMES', 'acting_as': 'user(Eugene)', 'scope': 'projectkoios-bootstrap', 'repository': 'projectkoios-bootstrap', 'delegated_operator': 'pi', 'architecture_domain': 'software'}

## Decision

Adopt a JSON schemas namespace for the UI/core family that holds schemas and contracts only.

The JSON schemas namespace:
- defines machine-readable shapes and contracts
- supports the shared UI/core family without replacing it
- may be referenced by workflow UI or renderer layers
- does not define the UI concept itself

The JSON schemas namespace does not cover:
- the UI/core domain model
- rendering implementation
- marshalling or unmarshalling
- framework choices
- transport or runtime internals

## Consequences

- schema and contract work stays separate from UI/core design
- the shared UI/core ADR can remain renderer-agnostic
- workflow UI can consume schemas without becoming the schema authority
- future tooling can validate against one schema namespace

## architecture-spec

The JSON schemas namespace is a supporting surface for the UI/core family.

It should define:
- schema files and contract files only
- the machine-readable shapes used by the shared UI/core family
- any constraints needed to validate those shapes

It should not define:
- shared UI/core semantics
- workflow UI behavior
- rendering internals

## acceptance-criteria

- a reviewer can tell that the namespace holds schemas only
- the UI/core concept remains defined elsewhere
- workflow UI can consume the namespace without being defined by it
- schema/contract validation remains separate from UI architecture decisions

## implementation-brief

If accepted, update UI architecture guidance so the JSON schemas namespace is linked as a separate adjacent surface next to `adr.ui-core` and `adr.workflow-ui`.

verification_method: review a proposed schema note and confirm that it defines shapes only, not UI semantics or renderer behavior.

## resolved_open_questions

- Which schema files belong in the first version of the namespace?
- Should the namespace be flat or grouped by family later?
- Which tooling should validate the schema files?

## non_goals

- defining the shared UI/core model itself
- choosing renderer implementation details
- defining workflow UI behavior
- merging schema work into UI core work

## validation_expectations

- schema documents can be identified as contracts only
- the shared UI/core model remains separate and renderer-agnostic
- workflow UI can reference schemas without losing its own boundary

## links

{'back_to': 'architecture.00', 'supersedes': None, 'superseded_by': None}
