```json
{
  "title": "HERMES decision: ADR JSON authority inventory/classification slice 0",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.141000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-inventory-classification-slice-0",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.140700_adr-json-authority-inventory-classification-slice-0.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.141000: ADR JSON authority inventory/classification slice 0

## Decision

HERMES approves `adr-json-authority-inventory-classification-slice-0` for VULCAN implementation.

## Rationale

The JSON-authoritative ADR direction requires a review-only corpus inventory before conversion or authority changes. The ATHENA brief is bounded to Phase 0 inventory/classification and preserves the required no-mutation, no-schema-change, no-authority-cutover boundaries.

## Approved implementation direction

- Inspect and classify `docs/adr/*.md` and ADR index/control files such as `docs/adr/README.md`.
- Produce review-only manifest/evidence under `dev/adr-json-authority-inventory-classification-slice-0/`.
- Record source path/hash, file kind, source title, observed status text and casing, normalized status candidate if safely inferable, parse confidence, warnings, category/disposition candidates, `authority_effect`, owner/domain review flags, automatic-conversion eligibility, and exclusion/blocking reasons.
- Keep all classification values candidate/review-only.

## Boundaries

Do not mutate `docs/adr/`, change `docs/schemas/`, move/rename/delete/archive ADR files, normalize source statuses, mark drafts superseded, create authoritative JSON records, perform corpus conversion, generate replacement Markdown projections, add database/storage authority, or commit mutable `.sqlite`/`.db` files.

## Required validation

VULCAN should validate JSON evidence, source/schema non-mutation, no DB files, deterministic/stable manifest behavior where practical, focused tests if code is added, Python policy if Python is changed, and `git diff --check`.
