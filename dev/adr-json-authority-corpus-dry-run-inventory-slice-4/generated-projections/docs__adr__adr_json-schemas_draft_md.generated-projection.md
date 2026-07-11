<!-- GENERATED SLICE 4 DRY-RUN PROJECTION EVIDENCE: non-authoritative; not ADR source. -->
# Slice 4 Projection Evidence: docs/adr/adr.json-schemas.draft.md

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
      "a reviewer can tell that the namespace holds schemas only",
      "the UI/core concept remains defined elsewhere",
      "workflow UI can consume the namespace without being defined by it",
      "schema/contract validation remains separate from UI architecture decisions"
    ],
    "consequences": "- schema and contract work stays separate from UI/core design\n- the shared UI/core ADR can remain renderer-agnostic\n- workflow UI can consume schemas without becoming the schema authority\n- future tooling can validate against one schema namespace",
    "decision": "Adopt a JSON schemas namespace for the UI/core family that holds schemas and contracts only.\n\nThe JSON schemas namespace:\n- defines machine-readable shapes and contracts\n- supports the shared UI/core family without replacing it\n- may be referenced by workflow UI or renderer layers\n- does not define the UI concept itself\n\nThe JSON schemas namespace does not cover:\n- the UI/core domain model\n- rendering implementation\n- marshalling or unmarshalling\n- framework choices\n- transport or runtime internals",
    "normalized_status_candidate": "draft",
    "observed_status_text": "draft",
    "status_missing": false,
    "title": "ADR 20260702.213000Z: JSON Schemas Namespace"
  },
  "conversion_completed_as_authoritative_record": false,
  "corpus_dry_run": true,
  "cutover_authorized": false,
  "database_authority": false,
  "entry_type": "adr_source_candidate",
  "object_type": "AdrJsonAuthorityCorpusDryRunCandidate",
  "outcome": "candidate_projectable_pending_review",
  "reviewed_inventory": {
    "authority_effect": "candidate",
    "automatic_conversion_eligibility_candidate": true,
    "category_candidate": "template_schema_contract",
    "disposition_candidate": "json_authority_candidate",
    "exclusion_blocking_reasons": [],
    "owner_domain_review_flags": {
      "domain_review_required": false,
      "manual_review_required": false,
      "owner_review_required": false
    }
  },
  "schema_change": false,
  "slice_name": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "source_hash": "c95dfb0928ba1398eb058a7bb16b21f2dad77f4116169cbcc8075fb5186c2df5",
  "source_mutation": false,
  "source_path": "docs/adr/adr.json-schemas.draft.md"
}
```
