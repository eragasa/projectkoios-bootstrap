```json
{
  "title": "KOIOS next proof input: ADR semantic rationalization after Slice 4",
  "artifact_type": "provenance-next-proof-input",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "semantic review of selected ADR/control-surface entries after accepted Slice 4"
}
```

# KOIOS next proof input: ADR semantic rationalization after Slice 4

## Authority boundary

This note is KOIOS provenance input only. It does not authorize source mutation, status changes, supersession, file moves/renames, schema changes, JSON authority, or migration.

The next slice should review whether selected ADR/control-surface entries still make semantic sense as current/project authority. It should be independent of conversion mechanics and should avoid deciding authority silently.

## Recommended slice shape

Recommended slice name:

```text
adr-semantic-rationalization-six-entry-slice-5
```

Recommended purpose:

- inspect the accepted Slice 4 six-entry subset as documents, not as conversion candidates;
- classify each entry's semantic role in current repository truth: current authority, candidate/draft, provenance/source draft, template/schema/control surface, or index/control surface;
- identify conflicts, stale authority claims, supersession candidates, and required owner decisions;
- produce a review-only semantic disposition table for ATHENA/HERMES decision-making;
- do not mutate files or normalize statuses.

## Recommended subset

Use the same six Slice 4 entries as the primary review subset. Do not add product/future-system ADRs in this slice.

```text
docs/adr/README.md
docs/adr/adr.petrinet.20260705.132740Z.md
docs/adr/adr.adr-template-contract.md
docs/adr/adr.json-schemas.draft.md
docs/adr/adr.schema-base.md
docs/adr/adr.adr-lifecycle.draft.md
```

This is the same membership as Slice 4, reordered for semantic review.

## Recommended ordering and rationale

### 1. `docs/adr/README.md`

Review first because it states the directory-level control rule: ADRs record bounded decisions; architecture blueprints, policies, templates, implementation reports, and process-chain records belong on their own surfaces. This is the semantic yardstick for the rest of the slice.

Expected semantic disposition: `index_control_surface`, not an ADR decision.

Watchpoints:

- Do not treat README as an ADR record.
- Do not let README wording silently move files or supersede existing ADRs.
- Use it only as local control-surface evidence for classification.

### 2. `docs/adr/adr.petrinet.20260705.132740Z.md`

Review next as the clearest current/accepted decision in the subset.

Expected semantic disposition: likely `current_decision_record` / `accepted_authority_candidate`, bounded to Petri-net definition/marking/binding/runtime separation.

Watchpoints:

- Confirm it is still consistent with accepted Petri-net follow-on and live workflow inspectability work.
- Do not extend it into product workflow engine, Operator Console, or current queue/runtime authority unless current architecture/implementation evidence supports that.
- Accepted source status does not imply JSON authority or migration readiness.

### 3. `docs/adr/adr.adr-template-contract.md`

Review after a clean current decision because it is accepted-like but semantically mixed: decision record plus template/schema contract.

Expected semantic disposition: likely `template_schema_contract_with_decision_status`, requiring ATHENA/HERMES review before treating it as ordinary current ADR authority.

Watchpoints:

- Preserve observed status casing `Accepted`; do not normalize.
- Determine whether its claims about `docs/schemas/adr.schema.json` as canonical remain current repo truth after later JSON-authority/bidirectional-object work.
- Distinguish template contract, schema authority, renderer behavior, and ADR source-of-truth claims.
- Do not silently supersede it with later draft architecture or dev evidence.

### 4. `docs/adr/adr.json-schemas.draft.md`

Review as a draft schema-namespace decision that Slice 4 treated as projectable but incomplete.

Expected semantic disposition: likely `draft_schema_namespace_candidate` or `schema/template_contract_draft`, not current authority unless separately accepted.

Watchpoints:

- It is UI/core-family schema namespace content, not necessarily ADR-store schema authority despite name overlap.
- Check for possible product/UI domain leakage.
- Its `routing` says proposed; do not promote to current authority.
- The source contains omitted sections in Slice 4 evidence; semantic review must inspect full source, not reduced candidate projection.

### 5. `docs/adr/adr.schema-base.md`

Review as a high-risk schema/base-class concept with missing top-level ADR status.

Expected semantic disposition: likely `schema_family_concept_or_architecture_blueprint_pending_status_review`, not current ADR authority.

Watchpoints:

- Missing status remains missing; do not infer draft/accepted/active.
- It appears to describe schema-family architecture, base record contracts, and projection semantics; this may belong in architecture/schema documents rather than ADR authority.
- Check relationship to later architecture surfaces and ADR object work before promotion.
- If retained, it may need explicit status/disposition authority from ATHENA/HERMES, not a conversion-derived decision.

### 6. `docs/adr/adr.adr-lifecycle.draft.md`

Review last because it should be compared against the accepted lifecycle/naming consolidation ADR and treated as source/provenance unless promoted.

Expected semantic disposition: `source_provenance_draft_for_accepted_lifecycle_adr`, not current authority.

Watchpoints:

- Compare against `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` as controlling accepted/current lifecycle authority.
- Do not supersede, delete, archive, or mark rejected by implication.
- Identify which claims, if any, remain useful as detailed guidance requiring separate promotion.
- Preserve provenance relationship to accepted lifecycle/naming ADR.

