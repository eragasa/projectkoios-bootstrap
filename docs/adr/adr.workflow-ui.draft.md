# ADR 20260702.213000Z: Workflow UI Surface

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

The repository needs a workflow-facing UI surface that sits on top of the shared UI/core model without becoming the source of authority for the model itself.

The workflow UI surface should remain separate from renderer implementation details.
- high level about client-specific concerns

## Definitions

- Workflow UI: the user-facing surface for workflow interactions.
- Shared UI/core: the renderer-agnostic model that workflow UI is built on.
- Client-specific concern: a concrete rendering or transport choice made by a consuming app or adapter.

## Decision

Adopt a workflow UI surface that is built on the shared UI/core model and stays separate from renderer implementation details.

The workflow UI surface:
- consumes the shared UI/core model
- presents workflow-facing interactions
- may vary by client or renderer at a high level
- does not redefine the shared UI/core model itself

The workflow UI surface does not cover:
- renderer implementation
- marshalling or unmarshalling
- framework choices
- transport or runtime internals

## Consequences

- workflow-facing UI can evolve without rewriting the shared model
- renderer/client concerns stay separated from core architecture
- future bindings can reuse the same core model across clients
- the shared UI/core ADR remains the mothership for the common model

## architecture-spec

The workflow UI surface is an adjacent surface to shared UI/core.

It should define:
- how workflow interactions present through the shared model
- how client-specific rendering can vary without changing the core
- how workflow UI stays aligned to the shared UI/core namespace

It should not define:
- UI/core semantics
- JSON schemas/contracts
- rendering internals

## acceptance-criteria

- a reviewer can distinguish workflow UI from shared UI/core
- workflow UI can be described without defining renderer internals
- the shared UI/core model remains the source of authority for common UI behavior
- client-specific concerns stay high-level and bounded

## implementation-brief

If accepted, update UI architecture guidance so workflow UI is treated as a separate surface built on shared UI/core and linked to `adr.ui-core`.

verification_method: review a proposed workflow UI note and confirm that it stays above renderer internals while remaining clearly built on the shared UI/core model.

## resolved_open_questions

- Which client surfaces are first consumers of workflow UI?
- Should workflow UI have its own subnamespace later?
- How much renderer/client variation is acceptable at the surface level?

## non_goals

- defining rendering internals
- choosing a framework
- redefining shared UI/core
- absorbing JSON schema work

## validation_expectations

- workflow UI can be described independently of the renderer implementation
- the shared UI/core boundary remains intact
- client-specific concerns do not leak into the core model

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Workflow-facing UI surface built on the shared UI/core model.

## links

- back_to: architecture.00
- related: [ADR 20260702.213000Z: Shared UI Core Namespace](adr.ui-core.draft.md)
- supersedes: None
- superseded_by: None
