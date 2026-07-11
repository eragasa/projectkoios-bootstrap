<!-- GENERATED SLICE 4 DRY-RUN PROJECTION EVIDENCE: non-authoritative; not ADR source. -->
# Slice 4 Projection Evidence: docs/adr/adr.adr-template-contract.md

## Projection metadata

- Slice name: adr-json-authority-corpus-dry-run-inventory-slice-4
- Authority mode: candidate evidence only; not repository authority
- Corpus dry run: true
- Bounded subset only: true
- Cutover authorized: false

```json adr-corpus-dry-run-candidate
{
  "authority_change": false,
  "authority_mode": "candidate-evidence-only-not-repository-authority",
  "blocked_from_authority_promotion": true,
  "bounded_subset_only": true,
  "bulk_migration": false,
  "candidate_only": true,
  "content_candidate": {
    "acceptance_criteria": [
      "New ADRs can be represented as JSON without losing any required data.",
      "The schema includes provenance, routing, the `dcn` field, and optional workflow-binding fields.- The schema enforces one architecture domain per ADR.",
      "Workflow-bound ADRs can render optional gate fields without losing schema consistency.",
      "A renderer can produce Markdown from the JSON object."
    ],
    "consequences": "- ADRs become machine-readable source artifacts.\n- Markdown can be generated from the same JSON in multiple styles.\n- Review and workflow tooling can validate a stable schema instead of prose\n  headings.\n- Future changes to ADR shape flow through one schema file.",
    "decision": "Adopt `docs/schemas/adr.schema.json` as the canonical ADR schema for\nthis repository and treat Markdown as a derived rendering of that JSON.\n\nThe schema should define the ADR content model, required provenance fields,\nstatus, routing, and the renderable decision sections.\nThe `workflow_binding` extension should stay optional and must point at\nexplicit ADR links when present.",
    "normalized_status_candidate": "accepted",
    "observed_status_text": "Accepted",
    "status_missing": false,
    "title": "ADR 20260701.131629: Canonical ADR proposal template"
  },
  "conversion_completed_as_authoritative_record": false,
  "corpus_dry_run": true,
  "cutover_authorized": false,
  "database_authority": false,
  "entry_type": "adr_source_candidate",
  "object_type": "AdrJsonAuthorityCorpusDryRunCandidate",
  "outcome": "projectable_candidate_blocked_pending_template_contract_and_status_review",
  "reviewed_inventory": {
    "authority_effect": "candidate",
    "automatic_conversion_eligibility_candidate": false,
    "category_candidate": "template_schema_contract",
    "disposition_candidate": "manual_review_required",
    "exclusion_blocking_reasons": [
      "manual_review_required",
      "status_casing_or_text_would_normalize"
    ],
    "owner_domain_review_flags": {
      "domain_review_required": false,
      "manual_review_required": true,
      "owner_review_required": true
    }
  },
  "schema_change": false,
  "slice_name": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "source_hash": "2876dfbe031105d383fa9e33cec7d5dd49cf569cea6f43eae59e8fa1da502895",
  "source_mutation": false,
  "source_path": "docs/adr/adr.adr-template-contract.md"
}
```
