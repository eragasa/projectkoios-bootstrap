# KOIOS review: architecture document control surface

## Metadata

- Type: provenance-review
- Status: advisory
- Captured: 20260704T023500Z
- Captured by: KOIOS
- Source artifact: `workspaces/athena/handoffs/incoming/architecture.documents.control-surface.20260704T000000Z.md`
- Related note: `workspaces/koios/handoffs/outgoing/20260704_architecture-document-control-surface-provenance.md`
- Repository: projectkoios-bootstrap

## Assessment

The architecture-document control surface is a strong candidate for future skill derivation.

The note correctly treats architecture documents as controlled blueprints rather than governing standards.

The note correctly requires explicit owner, scope, target domain, authority boundary, provenance, and validation expectations.

The note correctly prevents authority from being inferred from directory placement.

The note is not yet ready to become policy because its required structure overlaps too strongly with ADR structure.

## Key distinction to preserve

ADRs decide.

Architecture documents describe and constrain a bounded architectural surface.

Standards govern repeated practice.

Implementation briefs translate accepted architecture into work.

Process-capture notes record how artifacts moved through the workflow.

## Recommended clarification

Architecture documents SHOULD NOT be required to use ADR-shaped `Context`, `Decision`, and `Consequences` sections unless they are decision-bearing.

Architecture documents SHOULD instead require sections that expose control boundaries and validation expectations.

Suggested required sections:

- Purpose
- Owner
- Scope
- Target domain
- Controlled surface
- Non-controlled surface
- Requirements
- Validation expectations
- Provenance
- Status

Suggested optional sections:

- Context
- Decision
- Consequences
- Acceptance criteria
- Implementation brief guidance
- Open questions
- Non-goals
- Routing metadata

## Candidate architecture-document schema

```md
# Architecture document: <title>

## Metadata

- Status: draft | proposed | review | accepted | archived
- Owner:
- Scope:
- Target domain:
- Repository:
- Source artifacts:
- Next expected artifact:

## Purpose

## Controlled surface

## Non-controlled surface

## Requirements

## Validation expectations

## Provenance

## Consequences
```

## Candidate skill behavior

An architecture-document authoring skill SHOULD check for owner, scope, target domain, status, and provenance.

The skill SHOULD check that normative requirements use RFC-style terms.

The skill SHOULD check that informational background is separated from requirements.

The skill SHOULD check that the document states what it controls.

The skill SHOULD check that the document states what it does not control.

The skill SHOULD check that validation expectations are present.

The skill SHOULD warn when the document appears to claim governing-standard authority.

The skill SHOULD warn when the document relies on directory placement for authority.

The skill SHOULD warn when ADR-only structure is used without a decision-bearing purpose.

## Recommended next artifact

ATHENA should produce a revised architecture-document control-surface proposal that distinguishes architecture documents from ADRs, standards, implementation briefs, and process-capture notes.

KOIOS should preserve this review as provenance for future skill derivation.

## Non-authority statement

This review is advisory provenance only.

This review does not promote the source note into policy.

This review does not create an architecture-document standard.
