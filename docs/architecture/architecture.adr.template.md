---
status: draft
date: 20260701.131629Z
back_to: architecture.00
---

# ADR schema

## Purpose

This is the active bootstrap architecture note for the canonical ADR JSON
schema and render contract.

## Scope

It governs `docs/architecture/adr/adr.schema.json` as the source of truth for
ADR content and any Markdown or other rendering derived from that JSON.

## Control

This note is controlled by:

- `docs/architecture/adr/adr.20260701.131629_adr-template-contract.md`

## Schema shape

The canonical ADR JSON object includes:

- `id`
- `slug`
- `title`
- `status`
- `context`
- `decision`
- `consequences`
- `architecture_spec`
- `acceptance_criteria`
- `implementation_brief`
- `resolved_open_questions`
- `non_goals`
- `validation_expectations`
- `routing`
- `links`

## Related files

- `docs/architecture/adr/adr.schema.json`
- `docs/templates/ADR.proposal.template.md`
- `archon/workflows/create-adr.yaml`
- `docs/architecture/architecture.00.md`
