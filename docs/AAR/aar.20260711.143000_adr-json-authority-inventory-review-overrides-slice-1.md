# AAR 20260711.143000: ADR JSON authority inventory review/overrides slice 1

## Scope

VULCAN implementation of `adr-json-authority-inventory-review-overrides-slice-1` from ATHENA brief, KOIOS recommendations, HERMES decision, and Slice 0 inventory evidence.

## What happened

- Implemented a deterministic review-only override runner for Slice 0 ADR inventory evidence.
- Generated override evidence under `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Added tests for authority-forward downgrade behavior, domain/product review overrides, source/provenance overrides, messy canary recommendation, stable regeneration, valid artifacts, and no DB files.
- Validated tests, Python policy, JSON evidence syntax, no DB files, source/schema hash stability, evidence hash stability, and diff whitespace.

## Process issues

- Slice 0 labels were intentionally broad and authority-forward. Slice 1 had to turn those labels into safer candidate-only planning labels before any later conversion step can safely consume the inventory.
- The override code encodes KOIOS recommendations as deterministic rules. HERMES/USER review is still required because these are candidate evidence, not final per-file authority decisions.

## Proposed follow-up improvements

- If HERMES/USER accepts these overrides, a later slice can use the reviewed inventory as input to a messy canary plan.
- If many override rules change during review, consider a review-owned override table artifact rather than hard-coded deterministic rules.

## Candidate ADR or implementation topics

- Durable override table format for future ADR inventory reviews.
- Messy canary implementation brief using `docs/adr/adr.schema-base.md` as primary candidate if accepted by HERMES/USER.

## Current status

Implemented and validated. Awaiting HERMES/USER review.
