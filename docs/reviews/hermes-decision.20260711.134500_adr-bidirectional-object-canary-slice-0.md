```json
{
  "title": "HERMES decision: ADR bidirectional object canary slice 0",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.134500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-bidirectional-object-canary-slice-0",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.134500: ADR bidirectional object canary slice 0

## Decision

HERMES approves `adr-bidirectional-object-canary-slice-0` for VULCAN implementation.

## Rationale

The architecture direction and hierarchy/disposition addendum are sufficient to proceed with a single-source canary. The canary is intentionally evidence-only and should prove mechanics for a candidate `AdrBidirectionalObject` without changing ADR source authority, schema authority, storage authority, or repository-wide hierarchy.

## Approved implementation direction

- Use exactly one source: `docs/adr/adr.json-schemas.draft.md`.
- Create canary evidence under `dev/adr-bidirectional-object-canary-slice-0/`.
- Produce a candidate `AdrBidirectionalObject` envelope, not a published schema.
- Keep classification/disposition metadata outside ADR `content`.
- Preserve unsupported source fields such as `routing` and `links.related` in sidecar/evidence.
- Generate deterministic Markdown projection evidence and validate generated-projection parse-back semantic equality only.
- Record source/projection/schema hashes and source-mutation proof.
- Use precise authority language and avoid ambiguous `active ADRs` wording.

## Boundaries

Do not mutate `docs/adr/`, change or publish `docs/schemas/`, convert more than the one canary source, move/rename files, normalize statuses, mark drafts superseded, implement hand-authored Markdown ingest, add database/storage authority, commit mutable `.sqlite`/`.db` files, or add Petri-net, Operator Console, or workflow-object integration.

## Required validation

VULCAN should run focused ADR tests, Python policy validation for ADR surfaces, source/schema status checks, no-DB-file checks, JSON validity for the candidate object, and `git diff --check`, plus any specific validation needed for projection parse-back semantic equality.
