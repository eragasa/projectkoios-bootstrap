```json
{
  "title": "ADR template/schema contract",
  "artifact_type": "adr",
  "status": "accepted",
  "datetime": "20260711.181500Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "docs/adr/ and docs/schemas ADR-family contract",
  "source_slice": "adr-template-schema-contract-successor-draft-slice-11",
  "derived_from": "docs/adr/adr.adr-template-contract.md",
  "source_status_observed": "Accepted",
  "source_mutation": false,
  "schema_mutation": false,
  "authority_change": true
}
```

# ADR: ADR template/schema contract

## Status

accepted

## Provenance

Origin: USER/HERMES activation of `adr-template-schema-contract-successor-draft-slice-11`
From: HERMES
Acting-As: ATHENA
Repository: projectkoios-bootstrap
Scope: ADR template/schema contract successor draft
Delegated-Operator: pi

Primary source/provenance record:

- `docs/adr/adr.adr-template-contract.md`

Observed source status/casing preserved as provenance:

```text
Accepted
```

Planning and review basis:

- `docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md`
- `docs/reviews/hermes-acceptance.20260711.174500_adr-template-schema-contract-successor-planning-slice-10.md`
- `docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md`
- `docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md`
- `docs/schemas/README.md`
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- root `AGENTS.md` ADR filename/body convention

This ADR was reconstructed fresh from current accepted control surfaces. It does not use a bad HERMES reflog draft or Archon/Codex log draft as source text or authority.

## Context

`docs/adr/adr.adr-template-contract.md` is an accepted-like source/provenance record that mixes several concerns:

- ADR content-schema contract;
- template/rendering expectations;
- JSON source-of-truth direction;
- legacy `routing` expectations;
- `dcn` namespace/control language;
- optional workflow-binding rendering guidance.

Later control surfaces clarified the active boundary:

- `docs/schemas/adr.schema.json` is the current ADR content-shape schema until a later approved slice wraps, replaces, or retires it.
- `docs/schemas/schema.record-base.json` is draft record-envelope direction, not current universal record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated Markdown projections remain evidence or review/navigation surfaces unless a later accepted migration/cutover package changes a specific file's disposition.
- JSON authority is accepted staged direction, not current cutover.
- `routing` and `dcn` are not current ADR content-schema fields.
- `workflow_binding` is optional schema-supported content, not operational workflow authority.

This successor ADR states the current template/schema contract without mutating, normalizing, superseding, or migrating the older source.

## Decision

Project Koios treats this ADR as the accepted successor ADR template/schema contract.

### ADR content schema

`docs/schemas/adr.schema.json` is the current ADR content-shape schema until a later approved schema slice wraps, replaces, or retires it.

The content schema owns fields that are part of the ADR decision body or renderable ADR sections, including current fields such as:

- `title`
- `status` as the current flat-schema lifecycle value until envelope reconciliation is implemented
- `context`
- `decision`
- `consequences`
- `architecture_spec`
- `acceptance_criteria`
- `implementation_brief`
- `resolved_open_questions`
- `non_goals`
- `validation_expectations`
- `links`
- optional `workflow_binding`

The ADR content schema must not be assumed to own `routing`, `dcn`, source hashes, projection metadata, source/candidate disposition, migration conflict state, or unsupported-field preservation unless a future schema-change slice explicitly adds those fields.

### Record envelope boundary

`docs/schemas/schema.record-base.json` remains the draft direction for schema-backed record envelopes with top-level `metadata` and `content`.

The envelope direction owns record identity, schema identity/versioning, provenance, derivation, evidence, projection, repository/domain typing, and source-of-truth metadata only after an approved schema/record-envelope slice makes those rules authoritative for the relevant records.

This ADR must not be read as saying that every current ADR is already emitted, stored, or validated as a `metadata` + `content` record.

### Markdown source/control and projection boundary

Markdown under `docs/adr/` remains source/control for unmigrated records.

Generated Markdown projections remain evidence or review/navigation surfaces unless a later accepted migration/cutover package changes the specific file's disposition.

The target future where JSON records become authoritative depends on the gates in `docs/adr/adr.json-authoritative-adr-store.draft.md` and later HERMES/USER cutover decisions.

### `routing` disposition

`routing` is not current ADR content-schema data.

Default disposition:

```text
routing: preserve as sidecar/provenance evidence unless later promoted by workflow/envelope decision
```

Legacy routing prose must not be treated as current workflow, lifecycle, migration, or content-schema authority.

### `dcn` disposition

`dcn` is not current ADR content-schema data.

Default disposition:

```text
dcn: unresolved namespace/control metadata
```

Current identity needs should prefer stable filenames, `id`/`slug` fields where present, and future `metadata.record_id` only when record-envelope authority is explicitly approved. Existing `dcn` mentions should be preserved as legacy namespace/control provenance until a dedicated namespace/schema decision changes that disposition.

