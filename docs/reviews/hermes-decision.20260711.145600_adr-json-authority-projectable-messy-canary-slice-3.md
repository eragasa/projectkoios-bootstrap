```json
{
  "title": "HERMES decision: ADR JSON authority projectable messy canary slice 3",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.145600Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-projectable-messy-canary-slice-3",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md",
  "provenance_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.145600: ADR JSON authority projectable messy canary slice 3

## Decision

HERMES approves `adr-json-authority-projectable-messy-canary-slice-3` for VULCAN implementation.

## Rationale

ATHENA revised the implementation brief to align with KOIOS next-proof input and selected exactly one source: `docs/adr/adr.adr-template-contract.md`.

This is the appropriate next bounded proof point because it is messy but likely projectable: it has an observed `## Status` value of `Accepted`, Slice 1 reviewed it as `template_schema_contract` / `manual_review_required`, and it can exercise projection/parse-back and status-casing preservation without the missing-status blocker from Slice 2 or the product/training ambiguity of the deferred agent-production-trace ADR.

## Approved implementation direction

- Use exactly one source: `docs/adr/adr.adr-template-contract.md`.
- Use reviewed inventory/override evidence from `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Use Slice 2 acceptance/watchpoints from `docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md`.
- Produce candidate-only object, conversion, projection, parse-back, conflict/lossiness, and sidecar/provenance evidence under `dev/adr-json-authority-projectable-messy-canary-slice-3/`.
- Preserve observed status/casing `Accepted` separately from any normalized candidate such as `accepted`.
- Keep template/schema-contract ambiguity and manual-review blockers explicit.
- Treat all generated projection/parse-back artifacts as evidence only, not source authority.

## Boundaries

Do not mutate `docs/adr/`, change `docs/schemas/`, convert or project any file other than `docs/adr/adr.adr-template-contract.md`, create authoritative JSON ADR records, create replacement projections, move/rename/delete/archive files, normalize source status in source Markdown, mark drafts superseded, perform authority cutover, add database/storage authority, commit mutable `.sqlite`/`.db` files, or begin corpus conversion.

## Required post-implementation review

Before HERMES final acceptance, require:

- KOIOS provenance review focused on status-casing preservation, template-contract/manual-review blockers, projection safety, and evidence-vs-authority clarity.
- ATHENA architecture/conformance review focused on implementation-brief conformance and no-authority boundaries.

## Required validation

Validate source/schema non-mutation, exactly-one-source proof, JSON evidence validity, no DB files under the Slice 3 evidence path, generated projection only under the Slice 3 `dev/` path if produced, tests/type checks/Python policy if code changes, and `git diff --check` clean.
