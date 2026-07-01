---
status: draft
date: 20260701.131629Z
back_to: architecture.00
---

# ADR template

## Purpose

This is the active bootstrap architecture note for the canonical ADR proposal
template.

## Scope

It governs the reusable proposal template in `docs/templates/ADR.proposal.template.md`
and the `create-adr` workflow that emits new ADR drafts.

## Control

This note is controlled by:

- `docs/architecture/adr/adr.20260701.131629_adr-template-contract.md`

## Template shape

The canonical template uses these sections, in order:

- `# ADR YYYYMMDD.HHMMSS: <Title>`
- `## Status`
- `## Context`
- `## Decision`
- `## Consequences`
- `## architecture-spec`
- `## acceptance-criteria`
- `## implementation-brief`
- `## resolved-open-questions`
- `## non-goals`
- `## validation-expectations`
- `## routing`

## Related files

- `docs/templates/ADR.proposal.template.md`
- `archon/workflows/create-adr.yaml`
- `docs/architecture.00.md`
