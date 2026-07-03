# GraphRAG schema choice

## Recommendation
Use **JSON Schema** for validation.

## Why
- standardized and familiar
- machine-checkable
- good tooling support
- easy to keep separate from the YAML config
- explicit enough for scientific workflows

## Shape
- YAML is the authoring format
- JSON Schema is the validation contract
- a small runner validates config against schema before execution

## Consequences
- clear config contract
- reproducible validation
- easier downstream tooling
- less custom validation code to maintain
