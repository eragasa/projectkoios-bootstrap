# Opencode checklist — multi-repo execution readiness

Use this checklist after Archon has approved the repo-ownership decision and migration order.

## Preconditions

- [ ] Read `../maps/repositories.md`
- [ ] Read `../maps/packages.md`
- [ ] Read `../architecture/harness-boundaries.md`
- [ ] Confirm an approved Archon handoff exists with:
  - [ ] objective
  - [ ] scope and non-goals
  - [ ] target repos
  - [ ] likely file/package paths
  - [ ] validation expectations
  - [ ] open questions/blockers
- [ ] Confirm Goose inventory exists for ownership mismatches/import coupling

## Phase 1 — execution-readiness normalization

### Namespace packaging
- [ ] Inspect `pyproject.toml` in:
  - [ ] `~/repos/projectkoios-agent`
  - [ ] `~/repos/projectkoios-obsidian`
  - [ ] `~/repos/projectkoios-workflow`
  - [ ] `~/repos/projectkoios-search`
  - [ ] `~/repos/projectkoios-references`
  - [ ] `~/repos/projectkoios-api`
- [ ] Add or verify namespace-package discovery (`namespaces = true`) where missing
- [ ] Verify `projectkoios` and `projectkoios-ingestion` remain compatible with the namespace layout
- [ ] Validate editable installs across the affected repos

## Phase 2 — search extraction

- [ ] Confirm Archon-approved ownership: `projectkoios-search` owns search/indexing
- [ ] Inventory current source in `~/repos/projectkoios/src/python/projectkoios/search/`
- [ ] Inventory transitional indexing code such as `projectkoios/indexing/in_memory_chunk_index.py`
- [ ] Move search implementation into `~/repos/projectkoios-search/src/python/projectkoios/search/`
- [ ] Re-home indexing code under search ownership
- [ ] Update imports/tests/package metadata
- [ ] Remove or deprecate mothership-owned search/indexing paths as approved
- [ ] Run validation in `projectkoios-search`

## Phase 3 — API extraction

- [ ] Confirm Archon-approved ownership: `projectkoios-api` owns HTTP boundary/runtime wiring
- [ ] Inventory current source in `~/repos/projectkoios/src/python/projectkoios/api/`
- [ ] Inventory API-specific runtime wiring, especially `projectkoios/runtime/services.py`
- [ ] Move API implementation into `~/repos/projectkoios-api/src/python/projectkoios/api/`
- [ ] Move API composition/runtime wiring into `projectkoios-api`
- [ ] Update imports/tests/package metadata
- [ ] Remove or deprecate mothership-owned API paths as approved
- [ ] Run validation in `projectkoios-api`

## Phase 4 — obsidian/vault extraction

- [ ] Confirm Archon-approved ownership: `projectkoios-obsidian` owns obsidian/vault behavior
- [ ] Inventory current source in `~/repos/projectkoios/src/python/projectkoios/vault/`
- [ ] Decide whether compatibility shims are required for `projectkoios.vault` -> `projectkoios.obsidian`
- [ ] Move implementation into `~/repos/projectkoios-obsidian/src/python/projectkoios/obsidian/`
- [ ] Remove API/config coupling discovered during the move
- [ ] Update imports/tests/package metadata
- [ ] Remove or deprecate mothership-owned vault paths as approved
- [ ] Run validation in `projectkoios-obsidian`

## Phase 5 — mothership cleanup

- [ ] Reduce `~/repos/projectkoios` to mothership/docs/shared-only scope
- [ ] Reclassify remaining `chunking/` and `repositories/` only if still approved as shared transitional abstractions
- [ ] Remove stale ownership claims from code comments, docs, and package metadata
- [ ] Verify remaining code in `projectkoios` matches approved ownership boundaries

## Validation gates per repo

For each repo touched:
- [ ] `pytest`
- [ ] `ruff check .`
- [ ] `mypy src/python`
- [ ] editable install still works
- [ ] cross-repo imports resolve in the intended multi-repo setup

## Report back to Archon

- [ ] Summarize files changed per repo
- [ ] Record validations run and results
- [ ] Record deviations from the approved plan
- [ ] List unresolved architecture questions
- [ ] Note any required follow-up ADR or boundary-map update
