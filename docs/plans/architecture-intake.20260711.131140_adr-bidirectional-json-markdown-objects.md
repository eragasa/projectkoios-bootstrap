```json
{
  "title": "ADR bidirectional JSON-Markdown objects architecture intake",
  "artifact_type": "architecture-intake",
  "status": "draft-pending-hermes-user-review",
  "datetime": "20260711.131140Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_concern": "USER concern that ADRs are messy and could be rationalized into bidirectional JSON↔Markdown objects",
  "related_architecture": "docs/architecture/architecture.json-adr-storage-topology.md",
  "scope": "ADR rationalization / bidirectional JSON-Markdown object model intake only",
  "next_owner": "USER_HERMES"
}
```

# Architecture intake 20260711.131140: ADR bidirectional JSON-Markdown objects

## Purpose

Capture the USER architecture concern that ADRs are messy and may need rationalization into bidirectional JSON↔Markdown objects.

This is ATHENA-side architecture/spec intake only. It does not implement code, mutate ADR contents, migrate ADRs, change schema authority, or decide repository-wide ADR storage authority.

This intake is separate from active VULCAN workflow-engine Slice 6 work.

## Existing surfaces to use first

Primary architecture surface:

- `docs/architecture/architecture.json-adr-storage-topology.md`

Related current artifacts and constraints:

- `docs/schemas/adr.schema.json` — current ADR JSON shape target.
- `src/python/projectkoios/bootstrap/control_surface/adr/` — ADR document-family code surface.
- `src/python/projectkoios/bootstrap/control_surface/documents/` — generalized document/data object substrate.
- `src/python/projectkoios/bootstrap/control_surface/storage/` — storage adapter surface.
- `dev/adr-json-database-one-adr-pilot/` — one-ADR pilot evidence.
- `dev/adr-json-schemas-conformance/` — active conformance evidence for one ADR-shaped draft.
- `docs/implementation/json-schemas-adr-conformance.20260711.065704.md` — recent one-document conformance evidence.

Existing topology already says:

- bulk ADR migration is out of scope without a separate approval;
- Markdown review/navigation surfaces must remain;
- Markdown projection is currently evidence/projection, not silently editable authority;
- durable storage authority remains deferred;
- schema/lifecycle/workflow/storage authority redesign requires concrete pressure and approval.

## Problem statement

ADRs currently span multiple forms and authority levels:

- hand-authored Markdown under `docs/adr/`;
- schema-backed JSON records/checkpoints under dev evidence paths;
- generated Markdown projections;
- sidecar/manifest evidence carrying provenance, hashes, unsupported source fields, and conversion details;
- lifecycle/naming policy in separate ADR/architecture surfaces.

The current pilot/conformance approach is intentionally cautious, but the accumulated surfaces are becoming hard to operate. The user concern is that ADRs should become explicit objects that can round-trip between JSON and Markdown without losing authority/provenance clarity.

## Bounded architecture questions

### 1. What is the ADR object?

Questions:

- Is the object a schema-valid ADR payload only, or a wrapper around ADR payload plus provenance/conversion metadata?
- Which fields belong inside the ADR JSON schema versus a sidecar/object envelope?
- Should lifecycle/naming metadata be first-class object fields, object envelope fields, or preserved as separate authority surfaces?

Likely direction to evaluate:

- Keep `docs/schemas/adr.schema.json` as the content payload shape.
- Define an `AdrObject` or `AdrDocumentObject` envelope separately for conversion/provenance/state metadata.
- Do not force conversion-only metadata into the ADR content schema until repeated conformance pressure justifies schema revision.

### 2. What does bidirectional mean?

Questions:

- Is JSON→Markdown projection required to be deterministic and complete?
- Is Markdown→JSON ingest required for all ADR Markdown, or only for generated Markdown with explicit markers?
- How are human edits to Markdown detected, preserved, rejected, or merged?
- What is the conflict rule when JSON and Markdown diverge?

Likely direction to evaluate:

- Start with deterministic JSON→Markdown projection plus parse/equality for generated projections.
- Treat broad hand-authored Markdown→JSON ingest as a later slice unless a small canary ADR proves the shape.
- Require conflict classification rather than silent overwrite.

