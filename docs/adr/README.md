# ADR control surface

## Purpose

This directory stores Architecture Decision Records for `projectkoios-bootstrap`.

ADRs record bounded decisions and their consequences.

ADRs are not the same artifact type as architecture documents.

## Boundary

ADRs MUST record a decision.

ADRs MUST include the context needed to understand the decision.

ADRs MUST include consequences of the decision.

ADRs SHOULD link to architecture documents when a decision depends on or controls a broader architectural surface.

ADRs SHOULD NOT contain full architecture blueprints unless the blueprint is necessary to understand the decision.

Architecture blueprints SHOULD live under `docs/architecture/`.

Policies SHOULD live under `docs/policies/`.

Templates SHOULD live under `docs/templates/`.

Implementation reports SHOULD live under `docs/implementation/`.

Process-chain records SHOULD live under `docs/process-capture/`.

## Current migration note

The active ADR directory moved from `docs/architecture/adr/` to `docs/adr/`.

This move separates decision records from architecture-document control surfaces.

Some files in this directory may still need later classification and splitting.

KOIOS captured an advisory classification at `workspaces/koios/handoffs/outgoing/architecture.document.control-surface.adr-classification.20260704T024500Z.md`.

## Required minimum structure

ADR Markdown files SHOULD include `Status`, `Context`, `Decision`, and `Consequences` sections.

ADR JSON files SHOULD conform to the schema files in this directory when used.
