```json
{
  "title": "HERMES decision: ADR JSON authority messy canary slice 2",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.144200Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-messy-canary-slice-2",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.144200: ADR JSON authority messy canary slice 2

## Decision

HERMES approves `adr-json-authority-messy-canary-slice-2` for VULCAN implementation.

## Rationale

The accepted inventory review/override evidence identifies `docs/adr/adr.schema-base.md` as the primary messy canary candidate. ATHENA's brief and KOIOS commentary confirm this is the next bounded proof point for missing-status handling, schema/implementation-contract ambiguity, conflict/lossiness reporting, and sidecar/provenance preservation without inventing authority.

## Approved implementation direction

- Use exactly one source: `docs/adr/adr.schema-base.md`.
- Use reviewed inventory/override evidence from `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Produce candidate JSON/object/conversion evidence under `dev/adr-json-authority-messy-canary-slice-2/`.
- Preserve missing status as missing; do not invent `draft` or any other status to satisfy schema validation.
- Preserve schema/implementation-contract ambiguity explicitly; do not collapse the source into a normal decision record.
- Produce visible conflict/lossiness reporting, including `conversion_candidate_blocked_pending_review` or equivalent if status/schema gaps remain.
- Preserve source path/hash, title if parseable, reviewed category/disposition/authority-effect, parse warnings, source non-mutation proof, and sidecar/provenance evidence.
- Generated projection/parse-back evidence is allowed only if evidence-only and bounded.

## Boundaries

Do not mutate `docs/adr/`, change `docs/schemas/`, convert any file other than `docs/adr/adr.schema-base.md`, create authoritative JSON ADR records, create replacement projections, move/rename/delete/archive files, normalize source status, mark drafts superseded, perform authority cutover, add database/storage authority, or commit mutable `.sqlite`/`.db` files.

## Required validation

Validate source/schema non-mutation, exactly-one-source proof, JSON evidence validity, no DB files under the Slice 2 evidence path, tests/type checks/Python policy if code changes, and `git diff --check`.
