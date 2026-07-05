```json
{
  "record_id": "adr.templates-adr",
  "schema_id": "https://projectkoios.local/schemas/schema.record-base.json",
  "schema_version": "0.1.0-draft",
  "record_version": "0.1.0-active",
  "title": "Template ADR Control Surface",
  "status": "active",
  "created_on": "20260705.000000Z",
  "updated_on": "20260705.000000Z",
  "origin": {
    "type": "user_request",
    "method": "manual",
    "actor": "ATHENA",
    "authority": "user"
  },
  "scope": "projectkoios-bootstrap template-related ADR routing",
  "repository": "projectkoios-bootstrap",
  "domain": {
    "domain_type": "architecture",
    "domain_subtype": "templates",
    "domain_scope": "template-adr-routing"
  },
  "source_artifacts": [
    {
      "path": "docs/adr/adr.templates.md",
      "role": "ATHENA",
      "relationship": "controls",
      "note": "Broader active template representation contract."
    },
    {
      "path": "docs/adr/adr.schema-base.md",
      "role": "ATHENA",
      "relationship": "reference",
      "note": "Schema-base ADR format reference for embedded metadata and editable Markdown projections."
    },
    {
      "path": "intercom:koios:20260705-template-adr-review",
      "role": "KOIOS",
      "relationship": "review",
      "note": "KOIOS requested provenance, convention rationale, Decision section, and SHOULD/MUST consistency."
    },
    {
      "path": "intercom:vulcan:20260705-template-adr-review",
      "role": "VULCAN",
      "relationship": "review",
      "note": "VULCAN identified implementation and validation risks for premature enforcement."
    },
    {
      "path": "intercom:hermes:20260705-template-adr-review",
      "role": "HERMES",
      "relationship": "review",
      "note": "HERMES identified cross-domain authority and control-surface risks."
    }
  ],
  "derived_from": [],
  "evidence": [],
  "projections": [
    {
      "path": "docs/adr/adr.templates-adr.md",
      "projection_type": "editable_markdown",
      "source_record_id": "adr.templates-adr",
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

# ADR: Template ADR Control Surface

## Status

active

Controlled by: `docs/adr/adr.templates.md`

This is an active ADR-facing control surface for template-related ADR work. It is controlled by the broader template representation contract in `docs/adr/adr.templates.md`.

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this ADR are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Context

The template namespace now contains reusable templates and template revisions, including architecture-note template material. Template-related ADR surfaces need an explicit control surface back to the template representation contract so ADR-template work does not drift from the broader `docs/templates/` namespace contract.

This file intentionally uses the stable alias `docs/adr/adr.templates-adr.md` instead of a timestamped filename because it is a current control-surface join for the template ADR family. This convention rationale is expected to be revisited after schema-backed JSON-to-Markdown-to-JSON editing exists and the repository can preserve stable aliases through generated projections.

## Decision

Use this document as the ADR-facing control surface for template-related ADR surfaces. Preserve downward authority flow from the broader template representation contract while allowing narrower template-specific ADRs to remain encapsulated.

- MUST treat `docs/adr/adr.templates.md` as the broader active template representation contract.
- MUST NOT treat narrower template-specific ADRs as overriding the broader template representation contract unless the broader ADR or a later accepted ADR explicitly allows that override.
- SHOULD route template ADR material through `docs/adr/adr.templates.md` unless a narrower accepted ADR explicitly controls a specific template artifact.
- SHOULD treat authority as flowing downward from the broader active template contract to encapsulated template-specific ADRs.
- SHOULD supersede or constrain encapsulated template ADRs only to the extent stated by the broader ADR and its implementation language.
- SHOULD preserve narrower existing controls unless they are explicitly superseded or constrained.
- SHOULD revise or supersede this ADR when JSON-to-Markdown-to-JSON editing becomes implemented and validated as the human-in-the-loop document workflow.
- MAY upgrade this SHOULD-level routing rule to MUST after implementation reveals the stable control surface.

## Existing narrower controls

Some template-specific ADRs already control narrower template artifacts. This ADR-facing control surface keeps those controls valid while clarifying their relationship to the broader template namespace contract.

- MUST continue to treat `docs/adr/adr.adr-template-contract.md` as the specific control for the canonical ADR proposal template unless explicitly superseded.
- MUST continue to treat `docs/adr/adr.templates.md` as the broader reusable template namespace and representation contract.
- MUST NOT silently collapse narrower controls into the broader template contract without explicit supersession or constraint language.
- SHOULD use explicit language when a broader template rule constrains a narrower template-specific ADR.
- MAY add further template-specific ADRs when a bounded template artifact needs independent decision context.

## Enforcement boundary

The template contract is active as authority, but enforcement depends on implementation, validation, and migration evidence. This distinction allows the document system to iterate without invalidating existing files prematurely.

- MUST treat the template contract as active authority.
- MUST NOT treat active authority as automatic validator or policy enforcement readiness.
- SHOULD keep template enforcement inactive until the corresponding implementation, validation, and migration path are recorded.
- SHOULD use implementation feedback to refine the stable control surface before upgrading provisional SHOULD rules to MUST rules.
- MAY accept both legacy and new template forms during migration when their meaning is preserved.

## Consequences

Template-related ADR work now has a stable ADR-facing control surface while the document system continues to clarify authority flow, inheritance, and reusable implementation boundaries.

- MUST centralize the broader template namespace contract in `docs/adr/adr.templates.md`.
- MUST NOT pretend the final implementation control surface is already known.
- SHOULD use explicit downward-flow language to prevent collapsing authority between broader and narrower ADRs.
- SHOULD preserve specific template contracts when appropriate.
- MAY revise this ADR after implementation reveals a better control surface.

## Links

These links identify the controlling ADR and related navigation surfaces.

- MUST treat `docs/adr/adr.templates.md` as the controlling ADR for this surface.
- SHOULD use `docs/templates/templates.00.md` as the template namespace index.
- SHOULD use `docs/architecture/architecture.templates.md` as the template architecture note.
- MAY supersede this stable alias with a schema-backed routing record once JSON-to-Markdown-to-JSON editing is implemented.
