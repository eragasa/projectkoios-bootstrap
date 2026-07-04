# ADR 20260702.213000Z: Shared UI Core Namespace

## Status

draft
date: 20260702.213000Z

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The repository needs a long-term shared UI/core concept for a TypeScript-first application. That concept must stay renderer-agnostic so future workflow UI surfaces, shared renderers, and language bindings can all point at the same underlying model.

The shared UI/core concept must not be confused with JSON schema work or with the workflow UI surface itself. JSON remains reserved for schemas and contracts under `adr.json-schemas`, while workflow UI belongs to `adr.workflow-ui`.

## Definitions

- Shared UI/core: the long-term domain model for UI objects, state, and interactions that is independent of any renderer.
- Renderer: a concrete presentation implementation for a UI/core model.
- Workflow UI: the surface that renders workflow-facing interaction on top of the shared UI/core model.
- Schema/contract JSON: JSON used to define machine-readable schemas and contracts, not the UI/core runtime model.

## Decision

Adopt a shared UI/core namespace as the mothership concept for UI-related architecture in this repository.

The shared UI/core namespace is renderer-agnostic and is intended to support:
- a TypeScript-first application model
- future shared renderers
- future language bindings
- workflow UI as a separate surface built on top of the shared model

The shared UI/core namespace covers:
- the shared UI/core concept
- renderer-agnostic data and interaction modeling
- future multi-renderer portability

The shared UI/core namespace does not cover:
- rendering implementation
- marshalling or unmarshalling
- framework choices
- transport or runtime internals

JSON is reserved for schemas and contracts under `adr.json-schemas`.
Workflow UI is a separate surface under `adr.workflow-ui`.

## Consequences

- UI architecture can be discussed once at the shared core layer instead of being rewritten per renderer
- workflow UI can remain a surface choice rather than the source of authority
- future bindings can target one model without re-deciding the model each time
- JSON schema and workflow UI work stay separated from the shared UI/core concept

## architecture-spec

The shared UI/core namespace is a conceptual control surface for UI architecture.

It should define:
- the shared object model for UI state and interactions
- the portability expectations across renderers
- the boundary between core model and renderer-specific implementation
- the relationship between shared UI/core, workflow UI, and schema/contract JSON

It should not define:
- the rendering engine
- serialization plumbing
- application framework selection
- transport details

## acceptance-criteria

- a reviewer can state what belongs in the shared UI/core namespace
- a reviewer can state what is excluded from the namespace
- workflow UI can be described as a separate surface from shared UI/core
- JSON schema work can be kept separate from the shared UI/core model
- future renderer implementations can target the same conceptual core

## implementation-brief

If accepted, create or update the UI architecture guidance so the shared UI/core namespace becomes the reference point for future workflow UI and renderer work, with `adr.json-schemas` and `adr.workflow-ui` linked as separate adjacent surfaces.

verification_method: review a proposed UI architecture note and confirm that it can distinguish shared UI/core from renderer implementation, JSON schema/contract work, and workflow UI surface work.

## resolved_open_questions

- Should the shared UI/core namespace have its own bootstrap note or index entry?
- Should workflow UI be a sibling ADR or a child surface of the shared core ADR?
- Which language bindings are in scope first?

## non_goals

- defining rendering internals
- choosing a UI framework
- defining marshalling or transport mechanics
- collapsing JSON schema work into UI core work

## validation_expectations

- the boundary between shared UI/core and workflow UI is explicit
- JSON schemas/contracts remain separate from the UI/core model
- future renderer or language-binding work can cite the same core concept

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Mothership concept for shared UI/core, workflow UI adjacency, and renderer portability.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
