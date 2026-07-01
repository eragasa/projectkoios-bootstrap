# AAR 20260701.140312: Architecture file protection

## Scope

Added explicit protection rules for `docs/architecture*.md` files.

## What happened

Updated the agent charter, architecture template instructions, and architecture
index note so architecture files are treated as Hermes-only and require explicit
Zeus permission for edits.

## Process issues

- Architecture files needed a stronger access-control convention.
- The protection rule needed to live in both the charter and the formatting
template.

## Proposed follow-up improvements

- Add the protection rule to any future architecture note template.
- Consider a validation check that warns if a non-Hermes harness proposes an
architecture-file edit.

## Candidate ADR or implementation topics

- Architecture-file edit guardrails.

## Current status

Complete.
