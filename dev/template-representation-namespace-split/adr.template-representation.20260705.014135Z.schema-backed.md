# ADR: Template Representation and Namespace Split

```json
{
  "created_on": "20260705.014135Z",
  "derived_from": [
    {
      "path": "dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.proposed.md",
      "relationship": "derived_from",
      "role": "ATHENA"
    }
  ],
  "domain": {
    "domain_scope": "templates-implementation-namespace",
    "domain_subtype": "workflow-control-surface",
    "domain_type": "architecture"
  },
  "evidence": [
    {
      "claim": "Existing bootstrap Python package tree is the constrained future implementation target.",
      "kind": "file",
      "ref": "src/python/projectkoios/bootstrap/"
    },
    {
      "claim": "Draft ADR schema constrains this schema-backed record.",
      "kind": "file",
      "ref": "docs/schemas/adr-draft.schema.json"
    }
  ],
  "origin": {
    "actor": "ATHENA",
    "authority": "role",
    "method": "manual",
    "type": "role_output"
  },
  "projections": [
    {
      "editable": false,
      "generated_by": "ATHENA",
      "generated_on": "20260705.014135Z",
      "path": "dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.schema-backed.md",
      "projection_method": "renderer",
      "projection_type": "generated_markdown",
      "source_of_truth": "schema_record",
      "source_record_id": "adr.20260705.014135_template-representation-namespace-split",
      "source_schema_id": "https://projectkoios.local/schemas/adr-draft.schema.json",
      "source_schema_version": "0.1.0-draft"
    }
  ],
  "record_id": "adr.20260705.014135_template-representation-namespace-split",
  "record_version": "0.1.0-draft",
  "repository": "projectkoios-bootstrap",
  "schema_id": "https://projectkoios.local/schemas/adr-draft.schema.json",
  "schema_version": "0.1.0-draft",
  "scope": "projectkoios-bootstrap template/document transformation boundary",
  "source_artifacts": [
    {
      "path": "docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md",
      "relationship": "derived_from",
      "role": "ATHENA"
    },
    {
      "path": "docs/plans/template-representation-and-implementation-namespace-split.md",
      "relationship": "reference",
      "role": "ATHENA"
    },
    {
      "path": "docs/templates/templates.00.md",
      "relationship": "reference",
      "role": "ATHENA"
    },
    {
      "path": "docs/implementation/implementation.00.md",
      "relationship": "reference",
      "role": "ATHENA"
    },
    {
      "path": "docs/architecture/architecture.templates.md",
      "relationship": "reference",
      "role": "ATHENA"
    },
    {
      "path": "docs/adr/adr.templates.draft.md",
      "relationship": "reference",
      "role": "ATHENA"
    },
    {
      "path": "docs/adr/adr.implementation.draft.md",
      "relationship": "reference",
      "role": "ATHENA"
    }
  ],
  "status": "draft",
  "title": "Template Representation and Namespace Split",
  "updated_on": null
}
```

## Context

The repository needs a bounded template/document transformation decision without authorizing broad ingestion or product-domain template semantics.

### Concern
- MUST Preserve the distinction between template representation and broad ingestion.
- MUST Use the current repository layout as implementation-boundary evidence.
- SHOULD Treat predecessor draft ADRs and indexes as source context, not wholesale accepted authority.

## Decision

Adopt a narrow bootstrap slice for canonical template JSON, Markdown rendering, Markdown parsing, and namespace-aware document handling.

### Concern
- MUST Define reusable template documents through canonical JSON, Markdown render, Markdown import, and semantic equivalence boundaries.
- MUST Keep docs/templates/ separate from docs/implementation/ in meaning and classification.
- MUST NOT Authorize Graphify ingestion, vault ingestion, source crawling, projectkoios.ingestion, src/python/ingestion/, or product-domain template architecture.
- SHOULD Prefer src/python/projectkoios/bootstrap/template_representation/ for a first implementation slice if later authorized.

## Consequences

The decision clarifies architecture boundaries while leaving implementation and acceptance promotion as separate state transitions.

### Concern
- MUST Require future implementers to stop for architecture reconciliation before creating a top-level ingestion package.
- MUST NOT Treat acceptance of this ADR as code authorization by itself.
- SHOULD Allow the existing implementation plan to serve only as a constrained Vulcan handoff candidate after acceptance or explicit user direction.

## Acceptance Criteria

Reviewers must be able to inspect the bounded representation, namespace, package, and non-authorization claims.

### Concern
- MUST Distinguish template representation from broader ingestion systems.
- MUST Identify docs/templates/ and docs/implementation/ as separate namespaces with separate meanings.
- MUST Identify src/python/projectkoios/bootstrap/ as the current package tree and template_representation as the preferred first-slice module name.
- MUST NOT Infer code-change authorization from this ADR proposal alone.

## Implementation Brief

No implementation is authorized by this schema-backed draft; a future handoff must restate minimal representation and validation constraints.

### Concern
- MUST Define required fields, optional fields, ordering rules, and normalization behavior for the first supported template fixture before coding.
- MUST Prove one template can round-trip JSON to Markdown to JSON before expanding coverage.
- MUST Test allowed presentation variance, typed parse or equivalence errors, and namespace classification boundaries.
- MUST NOT Change Graphify ingestion, source retrieval, vault ingestion, product-domain code, or top-level ingestion package layout in this slice.

## Non Goals

The slice intentionally excludes broad ingestion, product architecture, and Athena-owned implementation work.

### Concern
- MUST NOT Define general-purpose ingestion architecture, repository crawling, vault ingestion, PDF ingestion, evidence ingestion, or Graphify replacement behavior.
- MUST NOT Create src/python/ingestion/ or projectkoios.ingestion.
- MUST NOT Define product-facing template architecture for the mothership vault or future product repositories.
- MUST NOT Implement code from the Athena workspace.

## Validation Expectations

Follow-on implementation, if authorized, should produce inspectable tests and path checks matching the narrow contract.

### Concern
- SHOULD Validate round-trip tests, presentation-variance fixtures, typed error tests, and namespace classification tests.
- SHOULD Run link/path checks for docs/templates/templates.00.md and docs/implementation/implementation.00.md.
- SHOULD Inspect repository paths to confirm no dependency on src/python/ingestion/ or projectkoios.ingestion.

## Rejected

### Freeform proposal body not represented in schema sections

Reason: The current draft ADR schema only supports the required section set plus normative concerns; richer prose remains in the derived proposal surface.

```text
See dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.proposed.md for full provenance, source traceability table, architecture contract prose, routing notes, and links.
```
