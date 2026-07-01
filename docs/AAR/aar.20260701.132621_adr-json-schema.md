# AAR 20260701.132621: ADR JSON schema

## Scope

Shifted the canonical ADR form from Markdown headings to a JSON schema.

## What happened

Added `docs/architecture/adr/adr.schema.json`, updated the active architecture note to treat JSON as the source of truth, revised the governing ADR, and switched the `create-adr` workflow to emit JSON ADR files.

## Process issues

No durable process issue observed.

## Proposed follow-up improvements

- Add a renderer or conversion command for JSON ADR → Markdown.
- Decide whether archived ADRs should be backfilled into JSON later.

## Candidate ADR or implementation topics

- ADR render pipeline and archive conversion.

## Current status

Canonical ADRs are now JSON-first.
