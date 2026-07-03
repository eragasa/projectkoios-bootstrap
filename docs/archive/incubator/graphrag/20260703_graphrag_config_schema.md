# GraphRAG config schema draft

```yaml
version: 1
project: projectkoios
pipeline:
  mode: derived-index
  retrieval_depth: 1
  answer_format: cited_summary
  citation_format: file:line
source:
  include:
    - docs/architecture/adr/**/*.md
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
  default:
    source:
      include:
        - docs/architecture/adr/**/*.md
```

## Notes
- Keep everything variable in config.
- Keep code generic.
- Add corpus-specific presets without changing the engine.
- Add more ontology types only by config, not code.
