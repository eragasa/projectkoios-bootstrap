# ADR 20260702.213000Z: JSON Schemas Namespace

## Status

draft
date: 20260702.213000Z

## Context

Origin: user request
From: HERMES
Acting-As: user(Eugene)
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The repository needs a JSON schema namespace for the UI/core family so schema and contract work stays separate from the shared UI/core concept itself.

The JSON schema namespace should hold schemas only. It should not define the UI concept, renderer behavior, or workflow UI surface.

## Definitions

- JSON schema namespace: the set of schema/contract documents that define machine-readable shapes.
- Shared UI/core: the renderer-agnostic UI model defined in a separate ADR.
- Workflow UI: the surface that consumes the shared UI/core model.

## Decision

Adopt a JSON schemas namespace for the UI/core family that holds schemas and contracts only.

The JSON schemas namespace:
- defines machine-readable shapes and contracts
- supports the shared UI/core family without replacing it
- may be referenced by workflow UI or renderer layers
- does not define the UI concept itself

The JSON schemas namespace does not cover:
- the UI/core domain model
- rendering implementation
- marshalling or unmarshalling
- framework choices
- transport or runtime internals

## Consequences

- schema and contract work stays separate from UI/core design
- the shared UI/core ADR can remain renderer-agnostic
- workflow UI can consume schemas without becoming the schema authority
- future tooling can validate against one schema namespace

## architecture-spec

The JSON schemas namespace is a supporting surface for the UI/core family.

It should define:
- schema files and contract files only
- the machine-readable shapes used by the shared UI/core family
- any constraints needed to validate those shapes

It should not define:
- shared UI/core semantics
- workflow UI behavior
- rendering internals

## acceptance-criteria

- a reviewer can tell that the namespace holds schemas only
- the UI/core concept remains defined elsewhere
- workflow UI can consume the namespace without being defined by it
- schema/contract validation remains separate from UI architecture decisions

## implementation-brief

If accepted, update UI architecture guidance so the JSON schemas namespace is linked as a separate adjacent surface next to `adr.ui-core` and `adr.workflow-ui`.

verification_method: review a proposed schema note and confirm that it defines shapes only, not UI semantics or renderer behavior.

## resolved_open_questions

- Which schema files belong in the first version of the namespace?
- Should the namespace be flat or grouped by family later?
- Which tooling should validate the schema files?

## non_goals

- defining the shared UI/core model itself
- choosing renderer implementation details
- defining workflow UI behavior
- merging schema work into UI core work

## validation_expectations

- schema documents can be identified as contracts only
- the shared UI/core model remains separate and renderer-agnostic
- workflow UI can reference schemas without losing its own boundary

## routing

- Owner: Athena
- Next phase: proposed
- Notes: JSON schema/contract surface for the UI/core family.

## links

- back_to: architecture.00
- related: [ADR 20260702.213000Z: Shared UI Core Namespace](adr.ui-core.draft.md)
- supersedes: None
- superseded_by: None
