```json
{
  "title": "Successor brief: ADR template/schema contract",
  "artifact_type": "successor-planning-brief",
  "status": "proposal-only-pending-hermes-user-acceptance",
  "datetime": "20260711.172500Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-successor-planning-slice-10",
  "target_source": "docs/adr/adr.adr-template-contract.md",
  "hermes_decision": "docs/reviews/hermes-decision.20260711.173500_adr-template-schema-contract-successor-planning-slice-10.md",
  "authority_change": false,
  "source_mutation": false,
  "schema_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# Successor brief 20260711.172500: ADR template/schema contract

## Purpose

Define what a future successor ADR/template-schema contract draft should contain before creating that draft.

This brief is proposal-only. It does not create a new ADR, edit `docs/adr/`, edit `docs/schemas/`, supersede `docs/adr/adr.adr-template-contract.md`, normalize status casing, convert Markdown to JSON, generate projections, migrate records, or cut over authority.

## Source and provenance basis

Primary source under repair planning:

```text
docs/adr/adr.adr-template-contract.md
```

Planning inputs:

```text
docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
docs/reviews/hermes-acceptance.20260711.172000_schema-family-doc-index-clarification-slice-9.md
docs/schemas/README.md
docs/adr/adr.adr-lifecycle.20260705.011836Z.md
```

The future successor must preserve `docs/adr/adr.adr-template-contract.md` as source/provenance unless HERMES/USER separately approves lifecycle/source disposition. The observed source status `Accepted` and its casing must be preserved as observed provenance and must not be silently normalized by this planning track.

## Intended future draft

Recommended future draft path:

```text
docs/adr/adr.adr-template-schema-contract.<YYYYMMDD.HHMMSSZ>.draft.md
```

Recommended initial status:

```text
draft
```

Rationale:

- The source needing repair is accepted-like and semantically mixed.
- A successor draft makes the proposed current contract explicit without in-place mutation.
- `draft` aligns with the accepted lifecycle vocabulary for a complete ADR review record that is not yet accepted authority.
- Acceptance, activation, or supersession must remain later HERMES/USER decisions.

Alternative if HERMES/USER wants one more non-ADR staging step: create a `docs/plans/` proposal packet first, then create the ADR draft in a separate approved slice.

## Future successor content requirements

A future successor ADR/template-schema contract draft should contain these sections and decisions.

### 1. Current ADR content-schema contract

State that `docs/schemas/adr.schema.json` is the current ADR content-shape schema until a later approved slice wraps, replaces, or retires it.

The successor should list current content-schema fields from the current schema/README boundary, including:

- `title`
- `status` as the current flat-schema lifecycle field until envelope reconciliation is implemented
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

The successor must not claim unsupported fields are current content-schema fields.

### 2. Record-envelope and schema-family boundary

State that `docs/schemas/schema.record-base.json` is the draft record-envelope direction with top-level `metadata` and `content`, and that family schemas such as `adr-draft.schema.json` demonstrate composition with that base envelope.

The successor should distinguish:

- ADR content payload: decision body and renderable ADR sections.
- Record envelope metadata: identity, schema identity/versioning, provenance, derivation, evidence, projection, repository/domain typing, and source-of-truth metadata.
- Sidecar/provenance evidence: unsupported source fields, hashes, observed status/casing, conversion warnings, omitted sections, inferred fields, and conflict classifications.

The successor must not publish or modify machine-readable schema authority under `docs/schemas/`.

### 3. Markdown source/control and projection boundary

State that Markdown under `docs/adr/` remains source/control for unmigrated records.

State that generated Markdown projections remain evidence or review/navigation surfaces unless a later accepted migration/cutover package changes the disposition of a specific file.

The successor may describe the target future where JSON records become authoritative, but must label it as staged direction that depends on the gates in `docs/adr/adr.json-authoritative-adr-store.draft.md` and later HERMES/USER cutover decisions.

### 4. `routing` disposition

The successor must state that `routing` is not a current ADR content-schema field.

Recommended default disposition:

```text
routing: preserve as sidecar/provenance evidence unless later promoted by workflow/envelope decision
```

The successor should explicitly exclude `routing` from current content-schema claims and avoid using legacy routing prose as current workflow, lifecycle, or migration authority.

### 5. `dcn` disposition

The successor must state that `dcn` is not a current ADR content-schema field.

Recommended default disposition:

```text
dcn: unresolved namespace/control metadata; preserve legacy mentions as provenance and prefer metadata.record_id / filename conventions for current identity needs until a dedicated namespace/schema decision is approved
```

The successor must not add `dcn` to `docs/schemas/adr.schema.json` or any schema file.

### 6. `workflow_binding` boundary

The successor should state that `workflow_binding` is optional schema-supported content in `docs/schemas/adr.schema.json`.

It must also state that `workflow_binding` is documentary/schema content only unless a later workflow authority decision gives it operational semantics. It must not imply that Petri-net workflow runtime, ADR lifecycle state, Operator Console state, or workflow activation is controlled by `workflow_binding`.

### 7. Status and lifecycle handling

The successor should use canonical lowercase lifecycle vocabulary from `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`:

```text
proposal, draft, accepted, active, superseded
```

It should preserve observed source status/casing from `docs/adr/adr.adr-template-contract.md` in provenance and must not silently normalize the source.

If the successor is later accepted, HERMES/USER must separately decide whether it merely coexists as newer authority, supersedes the old source, or triggers a later source-disposition/supersession slice.

### 8. Relationship to old source

The successor draft should include an explicit relation block naming:

- `docs/adr/adr.adr-template-contract.md` as source/provenance and repair target;
- `docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md` as the repair-plan basis;
- `docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md` and `docs/schemas/README.md` as schema-family layering basis;
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` as lifecycle vocabulary basis.

