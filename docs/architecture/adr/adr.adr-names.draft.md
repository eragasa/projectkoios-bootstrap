# ADR 20260702.180215: ADR Names

## Status

draft

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository is moving toward semantic JSON structuring of files, so ADR naming must separate the semantic title field from the storage filename. The current naming guidance is split across two ADRs, but the combined naming contract is easier to consume as one umbrella surface.

This ADR defines the umbrella naming model for ADRs and encapsulates the title and filename rules as linked child ADRs.

## Decision

Use a single ADR naming umbrella, `ADR Names`, to govern the semantic title and filename contract for ADRs.

The umbrella ADR defines the shared naming model:

- the ADR `title` is the semantic display name and queryable label
- the ADR filename is the storage locator
- title and filename may differ
- filename rules should remain machine-friendly and stable
- title rules should remain decision-oriented and readable

The detailed rules stay encapsulated in linked child ADRs:

- `docs/architecture/adr/adr.adr-title-naming-convention.draft.md`
- `docs/architecture/adr/adr.adr-filename-naming-convention.draft.md`

### Naming model

- **Title**: semantic, user-facing, and structured for JSON
- **Filename**: filesystem-oriented and derived from the slug
- **Index surface**: renders the semantic title, not the raw storage path

### Boundary

This ADR is the umbrella entry point for ADR names. It does not replace the detailed rules; it organizes them under one semantic contract.

## Consequences

- programmers get one place to look for ADR naming intent
- semantic titles are easier to distinguish from storage filenames
- future JSON-backed ADR tooling can query titles directly
- title naming and filename naming remain separate concerns under one umbrella
- the existing naming ADRs become encapsulated sub-guidance instead of competing entry points

## architecture_spec

The ADR naming contract has two layers:

1. **Semantic title layer**
   - describes what the ADR is about
   - is stored as structured metadata
   - should be readable in indexes and generated views

2. **Filename layer**
   - describes how the ADR is stored on disk
   - should remain stable, slug-based, and tooling-friendly
   - should not be treated as the authoritative semantic label

The umbrella ADR should be the first place a reader goes to understand ADR naming. The child ADRs should be the places they go for the detailed title and filename rules.

Stated negatively:
- do not collapse semantic title and filename into one rule
- do not use the filename as the authoritative title
- do not force storage syntax into semantic identity

## acceptance_criteria

- a reviewer can tell where ADR semantic title rules live
- a reviewer can tell where ADR filename rules live
- the repository has one umbrella ADR naming surface
- title and filename rules remain distinct
- JSON-backed ADR tooling can map title vs filename cleanly

## implementation_brief

If accepted, link this umbrella ADR from `architecture.00` and treat the existing title and filename ADRs as the detailed child surfaces under it.

## resolved_open_questions

- Should the umbrella ADR eventually supersede the two child ADRs?
- Should JSON generation treat the title as the canonical display field everywhere?
- Should the filename be generated automatically from the slug on promotion?

## non_goals

- Renaming existing ADR files immediately
- Removing the child naming ADRs
- Defining a new document database format
- Conflating semantic title rules with filesystem rules

## validation_expectations

- a reader can distinguish title semantics from filename semantics
- a tooling pass can derive filenames without losing title meaning
- the architecture index can point to one umbrella naming contract

## routing

- Owner: Athena
- Next phase: proposed

## links

- back_to: architecture.00
- child: [ADR 20260702.004118: ADR Title Naming Convention](adr.adr-title-naming-convention.draft.md)
- child: [ADR 20260702.004300: ADR Filename Naming Convention](adr.adr-filename-naming-convention.draft.md)
- supersedes: None
- superseded_by: None