## Consult-only provenance sources

The semantic review should consult these sources without adding them as candidate review entries unless HERMES/USER revises scope:

### Repository policy/control

- `AGENTS.md` — repo artifact model, ADR convention, role ownership, and document-domain rules.
- `docs/adr/README.md` — ADR directory boundary and migration note.
- `docs/architecture/architecture.adr.00.md` — ADR vs architecture document control surface.
- `docs/policies/architecture.adr.lifecycle.md` — lifecycle/status consumption aid.

### Current/accepted authority and prior reconciliation

- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` — accepted/current lifecycle and naming consolidation.
- `docs/adr/adr.petrinet.20260705.132740Z.md` — accepted Petri-net separation decision.
- `workspaces/koios/working/provenance-audit.20260709T012117Z_adr-lifecycle-followon-reconciliation.md` — lifecycle/naming pointer reconciliation audit.
- `workspaces/koios/working/provenance-note.20260705T100913Z_petrinet-followup-package.md` — Petri-net follow-up provenance.

### JSON authority / object migration context

- `docs/adr/adr.json-authoritative-adr-store.draft.md` — staged JSON authority direction.
- `docs/architecture/architecture.adr-bidirectional-objects.md` — bidirectional object/projection semantics if present/current.
- `docs/architecture/architecture.json-adr-storage-topology.md` — JSON storage topology and authority boundaries.
- `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md` — ATHENA intake for JSON↔Markdown objects.
- `workspaces/koios/working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`.
- `workspaces/koios/working/provenance-risk.20260711_adr-json-authority-mass-conversion.md`.
- `workspaces/koios/working/classification-proposal.20260711_adr-hierarchy-rationalization.md`.

### Slice evidence to use as provenance only

- `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/` — accepted candidate-only dry-run evidence, especially omitted/source-preserved sections.
- `docs/reviews/hermes-acceptance.20260711.154100_adr-json-authority-corpus-dry-run-inventory-slice-4.md` — accepted bounded scope and non-authorizations.
- `workspaces/koios/working/provenance-review.20260711_adr-json-authority-corpus-dry-run-inventory-slice-4.md` — KOIOS review and residual watchpoints.

## Desired output artifact

Recommended output path:

```text
docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md
```

or, if ATHENA owns the review artifact:

```text
docs/plans/semantic-rationalization-intake.20260711_adr-six-entry-slice-5.md
```

Expected fields/table columns:

- source path;
- observed status text and casing, or explicit missing status;
- file role: ADR decision / draft / source-provenance / template-contract / schema-architecture / index-control;
- current authority assessment: current authority, candidate authority, provenance-only, control surface, supersession-review-needed, or not-authority;
- controlling/related authority consulted;
- conflicts or stale claims;
- recommended next action: keep, review, reconcile, promote proposal, supersession candidate, move/classify later;
- required owner decision;
- explicit non-authority marker.

## Semantic review watchpoints

- Distinguish live repo truth from draft/provenance/control artifacts.
- Do not treat conversion evidence or generated projections as semantic authority.
- Do not infer current authority from file presence, filename, or parseability.
- Do not infer status where status is missing.
- Preserve status casing exactly when quoting observed source status.
- Do not silently mark drafts superseded, rejected, accepted, or active.
- Do not collapse template/schema contracts into ordinary ADR decisions without owner review.
- Do not collapse architecture blueprints into ADR decisions.
- Do not treat `docs/adr/README.md` as an ADR record.
- Do not treat `adr.adr-lifecycle.draft.md` as current authority over accepted lifecycle/naming ADR.
- Do not treat `adr.json-schemas.draft.md` as ADR JSON authority merely because it was a clean conversion candidate; it appears to concern a JSON schemas namespace for UI/core-family shapes.
- Do not let accepted `adr.petrinet...` become broader workflow/product authority than its bounded decision text supports.
- Record when a document may be stale but leave the actual disposition to ATHENA/HERMES/USER.

## Recommended non-authorizations for the brief

This semantic rationalization slice must not authorize:

- edits to any `docs/adr/` source;
- edits to `docs/schemas/`;
- status normalization;
- status changes;
- accepted/active/draft/rejected/superseded transitions;
- moving, renaming, deleting, archiving, or splitting files;
- replacing hand-authored Markdown with generated projections;
- JSON authority cutover or authoritative JSON ADR records;
- product/domain authority decisions;
- database/storage authority;
- treating `dev/` evidence as durable authority;
- implementation work beyond producing the semantic review artifact.

## KOIOS recommendation

Proceed with the six-entry subset, but reorder it as above for semantic reasoning. The next useful state is a review-only semantic disposition matrix that separates:

1. directory/control-surface truth (`README.md`),
2. clear accepted/current decision truth (`adr.petrinet...`),
3. accepted-like template/schema contract ambiguity (`adr.adr-template-contract.md`),
4. draft schema namespace candidate (`adr.json-schemas.draft.md`),
5. missing-status schema/base-class architecture concept (`adr.schema-base.md`), and
6. source/provenance draft status (`adr.adr-lifecycle.draft.md`).

The slice should produce decision input for ATHENA/HERMES, not make the semantic authority decisions itself.
