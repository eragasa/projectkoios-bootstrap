# AAR 20260711.144500: ADR JSON authority messy canary slice 2

## Scope

VULCAN implementation of `adr-json-authority-messy-canary-slice-2` from ATHENA brief, HERMES decision, reviewed inventory evidence, and KOIOS/HERMES watchpoints.

## What happened

- Implemented a deterministic one-source messy canary runner for `docs/adr/adr.schema-base.md`.
- Generated evidence under `dev/adr-json-authority-messy-canary-slice-2/`.
- Preserved missing Markdown status as missing while keeping embedded JSON status in sidecar/provenance.
- Reported `conversion_candidate_blocked_pending_review` due missing status and schema/implementation-contract ambiguity.
- Added focused tests for missing-status preservation, sidecar provenance, source non-mutation, no projection/DB files, stable generation, and JSON artifacts.

## Process issues

- The source contains embedded JSON with `status: draft`, but the approved watchpoint required missing Markdown status preservation. The implementation therefore treats embedded status as provenance only, not as a lifecycle status candidate.
- Projection was omitted to avoid implying a schema-valid ADR record or inventing status for a generated surface.

## Proposed follow-up improvements

- HERMES/USER should review whether missing-status messy canaries should remain blocked or receive a manual reviewed status in a later authority-changing plan.
- If more messy canaries are approved, factor shared evidence helpers while keeping per-source ambiguity rules explicit.

## Candidate ADR or implementation topics

- Reviewed-status override workflow for missing-status ADR sources.
- Explicit policy for embedded JSON metadata versus Markdown lifecycle status during JSON-authority migration.

## Current status

Implemented and validated. Awaiting HERMES/USER review.
