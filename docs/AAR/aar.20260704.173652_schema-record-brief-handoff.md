# AAR 20260704.173652: Schema-record brief handoff

## Scope

ATHENA reconciled KOIOS, HERMES, and VULCAN review comments for the schema-base pre-Vulcan slice and produced a bounded implementation brief.

## What happened

- Seeded provenance/evidence metadata in `docs/adr/adr.schema-base.md`.
- Corrected `origin.method` semantics in `docs/plans/schema-base-adr-records-workplan.md`.
- Clarified editable projection/source-of-truth semantics until a separate schema-backed JSON source record exists.
- Tightened projection requirements in `docs/schemas/schema.record-base.json`.
- Reconciled `RejectedMarkdown` wording in `docs/schemas/adr-draft.schema.json`.
- Drafted `docs/plans/implementation-brief.20260704.172632_schema-record-base.md` for VULCAN.

## Process issues

- Reviews arrived through intercom messages while the checkout also had unrelated dirty VULCAN-owned GraphRAG implementation files.
- The schema files remain untracked, so commit/staging separation remains a coordination issue.
- The ADR Markdown embeds metadata but does not yet have a separate schema-backed JSON source record, requiring explicit projection/source-of-truth caveats.

## Proposed follow-up improvements

- Use worktree isolation or explicit staging separation before VULCAN implements the schema-record base slice.
- Preserve validator command output in future AARs when making durable validation claims.
- Consider adding a concrete JSON source-record artifact in a later slice if Markdown projections are expected to cite `schema_record` as source of truth.

## Candidate ADR or implementation topics

- Schema-record base implementation under `src/python/projectkoios/bootstrap/schema_records/`.
- Local JSON Schema registry/resolver for `https://projectkoios.local/schemas/<filename>`.
- Future source-record artifact convention for schema-backed Markdown projections.

## Current status

The schema-record base slice has an implementation-ready draft brief. Implementation remains VULCAN-owned and should wait for worktree/commit separation from concurrent GraphRAG changes.
