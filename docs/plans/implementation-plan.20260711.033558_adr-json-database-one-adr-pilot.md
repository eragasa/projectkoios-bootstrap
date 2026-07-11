```json
{
  "title": "ADR JSON/database one-ADR pilot implementation plan",
  "artifact_type": "implementation-plan",
  "status": "storage-adapter-revised-approval-required-before-coding",
  "datetime": "20260711.034817Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_architecture": "docs/architecture/architecture.json-adr-storage-topology.md",
  "source_brief": "docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md",
  "representative_adr": "docs/adr/adr.json-database-for-adr-storage.draft.md",
  "approval_gate": "Coding begins only after user/Hermes approval of this plan."
}
```

# Implementation plan 20260711.033558: ADR JSON/database one-ADR pilot

## Status

Approval required before coding. This plan intentionally stops before implementation.

## Provenance

- Acting-As: VULCAN
- Repository: `projectkoios-bootstrap`
- Workspace: `workspaces/vulcan/`
- Architecture blueprint: `docs/architecture/architecture.json-adr-storage-topology.md`
- Implementation brief: `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`
- Representative legacy/source ADR fixture: `docs/adr/adr.json-database-for-adr-storage.draft.md`
- Canonical pilot record identity: `id = adr.json-database-for-adr-storage`, `slug = json-database-for-adr-storage`, `status = draft` inside record content
- Schema: `docs/schemas/adr.schema.json`

## Scope

Implement only a one-ADR pilot using `docs/adr/adr.json-database-for-adr-storage.draft.md` as legacy/source evidence after approval.

The implementation will optimize for decision evidence with minimal code. It will not build a reusable ingestion framework, will not bulk-migrate ADRs, and will not overwrite the hand-authored source ADR.

Canonical generated identities and filenames must not encode `.draft` as part of the record identity. The source filename's `.draft` suffix is legacy/source evidence only. The ADR status belongs inside the structured record content as `status = draft`.

## Proposed implementation approach

Use a narrow Python package under `projectkoios.bootstrap.adr_records` to:

1. map the one source Markdown ADR into a plain `adr.schema.json` JSON object;
2. validate the JSON object with the local schema registry or equivalent offline JSON Schema validator;
3. access ADR storage through a narrow storage adapter boundary;
4. use SQLite only as the approved pilot adapter implementation behind that boundary;
5. load the object into generated local SQLite operational storage via the adapter;
6. export the stored row back through the adapter to schema-backed JSON checkpoint form;
7. render a deterministic Markdown projection to a pilot artifact path;
8. compare original JSON, adapter-exported JSON, and projection-derived/mapped JSON under an explicit semantic equality policy;
9. write a committed pilot manifest/config and evidence index at `dev/adr-json-database-one-adr-pilot/manifest.json`;
10. write inspectable pilot evidence without committing a mutable `.sqlite`/`.db` authority file.

ADR mapping, validation, projection, and equality logic must not depend directly on SQLite. SQLite-specific code should be isolated to the pilot SQLite adapter.

## Decision table for approval

