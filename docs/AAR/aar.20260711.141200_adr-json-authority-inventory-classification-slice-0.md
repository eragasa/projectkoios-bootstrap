# AAR 20260711.141200: ADR JSON authority inventory/classification slice 0

## Scope

VULCAN implementation of `adr-json-authority-inventory-classification-slice-0` from the accepted JSON-authority direction, HERMES acceptance, ATHENA brief, and HERMES implementation decision.

## What happened

- Implemented a deterministic review-only ADR Markdown inventory runner.
- Generated inventory evidence under `dev/adr-json-authority-inventory-classification-slice-0/`.
- Added tests covering review-only manifest markers, required per-file fields, status preservation, index/control file classification, stable regeneration, source non-mutation assumptions, and no database files.
- Validated tests, Python policy, JSON evidence syntax, no DB files, source/schema hash stability, evidence hash stability, and diff whitespace.

## Process issues

- `docs/adr/adr.json-authoritative-adr-store.draft.md` was already modified in the dirty tree as an authorizing artifact. The validation report therefore needed to distinguish existing dirty authorizing state from mutation caused by inventory generation.
- Heuristic classification is intentionally conservative but still may produce candidate labels that require HERMES/USER review before any authority-changing step.

## Proposed follow-up improvements

- HERMES/USER should review `source-inventory.json` before any conversion or authority transition.
- If the inventory vocabulary is accepted, a later slice can add richer category rules or explicit override files, still without mutating ADR sources.

## Candidate ADR or implementation topics

- Review/acceptance workflow for inventory classification manifests.
- Explicit override mechanism for category/disposition candidates before corpus conversion.

## Current status

Implemented and validated. Awaiting HERMES/USER review.
