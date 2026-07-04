# AAR 20260704.172155: Schema-base pre-Vulcan refinement

## Scope

ATHENA refined the schema-base ADR/workplan control surface for the current pre-Vulcan schema-record slice.

## What happened

- Settled the Markdown ingest open question by defining fatal errors versus deterministic `## Rejected` capture.
- Settled the first ADR-family schema composition strategy as JSON Schema `$ref` plus `allOf`, with a local schema registry fallback for project-local `$id` URLs.
- Updated `docs/adr/adr.schema-base.md`, `docs/plans/schema-base-adr-records-workplan.md`, and `docs/schemas/README.md` to agree on those decisions.
- Updated Athena `active.md` to mark current schema-base blockers as resolved for the pre-Vulcan slice.
- Local process check: ran `python -m json.tool` against edited JSON schema drafts during the session; command output was not preserved in this AAR as durable validation evidence.

## Process issues

- The working tree already contained substantial Vulcan-owned implementation changes and untracked schema artifacts. ATHENA avoided implementation files and limited edits to architecture/spec surfaces.
- Several schema files remain untracked, so normal `git diff` does not show their content changes unless added or inspected directly.

## Proposed follow-up improvements

- Prepare a separate Vulcan implementation brief from the now-settled schema-base slice.
- Have Hermes or the user decide when the untracked schema namespace migration should be staged/committed separately from Vulcan implementation work.

## Candidate ADR or implementation topics

- Schema-record base implementation slice under a bootstrap/schema-record package boundary.
- Local schema registry for resolving `https://projectkoios.local/schemas/<filename>` during validation.

## Current status

Pre-Vulcan schema-base design blockers are resolved for implementation-brief preparation in this slice. The next step is consistency review and implementation-brief preparation, not implementation from Athena.
