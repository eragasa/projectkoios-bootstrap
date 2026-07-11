```json
{
  "title": "HERMES acceptance: JSON-authoritative ADR store staged direction",
  "artifact_type": "acceptance-review",
  "status": "accepted-staged-direction-with-watchpoints",
  "datetime": "20260711.140500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "json-authoritative-adr-store",
  "reviewed_artifact": "docs/adr/adr.json-authoritative-adr-store.draft.md"
}
```

# HERMES acceptance 20260711.140500: JSON-authoritative ADR store staged direction

## Verdict

Accepted as the controlling staged direction, with watchpoints.

## Meaning of acceptance

This acceptance authorizes planning and implementation of the staged migration path described in `docs/adr/adr.json-authoritative-adr-store.draft.md`, starting with inventory/classification and dry-run evidence.

This acceptance does not by itself execute migration, publish or change `docs/schemas/`, mutate `docs/adr/`, demote Markdown authority for any record, move/rename files, normalize statuses, mark drafts superseded, or flip repository authority to JSON.

## Review basis

- `docs/adr/adr.json-authoritative-adr-store.draft.md`
- `docs/architecture/architecture.adr-bidirectional-objects.md`
- `docs/architecture/architecture.json-adr-storage-topology.md`
- `workspaces/koios/working/provenance-risk.20260711_adr-json-authority-mass-conversion.md`
- `docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md`
- `docs/reviews/hermes-acceptance.20260711.135800_adr-bidirectional-object-canary-slice-0.md`

## Accepted staged path

The next implementation slice should begin Phase 0: inventory/classification manifest.

Required next-slice boundaries:

- inspect and classify `docs/adr/*.md` plus index/control files;
- record observed status/casing separately from any normalized status;
- classify document type/disposition and uncertainty;
- produce review-only manifest/evidence under `dev/`;
- do not mutate `docs/adr/`;
- do not create or publish authoritative JSON records;
- do not change `docs/schemas/`;
- do not move/rename files;
- do not normalize statuses;
- do not mark drafts superseded;
- do not commit mutable database files;
- do not perform corpus conversion or authority cutover.

## Watchpoints

Not every `docs/adr/*.md` file is automatically an ADR decision eligible for JSON authority. Architecture, policy/process, template/schema/contract, implementation workflow support, index/control, source/provenance, and product/future-system documents must be classified and may require exclusion or owner/domain review.

Per-record conflicts or lossiness block authority promotion until reviewed, resolved, or excluded. File-based JSON remains the default target authority; SQLite/database authority remains deferred unless a later accepted ADR promotes it.
