# KOIOS provenance audit 20260711T065332Z: ADR JSON schemas conformance slice

## Metadata

- Type: provenance-audit
- Status: advisory-reviewed
- Acting-As: KOIOS
- Repository: projectkoios-bootstrap
- Scope: current uncommitted ADR JSON schemas conformance slice

## Audited sources

- `workspaces/athena/working/adr-json-schemas-conformance-intake.20260711.063019.md`
- `docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md`
- `docs/architecture/architecture.json-adr-storage-topology.md`
- `src/python/projectkoios/bootstrap/control_surface/adr/conformance.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/markdown.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py`
- `dev/adr-json-schemas-conformance/adr.json-schemas.json`
- `dev/adr-json-schemas-conformance/mapping.json`
- `dev/adr-json-schemas-conformance/conversion-evidence.json`
- `dev/adr-json-schemas-conformance/manifest.json`
- `dev/adr-json-schemas-conformance/database-evidence.md`

## Validation performed by KOIOS

```bash
cd ../..
uv run pytest tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py -q
# 3 passed in 0.06s

find dev/adr-json-schemas-conformance -type f \( -name '*.sqlite' -o -name '*.db' \) -print
# no output

git diff --check
# clean

git diff -- docs/schemas/adr.schema.json docs/adr/adr.json-schemas.draft.md
# no output
```

## Provenance findings

The uncommitted conformance slice is provenance-safe for its stated bounded scope.

- The ATHENA intake identifies `docs/adr/adr.json-schemas.draft.md` as the one-document conformance target and requires `routing.*`, `links.related`, source date/status/path/hash, and generated artifact hashes to be preserved outside the schema record.
- The VULCAN implementation plan scopes the work to `dev/adr-json-schemas-conformance/`, forbids source Markdown mutation, preserves source status `draft`, treats the JSON checkpoint as active going forward, and defers schema/lifecycle/workflow/storage-authority redesign.
- The generated record `dev/adr-json-schemas-conformance/adr.json-schemas.json` contains `id: adr.json-schemas`, `slug: json-schemas`, and `status: draft`; it does not contain `routing` or `links.related`.
- `conversion-evidence.json` and `mapping.json` preserve source path, source date, source hash, routing owner/next phase/notes, `links.related`, generated JSON hash, projection hash, and explicit omitted-from-record fields.
- `manifest.json` records `authority_mode: active-json-checkpoint-with-sidecar-provenance`, source Markdown `mutated: false`, `routing_allowed: false`, generic `json_documents` storage, local generated SQLite policy, and watchpoints for no docs/ADR mutation and no committed database files.
- `database-evidence.md` documents the generic `json_documents` DDL and adapter evidence for `list_by_kind(DocumentType.ADR)`, with SQLite framed as generated-local operational state only.
- No diff exists for `docs/adr/adr.json-schemas.draft.md` or `docs/schemas/adr.schema.json` in the audited state.
- No `.sqlite` or `.db` files exist under `dev/adr-json-schemas-conformance/` after the conformance runner cleanup.

## Authority boundary

This audit does not make the conformed JSON checkpoint the canonical ADR storage authority for the repository as a whole.

This audit does not promote `docs/adr/adr.json-schemas.draft.md` from `draft`, accept the JSON schemas ADR, alter UI/core architecture authority, reintroduce routing into the ADR schema, or authorize bulk ADR migration.

The active-forward claim is limited to the generated conformance artifact for this one target ADR: `dev/adr-json-schemas-conformance/adr.json-schemas.json` is treated as the active conformed record artifact for this slice while sidecars preserve conversion provenance.

## Residual watchpoints

- There is not yet a VULCAN implementation report specifically for the `adr.json-schemas` conformance implementation; the current durable implementation authority is the plan plus generated artifacts/tests.
- The architecture document has been updated to recommend an additional bounded YAGNI conformance slice; this audit confirms the current slice evidence but does not decide the next target.
- The checkpoint lives under `dev/`; any later promotion into a durable ADR storage surface needs separate architecture authority.
- Projection policy remains evidence/projection-only; generated Markdown should not be treated as ADR authority unless a later decision says so.
- Repeated conformance slices may create pressure for reusable conformance policy, schema metadata, or storage authority, but that pressure is observational only until Athena/user promotes it.

## KOIOS recommendation

Package this audit with the current conformance slice. Before committing, request or produce a VULCAN implementation report for the completed `adr.json-schemas` conformance implementation if the workflow requires a report artifact beyond the plan and tests.
