```json
{
  "title": "KOIOS provenance review: ADR JSON authority inventory/classification slice 0",
  "artifact_type": "provenance-review",
  "status": "reviewed-with-watchpoints",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-inventory-classification-slice-0",
  "reviewed_report": "docs/implementation/adr-json-authority-inventory-classification-slice-0.20260711.141200.md",
  "evidence_dir": "dev/adr-json-authority-inventory-classification-slice-0/"
}
```

# KOIOS provenance review: ADR JSON authority inventory/classification slice 0

## Verdict

Reviewed with watchpoints.

The slice is provenance-adequate as a **review-only inventory/classification evidence package**. It is not adequate as a direct basis for conversion or authority cutover without HERMES/USER review of classifications and likely override/correction of several category/domain-review candidates.

## Sources reviewed

- `docs/implementation/adr-json-authority-inventory-classification-slice-0.20260711.141200.md`
- `docs/AAR/aar.20260711.141200_adr-json-authority-inventory-classification-slice-0.md`
- `docs/plans/implementation-brief.20260711.140700_adr-json-authority-inventory-classification-slice-0.md`
- `docs/adr/adr.json-authoritative-adr-store.draft.md`
- `workspaces/koios/working/provenance-risk.20260711_adr-json-authority-mass-conversion.md`
- `workspaces/koios/working/classification-proposal.20260711_adr-hierarchy-rationalization.md`
- `dev/adr-json-authority-inventory-classification-slice-0/manifest.json`
- `dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json`
- `dev/adr-json-authority-inventory-classification-slice-0/classification-summary.json`

## Adequate provenance findings

- Evidence is clearly marked review-only: `authority_change: false`, `review_only: true`, `source_mutation_allowed: false`, `schema_change_allowed: false`, and `database_authority: false`.
- Per-file source hashes are recorded.
- Observed status text/casing is preserved separately from normalized status candidates.
- Missing/non-canonical status cases are flagged for manual review.
- `docs/adr/README.md` is classified as `index_or_control_surface`, not an ADR authority candidate.
- Candidate categories/dispositions/authority effects are explicit machine-readable fields.
- Evidence directory contains only JSON artifacts; no `.sqlite` or `.db` files were found under the evidence path.
- Implementation report records validation for JSON validity, no DB files, source/schema hash stability, deterministic evidence hash, tests, Python policy, and diff check.
- Report distinguishes pre-existing dirty `docs/adr/adr.json-authoritative-adr-store.draft.md` authorizing state from inventory generation.

## Watchpoints / provenance concerns before next slice

### 1. Candidate labels are too authority-forward for heterogeneous corpus

`classification-summary.json` reports 39 files as:

- `disposition_candidate: json_authority_candidate`
- `authority_effect: proposed_authority`
- `automatic_conversion_eligibility_candidate: true`

This is acceptable only if read as review-only candidate metadata. It should not be treated as HERMES/USER acceptance that those 39 files are ready for conversion or JSON authority.

KOIOS recommends HERMES/USER require an explicit override/review step before any conversion slice consumes `proposed_authority` or `json_authority_candidate` values.

### 2. Product/future-system and domain-review ambiguity appears under-flagged

KOIOS prior classification flagged several files as likely product/future-system or domain-review candidates. The generated inventory does not set `domain_review_required` for examples such as:

- `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md`
- `docs/adr/adr.agent-windows-on-message-triggers.draft.md`
- `docs/adr/adr.ui-core.draft.md`
- `docs/adr/adr.workflow-ui.draft.md`

These may still be convertible as records later, but should not become bootstrap JSON authority without owner/domain review.

### 3. Architecture/policy/template distinctions need human review

The generated category counts are heavily concentrated in `template_schema_contract` and `implementation_workflow_support`, with only one `architecture_blueprint` and no `product_future_system_draft` category in the summary. This likely underrepresents the mixed nature KOIOS observed in `docs/adr/`.

Before conversion, HERMES/ATHENA should review whether architecture blueprints, policy/process docs, template/schema contracts, and implementation workflow supports need distinct authority/disposition handling.

### 4. Manifest validation summary says pending

`manifest.json` has `validation_command_summary` entries marked `pending closeout validation`, while the implementation report records completed validation. This is not a blocker for review-only evidence, but it is a traceability mismatch. If this manifest becomes the source for later automation, it should be updated or a later accepted review should explicitly cite the implementation report as closeout validation.

### 5. Classification evidence is not conflict/lossiness evidence

This slice inventories and classifies; it does not prove Markdown-to-JSON conversion, unsupported-field preservation, projection equality, or source/projection conflict behavior. It must not be treated as satisfying mass-conversion gates beyond Phase 1 inventory/classification.

## Boundary confirmation

KOIOS found no evidence in the reviewed artifacts of:

- source ADR mutation by the inventory generator;
- `docs/schemas/` mutation;
- file moves, renames, deletes, or archives;
- source status normalization;
- draft supersession;
- authoritative JSON ADR records;
- corpus conversion;
- generated Markdown projection replacement;
- database/storage authority;
- committed mutable database files under the evidence path.

## KOIOS recommendation

Accept this slice only as review-only inventory/classification evidence with watchpoints.

Before any conversion or authority cutover:

1. HERMES/USER should review and approve or correct category/disposition/authority-effect candidates.
2. Add or approve an override mechanism for domain-review and mixed-document classifications.
3. Treat all `proposed_authority` and `json_authority_candidate` values as candidate labels, not final authority.
4. Require a conversion/canary slice to prove unsupported-field preservation, sidecar behavior, projection equality, and conflict/lossiness reporting before mass conversion.
