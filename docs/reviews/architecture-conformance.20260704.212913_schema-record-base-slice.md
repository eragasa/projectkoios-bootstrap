# Architecture conformance review 20260704.212913: Schema-record base slice

## Status

conforms-with-gaps

## Provenance

- Acting-As: ATHENA
- Repository: projectkoios-bootstrap
- Workspace: workspaces/athena/
- Review type: bounded architecture-conformance review
- Scope: schema-record base and draft ADR record implementation slice
- Outcome vocabulary: `conforms`, `conforms-with-gaps`, `deviation-found`, `insufficient-evidence`

## Review packet

### Controlling source artifacts

- `docs/adr/adr.schema-base.md`
- `docs/plans/schema-base-adr-records-workplan.md`
- `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`
- `docs/schemas/README.md`
- `docs/schemas/schema.record-base.json`
- `docs/schemas/adr-draft.schema.json`

### Implementation and validation evidence

- `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`
- `docs/implementation/implementation-report.20260704.205637_schema-package-policy-remediation.md`
- Current local validation, run from `/Users/eugene/repos/projectkoios-bootstrap` on 20260704.212913:

```text
uv run python -m json.tool docs/schemas/schema.record-base.json >/dev/null
uv run python -m json.tool docs/schemas/adr-draft.schema.json >/dev/null
uv run pytest tests/projectkoios/bootstrap/schema -q
17 passed in 0.11s
uv run pytest -q
209 passed in 1.05s
```

Supplemental local validation, run from `/Users/eugene/repos/projectkoios-bootstrap` after Vulcan's review-activity response:

```text
uv run pytest tests/projectkoios/bootstrap/schema tests/projectkoios/bootstrap/python_policy -q
34 passed in 0.12s
uv run mypy src/python/projectkoios/bootstrap/schema src/python/projectkoios/bootstrap/python_policy
Success: no issues found in 10 source files
Python policy validator against src/python/projectkoios/bootstrap/schema
findings 0
```

### Changed files under review

Primary schema-record implementation surface:

- `pyproject.toml`
- `src/python/projectkoios/bootstrap/schema/__init__.py`
- `src/python/projectkoios/bootstrap/schema/paths.py`
- `src/python/projectkoios/bootstrap/schema/schemas.py`
- `src/python/projectkoios/bootstrap/schema/models.py`
- `src/python/projectkoios/bootstrap/schema/adr_markdown.py`
- `tests/projectkoios/bootstrap/schema/test__SchemaRegistry__validate.py`
- `tests/projectkoios/bootstrap/schema/test__DraftAdrRecord__markdown.py`

Supporting/report artifacts reviewed:

- `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`
- `docs/implementation/implementation-report.20260704.205637_schema-package-policy-remediation.md`
- `docs/AAR/aar.20260704.174859_schema-record-worktree-implementation.md`
- `docs/AAR/aar.20260704.205637_schema-package-policy-remediation.md`

Observed history also includes the package rename from `projectkoios.bootstrap.schemas` to `projectkoios.bootstrap.schema` in commit `dc41aa1`.

### Declared non-goals and exclusions

The review excludes:

- GraphRAG behavior changes;
- implementation under `projectkoios.ingestors`;
- CLI integration except isolated test support;
- active/completed/superseded/rejected ADR record implementations;
- implementation-report or workspace-state record families;
- broad historical ADR migration;
- legacy schema reconciliation beyond treating legacy files as non-canonical;
- product architecture decisions;
- database, vector-store, or renderer productization behavior;
- ADR status promotion for `docs/adr/adr.schema-base.md`.

Current original-checkout dirty state is limited to Athena workspace control files at review time:

```text
M workspaces/athena/active.md
M workspaces/athena/state.md
```

## Conformance findings

### Artifact chain

Finding: conforms.

- Source architecture artifact exists at `docs/adr/adr.schema-base.md` and remains `status: draft`.
- Workplan and implementation brief exist and declare authority boundary, scope, non-goals, and package boundary.
- Vulcan implementation reports exist and cite changed files and validation evidence.
- Validation evidence exists in reports and was locally re-run for JSON syntax and pytest coverage.
- This review cites repository files and local command output, not hidden chat/intercom as sole authority.

### Scope boundary

Finding: conforms.

- Current implementation lives under `src/python/projectkoios/bootstrap/schema/`, outside `src/python/projectkoios/ingestors/`.
- Tests live under `tests/projectkoios/bootstrap/schema/`.
- No GraphRAG files are included in the reviewed implementation surface.
- The package-boundary deviation from the original recommendation, `schema_records/` to `schema/`, is reported by Vulcan and remains architecture-compatible because the brief allowed equivalent package paths when documented.
- No automatic ADR status promotion was observed; the source ADR remains draft.

