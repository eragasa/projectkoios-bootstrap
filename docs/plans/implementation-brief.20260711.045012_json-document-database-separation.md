```json
{
  "title": "JSON document database separation-of-concerns brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-plan-revision-requested-enums-no-dangling-constants",
  "datetime": "20260711.050935Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "source_request": "User direction that the next slice is separation of concerns: a generalized JSON document database, initially piloted as SQLite with blobs, with ADR concerns separated by documents and likewise separated in code.",
  "scope": "separate generic JSON document database substrate from ADR-specific document mapping/projection/policy for the existing one-ADR pilot",
  "next_owner": "VULCAN_PLAN_PAUSE"
}
```

# Implementation brief 20260711.045012: JSON document database separation of concerns

## Status

VULCAN planning-ready ATHENA implementation brief from explicit user direction. This brief does not authorize coding; VULCAN must produce an implementation plan and pause before implementation.

User/HERMES correction 20260711.045316Z: this slice does not require backward compatibility. Nothing is backcompat. The implementation may intentionally replace prior pilot storage names/paths/shapes, but it must define the break/replacement behavior before code changes and preserve evidence for what changed.

ATHENA update 20260711.050017Z: the architecture next-slice section has been reduced to this brief as the active implementation slice.

User correction 20260711.050935Z: enumerated types must be represented as enumerations, and the implementation must not introduce dangling constant variables. Semantic values such as document kind/family, backend kind, source-of-truth mode, artifact disposition, or replacement action must be modeled through scoped enum/type definitions or validated schema enums, not free string constants scattered through modules.

## Objective

Refactor the completed one-ADR pilot so storage is separated into a small generalized JSON document database substrate, while ADR-specific concerns remain in ADR document code.

The intended shape is:

- a generalized JSON document database stores JSON documents by stable document identity and document-kind metadata;
- SQLite is the initial pilot backend, storing canonical JSON payloads as blobs/text plus minimal generic index columns;
- ADR-specific parsing, schema validation, naming/lifecycle metadata, Markdown projection, semantic equality, and pilot evidence remain outside the generic database substrate;
- the existing one-ADR pilot continues to be the only exercised document family and evidence slice.

## Control boundary

| Concern | Belongs in generic JSON document database substrate | Belongs in ADR document layer |
|---|---:|---:|
| Store/load/export JSON document payload by ID | Yes | No |
| SQLite connection, table creation, payload persistence | Yes | No |
| Generic document kind/type metadata | Yes | Uses `adr`/ADR-specific kind value only |
| Generic payload hash/freshness metadata | Yes | May consume/report hash evidence |
| ADR schema validation against `docs/schemas/adr.schema.json` | No | Yes |
| ADR `status`, `routing.next_phase`, lifecycle semantics | No | Yes, by referenced control surfaces |
| ADR naming, slug, filename, legacy `.draft.md` evidence | No | Yes |
| Markdown ADR projection and parse/equality policy | No | Yes |
| Pilot manifest/mapping evidence shape | No, except generic DB evidence fields | Yes |
| Bulk ADR migration or database-authority promotion | No | No |

## Required implementation shape

VULCAN should propose exact paths, but the plan should preserve these boundaries:

- generic substrate package under a non-ADR namespace such as `src/python/projectkoios/bootstrap/control_surface/documents/` and `src/python/projectkoios/bootstrap/control_surface/storage/`;
- generic tests under a matching non-ADR test namespace;
- ADR-specific code remains under `src/python/projectkoios/bootstrap/control_surface/adr/`;
- ADR storage adapter becomes a thin ADR-facing wrapper over the generic document store, or delegates to it explicitly;
- SQLite schema/table names in the generic substrate must not be ADR-specific; old ADR-specific names may be cited as historical migration evidence only;
- existing pilot artifacts under `dev/adr-json-database-one-adr-pilot/` remain pilot-local evidence and must record any migration from ADR-specific storage names to generic document-store names.

## Generic JSON document database contract

