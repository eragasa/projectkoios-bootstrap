```json
{
  "title": "HERMES decision: ADR JSON authority inventory review/overrides slice 1",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.142700Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-inventory-review-overrides-slice-1",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.142700: ADR JSON authority inventory review/overrides slice 1

## Decision

HERMES approves `adr-json-authority-inventory-review-overrides-slice-1` for VULCAN implementation.

## Rationale

The accepted Phase 0 inventory surfaced authority-forward candidate labels and under-flagged domain/category ambiguity. KOIOS produced concrete override recommendations. A review-only override evidence slice is the smallest safe next step before any messy canary or conversion consumes the inventory.

## Required inputs

- `dev/adr-json-authority-inventory-classification-slice-0/`
- `docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md`
- `workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md`
- `docs/reviews/hermes-acceptance.20260711.142000_adr-json-authority-inventory-classification-slice-0.md`

## Approved implementation direction

- Produce review-only override evidence under `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Review every `proposed_authority` / `json_authority_candidate` entry.
- Add `candidate_only: true` to reviewed entries.
- Prefer safer `authority_effect: candidate` over `proposed_authority` unless explicitly justified as a candidate label only.
- Apply KOIOS recommendations for domain-review files, source/provenance drafts, mixed architecture/policy/template documents, and exclusions from automatic conversion.
- Record original values, reviewed values, changed flag, rationale, and source basis for each keep/override decision.
- Recommend messy canary candidate(s), with `docs/adr/adr.schema-base.md` as the primary KOIOS recommendation unless implementation evidence suggests otherwise.

## Boundaries

Do not mutate `docs/adr/`, change `docs/schemas/`, create authoritative JSON ADR records, convert Markdown ADRs to JSON records, create replacement projections, move/rename/delete/archive files, normalize source statuses, mark drafts superseded, add database/storage authority, or commit mutable `.sqlite`/`.db` files.

## Required validation

Validate all generated JSON evidence, source/schema non-mutation, no DB files under evidence path, deterministic/stable output where practical, focused tests/Python policy/type checks if code changes, and `git diff --check`.
