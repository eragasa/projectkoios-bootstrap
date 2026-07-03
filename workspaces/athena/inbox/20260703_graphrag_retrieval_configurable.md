# GraphRAG retrieval scope

## Decision
Make retrieval **configurable**.

## Default
Use **1-hop** as the default preset for the first slice.

## Allowed presets
- `1-hop`
- `2-hop` (optional later)

## Rationale
- 1-hop keeps the first academic slice small and explainable
- configurability avoids hardcoding the retrieval boundary
- later experiments can compare retrieval depth without changing the engine

## Recommendation
Keep the engine generic and make retrieval depth a config value, not code.