The relation block must say that the old source is not superseded, edited, renamed, moved, archived, normalized, split, or migrated by creating the successor draft.

## Acceptance criteria for a future ADR-creation slice

A future ADR-creation slice is acceptable only if all criteria below are met:

1. Creates at most one successor draft/proposal artifact at the approved path.
2. Does not edit `docs/adr/adr.adr-template-contract.md` or any other existing `docs/adr/` source unless HERMES/USER separately approves that mutation.
3. Does not edit `docs/schemas/` JSON schema files.
4. Uses lifecycle status `draft` for the successor unless HERMES/USER approves a different lifecycle state.
5. Preserves the source file's observed `Accepted` status/casing as provenance rather than normalizing it.
6. Separates current content-schema fields from record-envelope metadata, sidecar/provenance evidence, generated projections, and migration/cutover authority.
7. States that `routing` is not current content-schema data and defaults it to sidecar/provenance preservation unless a later decision promotes another disposition.
8. States that `dcn` is unresolved namespace/control metadata and does not add it to schema authority.
9. States that `workflow_binding` is optional schema content and not operational workflow authority.
10. States that Markdown remains source/control for unmigrated records and that generated projections are not source authority without later cutover.
11. Includes explicit non-actions for supersession, source mutation, schema edits, JSON authority cutover, bulk migration, DB/storage authority, generated projection replacement, file moves/renames/deletes/archives/splits, status normalization, acceptance, activation, rejection, promotion, or demotion.
12. Includes closeout evidence proving the future slice did not mutate forbidden source/schema/evidence surfaces.

## Owner decisions required before later authority changes

HERMES/USER must separately decide all of the following before any change beyond proposal/draft creation:

- whether the old source is superseded, retained as accepted source/provenance, left with errata, or handled by another source-disposition path;
- whether a successor draft becomes `accepted` or `active`;
- whether source status casing is ever normalized, and where observed casing remains preserved;
- whether `routing` remains legacy/source-only, sidecar/provenance, workflow metadata, record-envelope metadata, or excluded;
- whether `dcn` becomes `metadata.record_id`, filename/title convention guidance, a separate metadata field, content data, or legacy provenance only;
- whether `workflow_binding` remains documentary content or gains operational semantics in a separate workflow authority slice;
- whether a later schema-change slice wraps/replaces/retires `adr.schema.json` or reconciles `adr-active.schema.json`;
- whether JSON authority cutover occurs for any record, and where authoritative JSON records live.

## Explicit exclusions for this successor-planning brief

This brief does not authorize:

- creating the successor ADR draft;
- editing existing `docs/adr/` files;
- editing `docs/schemas/`;
- changing source status or casing;
- supersession, acceptance, activation, rejection, promotion, demotion, or lifecycle transition;
- file moves, renames, deletes, archives, or splits;
- JSON conversion, generated projection creation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover;
- treating `routing`, `dcn`, or `workflow_binding` beyond the boundaries stated above as current operational authority.

## Recommended next transition

If HERMES/USER accepts this planning brief, the next bounded action should be an ATHENA-owned ADR-creation/drafting slice for one successor draft, still with no existing source/schema mutation.

Suggested next slice name:

```text
adr-template-schema-contract-successor-draft-slice-11
```

Suggested output path for that later slice:

```text
docs/adr/adr.adr-template-schema-contract.<YYYYMMDD.HHMMSSZ>.draft.md
```

HERMES/USER may instead choose a lower-risk errata/reconciliation note or stop with this plan.

## Closeout validation expectations

ATHENA/HERMES closeout for this planning slice should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result: no `docs/adr/`, `docs/schemas/`, or dry-run evidence mutation, and clean whitespace validation.
