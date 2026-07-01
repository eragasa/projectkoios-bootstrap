# AAR 20260701.125559: Role prose pruning

## Scope

Reduced duplicate harness-role prose in the bootstrap README and AGENTS file.

## What happened

Replaced the bootstrap README harness table with a pointer to `docs/agent-charter.md` and trimmed the top-level AGENTS harness summary so the charter is the canonical routing source.

## Process issues

- Role language had accumulated in multiple bootstrap docs.
- The charter needed to remain the single source of routing truth.

## Proposed follow-up improvements

- Prefer pointers over repeated role tables in bootstrap-facing docs.
- Keep the charter as the only place that defines the canonical split.

## Candidate ADR or implementation topics

- Canonical-doc precedence policy for bootstrap documentation.

## Current status

Complete.
