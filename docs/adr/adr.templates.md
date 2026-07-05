```json
{
  "record_id": "adr.templates",
  "schema_id": "https://projectkoios.local/schemas/schema.record-base.json",
  "schema_version": "0.1.0-draft",
  "record_version": "0.1.0-active",
  "title": "Template Representation Contract",
  "status": "active",
  "created_on": "20260702.182000Z",
  "updated_on": "20260705.000000Z",
  "origin": {
    "type": "user_request",
    "method": "manual",
    "actor": "ATHENA",
    "authority": "user"
  },
  "scope": "projectkoios-bootstrap",
  "repository": "projectkoios-bootstrap",
  "domain": {
    "domain_type": "architecture",
    "domain_subtype": "templates",
    "domain_scope": "template-representation"
  },
  "source_artifacts": [
    {
      "path": "docs/templates/templates.00.md",
      "role": "ATHENA",
      "relationship": "controls",
      "note": "Template namespace index."
    },
    {
      "path": "docs/templates/architecture.template.md",
      "role": "ATHENA",
      "relationship": "supports",
      "note": "Active architecture-note template governed by this contract."
    },
    {
      "path": "docs/adr/adr.schema-base.md",
      "role": "ATHENA",
      "relationship": "reference",
      "note": "Schema-base ADR format reference for embedded metadata and editable Markdown projections."
    }
  ],
  "derived_from": [],
  "evidence": [],
  "projections": [
    {
      "path": "docs/adr/adr.templates.md",
      "projection_type": "editable_markdown",
      "source_record_id": "adr.templates",
      "source_schema_id": "https://projectkoios.local/schemas/schema.record-base.json",
      "source_schema_version": "0.1.0-draft",
      "projection_method": "manual",
      "generated_by": "ATHENA",
      "editable": true,
      "source_of_truth": "projection"
    }
  ]
}
```

# ADR: Template Representation Contract

## Status

active

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this ADR are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Context

The repository needs one canonical contract for reusable template documents so the JSON form, the Markdown form, and any cross-format rendering agree on what a template is, even when the Markdown form contains presentation choices that do not exist in the JSON structure.

Today, template material exists in both Markdown and instruction form, but the boundary between template content and template implementation detail is not explicit. That makes it hard to say which differences matter to the contract and which are just rendering choices.

## Decision

Adopt `docs/templates/` as the canonical namespace for reusable template documents and instruction files. Define a representation contract for that namespace so reusable templates can be represented in JSON, rendered as Markdown, and interpreted without losing required meaning.

- MUST use `docs/templates/` as the canonical namespace for reusable template documents and instruction files in this repository.
- MUST define `adr.template-json` as the canonical JSON representation of a reusable template.
- MUST define `adr.template-md` as the canonical Markdown representation of the same reusable template.
- MUST preserve stable meaning across JSON and Markdown forms.
- MUST NOT treat Markdown-only presentation choices as contract changes when the underlying template meaning is preserved.
- MUST NOT require this ADR to prescribe parser, serializer, storage, or file IO internals.
- SHOULD allow explicit transform roles such as `JsonRenderer.to_md()` for JSON-to-Markdown rendering and `ingestion.MdIngester.to_json()` for Markdown-to-JSON ingestion.
- SHOULD treat transform names in this ADR as role descriptions rather than mandatory implementation class names.
- MAY allow multiple Markdown render styles when they preserve the same template meaning.

## Consequences

This decision creates a stable template namespace and a cross-format contract without freezing implementation internals too early.

- MUST keep reusable template documents aligned with the namespace and representation contract defined by this ADR.
- MUST NOT use rendering differences alone as evidence that two template forms disagree.
- SHOULD keep Markdown templates readable for humans while preserving the JSON source shape.
- SHOULD allow implementation teams to build render/ingest code without embedding marshalling details in this ADR.
- MAY tolerate layout, list-style, emphasis, quoting, and heading choices that preserve template meaning.

## Template ADR routing

Template authority is intended to flow downward from this broader representation contract to encapsulated template-specific ADRs when the relationship is explicitly stated. This flow is intentionally provisional while implementation reveals the stable control surface. This ADR is expected to be revised or superseded after the repository supports a JSON-to-Markdown, human edit, Markdown-to-JSON loop that keeps humans in the agent-mediated document workflow.