| Decision area | Proposed choice | Proposed paths/details | Evidence produced | Approval question |
|---|---|---|---|---|
| Pilot boundary | Exactly one legacy/source ADR fixture | Source only: `docs/adr/adr.json-database-for-adr-storage.draft.md`; treat `.draft` in filename as source evidence, not canonical identity | Test guardrails proving no other ADR fixture is used; mapping evidence records source filename/status separation | Approve one-fixture-only implementation? |
| Package path | Add narrow pilot package, not a reusable framework | `src/python/projectkoios/bootstrap/adr_records/` | Small modules for mapping, validation, storage adapter boundary, SQLite adapter, projection, equality | Approve this package boundary? |
| Test path | Add focused tests for the pilot | `tests/projectkoios/bootstrap/adr_records/` | Unit tests for schema validation, fixture guard, storage adapter contract, SQLite adapter export, projection stability, equality | Approve focused test surface? |
| JSON checkpoint/export shape | Primary artifact is a plain `docs/schemas/adr.schema.json` object with status-free canonical identity | `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json`; `id = adr.json-database-for-adr-storage`; `slug = json-database-for-adr-storage`; `status = draft` inside record content; required schema fields only, optional `links` as present/mapped | Schema validation result; semantic equality comparison; mapping evidence records source `.draft` filename as legacy/source evidence | Approve plain ADR schema instance with identity/status separation as checkpoint? |
| Pilot manifest/config | Add committed pilot-local manifest/config and evidence index | `dev/adr-json-database-one-adr-pilot/manifest.json`; configuration for this slice stays under `dev/adr-json-database-one-adr-pilot/`, not reusable/global ADR storage config | Declares pilot status, source/checkpoint/projection paths and hashes, identity/status rule, SQLite policy, schema info, generation method, conflict rule, validation/evidence paths, and controlling architecture/brief/plan paths | Approve pilot-local manifest/config artifact? |
| Mapping metadata shape | Keep projection/source metadata separate from plain ADR record | `dev/adr-json-database-one-adr-pilot/mapping.json` and/or `mapping.md` | Copied-vs-inferred-vs-normalized field table, including source path with `.draft`, canonical status-free ID/slug, `status = draft`, `delegated_operator`, `date`, source hash, JSON hash, and `proposed -> proposal` | Approve sidecar metadata rather than schema wrapper? |
| Storage adapter boundary | Add a minimal adapter interface between ADR workflow logic and backend storage | Proposed operations: `store(record)`, `get(record_id)`, `export(record_id)`, and a minimal query/list operation for decision evidence; ADR mapping/validation/projection/equality call the boundary, not SQLite | Adapter contract tests prove non-SQLite logic is isolated from backend details | Approve narrow adapter boundary? |
| SQLite adapter/backend | SQLite is the selected pilot adapter implementation and operational/local generated state | Temp path in test/run output such as `.tmp/adr-json-database-one-adr-pilot/pilot.sqlite` or pytest `tmp_path`; no `.sqlite`/`.db` committed | SQL schema text, adapter load/export transcript, checksum/query evidence in committed Markdown | Approve SQLite as one adapter behind the boundary? |
| SQLite adapter/schema shape | Minimal SQLite adapter table holding schema-backed ADR JSON plus query fields | Table `adr_records(id TEXT PRIMARY KEY, slug TEXT NOT NULL, title TEXT NOT NULL, status TEXT NOT NULL, routing_owner TEXT NOT NULL, routing_next_phase TEXT NOT NULL, schema_id TEXT NOT NULL, content_hash TEXT NOT NULL, record_json TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)` | Demonstrates backend query/update surface behind the adapter without inventing a generalized database framework | Approve one-table SQLite adapter schema? |
| SQL evidence | Commit reviewable DB evidence, not DB file | `dev/adr-json-database-one-adr-pilot/database-evidence.md`; optional `.sql` schema/dump text if useful | Schema DDL, representative insert/export/query, record hash, statement of non-committed DB file | Approve text evidence over committed SQLite file? |
| Markdown projection path | Write generated projection outside `docs/adr/` to avoid overwriting source draft, using status-free canonical artifact filename | `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md` | Deterministic projection fixture and byte-stability test; projection metadata cites legacy source path | Approve dev-local generated projection path? |
| Markdown projection metadata | Projection starts with explicit generated/pilot metadata | Include source record ID, schema ID, generation method, source-of-truth mode `database-operational/json-checkpointed`, derivative/non-authoritative marker, source hash, conflict rule | Projection invariant test | Approve this metadata banner/frontmatter? |
| Projection parse-back | Keep parse-back narrow and deterministic | Map the generated projection back to the same ADR schema fields where feasible; projection metadata is checked separately | Equality test distinguishing ADR content equality from projection metadata checks | Approve projection-derived equality scope? |
| Semantic equality policy | Compare all schema fields in the ADR record; exclude projection-only metadata | Normalization `routing.next_phase: proposed -> proposal` allowed only with mapping evidence; inferred `context.delegated_operator: HERMES` allowed only as marked pilot metadata; source `date` preserved in sidecar/report | Equality test and report section | Approve this equality policy? |
| Validation commands | Use brief-requested validation surface | `uv run pytest tests/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/schema -q`; `uv run mypy src/python/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/adr_records`; `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/adr_records`; `git diff --check` | Test results in implementation report | Approve these commands? |
| Implementation report | Produce VULCAN report mapped back to architecture invariants | `docs/implementation/adr-json-database-one-adr-pilot.20260711.<time>.md` | Deviations, validation results, authority-model evidence, follow-up ADR/schema questions | Approve report target? |
| Architecture reconciliation | Do not edit architecture as VULCAN implementation authority | VULCAN report will identify evidence for ATHENA to revise `docs/architecture/architecture.json-adr-storage-topology.md` into as-built documentation | Clear handoff to ATHENA/user/Hermes | Approve no architecture edits during coding unless explicitly requested? |

## Proposed JSON checkpoint shape

The primary checkpoint will be a plain object conforming to `docs/schemas/adr.schema.json`.

Expected field mapping for the source fixture:

