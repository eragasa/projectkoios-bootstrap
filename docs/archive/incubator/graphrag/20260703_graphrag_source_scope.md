# GraphRAG source scope

## Decision
Use **ADRs only** for the first GraphRAG slice.

## Why
- narrowest meaningful academic corpus
- stable structure for retrieval experiments
- easier citation and evaluation
- avoids mixed-document noise in v1

## Scope
Include:
- `docs/architecture/adr/**/*.md`

Exclude:
- AARs
- incubator notes
- spikes
- archive surfaces
- non-ADR workflow logs

## Consequences
- the first prototype stays small and auditable
- retrieval quality is easier to evaluate
- expansion to AARs can happen later as a separate preset
