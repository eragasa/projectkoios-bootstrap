# AAR 20260701.122628: Docs architecture canonicalization

## Scope

Updated the bootstrap architecture index and docs architecture note to make the documentation system's canonical active file and archive rule explicit.

## What happened

- Marked `docs/architecture/architecture.docs.md` as the stable docs architecture key.
- Added `docs/architecture/architecture.00.md` guidance pointing to the canonical docs architecture note.
- Reaffirmed portable docs modeling for Python 3, TypeScript, and Rust.
- Refreshed Graphify after the doc edits.

## Process issues

- A transient filename mismatch briefly appeared while normalizing the docs architecture file path.

## Proposed follow-up improvements

- Keep the canonical docs architecture filename stable and archive only timestamped replacements.

## Candidate ADR or implementation topics

- None.

## Current status

- Docs architecture references now point at `architecture.docs.md`.
- Graphify was updated after the edit.
