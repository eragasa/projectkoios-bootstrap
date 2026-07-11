```json
{
  "title": "HERMES decision: ADR JSON authority corpus dry-run inventory slice 4",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.152000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md",
  "provenance_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.152000: ADR JSON authority corpus dry-run inventory slice 4

## Decision

HERMES approves `adr-json-authority-corpus-dry-run-inventory-slice-4` for VULCAN implementation.

## Rationale

ATHENA revised the implementation brief to align with KOIOS Slice 4 provenance input. The brief now uses the KOIOS-recommended six-entry bounded subset, preserves corpus-style reporting as a subset dry run rather than a migration, and explicitly excludes higher-risk product/domain files unless separately approved.

This is the appropriate next proof point after accepted Slices 2 and 3 because it tests multi-file reporting, skipped/blocked/projectable outcome aggregation, source-to-candidate lossiness visibility, sidecar/provenance needs, and candidate-only/no-authority signaling without expanding to all ADRs or performing authority cutover.

## Approved subset

Use exactly these six entries:

```text
docs/adr/adr.json-schemas.draft.md
docs/adr/adr.petrinet.20260705.132740Z.md
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
docs/adr/adr.adr-lifecycle.draft.md
docs/adr/README.md
```

No other ADR source may be converted, projected, parsed as a candidate, or counted as part of the dry-run subset.

Explicitly excluded unless HERMES/USER separately approves them:

```text
docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md
docs/adr/adr.20260702.043600_koios-adversarial-code-review-authority.draft.md
```

## Approved implementation direction

- Use evidence path `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`.
- Produce candidate-only corpus-style dry-run evidence over the approved six-entry subset.
- Preserve exact source paths and current source hashes; compare against Slice 1 reviewed values and report staleness if encountered.
- Preserve per-source reviewed inventory values, observed status/casing, normalized candidates if any, blockers, lossiness findings, sidecar/provenance needs, and final outcomes.
- Aggregate counts by category, disposition, authority effect, auto-conversion eligibility, entry type, outcome, projection status, parse-back status, missing-status findings, status-normalization sensitivity, domain/manual-review blockers, skipped/index-control rows, and sidecar/provenance needs.
- Keep Slice 2 missing-status behavior and Slice 3 wrapped-list/status-casing regression behavior visible.
- Treat `docs/adr/README.md` as an index/control surface skipped/excluded row, not an ADR record.
- Treat `docs/adr/adr.adr-lifecycle.draft.md` as source/provenance draft handling, not current lifecycle authority or supersession.
- Treat accepted/current source status in `docs/adr/adr.petrinet.20260705.132740Z.md` as source observation only, not JSON authority.

## Boundaries

Do not mutate `docs/adr/`, change `docs/schemas/`, normalize source status in source Markdown, create authoritative JSON ADR records, create replacement projections, convert/project/parse candidate records outside the approved six-entry subset, move/rename/delete/archive/supersede files, add database/storage authority, commit mutable `.sqlite`/`.db` files, treat `dev/` evidence as durable authority, run an all-ADR conversion, perform bulk migration, or authorize JSON authority cutover.

## Required post-implementation review

Before HERMES final acceptance, require:

- KOIOS provenance review focused on whether multi-file aggregation preserves per-source provenance, blocker specificity, source-to-candidate lossiness visibility, sidecar/provenance clarity, and no-authority signaling.
- ATHENA architecture/conformance review focused on implementation-brief conformance, accepted Slice 2/Slice 3 watchpoints, exact subset enforcement, and no-authority boundaries.

## Required validation

Validate exactly-six-source proof, source/schema non-mutation, JSON evidence validity, no DB files under the Slice 4 evidence path, generated projections only under the Slice 4 `dev/` path if produced, aggregate counts matching per-source records, tests/type checks/Python policy if code changes, and `git diff --check` clean.
