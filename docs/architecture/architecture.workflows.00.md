```json
{
  "title": "Workflow Architecture Index",
  "artifact_type": "architecture-index",
  "status": "working-draft",
  "datetime": "20260705",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "bootstrap-held workflow architecture decomposition and implementation evidence index",
  "canonical_location": "docs/architecture/architecture.workflows.00.md"
}
```

# Architecture: Workflows

## Status

working-draft

## Purpose

Index workflow-related architecture decomposition surfaces, controlling ADRs, and implementation evidence for `projectkoios-bootstrap`.

This document is an index and navigation surface. It does not create new workflow architecture authority by itself.

## Authority boundary

Workflow architecture in this repository applies to bootstrap-held workflow surfaces unless a separate product-domain decision accepts it elsewhere.

## Architecture-led slicing workflow

The intended workflow is architecture-led:

1. Architecture documents set the long-term vision and blueprint for a system surface.
2. Implementation work is sliced from that blueprint into bounded briefs, plans, and patches.
3. Implementation evidence is reconciled back into the architecture document.
4. At the end of implementation, the architecture document becomes or is revised into the as-built documentation for the delivered system.

Implementation briefs and reports are slice artifacts. They support the architecture surface but do not replace it as the long-term system document.

## Index

| Architecture Decomposition | Applicable ADR |
|---|---|
| [architecture.petrinet.00](architecture.petrinet.00.md) | [adr.petrinet.20260705.132740Z](../adr/adr.petrinet.20260705.132740Z.md) |
| [workflow-adapter-dependency-encapsulation.20260705.105604](../implementation/workflow-adapter-dependency-encapsulation.20260705.105604.md) | [adr.petrinet.20260705.132740Z](../adr/adr.petrinet.20260705.132740Z.md) |

## Implementation

### Reports

- [workflow-petri-net-executor-first-slice.20260705.102506](../implementation/workflow-petri-net-executor-first-slice.20260705.102506.md)