This draft does not add `dcn` to any schema.

### `workflow_binding` boundary

`workflow_binding` is optional schema-supported content in `docs/schemas/adr.schema.json`.

It is documentary/schema content only unless a later workflow authority decision gives it operational semantics. It does not control Petri-net workflow runtime, ADR lifecycle state, Operator Console state, or workflow activation.

### Lifecycle and filename boundary

This ADR uses status `accepted` according to the accepted lifecycle vocabulary:

```text
proposal, draft, accepted, active, superseded
```

This ADR uses stable semantic filename:

```text
docs/adr/adr.adr-template-schema-contract.md
```

Timestamps for this draft belong in metadata, provenance, review artifacts, and git history rather than the ADR filename.

The observed old-source status/casing `Accepted` remains provenance and is not normalized by this ADR.

### Relationship to prior source

Accepting this ADR does not supersede, edit, rename, move, archive, normalize, split, delete, migrate, or demote `docs/adr/adr.adr-template-contract.md`.

A later HERMES/USER decision is required to decide whether the older source is superseded, retained as accepted source/provenance, left with errata, or handled by another source-disposition path.

## Consequences

- Reviewers get a current proposed contract that separates ADR content schema, draft record-envelope direction, Markdown source/control, generated projections, sidecar/provenance evidence, and migration/cutover authority.
- The older template contract remains available as source/provenance without silent status normalization or in-place mutation.
- Tooling and future migration slices have a clearer boundary for unsupported source material such as `routing` and `dcn`.
- Future schema changes remain separately gated and are not implied by this draft.
- Future JSON authority cutover remains separately gated and is not implied by this draft.

## Acceptance criteria

Reviewers confirmed:

- The draft identifies `docs/schemas/adr.schema.json` as current ADR content-shape schema only.
- The draft distinguishes ADR content payload from record-envelope metadata and sidecar/provenance evidence.
- The draft states that Markdown under `docs/adr/` remains source/control for unmigrated records.
- The draft states that generated projections are not source authority without later accepted cutover.
- The draft states that `routing` is not current ADR content-schema data and defaults to sidecar/provenance preservation unless later promoted.
- The draft states that `dcn` is unresolved namespace/control metadata and does not add it to schema authority.
- The draft states that `workflow_binding` is optional schema content and not operational workflow authority.
- The draft preserves observed old-source status/casing `Accepted` as provenance and does not normalize the source.
- The draft does not edit `docs/adr/adr.adr-template-contract.md` or any other existing ADR source.
- The draft does not edit `docs/schemas/`.
- The draft does not authorize supersession, source mutation, schema edits, JSON authority cutover, bulk migration, database/storage authority, generated projection replacement, file moves/renames/deletes/archives/splits, status normalization, acceptance, activation, rejection, promotion, or demotion.

## Implementation brief

No code implementation is authorized by this draft.

If this draft is accepted, possible follow-up slices remain separately gated:

1. HERMES/USER acceptance or revision of this draft.
2. Source-disposition decision for `docs/adr/adr.adr-template-contract.md`.
3. Naming-policy/documentation reconciliation for stable semantic ADR filenames and `# ADR: Title` headings across active guidance.
4. Schema-family reconciliation if HERMES/USER wants `metadata` + `content` record-envelope rules to become machine-readable schema authority.
5. Migration/cutover planning only after JSON-authority gates are explicitly satisfied.

## Resolved open questions

- `routing` is not current ADR content-schema data.
- `dcn` is not current ADR content-schema data.
- `workflow_binding` is optional schema-supported content, not operational workflow authority.
- Markdown remains source/control for unmigrated records.
- Generated projections remain evidence/review/navigation unless later cutover changes a specific file's disposition.
- Record-envelope direction is draft direction, not current universal emitted-record authority.

## Non-goals

This ADR does not:

- edit `docs/adr/adr.adr-template-contract.md`;
- edit any existing `docs/adr/` source;
- edit `docs/schemas/`;
- change source status or casing;
- supersede, accept, activate, reject, promote, demote, move, rename, delete, archive, or split any ADR;
- generate projections;
- create authoritative JSON ADR records;
- change database/storage authority;
- migrate records;
- cut over JSON authority;
- define operational Petri-net workflow semantics.

## Validation expectations

Reviewers should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result for this slice: only the accepted successor ADR rename/update appears under `docs/adr/`; no existing ADR source beyond this successor, schema, or dry-run evidence surfaces are modified; diff hygiene passes.

## Links

- `docs/adr/adr.adr-template-contract.md`
- `docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md`
- `docs/reviews/hermes-acceptance.20260711.174500_adr-template-schema-contract-successor-planning-slice-10.md`
- `docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md`
- `docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md`
- `docs/schemas/README.md`
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
