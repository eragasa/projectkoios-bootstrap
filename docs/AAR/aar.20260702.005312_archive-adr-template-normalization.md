# AAR 20260702.005312: Archive ADR Template Normalization

## Scope
Normalized the archived ADR set under `docs/archive/architecture/adr/` to a template-compatible render shape.

## What happened
Each archived ADR now has a standardized front matter-like Markdown wrapper with the canonical ADR sections, a `## links` section, and the original historical text preserved below `---` under `## original`.

## Process issues
This was a broad mechanical rewrite, so future passes should use a script rather than manual edits.

## Proposed follow-up improvements
If the archived ADRs need stronger machine readability later, consider generating the wrapper instead of storing it inline.

## Candidate ADR or implementation topics
- Generated archived-ADR render pipeline
- Whether `## original` should become a formal archive convention

## Current status
Archived ADRs are now template-compatible while preserving the original text verbatim below the normalized render.
