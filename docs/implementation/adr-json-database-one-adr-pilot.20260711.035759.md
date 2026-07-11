```json
{
  "title": "ADR JSON/database one-ADR pilot implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated-ready-for-athena-review",
  "datetime": "20260711.035759Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.json-adr-storage-topology.md",
  "source_brief": "docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md",
  "source_plan": "docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md",
  "representative_adr": "docs/adr/adr.json-database-for-adr-storage.draft.md"
}
```

# Implementation report 20260711.035759: ADR JSON/database one-ADR pilot

## Summary

Implemented the bounded one-ADR ADR JSON/database pilot for `docs/adr/adr.json-database-for-adr-storage.draft.md` as source evidence.

The implementation follows the approved database-operational / JSON-checkpointed mode:

- ADR mapping, schema validation, projection, and semantic equality are independent of SQLite.
- Storage access goes through a narrow adapter boundary.
- SQLite is implemented as the selected pilot adapter backend only.
- Mutable `.sqlite`/`.db` files are generated local state and are not committed.
- The committed JSON checkpoint and generated projection are explicitly pilot-derived/non-authoritative through manifest, mapping, projection, and this report.

## Files changed

### Code

- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/equality.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/hashing.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/manifest.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/markdown.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/models.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/pilot.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/storage.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/validation.py`

### Tests

- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrStoragePilot__run.py`

### Pilot evidence artifacts

- `dev/adr-json-database-one-adr-pilot/manifest.json`
- `dev/adr-json-database-one-adr-pilot/mapping.json`
- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json`
- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md`
- `dev/adr-json-database-one-adr-pilot/database-evidence.md`

### Workspace tracking

- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

## Architecture invariant evidence

| Architecture invariant / open question | Evidence produced |
|---|---|
| One representative ADR only | Tests and code use only `docs/adr/adr.json-database-for-adr-storage.draft.md`; no bulk ADR migration. |
| Plain ADR schema JSON checkpoint | `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json` validates against `docs/schemas/adr.schema.json`. |
| Status-free canonical identity | JSON checkpoint uses `id = adr.json-database-for-adr-storage`, `slug = json-database-for-adr-storage`, and `status = draft` in record content. |
| Source `.draft.md` is legacy/source evidence | `manifest.json` and `mapping.json` record the legacy source path and `.draft` filename suffix separately from canonical identity. |
| Pilot-local manifest/config | `dev/adr-json-database-one-adr-pilot/manifest.json` declares pilot status, paths, hashes, adapter policy, SQLite selection, conflict rule, and architecture/brief/plan paths. |
| Storage adapter boundary | `AdrStorageAdapter` protocol defines `store`, `get`, `export`, and `list_by_status`; `MemoryAdrStorageAdapter` test proves the boundary without SQLite. |
| SQLite as selected pilot adapter only | `SqliteAdrStorageAdapter` contains SQLite-specific DDL/connection logic; mapping, validation, projection, and equality modules do not depend on SQLite. |
| No committed mutable DB | Pilot removes generated local SQLite state after evidence capture; validation found no `.sqlite` or `.db` files under the pilot artifact directory. |
| JSON checkpoint reviewability | Manifest records JSON checkpoint path and content hash `9e2bd6ed13f8cfa2d9e8b63c444248f19da960e818f22eb3d8a516bcebefb55e`. |
| Markdown projection as evidence | `adr.json-database-for-adr-storage.projected.md` includes generated/non-authoritative marker, source record ID, schema ID, generation method, authority mode, hashes, and conflict rule. |
| Source hash preservation | Manifest records source content hash `b7e48d5b2a07c14704689b4dcae738c8f21731e6d20e8d63d8eab33c75819d87`. |
| Source date preservation despite schema gap | `mapping.json` preserves `source_date = 20260702.121432Z` outside the plain ADR schema. |
| Schema failure distinguishability | `mapping.json` records an invalid status validation error for schema failure evidence. |
| Semantic equality | Tests and pilot compare source-derived JSON, adapter-exported JSON, and projection-derived JSON under `AdrRecordComparer`. |

## Mapping notes

- `context.delegated_operator` is inferred as `HERMES` per brief and recorded in `mapping.json`.
- `routing.next_phase` is normalized from source `proposed` to schema enum `proposal` and recorded in `mapping.json`.
- `date: 20260702.121432Z` is absent from `adr.schema.json`; it is preserved in `mapping.json` rather than added to the plain schema object.
- Source filename status suffix `.draft` is recorded as source provenance only.

## Validation evidence

Commands run from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q
# 24 passed in 0.17s

uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
# Success: no issues found in 10 source files

uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
# summary: 0 finding(s), 10 file(s)

git diff --check
# clean

find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print
# no output
```

## Deviations

No intentional deviations from the approved architecture blueprint, implementation brief, or revised implementation plan.

## KOIOS terminology/provenance comment

KOIOS reviewed the user-facing characterization of whether the pilot "stood up a JSON database" and found it accurate only with bounded-pilot terminology.

Provenance-safe wording:

> Yes, for the pilot: we stood up a SQLite operational store behind an ADR storage adapter that stores schema-backed ADR JSON records and exports a reviewable JSON checkpoint. We did not create a persistent or repository-authoritative database service.

Qualifications:

- This is not a JSON-native/document database.
- This is not a persistent database service.
- This is not repository-authoritative database state.
- This is not global ADR database configuration.
- This is not bulk ADR migration.
- The JSON checkpoint is schema-valid and committed for review, but remains pilot-derived/non-authoritative unless a later ADR/action promotes the storage model.
- SQLite was exercised as the selected pilot backend behind an adapter; the architecture decision between JSON-file canonical, database-authoritative, and hybrid checkpoint remains unresolved except as pilot evidence.

KOIOS found no blocking provenance gap in the inspected artifacts. The naming/architecture watchpoint was implemented after user approval: code now lives under `projectkoios.bootstrap.control_surface.adr`, which names authority/projection/storage boundaries rather than only record data.

## Packaging update

After KOIOS comment and user approval, VULCAN moved the pilot implementation from `projectkoios.bootstrap.adr_records` to `projectkoios.bootstrap.control_surface.adr` and moved tests from `tests/projectkoios/bootstrap/adr_records/` to `tests/projectkoios/bootstrap/control_surface_adr/`.

The pilot manifest/projection generation method now records `projectkoios.bootstrap.control_surface.adr.pilot.AdrStoragePilot.run`.

## Residual risks and follow-up questions for ATHENA

- The pilot demonstrates topic-stable status-free identity, but does not decide whether future canonical ADR identity should be topic-stable, event/timestamp-stable, or another scheme.
- The plain ADR schema still lacks a field for source date/provenance timestamp; the pilot preserved that value in mapping evidence.
- The Markdown projection currently embeds the complete ADR JSON for deterministic parse-back. ATHENA should decide whether future projections should be human-readable-only, JSON-embedded, or both.
- The SQLite schema is intentionally minimal and adapter-local; future database-authoritative policy still requires an ADR decision before mutable database state can become repository authority.

## Next owner

ATHENA/user/Hermes for conformance review and architecture as-built reconciliation.
