# ADR 20260702.182000Z: Template Representation Contract

## Status

draft
date: 20260702.182000Z

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository needs one canonical contract for reusable template documents so the JSON form, the Markdown form, and any cross-format rendering agree on what a template is, even when the Markdown form contains presentation choices that do not exist in the JSON structure.

Today, template material exists in both Markdown and instruction form, but the boundary between “template content” and “template implementation details” is not explicit. That makes it hard to say which differences matter to the contract and which are just rendering choices.

## Decision

Adopt `docs/templates/` as the canonical namespace for reusable template documents and instruction files, and define a representation contract for that namespace.

This ADR defines:

- `adr.template-json` — the canonical JSON representation of a reusable template
- `adr.template-md` — the canonical Markdown representation of the same template
- the mapping expectations between those two forms

The contract explicitly allows Markdown-only presentation choices that are not modeled in the JSON spec, such as:

- numbered lists vs bullet lists
- heading depth and ordering within the rendered template
- emphasis, quoting, and other presentation-only Markdown conventions
- layout choices that preserve meaning without changing the underlying template data

The contract also allows explicit transform hooks, such as:

- `JsonRenderer.to_md()` for JSON → Markdown rendering
- `ingestion.MdIngester.to_json()` for Markdown → JSON ingestion

Those names describe the expected roles of the transforms, not their implementation architecture.

## Consequences

- template documents have a stable namespace and a stable representation contract
- Markdown can be used for human-friendly template authoring without losing the JSON source shape
- rendering differences that do not change meaning can be tolerated intentionally
- implementation teams can build render/ingest code without the ADR having to prescribe internals

## architecture-spec

The template representation contract covers:

- the canonical JSON shape of reusable templates
- the canonical Markdown rendering of those templates
- stable cross-format meaning
- allowed presentation differences that do not alter template intent

The contract does not cover:

- marshalling and unmarshalling internals
- parser or serializer architecture
- storage, file IO, or runtime plumbing
- exact class layout beyond the named transform roles

## acceptance-criteria

- a reviewer can tell what makes a template valid in JSON form
- a reviewer can tell what makes the same template valid in Markdown form
- Markdown presentation choices that do not change meaning are recognized as allowable
- the contract can be implemented without embedding marshalling details in the ADR
- template docs remain readable on their own while staying contract-aligned

## implementation-brief

If accepted, update the template namespace index and template guidance to point reusable template material at `docs/templates/`, then implement or adjust the JSON↔Markdown transforms to follow the representation contract.

## resolved_open_questions

- Should the JSON representation be the authoritative source and Markdown a render target? Yes, for now.
- Should Markdown allow multiple valid render styles when meaning is preserved? Yes.
- Should the transform names be formal API names or descriptive placeholders? Descriptive placeholders for now.

## non-goals

- Defining marshalling/unmarshalling internals
- Defining the storage backend for templates
- Replacing the ADR lifecycle
- Forcing one rigid Markdown style when multiple styles preserve meaning

## validation_expectations

- a JSON template can be rendered to Markdown without losing required meaning
- a Markdown template can be ingested into the canonical JSON form without losing required meaning
- list style and similar presentational choices do not cause false contract failures

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Documentation-surface control object for reusable templates and cross-format representation.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
