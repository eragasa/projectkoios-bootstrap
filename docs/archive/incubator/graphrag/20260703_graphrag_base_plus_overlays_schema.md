# GraphRAG base + overlay schema draft

## Base config: `projectkoios.ingestion.config`

```yaml
version: 1
project: projectkoios
pipeline:
  mode: derived-index
  retrieval_depth: 1
  answer_format: cited_summary
  citation_format: file:line
source:
  include: []
  exclude:
    - docs/archive/**
    - graphify-out/**
  types:
    - markdown
ontology:
  entities:
    - id: WS
      name: WorkflowStep
    - id: HE
      name: HarnessEvent
    - id: FM
      name: FailureMode
    - id: MI
      name: Mitigation
  edges:
    - DEPENDS_ON
    - TRIGGERED
    - RESOLVED
    - VIOLATED
extraction:
  deterministic:
    enabled: true
    fields:
      - id
      - timestamp
      - status
      - path
      - step
  semantic:
    enabled: true
    model: local-or-host
retrieval:
  strategy: 1-hop
  seed: vector
  expand: graph
  max_nodes: 25
evaluation:
  mode: academic
  require_citations: true
presets:
  adr:
    source:
      include:
        - docs/architecture/adr/**/*.md
  aar:
    source:
      include:
        - docs/AAR/**/*.md
  workflow:
    source:
      include:
        - docs/workflow/**/*.md
```

## Overlay rules

- overlays only replace or extend data fields
- overlays must not define executable logic
- overlays may tune source globs, retrieval hints, and evaluation mode
- overlays inherit ontology and extraction defaults unless explicitly overridden
- base config remains valid on its own

## Merge order

1. load base config
2. load preset overlay
3. deep-merge overlay into base
4. validate final config
5. run pipeline

## Recommendation

Keep the base config small and stable; let overlays express corpus-specific variation.