### 3. What is authoritative?

Questions:

- Is JSON authoritative, Markdown authoritative, database authoritative, or database-operational with JSON checkpoint authority?
- Does authority differ by ADR lifecycle status?
- Is `docs/adr/` a projection surface, an editable source surface, or both with explicit markers?

Likely direction to evaluate:

- Do not change repository-wide authority in the first rationalization slice.
- Define object mechanics as non-authoritative/candidate until an ADR accepts storage authority.
- Use one or two canary ADRs as evidence before authority promotion.

### 4. How are unsupported/extra fields preserved?

Questions:

- Where do removed/unsupported fields such as old `routing` or unsupported link shapes live during conversion?
- How are source text, source hashes, conversion timestamps, and conversion warnings represented?
- Does the object require a standard `sidecar` section?

Likely direction to evaluate:

- Keep unsupported source fields in an object sidecar/evidence envelope.
- Preserve source refs/hashes for every conversion.
- Make lossiness explicit and testable.

### 5. How does this relate to the generalized JSON document store?

Questions:

- Is an ADR object stored as a generic `DocumentRecord` payload?
- Does ADR-specific object behavior live entirely above the generic document-store adapter?
- Are query/index needs ADR-specific projections rather than generic storage columns?

Likely direction to evaluate:

- Preserve current separation: generic document store stores JSON objects; ADR object behavior lives in ADR document-family code.
- Do not add ADR-specific fields to generic storage.

### 6. What is the minimum canary slice?

Questions:

- Which existing ADR should be used as a representative canary?
- Should the canary be a clean schema-adjacent draft, a messy historical ADR, or both?
- What evidence proves round-trip safety without bulk migration?

Candidate canaries:

- `docs/adr/adr.json-schemas.draft.md` — already used for conformance, small, schema-adjacent, has useful unsupported-field canaries.
- `docs/adr/adr.json-database-for-adr-storage.draft.md` — directly related to ADR storage authority, but may conflate mechanics with authority decision.

ATHENA preference for first slice: use `adr.json-schemas.draft.md` again because it is already schema-adjacent and has prior sidecar evidence.

## Likely next artifact

Recommended next artifact:

- `docs/architecture/architecture.adr-bidirectional-objects.md`

Purpose of that architecture note:

- define `AdrObject` / `AdrMarkdownProjection` / `AdrConversionEvidence` vocabulary;
- define JSON↔Markdown round-trip invariants;
- define authority boundaries and conflict rules;
- identify a one-ADR canary implementation slice;
- explicitly defer bulk migration and repository-wide authority change.

Alternative if HERMES/USER wants implementation sooner:

- `docs/plans/implementation-brief.<timestamp>_adr-bidirectional-object-canary.md`

But ATHENA recommends architecture note first because the core ambiguity is authority and bidirectional semantics, not file-level code mechanics.

## Candidate first canary slice, if later approved

Candidate slice name:

`adr-bidirectional-object-canary-slice-0`

Candidate scope:

- define an ADR object envelope for exactly one canary ADR;
- convert Markdown source to ADR object JSON plus conversion evidence;
- render deterministic Markdown projection from object;
- prove JSON→Markdown→object semantic equality for generated projection only;
- preserve unsupported source fields in sidecar/evidence;
- do not mutate `docs/adr/` source Markdown;
- do not bulk migrate;
- do not change `docs/schemas/adr.schema.json` unless a separate schema decision is approved.

## Non-goals for this intake

- No code implementation.
- No ADR content mutation.
- No `docs/adr/` rewrite.
- No bulk migration.
- No repository-wide authority decision.
- No database-authoritative policy decision.
- No schema revision.
- No workflow/Petri-net integration.
- No Operator Console integration.

## Pause / review request

HERMES/USER should decide whether ATHENA should next draft:

1. `docs/architecture/architecture.adr-bidirectional-objects.md` as the controlling architecture note; or
2. a narrower canary implementation brief directly; or
3. no action yet, leaving this intake as queued architecture concern.
