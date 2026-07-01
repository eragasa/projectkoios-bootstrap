# ADR 20260701.131629: Canonical ADR proposal template

## Status

Accepted

## Context

Origin: user request
From: Hermes
Acting-As: Hermes
Scope: projectkoios-bootstrap docs-template surface
Repository: projectkoios-bootstrap
Delegated-Operator: pi

The repository needs one canonical proposal template for new ADRs so draft
content, review tooling, and workflow prompts all ask for the same sections in
the same order.

The current reusable starter lives at `docs/templates/ADR.proposal.template.md`.
The `create-adr` workflow should emit the same structure when generating new
ADRs.

The template must stay focused on one architecture domain, use provenance
fields, and preserve the repository's canonical ADR section names:
`architecture-spec`, `acceptance-criteria`, `implementation-brief`,
`resolved-open-questions`, `non-goals`, `validation-expectations`, and
`routing`.

## Decision

Adopt `docs/templates/ADR.proposal.template.md` as the canonical ADR proposal
template for this repository and treat it as the source for new ADR drafting
and review guidance.

The template should keep the canonical ADR header and section order, require a
single architecture domain, and use the repository's normalized section names.

## Consequences

- New ADR drafts start from a consistent shape.
- Review and workflow tooling can validate the same headings every time.
- The template becomes the active reference for `architecture.adr.template`.
- Future changes to ADR draft shape should flow through one document.

## architecture-spec

The canonical ADR proposal template contains:

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

## acceptance-criteria

- New ADR drafts use the canonical section order.
- The template includes the required provenance fields.
- The template keeps exactly one architecture domain per proposal.
- The repository can point to one active ADR template note.

## implementation-brief

No code implementation is required for the template decision itself.

## resolved-open-questions

- Should future ADR types get separate templates?
- Should template validation be enforced by the review workflow?

## non-goals

- This ADR does not redesign the full lifecycle policy.
- This ADR does not create a second competing ADR template.
- This ADR does not broaden the template beyond ADR proposal drafting.

## validation-expectations

- The template file matches the canonical section list.
- The `create-adr` workflow emits the same proposal shape.
- The active architecture note links to the template and this ADR.

## routing

- Owner: Athena
- Next phase: accepted
- Notes: This ADR governs the active ADR proposal template surface.