The generic substrate should support only the minimum operations needed by the current pilot:

- store one JSON object document with:
  - stable `document_id`;
  - `document_kind` or equivalent family discriminator represented by an explicit enum/type, not an unscoped string constant;
  - canonical JSON payload;
  - content hash;
  - deterministic created/updated timestamps supplied by caller/test;
- get/export one JSON object by `document_id`;
- list/query by generic `document_kind` and, only if needed, generic metadata fields chosen by the brief/plan;
- hide SQLite implementation details behind a protocol/interface;
- provide an in-memory implementation or equivalent test double so ADR tests can prove they are not coupled to SQLite.

The generic substrate must not know ADR schema fields such as `slug`, `status`, `routing`, `owner`, `next_phase`, supersession chains, projection paths, or lifecycle status.

Enumerated values must be enumerated. At minimum, VULCAN must model document kind/family and any replacement/evidence disposition values with scoped enums or schema enum definitions. Do not add dangling module-level semantic constants such as bare `DOCUMENT_KIND_ADR = "adr"`; keep semantic values owned by their enum/type or local to the call site when they are not reusable domain concepts.

## ADR layer contract

The ADR layer remains responsible for:

- mapping source Markdown evidence into ADR JSON;
- validating ADR JSON against `docs/schemas/adr.schema.json`;
- preserving source path/hash/status-suffix rationale;
- applying externally controlled ADR naming/lifecycle metadata;
- generating deterministic Markdown projection evidence;
- producing pilot manifest/mapping/database evidence;
- preserving migration evidence for the existing one-ADR pilot artifacts.

If the ADR layer needs query columns for ADR-specific fields, VULCAN must pause and propose whether those fields belong in an ADR-specific index/projection table rather than in the generic JSON document database table.

## Intentional replacement and evidence gate

Before coding, VULCAN must choose and get approval for intentional break/replacement behavior for existing pilot artifacts and code paths. Backward compatibility is not required for this slice.

The plan must state which prior pilot artifacts, adapter names, table names, output paths, and generated evidence are replaced, retained as historical evidence, or deleted if generated/local. It must not add alias/load or validate-as-is behavior merely for compatibility.

Acceptance requires a replacement/migration evidence artifact under `dev/adr-json-database-one-adr-pilot/` that records:

- old ADR-specific adapter/table/package names;
- new generic document-store adapter/table/package names;
- old and new JSON checkpoint hashes if regenerated;
- copied, normalized, inferred, and newly represented fields;
- proof that source `.draft.md` path/hash evidence is retained;
- proof that no mutable `.sqlite`/`.db` file is committed.

## Acceptance criteria

- Generic JSON document database code is separated from ADR-specific code by package/module boundary.
- Enumerated semantic values are represented as scoped enums/types or schema enums, with no dangling constant variables for document kind, backend kind, source-of-truth mode, artifact disposition, or replacement action.
- Generic substrate stores opaque JSON document payloads and generic metadata only; no ADR schema/lifecycle/projection logic appears in generic code.
- ADR layer continues to validate, project, and compare the one representative ADR without losing prior mapping provenance.
- SQLite remains an implementation of the generic document store, not the ADR architecture itself.
- Existing one-ADR pilot evidence is intentionally replaced or retained as historical evidence with explicit migration/migration evidence.
- Tests prove ADR behavior works against SQLite and a non-SQLite/test implementation or test double.
- Validation includes pytest, mypy, python policy validation, `git diff --check`, and a check that no mutable `.sqlite`/`.db` files are committed under the pilot directory.
- VULCAN pauses if generic document-store schema shape, intentional replacement behavior, or ADR/generic boundary placement is underspecified.

## Non-goals

- Bulk ADR migration.
- Repository-authoritative SQLite/database policy.
- Reusable repository-level ADR storage config.
- Generic ingestion framework for arbitrary external documents.
- Product-facing `projectkoios` document database architecture.
- ADR naming/lifecycle policy changes beyond preserving externally controlled metadata.
