# GraphRAG model backends

## Decision
Make the GraphRAG engine **pluggable** across model backends.

## Supported backends
- Ollama
- OpenRouter
- Hugging Face

## Rule
The engine should depend on a backend interface, not a specific provider.
Provider choice must be configurable.

## Rationale
- supports local and hosted runs
- avoids locking the pipeline to one vendor
- makes experiments comparable across models
- preserves portability for scientific workflows

## Recommendation
Use one backend abstraction with provider adapters underneath.
