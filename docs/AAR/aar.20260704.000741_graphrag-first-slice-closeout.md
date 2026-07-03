# AAR 20260704.000741: GraphRAG first slice closeout

## Scope

VULCAN stabilized and validated the Project Koios GraphRAG first slice in `projectkoios-bootstrap`.

## What happened

Implemented a config-driven ADR-only GraphRAG slice with a committed YAML config, JSON Schema, runtime validation, explicit preset replacement overlays, CLI wiring, in-memory ADR section indexing, retrieval evidence citations, answer formatting, backend selection, backend failure policy, and tests.

## Process issues

- Some unrelated workspace instruction changes were present in the working tree during slice closeout and are being preserved rather than overwritten.
- Generated Python cache files accumulated during test runs and had to be removed before commit.
- Early validation commands used `python`; subsequent validation used the repository virtualenv `python3` at `.venv/bin/python3`.

## Proposed follow-up improvements

- Add an explicit clean/check target to remove generated caches before commit.
- Add a persisted index command as the next GraphRAG slice.
- Keep future GraphRAG commits separated from workspace policy/naming changes where possible.

## Candidate ADR or implementation topics

- Persisted GraphRAG index output and deterministic JSON format.
- Workspace instruction filename standardization validation.
- Backend execution policy for local vs remote model adapters.

## Current status

Validation passed with `.venv/bin/python3`:

- `171 passed`
- `koios validate: schema=True runtime=True sources=37`