### Schema namespace and schema contracts

Finding: conforms.

- `docs/schemas/README.md` declares `docs/schemas/` as canonical and marks `legacy-*` files as migration markers.
- `schema.record-base.json` defines exactly the top-level `metadata` and `content` envelope with `additionalProperties: false` and the settled metadata fields.
- `adr-draft.schema.json` composes with the base schema through `$ref` and `allOf`, narrows `metadata.schema_id`, narrows `metadata.status` to `draft`, and constrains family-owned draft ADR content.
- The implementation provides offline project-local schema resolution using `jsonschema.Draft202012Validator`, `referencing.Registry`, and `Resource.from_contents`.
- Dependency additions `jsonschema>=4.25.1` and `types-jsonschema>=4.25.1.20250822` are acceptable for this slice because the brief required draft 2020-12 JSON Schema validation, offline `$id` resolution, and type-checkable implementation code.
- Tests cover canonical schema loading, offline `$id` resolution, top-level envelope rejection, base metadata requirements through `allOf`, draft ADR narrowing, and legacy schema rejection.

### Model, renderer, and ingester behavior

Finding: conforms-with-gaps.

Conforming evidence:

- `DraftAdrRecord.from_dict` validates against `adr-draft.schema.json` before constructing the record.
- `SchemaRecordBase.from_dict` validates against `schema.record-base.json` before constructing the base record.
- Renderer output is deterministic by section order and concern keyword order.
- Metadata title is projected into the Markdown heading and checked by ingest.
- Ingest fails for missing metadata, missing/out-of-order required sections, malformed concern keywords, ambiguous heading depth, unsupported first-slice subsections, and over-600-character required descriptions.
- Deterministic extra top-level sections are captured under `content.rejected`.
- Round-trip tests prove JSON -> Markdown -> JSON preservation for the fixture surface.

Gap:

- The implementation presents immutable dataclass wrappers, but metadata and some generic content mappings are frozen only shallowly. `RecordMetadata.from_dict` and `SchemaRecordBase.from_dict` use shallow `MappingProxyType(dict(value))`; nested dictionaries/lists from the input can remain mutable by reference. This is weaker than the brief's `immutable construction from valid dictionaries/JSON` requirement and should be remediated or explicitly narrowed before the immutable-record claim is treated as fully satisfied.

This gap does not invalidate the schema envelope, namespace, renderer/ingester contract, or bounded package placement, but it does mean the immutability guarantee is not fully proven.

### Validator-of-record coverage

Finding: conforms.

- JSON syntax validation was run locally for both controlling schemas.
- Schema and implementation behavior are covered by focused tests: `17 passed`.
- Broader repository pytest passed locally: `209 passed`.
- Vulcan separately reports Python policy validation and mypy success for the schema package in `docs/implementation/implementation-report.20260704.205637_schema-package-policy-remediation.md`; Athena also re-ran the focused schema/python-policy tests, mypy checks, and schema-package Python policy validator after receiving Vulcan's review-activity response.
- Athena owns this architecture-conformance finding; no Koios knowledge promotion is performed in this review.

## Known gaps and waivers

- Gap: shallow immutability in metadata/generic mappings as described above.
- Waiver accepted for this conformance review: package path `src/python/projectkoios/bootstrap/schema/` rather than the brief's recommended `schema_records/`, because the deviation is documented, user-corrected, outside ingestors, and behaviorally equivalent for this slice.
- No waiver is granted for ADR status promotion; `docs/adr/adr.schema-base.md` remains draft.
- No waiver is granted for broad historical migration; it remains excluded.

## Architecture decision

Outcome: `conforms-with-gaps`.

The implemented schema-record base slice conforms to the controlling architecture on namespace, base envelope, ADR-family schema composition, offline validator strategy, bounded package placement, deterministic renderer/ingester behavior, and validation coverage.

The only architecture-relevant gap found is the shallow immutability of metadata/generic mappings. Vulcan should either deepen immutability/copying for schema-record models or update the implementation report with a precise limitation and tests that prove the accepted immutability boundary. Until then, Athena should not promote the immutable-record guarantee as fully satisfied.

## Next transition

- Owner: VULCAN if remediating the shallow immutability gap.
- Owner: ATHENA if drafting a follow-up brief for deeper immutable record semantics or next schema-family slice.
- Owner: HERMES/user if deciding commit/staging boundaries for the remaining Athena workspace-state modifications.
