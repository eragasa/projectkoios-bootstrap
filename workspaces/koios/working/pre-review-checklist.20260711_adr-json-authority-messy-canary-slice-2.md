```json
{
  "title": "KOIOS pre-review checklist: ADR JSON authority messy canary slice 2",
  "artifact_type": "pre-review-checklist",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-messy-canary-slice-2",
  "source_canary": "docs/adr/adr.schema-base.md"
}
```

# KOIOS pre-review checklist: ADR JSON authority messy canary slice 2

## Authority boundary

This checklist is KOIOS provenance support only. It does not authorize implementation, source mutation, schema changes, conversion authority, or cutover.

## Sources checked

- `docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md`
- `docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json`
- Source canary: `docs/adr/adr.schema-base.md`

## Slice 1 reviewed source facts to preserve

For `docs/adr/adr.schema-base.md`, Slice 1 reviewed inventory records:

- `source_hash`: `48a5fed34bec41b18885fdb57d7491895783f735c07efc33202098bbf61a2d51`
- `category_candidate`: `template_schema_contract`
- `disposition_candidate`: `manual_review_required`
- `authority_effect`: `candidate`
- `automatic_conversion_eligibility_candidate`: `false`
- `exclusion_blocking_reasons`: `manual_review_required`, `missing_observed_status`, `missing_status`
- `owner_domain_review_flags.manual_review_required`: `true`
- `candidate_only`: `true`
- `authority_change`: `false`
- `source_mutation`: `false`

## Important source nuance

`docs/adr/adr.schema-base.md` has no top-level ADR `## Status` section or leading ADR metadata status detectable by the inventory, but it contains an embedded JSON block under `## Context` with `"status": "draft"` inside a schema-record-like payload.

Expected handling:

- Preserve the inventory finding that the source ADR status is missing.
- Preserve embedded JSON `status: draft` as embedded/source payload evidence only.
- Do not promote embedded payload status into ADR lifecycle status unless a later ATHENA/USER decision defines that mapping.
- Do not invent a top-level ADR status to satisfy schema validation.

## VULCAN evidence checklist

### Required preservation

- [ ] Source path recorded exactly: `docs/adr/adr.schema-base.md`.
- [ ] Source hash recorded and checked before/after.
- [ ] Source title captured if parsed: `ADR: Schema Base Class for ADR Records`.
- [ ] Slice 1 reviewed values referenced or copied with source hash.
- [ ] Missing top-level status preserved as missing.
- [ ] Embedded JSON `status: draft` preserved as embedded payload/source evidence, not silently elevated.
- [ ] Schema/implementation-contract ambiguity recorded: this source is not a normal decision record.
- [ ] Manual-review requirement preserved.

### Conflict/lossiness expected findings

- [ ] `missing_status` conflict/finding present.
- [ ] Candidate object validation either fails/blocks due to missing required ADR status, or clearly marks content incomplete/review-only.
- [ ] No normalized status candidate is inserted into authoritative content.
- [ ] If any field is inferred, it is marked `requires_review: true` with rationale.
- [ ] Unsupported or ambiguous material is preserved in sidecar/provenance, not dropped.
- [ ] Final outcome is visibly review-only, e.g. `conversion_candidate_blocked_pending_review` or `candidate_object_generated_with_conflicts`.

### Sidecar/provenance expected content

- [ ] Source path/hash/title.
- [ ] Observed missing status and parse warnings.
- [ ] Embedded JSON block provenance, including embedded `record_id`, `schema_id`, `status`, dates, projections, links/source artifacts where captured.
- [ ] Fields omitted from ADR `content` and why.
- [ ] Fields preserved outside `content` because they are schema-record/envelope material rather than ADR payload.
- [ ] Reviewed inventory category/disposition/authority-effect and manual-review rationale.

### One-source and boundary proof

- [ ] Exactly one source attempted/converted: `docs/adr/adr.schema-base.md`.
- [ ] No other `docs/adr/*.md` included as a second source canary.
- [ ] No `docs/adr/` mutation.
- [ ] No `docs/schemas/` mutation.
- [ ] No file moves/renames/deletes/archives.
- [ ] No source status normalization.
- [ ] No draft supersession.
- [ ] No authoritative JSON ADR record.
- [ ] No authority cutover.
- [ ] No database/storage authority.
- [ ] No `.sqlite` or `.db` files under Slice 2 evidence path.

### Projection caveat if implemented

- [ ] Projection is under `dev/adr-json-authority-messy-canary-slice-2/` only.
- [ ] Projection is marked generated evidence only.
- [ ] Parse-back is only for generated projection.
- [ ] Projection equality does not resolve missing source status.
- [ ] Projection does not replace or mutate `docs/adr/adr.schema-base.md`.

## KOIOS expected review stance

A good Slice 2 result may be a blocked/partial candidate. Success is not “make `adr.schema-base.md` validate by inventing `draft`.” Success is proving that the migration machinery can preserve messy source facts, report missing status and contract ambiguity, and stop short of authority when evidence is incomplete.
