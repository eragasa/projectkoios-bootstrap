<!-- GENERATED PILOT PROJECTION: non-authoritative; do not edit as ADR authority. -->
# ADR Projection: JSON ADR Storage Topology

## Projection metadata

- Pilot status: non-authoritative-pilot
- Source record ID: adr.json-database-for-adr-storage
- Canonical slug: json-database-for-adr-storage
- Record status: draft
- Legacy/source path: docs/adr/adr.json-database-for-adr-storage.draft.md
- Schema ID: https://projectkoios.local/schemas/adr.schema.json
- Generation method: projectkoios.bootstrap.control_surface.adr.pilot.AdrStoragePilot.run
- Source-of-truth mode: database-operational/json-checkpointed
- Source hash: b7e48d5b2a07c14704689b4dcae738c8f21731e6d20e8d63d8eab33c75819d87
- JSON checkpoint hash: 0bb030d8f33bd1081f5415871431e10aeb943d23d00dd346dc91b645ede45d04
- Conflict rule: Source Markdown remains migration evidence; SQLite is local operational state behind the adapter; JSON checkpoint is committed review checkpoint; generated Markdown projection is non-authoritative pilot evidence.

```json adr-record
{
  "acceptance_criteria": [
    "ADRs can be represented as JSON without losing schema fields",
    "Markdown renderings remain available for review",
    "lookup by status/title/routing is simpler than grep-only inspection",
    "the authority boundary between source JSON and cache/index is explicit"
  ],
  "architecture_spec": "This ADR defines the ADR storage authority, not just the filename convention.\n\nThe canonical record is JSON-shaped and should include the existing ADR schema fields. Markdown is derived from that record for review and navigation.\n\nIf SQLite is added, it is an index/cache layer only unless a later ADR changes its authority.",
  "consequences": "- ADR content becomes easier to query and validate\n- Markdown remains useful for review and diff-friendly rendering\n- the repository can preserve a structured source of truth while still being legible\n- index/cache behavior must be kept separate from canonical authority",
  "context": {
    "acting_as": "HERMES",
    "architecture_domain": "software",
    "delegated_operator": "HERMES",
    "from": "HERMES",
    "origin": "user request",
    "repository": "projectkoios-bootstrap",
    "scope": "projectkoios-bootstrap"
  },
  "decision": "Adopt JSON files on disk as the canonical ADR storage shape and treat Markdown as a render or presentation form.\n\nThe storage model should support:\n- stable schema validation\n- indexed lookup by title, status, and routing\n- human-readable rendering for review\n- promotion without losing the underlying structured record\n\nSQLite may be used as an index/cache, but it must not become the primary authority unless explicitly promoted later.",
  "id": "adr.json-database-for-adr-storage",
  "implementation_brief": "If accepted, update the ADR creation and render guidance so new ADRs treat JSON as canonical and Markdown as a derived view.\n\nverification_method: validate that a representative ADR can round-trip from JSON to Markdown and back without losing required fields.",
  "links": {
    "back_to": "architecture.00",
    "superseded_by": null,
    "supersedes": null
  },
  "non_goals": [
    "changing the ADR schema itself",
    "removing Markdown from the review workflow",
    "forcing a database migration before the authority decision is settled"
  ],
  "resolved_open_questions": [
    "Should SQLite be cache-only or a persistent index?",
    "Should promoted ADRs still have Markdown-first review files?",
    "Should the repository migrate existing ADR drafts into JSON records later?"
  ],
  "slug": "json-database-for-adr-storage",
  "status": "draft",
  "title": "JSON ADR Storage Topology",
  "validation_expectations": [
    "a reviewer can identify the canonical source form",
    "the render stays consistent with the stored record",
    "lookup and promotion behavior remain explicit"
  ]
}
```

## Status

draft

## Context

{'acting_as': 'HERMES', 'architecture_domain': 'software', 'delegated_operator': 'HERMES', 'from': 'HERMES', 'origin': 'user request', 'repository': 'projectkoios-bootstrap', 'scope': 'projectkoios-bootstrap'}

## Decision

Adopt JSON files on disk as the canonical ADR storage shape and treat Markdown as a render or presentation form.

The storage model should support:
- stable schema validation
- indexed lookup by title, status, and routing
- human-readable rendering for review
- promotion without losing the underlying structured record

SQLite may be used as an index/cache, but it must not become the primary authority unless explicitly promoted later.

## Consequences

- ADR content becomes easier to query and validate
- Markdown remains useful for review and diff-friendly rendering
- the repository can preserve a structured source of truth while still being legible
- index/cache behavior must be kept separate from canonical authority

## architecture-spec

This ADR defines the ADR storage authority, not just the filename convention.

The canonical record is JSON-shaped and should include the existing ADR schema fields. Markdown is derived from that record for review and navigation.

If SQLite is added, it is an index/cache layer only unless a later ADR changes its authority.

## acceptance-criteria

- ADRs can be represented as JSON without losing schema fields
- Markdown renderings remain available for review
- lookup by status/title/routing is simpler than grep-only inspection
- the authority boundary between source JSON and cache/index is explicit

## implementation-brief

If accepted, update the ADR creation and render guidance so new ADRs treat JSON as canonical and Markdown as a derived view.

verification_method: validate that a representative ADR can round-trip from JSON to Markdown and back without losing required fields.

## resolved_open_questions

- Should SQLite be cache-only or a persistent index?
- Should promoted ADRs still have Markdown-first review files?
- Should the repository migrate existing ADR drafts into JSON records later?

## non_goals

- changing the ADR schema itself
- removing Markdown from the review workflow
- forcing a database migration before the authority decision is settled

## validation_expectations

- a reviewer can identify the canonical source form
- the render stays consistent with the stored record
- lookup and promotion behavior remain explicit

## links

{'back_to': 'architecture.00', 'superseded_by': None, 'supersedes': None}
