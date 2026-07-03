# GraphRAG config schema draft

## Base config: `projectkoios.ingestion.config`

```yaml
version: 1
project: projectkoios
pipeline:
  mode: derived-index
  retrieval_depth: 1
  answer_format: cited_summary
  citation_format: multi
validation:
  mode: strict
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
    backend: ollama
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

## Normative rules

- The base config **MUST** be valid on its own.
- The config **MUST** be authored in YAML.
- Validation **MUST** occur in two layers:
  - JSON Schema for static shape
  - runtime checks for paths, globs, and references
- Overlays **MUST** use explicit replacement for any section they change.
- Overlays **MUST NOT** rely on implicit deep merge.
- The source surface for v1 **MUST** default to ADRs only.
- Retrieval depth **MUST** be configurable, with `1-hop` as the default.
- Answer format **MUST** be selectable by prompt.
- Citation support **MUST** fall back to the strongest supported form.
- Backend selection **MUST** be configurable.
- The first implementation slice **MUST** require only one working backend.

## Validation contract

The schema **MUST** validate:
- required keys
- field types
- enum values
- nested object shape

The runtime validator **MUST** validate:
- source glob resolution
- preset existence
- file existence where required
- ontology and edge coherence
- usable retrieval and evaluation settings

## Notes
- Use RFC normative language throughout user-facing specs.
- Keep policy in config, not code.
- Keep the engine generic and the presets small.