| JSON field | Source/mapping rule |
|---|---|
| `id` | Deterministic status-free canonical ID: `adr.json-database-for-adr-storage` |
| `slug` | Deterministic status-free canonical slug: `json-database-for-adr-storage` |
| `title` | From ADR H1 title text |
| `status` | From `## Status`: `draft`; status lives inside record content, not in canonical ID or artifact stem |
| `context.origin` | From `Origin: user request` |
| `context.from` | From `From: HERMES` |
| `context.acting_as` | From `Acting-As: HERMES` |
| `context.scope` | From `Scope: projectkoios-bootstrap` |
| `context.repository` | From `Repository: projectkoios-bootstrap` |
| `context.delegated_operator` | Inferred as `HERMES` per brief; recorded as inferred pilot metadata |
| `context.architecture_domain` | From `Architecture-Domain: software` |
| `decision`, `consequences`, `architecture_spec`, `implementation_brief` | From corresponding Markdown sections |
| `acceptance_criteria`, `resolved_open_questions`, `non_goals`, `validation_expectations` | From bullet lists in corresponding Markdown sections |
| `routing.owner` | Normalize source `Athena` if needed to schema enum spelling |
| `routing.next_phase` | Normalize source `proposed` to schema enum `proposal`; record as normalization |
| `routing.notes` | From routing notes |
| `links` | From links section, preserving `None` as `null` where schema allows |

The source date `20260702.121432Z` will not be added to the ADR schema object because the schema does not define a date field. It will be preserved in mapping evidence and the implementation report.

The source filename `adr.json-database-for-adr-storage.draft.md` will be preserved in mapping evidence as legacy/source provenance. The canonical generated identity separates status from identity: `id = adr.json-database-for-adr-storage`, `slug = json-database-for-adr-storage`, and `status = draft` in the ADR record.

## Proposed pilot manifest/config shape

Add committed pilot-local manifest/config and evidence index at:

```text
dev/adr-json-database-one-adr-pilot/manifest.json
```

The manifest is not a reusable/global ADR storage configuration. It is bounded pilot configuration and evidence index for this slice only.

Minimum proposed manifest fields:

| Manifest field | Proposed content |
|---|---|
| `pilot.name` | `adr-json-database-one-adr-pilot` |
| `pilot.status` | `non-authoritative-pilot` |
| `source_adr.path` | `docs/adr/adr.json-database-for-adr-storage.draft.md` |
| `source_adr.content_hash` | Hash of the source Markdown content computed during implementation |
| `canonical_record.id` | `adr.json-database-for-adr-storage` |
| `canonical_record.slug` | `json-database-for-adr-storage` |
| `canonical_record.status_location_rule` | Lifecycle status belongs in record content, not filename/record identity |
| `json_checkpoint.path` | `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json` |
| `json_checkpoint.content_hash` | Hash of the generated JSON checkpoint computed during implementation |
| `markdown_projection.path` | `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md` |
| `storage_adapter.policy` | ADR mapping, validation, projection, and equality use a narrow storage adapter boundary and do not depend directly on SQLite |
| `storage_adapter.selected` | `sqlite` for this pilot |
| `sqlite_operational_store.policy` | Mutable `.sqlite`/`.db` files are local/generated and not committed |
| `schema.path` | `docs/schemas/adr.schema.json` |
| `schema.id` | Schema `$id` from the schema when available |
| `generation.method` | Tool/function entry point used to generate the pilot artifacts once implemented |
| `conflict_rule` | Source Markdown remains migration evidence; SQLite is local operational state; JSON checkpoint is committed review checkpoint; generated Markdown projection is non-authoritative pilot evidence |
| `evidence.paths` | Mapping evidence, database evidence, validation output/report paths |
| `architecture.path` | `docs/architecture/architecture.json-adr-storage-topology.md` |
| `brief.path` | `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md` |
| `plan.path` | `docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md` |

The manifest will explicitly carry KOIOS watchpoints: non-authoritative pilot markers, source hash, JSON hash, no database committed, no `docs/adr` mutation, and evidence mapped to architecture invariants.

## Proposed storage adapter boundary

Add a minimal storage adapter boundary inside `src/python/projectkoios/bootstrap/adr_records/` so backend storage is replaceable for evidence purposes without turning the pilot into a generic database framework.

Proposed boundary shape:

| Adapter operation | Purpose |
|---|---|
| `store(record)` | Persist one schema-backed ADR record into the selected backend |
| `get(record_id)` | Retrieve one ADR record by canonical ID |
| `export(record_id)` | Return the stored record in schema-backed JSON checkpoint form |
| `list/query` minimal operation | Exercise title/status/routing lookup evidence without committing to a broad query framework |

