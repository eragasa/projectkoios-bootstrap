# Implementation report 20260704.174859: Schema-record base and draft ADR record slice

## Status

Implementation complete; ready for ATHENA conformance review.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Worktree: `/Users/eugene/repos/projectkoios-bootstrap-schema-record-base`
- Branch: `vulcan/schema-record-base`
- Source artifact: `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`
- Source ADR: `docs/adr/adr.schema-base.md`
- Source workplan: `docs/plans/schema-base-adr-records-workplan.md`
- Source schemas: `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`
- Previous artifact: ATHENA implementation-ready brief
- Next expected artifact: ATHENA conformance review of this implementation report and patch

## Summary

Implemented the schema-record base slice in an isolated git worktree to avoid mixing with concurrent dirty GraphRAG/schema-record changes in the original checkout.

Changed files:

- `pyproject.toml`
  - Added `jsonschema>=4.25.1` as the JSON Schema draft 2020-12 validation dependency.
- `src/python/projectkoios/bootstrap/schemas/__init__.py`
  - Exposes the schemas package API.
- `src/python/projectkoios/bootstrap/schemas/paths.py`
  - Defines repository/schema paths and rejects legacy schema files as non-canonical.
- `src/python/projectkoios/bootstrap/schemas/schemas.py`
  - Loads canonical schemas from `docs/schemas/`.
  - Builds an offline local registry for `https://projectkoios.local/schemas/<filename>`.
  - Validates with `jsonschema.Draft202012Validator` and `referencing.Registry`.
- `src/python/projectkoios/bootstrap/schemas/models.py`
  - Adds immutable dataclass models for schema records, draft ADR records, sections, concerns, rejected Markdown, and metadata.
  - Validates `SchemaRecordBase` and `DraftAdrRecord` construction against the local JSON Schema registry.
- `src/python/projectkoios/bootstrap/schemas/adr_markdown.py`
  - Adds deterministic draft ADR JSON-to-Markdown rendering.
  - Adds strict controlled Markdown-to-JSON ingest.
  - Fails fatally for missing metadata, missing/out-of-order sections, malformed concern keywords, ambiguous heading depth, and over-600-character required section descriptions.
  - Captures deterministic extra top-level sections under `content.rejected`.
- `tests/projectkoios/bootstrap/schemas/test__SchemaRegistry__validate.py`
  - Covers schema loading, local registry resolution, top-level envelope validation, metadata requirements through `allOf`, draft ADR schema narrowing, and non-canonical legacy schema rejection.
- `tests/projectkoios/bootstrap/schemas/test__DraftAdrRecord__markdown.py`
  - Covers immutable model construction, renderer ordering, JSON -> Markdown -> JSON round trip, fatal ingest failures, rejected extra-section capture, and 600-character description enforcement.

## Validation evidence

Commands run from `/Users/eugene/repos/projectkoios-bootstrap-schema-record-base`:

```bash
uv run python -m json.tool docs/schemas/schema.record-base.json >/dev/null
uv run python -m json.tool docs/schemas/adr-draft.schema.json >/dev/null
uv run pytest tests/projectkoios/bootstrap/schemas -q
```

Result:

```text
17 passed in 0.11s
```

Broader validation:

```bash
uv run pytest -q
```

Result:

```text
192 passed in 1.28s
```

Validation note: `uv run` created an isolated `.venv` in the schema-record worktree and warned that the original checkout's `VIRTUAL_ENV=/Users/eugene/repos/projectkoios-bootstrap/.venv` did not match the worktree environment. The warning did not affect test results.

## Validator/API decision

The implementation uses:

- `jsonschema.Draft202012Validator` for JSON Schema draft 2020-12 validation;
- `referencing.Registry` and `Resource.from_contents` for offline project-local `$id` resolution.

`jsonschema>=4.25.1` was added as a runtime dependency because the implementation brief required draft 2020-12 validation with explicit local `$id` resolution. `referencing` is used through the validator stack installed with `jsonschema`.

## Deviations

- Package boundary was renamed from the brief's recommended `src/python/projectkoios/bootstrap/schema_records/` to `src/python/projectkoios/bootstrap/schemas/` after user correction. The implementation remains outside `projectkoios.ingestors` and retains the same bounded behavior.
- No CLI integration was added; this matches the brief's non-goals.
- No active/completed/superseded/rejected ADR states were implemented; only `DraftAdrRecord` was added.
- No historical ADR migration was attempted.
- Required-section description overflow is treated as a fatal ingest error rather than `content.rejected` capture because preserving the required section while moving overflow would be lossy for the first slice.
- The first-slice ingester rejects `###` subsections inside required sections as unsupported rather than trying to map them. This keeps metadata/content separation deterministic and can be widened in a later schema-controlled slice.

## Worktree separation

Implementation occurred in `/Users/eugene/repos/projectkoios-bootstrap-schema-record-base` on branch `vulcan/schema-record-base`. The original checkout remains available separately with its concurrent dirty GraphRAG/schema-record state.

## Current status

The schema-record base implementation is complete in the isolated worktree and ready for ATHENA conformance review after the user decides whether to commit, merge, or further review the branch.
