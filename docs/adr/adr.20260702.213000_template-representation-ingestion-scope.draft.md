# ADR 20260702.213000Z: Template Representation Ingestion Scope

## Status

draft
date: 20260702.213000Z

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository needs a narrowly scoped ingestion surface for the template representation contract and the implementation namespace split. In this context, ingestion means only the JSON↔Markdown handling needed for reusable template documents and the namespace-aware indexing of implementation notes. It does not mean the broader Graphify ingestion daemon, source-corpus crawling, or a general-purpose evidence-ingestion system.

The current repository also does not contain `src/python/ingestion/`, so the implementation boundary must match the existing package layout unless the repo is intentionally restructured.

## Decision

Define the ingestion surface for this slice as a template-document transformation boundary inside the existing `projectkoios.bootstrap` Python tree.

This slice covers only:

- canonical template JSON representation
- Markdown rendering of that template representation
- Markdown ingestion back to canonical JSON for templates
- namespace-aware handling for `docs/templates/` and `docs/implementation/`
- index-note wiring for `templates.00` and `implementation.00`

This slice explicitly excludes:

- the Graphify ingestion daemon
- broad repository or vault ingestion
- source acquisition pipelines
- a new top-level `projectkoios.ingestion` package
- any generic ingestion framework beyond the template/document contract

## Consequences

- the word “ingestion” is now bounded to template/document transformation in this repo slice
- the implementation target can stay inside the existing bootstrap package tree
- the repository avoids creating a misleading general ingestion namespace
- future broader ingestion work will need a separate ADR with its own scope

## architecture-spec

The ingestion scope for this ADR is constrained to document transformation and namespace alignment:

- template JSON↔Markdown round-tripping
- allowed Markdown presentation variance that does not change meaning
- implementation-document indexing and navigation
- no broader content ingestion behavior

## acceptance-criteria

- a template document can round-trip between JSON and Markdown within the allowed contract
- implementation documents are handled through `docs/implementation/`
- no code or ADR in this slice depends on a nonexistent `src/python/ingestion/` tree
- the scope does not overlap the Graphify ingestion daemon or other general ingestion work

## implementation-brief

If accepted, create a file-level implementation plan that targets the existing `src/python/projectkoios/bootstrap/` tree, adds the template transform machinery, and updates the template and implementation namespace indexes.

### Verification method

- round-trip tests for template JSON and Markdown
- link/path checks for `docs/templates/templates.00.md` and `docs/implementation/implementation.00.md`
- repository-path inspection to confirm the implementation stays inside the existing bootstrap package tree

## resolved_open_questions

- Should this slice create a new top-level `ingestion` package? No.
- Should this slice cover Graphify ingestion? No.
- Should template Markdown allow presentation-only variation? Yes.

## non-goals

- General-purpose ingestion architecture
- Repository-wide content crawling
- Vault or PDF ingestion
- Replacing the Graphify daemon
- Creating a new top-level `projectkoios.ingestion` package

## validation_expectations

- the implementation plan is clearly scoped to the template/document surface
- the repo can explain the meaning of “ingestion” in this slice without confusing it with the Graphify daemon
- the final code path lives under the existing bootstrap package layout

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Narrow scope ADR for template transformation and namespace alignment only.
