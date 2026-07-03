# GraphRAG ingestion spike

## Purpose
Scratchpad for the first Koios GraphRAG slice.

## Current direction
- Top-level command surface: `koios`
- Internal API first
- OOP with DataObject / ActionObject separation
- ADR-only discovery
- Ollama backend first

## Notes
- Keep CLI thin.
- Prefer explicit classes over free functions.
- Keep config validation separate from runtime source resolution.
