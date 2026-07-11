```json
{
  "title": "Implementation reality review: ADR template/schema contract successor planning slice 10",
  "artifact_type": "implementation-reality-review",
  "status": "review-complete-implementation-feasible-with-minor-watchpoints",
  "datetime": "20260711",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-successor-planning-slice-10",
  "reviewed_artifact": "docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md",
  "requested_by": "HERMES",
  "current_head": "571bd7b6 Route template schema contract successor planning to Athena"
}
```

# Implementation reality review: ADR template/schema contract successor planning slice 10

## Verdict

VULCAN verdict: **implementation-feasible / no blocking implementation objection**, with minor watchpoints.

ATHENA's successor-planning brief is consistent with current schemas/tooling and with VULCAN's Slice 6 implementation-reality check. It correctly distinguishes current ADR content schema from the draft record envelope, keeps Markdown source/control separate from generated projection evidence, treats `routing` and `dcn` as non-content-schema fields, bounds `workflow_binding`, and defers all source/schema/migration side effects to later explicit HERMES/USER approvals.

## Reviewed artifact

- `docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md`

Current repository state reported by HERMES and observed locally:

- HEAD: `571bd7b6 Route template schema contract successor planning to Athena`
- ATHENA output is working-tree, not HERMES-accepted yet.
- Relevant dirty files observed: `docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md`, `workspaces/athena/state.md`, `workspaces/athena/active.md`.

## Implementation reality findings

### Content schema vs record envelope

The brief's separation is consistent with current repository state.

- `docs/schemas/adr.schema.json` is a flat ADR content-shape schema. It includes the current content fields and optional `links` / `workflow_binding`, and does not include envelope metadata such as hashes, projections, source artifacts, or migration conflict state.
- `docs/schemas/schema.record-base.json` is a draft `metadata` + `content` envelope with `metadata.record_id`, schema identity/versioning, origin, domain, source artifacts, evidence, and projections.
- `docs/schemas/README.md` already states this layering and names `adr-active.schema.json` as a compatibility/reconciliation candidate rather than co-authority by implication.

Implementation constraint: a future successor draft can describe these layers, but must not imply that existing Python tooling has already migrated all ADR records to the base envelope.

### Markdown source/control vs generated projections

The brief's wording is consistent with current tooling.

- Current ADR conversion/control-surface code reads hand-authored Markdown as source input/evidence and writes generated JSON/projection evidence under `dev/`.
- Existing runners and evidence mark generated projections as non-authoritative evidence, with parse-back scoped to generated projection artifacts only.
- Existing tests protect source non-mutation and generated-only projection parse-back.

Implementation constraint: the future draft should keep the brief's language that Markdown remains source/control for unmigrated records and generated projections are not source authority without later cutover.

### `routing`

The brief is implementation-consistent.

- `docs/schemas/adr.schema.json` has no `routing` property and uses `additionalProperties: false`.
- `AdrMarkdownRecordParser`, conformance, bidirectional, Slice 3, and Slice 4 evidence preserve routing outside candidate/content records as sidecar/provenance where encountered.
- Tests assert `routing` is absent from conformed records/checkpoints/projection records and preserved outside schema where relevant.

Implementation constraint: future drafting should not call `routing` a current ADR content-schema field. Sidecar/provenance default is feasible.

### `dcn`

The brief is implementation-consistent.

- Current Python ADR conversion/storage/schema tooling does not implement `dcn`.
- `docs/schemas/adr.schema.json` has no `dcn` property.
- `schema.record-base.json` has `metadata.record_id`, which can satisfy current identity needs if/when envelope schemas are used, but that is not the same as implementing `dcn`.

Implementation constraint: the brief's proposed default is safe: treat `dcn` as unresolved namespace/control metadata and do not add it to schema authority in this planning/draft path.

### `workflow_binding`

The brief is implementation-consistent.

- `docs/schemas/adr.schema.json` contains optional `workflow_binding` schema content.
- Current Python ADR conversion/storage/control-surface code does not operationalize `workflow_binding` as Petri-net runtime, ADR lifecycle state, Operator Console state, or activation control.

Implementation constraint: future drafting should keep `workflow_binding` documentary/schema-supported unless a separate workflow authority slice gives it operational semantics.

### Side-effect boundaries

The future ADR-creation acceptance criteria are feasible and appropriately constrained.

The brief explicitly forbids or defers:

- editing `docs/adr/adr.adr-template-contract.md` or other existing ADR sources;
- editing `docs/schemas/` JSON schema files;
- source status normalization;
- supersession / acceptance / activation / lifecycle transition;
- generated projections, JSON conversion, generated projection replacement, migration, cutover, DB/storage authority;
- file moves/renames/deletes/archives/splits.

This matches implementation reality and should be retained for HERMES acceptance.

## Minor watchpoints / recommendations

1. **Future ADR filename should be checked against current ADR filename conventions before creation.** The suggested path `docs/adr/adr.adr-template-schema-contract.<YYYYMMDD.HHMMSSZ>.draft.md` appears plausible in current repository style, but the future slice should verify it against active naming/lifecycle guidance before writing.

2. **Do not overstate envelope implementation.** The brief correctly calls `schema.record-base.json` a draft record-envelope direction. Future drafting should preserve that wording and avoid implying that current ADR conversion/storage code universally emits `metadata` + `content` records.

3. **Keep `metadata.record_id` distinct from `dcn`.** The brief's `dcn` disposition references `metadata.record_id` / filename conventions for current identity needs. That is feasible, but future text should not silently define `dcn == metadata.record_id` without an explicit namespace/schema decision.

4. **Future draft creation is document-domain work, not VULCAN implementation.** No implementation change is needed for the successor-planning brief itself. If later schema/tooling changes are desired, they should be separate ATHENA/VULCAN-scoped slices.

## VULCAN recommendation to HERMES

HERMES can accept/package the ATHENA Slice 10 successor-planning brief from an implementation feasibility perspective, provided acceptance preserves the brief's proposal-only/no-side-effect boundaries and the minor watchpoints above.

## Read-only closeout

VULCAN did not mutate `docs/adr/` or `docs/schemas/` for this review. This review artifact is the only VULCAN-authored output from the check.

Observed commands:

```bash
git status --short --branch
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Results:

- branch status showed `master...origin/master [ahead 1]` with ATHENA working-tree files pending;
- `docs/adr`, `docs/schemas`, and Slice 4 evidence status check produced no output;
- `git diff --check` passed.
