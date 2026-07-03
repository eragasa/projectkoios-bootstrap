# GraphRAG answer format

## Decision
Allow **both** answer formats, selected by prompt.

## Allowed formats
- `cited_summary`
- `structured_json`

## Rule
The prompt selects the response shape; the engine does not hardcode one output style.

## Rationale
- supports different user needs
- keeps the system generic
- allows scientific and narrative outputs from the same pipeline
- avoids building a second engine for formatting

## Default recommendation
Use `cited_summary` unless the prompt explicitly requests structured output.
