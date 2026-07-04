# AAR 20260704.123324: Workspace layout commit closeout

## Scope

HERMES/VULCAN committed and pushed the pending workspace layout and document-state changes after stabilizing validation.

## What happened

The working tree contained workspace layout updates, moved/removed handoff files, workspace state changes, and updates to tests and GraphRAG config path assumptions. Validation initially failed because tests and runtime validation disagreed about the current ADR path (`docs/adr/` versus the prior `docs/architecture/adr/`) and workspace initialization tests still expected `AGENT.md` plus handoff directories.

## Process issues

- Repository ADR location changed to `docs/adr/`, but GraphRAG helper tests and runtime assumptions were temporarily inconsistent.
- Workspace initialization behavior now creates `AGENTS.md`, `sessions/`, `working/`, `scratch/`, and `decisions/`, while tests still expected the older handoff-directory layout.
- Generated Python cache files appeared during validation and had to be removed before commit.

## Proposed follow-up improvements

- Add a single documented ADR path constant or config default to reduce path drift.
- Keep workspace-layout refactors and GraphRAG path updates explicitly linked in future commits.
- Add a clean target for generated Python cache files.

## Candidate ADR or implementation topics

- Canonical ADR path contract for repo-local tooling.
- Workspace layout migration validation.
- Cleanup command for generated local artifacts.

## Current status

Validation passed before commit:

- `.venv/bin/python3 -m pytest -q` => `170 passed`
- `.venv/bin/python3 -m projectkoios.bootstrap koios validate --schema projectkoios.ingestion.schema.json --preset adr` => `schema=True runtime=True sources=38`
