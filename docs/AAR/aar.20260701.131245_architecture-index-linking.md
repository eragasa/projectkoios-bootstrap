# AAR 20260701.131245: Architecture index linking

## Scope

Rewrote the bootstrap architecture index note and linked the new `architecture.*` note set back to it.

## What happened

Replaced `docs/architecture.00.md` with a namespace index for bootstrap architecture notes and updated the workspace/repo projection notes to point back to `[[architecture.00]]`.

## Process issues

- The architecture notes needed a single Obsidian-style entry point.
- The note set had grown faster than the index structure.

## Proposed follow-up improvements

- Keep new architecture notes linked from `architecture.00` at creation time.
- Consider a lightweight note template for future `architecture.*` files.

## Candidate ADR or implementation topics

- Architecture note template and naming policy.

## Current status

Complete.