Rules:

- mapping Markdown to ADR JSON does not import or call SQLite;
- schema validation does not import or call SQLite;
- Markdown projection does not import or call SQLite;
- semantic equality does not import or call SQLite;
- only the SQLite adapter implementation contains SQLite-specific DDL/connection logic;
- workflow code may select the SQLite adapter for this pilot through the manifest/config.

## Proposed SQLite adapter/schema shape

The SQLite database will be generated locally during tests/runs through the SQLite adapter. The mutable database file will not be committed.

Proposed DDL shape:

```sql
CREATE TABLE adr_records (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  routing_owner TEXT NOT NULL,
  routing_next_phase TEXT NOT NULL,
  schema_id TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  record_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

Rationale: this table exercises database-operational behavior and query fields behind the adapter while keeping the authoritative ADR content as schema-backed JSON. It avoids prematurely designing a normalized ADR database framework.

## Proposed Markdown projection approach

Generated projection will be written to:

```text
dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md
```

The projection will include a generated metadata block or banner that states:

- generated pilot derivative/non-authoritative status;
- source record ID (`adr.json-database-for-adr-storage`);
- canonical slug (`json-database-for-adr-storage`) and record status (`draft`) as separate values;
- legacy/source path (`docs/adr/adr.json-database-for-adr-storage.draft.md`);
- schema ID/version or `$id`;
- generation method;
- source-of-truth mode: `database-operational / JSON-checkpointed`;
- source content hash and JSON checkpoint hash or equivalent freshness markers;
- non-authoritative pilot derivative marker;
- conflict rule: hand-authored Markdown source remains migration evidence; structured JSON checkpoint is the committed review checkpoint for this pilot; mutable SQLite is local operational state.

The projection will preserve the ADR sections when present and render deterministically for unchanged source content.

## Authority-model evidence the pilot will produce

The pilot will produce evidence for the three candidate models without changing repository authority. The manifest will index the evidence, make the configured authority mode inspectable, and declare SQLite as the selected pilot adapter rather than as the storage architecture itself.

| Authority model | Pilot evidence |
|---|---|
| JSON-file canonical | Plain schema-valid JSON checkpoint in git; reviewable JSON diff; equality against source-derived semantics |
| Database-authoritative | SQLite operational load/query/export transcript and schema evidence; report limitations of not committing mutable database authority |
| Database-operational / JSON-checkpointed | End-to-end workflow where SQLite is exercised operationally through the adapter, JSON checkpoint is committed/reviewable, and Markdown is generated projection evidence |

The implementation report will state that repository-authoritative database storage remains recommendation-only unless a follow-up ADR authorizes it.

## Deviations from architecture blueprint or brief

No intentional deviations are proposed.

Potential approval-sensitive details:

- The plan proposes a narrow storage adapter boundary; SQLite is the selected pilot adapter implementation, not a direct dependency for mapping/validation/projection/equality logic.
- The plan proposes a committed pilot-local manifest/config at `dev/adr-json-database-one-adr-pilot/manifest.json`; no reusable/global ADR storage config is proposed.
- The plan proposes status-free canonical generated artifact names and record identity; `.draft` remains only in the legacy/source path and `status = draft` remains record content.
- The plan proposes a sidecar mapping artifact because `adr.schema.json` is a plain ADR object and does not contain projection/source metadata fields.
- The plan proposes generated projection under `dev/` rather than `docs/adr/` to avoid overwriting the source draft and to keep the hand-authored source as migration evidence.
- The plan proposes SQL text/evidence in git, not a committed mutable SQLite file.

If any of these are rejected, VULCAN should revise this plan before coding.

## Validation plan

After approval and implementation, run:

```bash
uv run pytest tests/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/schema -q
uv run mypy src/python/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/adr_records
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/adr_records
git diff --check
```

The implementation report will record exact command outputs.

## Revision note

Revised at `20260711.034111Z` to separate canonical identity from status: source `.draft` filename is legacy/source evidence only; canonical generated IDs and filenames use `adr.json-database-for-adr-storage`; record content carries `status = draft`.

Revised at `20260711.034700Z` to add the committed pilot-local manifest/config and evidence index at `dev/adr-json-database-one-adr-pilot/manifest.json`, while keeping configuration for this slice under the pilot `dev/` directory and not introducing reusable/global ADR storage config.

Revised at `20260711.034817Z` to add a narrow storage adapter boundary and clarify that SQLite is the approved pilot adapter implementation behind that boundary, not a direct dependency of ADR mapping, validation, projection, or equality logic.

## Approval gate

Coding must not begin until user/Hermes approves this revised plan or provides revisions.
