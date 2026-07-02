# ADR 20260701.131629: Canonical ADR proposal template

## Status

Accepted

## Context

Origin: user request
From: Hermes
Acting-As: Hermes
Scope: projectkoios-bootstrap docs-template surface
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository needs one canonical ADR data model so draft content, review
workflow, and rendering all agree on the same fields and order.

The canonical source now lives at `docs/architecture/adr/adr.schema.json`.
Markdown is a render target, not the source of truth.

The data model must stay focused on one architecture domain, keep provenance in
`context`, and preserve the repository's canonical ADR fields.

## Decision

Adopt `docs/architecture/adr/adr.schema.json` as the canonical ADR schema for
this repository and treat Markdown as a derived rendering of that JSON.

The schema should define the ADR content model, required provenance fields,
status, routing, and the renderable decision sections.

## Consequences

- ADRs become machine-readable source artifacts.
- Markdown can be generated from the same JSON in multiple styles.
- Review and workflow tooling can validate a stable schema instead of prose
  headings.
- Future changes to ADR shape flow through one schema file.

## architecture-spec

The canonical ADR JSON schema contains:

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

`context` must carry provenance and single-domain metadata:

- `origin`
- `from`
- `acting_as`
- `scope`
- `repository`
- `delegated_operator`
- `architecture_domain`

## acceptance-criteria

- New ADRs can be represented as JSON without losing any required data.
- The schema includes provenance and routing fields.
- The schema enforces one architecture domain per ADR.
- A renderer can produce Markdown from the JSON object.

## implementation-brief

No code implementation is required for the schema decision itself.

## resolved-open-questions

- Should Markdown be one renderer or multiple render profiles?
- Should the archived ADR set be converted to JSON later?

## non-goals

- This ADR does not define the renderer implementation.
- This ADR does not convert existing archived ADRs yet.
- This ADR does not broaden ADR scope beyond one architecture domain.

## validation-expectations

- The JSON schema validates a representative ADR object.
- The create-ADR workflow can emit JSON matching the schema.
- A Markdown render can be generated from the same object.

## routing

- Owner: Athena
- Next phase: accepted
- Notes: This ADR governs the JSON ADR source-of-truth surface.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
