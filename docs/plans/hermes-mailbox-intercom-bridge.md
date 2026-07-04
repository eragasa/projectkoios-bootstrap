# Superseded Plan: Hermes intercom bridge

## Status

superseded by document-state orchestration

## Scope

This file previously described a filesystem transport layer for workspace-to-workspace coordination.
That approach is no longer the active control surface.

## Current direction

- The repository document set and document statuses are the durable workflow state.
- Hermes owns cross-domain consistency and resolves inconsistencies between document domains.
- Each agent owns a document domain and writes bounded state changes in that domain.
- Workspace directory placement and live notifications are not authority.

## Replacement validation

A sufficient replacement proves that:

1. the document domain is explicit;
2. the current and target document statuses are explicit;
3. provenance survives document-state changes;
4. no agent has to infer authority from transport mechanics.