- MUST treat this ADR as active template-namespace authority.
- MUST NOT enforce template rules mechanically until implementation reports, validation evidence, and migration guidance identify what can safely be checked.
- SHOULD route encapsulated template-specific ADRs through this broader template representation contract when the relationship is explicitly stated.
- SHOULD supersede or constrain encapsulated template ADRs only to the extent described by accepted ADR language and implemented validation behavior.
- SHOULD keep `docs/adr/adr.templates-adr.md` as the active ADR-facing routing surface for template ADR work.
- SHOULD revise or supersede this ADR when JSON-to-Markdown-to-JSON editing becomes implemented and validated as the human-in-the-loop document workflow.
- MAY upgrade the SHOULD-level routing rule to MUST after implementation demonstrates reusable control surfaces, inheritance/reuse mechanics, and migration boundaries.

## Architecture spec

The template representation contract covers reusable template shape, cross-format meaning, and presentation-tolerant rendering boundaries. It does not decide runtime plumbing or exact code structure.

- MUST cover the canonical JSON shape of reusable templates.
- MUST cover the canonical Markdown rendering of reusable templates.
- MUST preserve stable cross-format meaning.
- MUST distinguish presentation differences from semantic template differences.
- MUST NOT define marshalling or unmarshalling internals.
- MUST NOT define the storage backend for templates.
- MUST NOT require exact parser, serializer, or class layout beyond named transform roles.
- SHOULD keep the representation contract portable across implementation languages and storage choices.

## Acceptance criteria

A reviewer must be able to inspect a template and decide whether it conforms to the representation contract without relying on hidden chat context or implementation internals.

- MUST let a reviewer identify what makes a template valid in JSON form.
- MUST let a reviewer identify what makes the same template valid in Markdown form.
- MUST let a reviewer distinguish semantic template differences from presentation-only Markdown differences.
- MUST NOT require implementation-specific marshalling details to determine contract conformance.
- SHOULD keep template docs readable on their own while staying contract-aligned.

## Implementation brief

With this ADR active, implementation may proceed when the enforcement path is ready. Implementation should keep the namespace index and template guidance aligned with `docs/templates/` while avoiding premature enforcement.

- MUST keep the template namespace index and template guidance pointed at `docs/templates/`.
- MUST NOT enforce checks that invalidate existing template or architecture notes before migration guidance exists.
- SHOULD implement or adjust JSON-to-Markdown and Markdown-to-JSON transforms to follow this representation contract.
- SHOULD record implementation reports, validation evidence, and migration guidance before template enforcement becomes active.
- MAY accept both legacy and new presentation forms during migration when their meaning is preserved.

## Resolved open questions

These questions are resolved for the active template representation contract, while implementation details remain open until a bounded implementation slice records evidence.

- MUST treat the JSON representation as the authoritative source for now.
- MUST allow Markdown to serve as the human-readable render target for now.
- SHOULD allow multiple valid Markdown render styles when meaning is preserved.
- SHOULD treat transform names as descriptive placeholders unless a later accepted decision makes them formal API names.

## Non-goals

The representation contract intentionally avoids over-specifying implementation machinery or replacing other document lifecycle rules.

- MUST NOT define marshalling or unmarshalling internals.
- MUST NOT define the storage backend for templates.
- MUST NOT replace the ADR lifecycle.
- MUST NOT force one rigid Markdown style when multiple styles preserve meaning.
- MAY defer implementation-specific parser, serializer, and persistence decisions to later implementation briefs or ADRs.

## Validation expectations

Validation should demonstrate cross-format preservation without confusing presentation choices for semantic differences.

- MUST validate that a JSON template can be rendered to Markdown without losing required meaning.
- MUST validate that a Markdown template can be ingested into the canonical JSON form without losing required meaning.
- MUST NOT fail solely because list style or comparable presentation choices differ while meaning is preserved.
- SHOULD include tests or review artifacts that distinguish semantic mismatch from presentation-only variation.

## Routing

Athena owns this ADR as an architecture/specification artifact. Enforcement remains dependent on implementation and migration evidence.

- MUST treat Athena as the owner for this ADR's architecture/specification state.
- MUST treat the current phase as active.
- MUST NOT treat active status as automatic enforcement readiness.
- SHOULD record implementation and migration evidence before enabling validators or policy checks based on this ADR.

## Links

These links identify related navigation and lifecycle surfaces for the template representation contract.

- MUST treat `docs/architecture/architecture.00.md` as the architecture index back-reference.
- SHOULD treat `docs/adr/adr.templates-adr.md` as the ADR-facing template routing surface.
- SHOULD add supersession links when later accepted ADRs replace or narrow this contract.
- MAY supersede this ADR with a schema-backed template contract once JSON-to-Markdown-to-JSON editing is implemented.
