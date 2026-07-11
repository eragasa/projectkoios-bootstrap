```json
{
  "title": "One-ADR schema-backed JSON/database pilot brief",
  "artifact_type": "implementation-brief",
  "status": "architecture-planning-ready-koios-vulcan-watchpoints-incorporated",
  "datetime": "20260709.014124Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "source_request": "HERMES/user architecture-intake for JSON-authoritative/database-backed ADR direction",
  "scope": "one representative ADR only; no bulk migration",
  "next_owner": "USER_OR_HERMES_THEN_VULCAN"
}
```

# Implementation brief 20260709.014124: One-ADR schema-backed JSON/database pilot

## Status

Architecture planning brief. This brief is implementation-ready only after user/Hermes approval of the bounded pilot scope. It does not authorize bulk ADR migration, authoritative ADR rewrites, or promotion of draft ADRs.

## Provenance

- Acting-As: ATHENA
- Repository: `projectkoios-bootstrap`
- Workspace: `workspaces/athena/`
- User direction relayed by HERMES intercom from session `subagent-chat-019f3fe8`: move toward ADRs being JSON-authoritative, stored on a database implementation, with `docs/adr/` becoming a projection surface of JSON.
- Source-request durability note: the originating user direction is currently a relayed intercom/session input, not yet a durable ADR or committed request artifact. Any follow-up ADR revision or replacement must preserve this provenance as relayed/non-durable input unless Hermes creates a durable intake artifact.
- KOIOS provenance review relayed by session `subagent-chat-019f4487`: incorporated watchpoints on derivative pilot artifacts, source draft preservation, schema/projection metadata gaps, mapping normalization, inspectable DB evidence, round-trip equality policy, and evidence-vs-recommendation separation.
- VULCAN implementability review relayed by session `subagent-chat-019f4471`: incorporated clarifications on schema shape, fixture normalization rules, output paths, implemented authority mode, test expectations, semantic equality policy, validation commands, and package boundary.
- Existing decision candidate: `docs/adr/adr.json-database-for-adr-storage.draft.md`
- Architecture surface: `docs/architecture/architecture.json-adr-storage-topology.md`
- Existing tension: that draft currently says JSON files on disk are canonical and SQLite may be index/cache only; user direction may require revising or superseding that authority model.
- Related schemas:
  - `docs/schemas/adr.schema.json`
  - `docs/schemas/schema.record-base.json`

## Objective

Run a one-ADR pilot that proves, with inspectable artifacts, whether a schema-backed ADR record can be treated as the canonical structured ADR authority while `docs/adr/` is a deterministic Markdown projection surface.

The pilot must implement against the architecture blueprint in `docs/architecture/architecture.json-adr-storage-topology.md`. The implementation brief is subordinate to that blueprint. After implementation, ATHENA must use the implementation report and validation evidence to revise the architecture document into as-built documentation or record why the delivered pilot should not be treated as the as-built system.

The pilot must explicitly compare authority models for JSON record, database row/document, and Markdown projection before any bulk ADR migration begins.

## Representative ADR for pilot

Use exactly one representative source ADR:

```text
docs/adr/adr.json-database-for-adr-storage.draft.md
```

Rationale: this ADR already expresses the storage-authority question and exposes the current conflict between "JSON files canonical, SQLite cache" and the user's newer database-authoritative direction.

If VULCAN determines this ADR is unsuitable as a fixture, stop and produce a deviation report proposing one alternate ADR. Do not proceed with multiple ADRs.

## Authority model questions to resolve in the pilot

The pilot must produce an explicit comparison of these authority models:

1. **JSON-file canonical model**
   - A schema-backed JSON ADR file is the durable source of truth in git.
   - Database rows/documents are derived index/cache.
   - `docs/adr/*.md` files are generated or editable projections, as separately declared.

2. **Database-authoritative model**
   - A database row/document is the durable source of truth.
   - JSON files on disk, if present, are export/projection/checkpoint artifacts.
   - `docs/adr/*.md` files are projection surfaces generated from the database-backed record.

3. **Hybrid checkpoint model**
   - A database is operationally authoritative for workflows.
   - A schema-backed JSON export in git is the reviewable/checkpoint authority for repo history.
   - Projection metadata declares how conflicts between DB state, JSON checkpoint, and Markdown projection are resolved.

The pilot may recommend one model, but must not silently change repository authority. Any durable change to ADR storage authority requires a follow-up ADR revision, replacement, or acceptance action.

## Implemented authority mode for this pilot

The first implementation must exercise a **database-operational / JSON-checkpointed pilot** model.

For this pilot:

- SQLite is the operational store exercised by the pilot workflow during ingest, update/query as needed, export, and projection.
- The schema-backed JSON ADR export is the committed, reviewable checkpoint for repository history and code review.
- The SQLite database file is generated/local pilot state and must not be committed as mutable repository authority.
- The Markdown projection is generated pilot evidence and must not overwrite the hand-authored source ADR unless the user explicitly authorizes that overwrite.
- Database-authoritative storage may be exercised operationally within the pilot and analyzed as a future authority model, but repository authority must remain JSON-checkpointed until a follow-up ADR authorizes a stronger database-authoritative policy.

## Schema shape and fixture mapping rules

`docs/schemas/adr.schema.json` is currently a plain ADR object schema, not a `schema.record-base.json` envelope. VULCAN must produce and validate a plain `adr.schema.json` instance as the primary pilot ADR record.

If VULCAN also needs envelope/projection metadata for pilot evidence, keep it as a separate pilot metadata wrapper or sidecar. Do not require the same artifact to validate simultaneously as both `adr.schema.json` and `schema.record-base.json`. If this separation is insufficient, stop and produce a schema revision request or deviation report.

Fixture mapping rules for `docs/adr/adr.json-database-for-adr-storage.draft.md`:

- `context.delegated_operator`: required by schema and absent from the source Markdown. Set deterministically to `HERMES` for this pilot because the source ADR provenance says `From: HERMES`; record this as inferred pilot metadata, not a copied source claim.
- `date: 20260702.121432Z`: present under Markdown status but absent from `adr.schema.json`. Preserve it in pilot metadata, source notes, or implementation report; do not add it to the plain ADR schema instance unless a schema revision is approved.
- `routing.next_phase`: normalize source value `proposed` to schema enum value `proposal`; record the normalization in mapping evidence.
- All other defaults, normalizations, or inferred fields must be listed in the implementation report with copied-vs-inferred provenance.


## Storage implementation choice and repo/git implications

The pilot design must document the intended storage backend and its git consequences before implementation.

Minimum comparison dimensions:

- SQLite file in repo vs local generated SQLite database vs JSONL/file-backed document store.
- Whether the database file is committed, ignored, or regenerated.
- Whether git diffs review JSON records, Markdown projections, SQL dumps, migration files, or some combination.
- How merge conflicts are expected to be resolved.
- How records preserve stable IDs, timestamps, statuses, routing, provenance, and projections.
- How local machine state and generated caches stay out of committed authority unless explicitly authorized.

Initial pilot constraint: do not commit a mutable database file as canonical authority unless a specific ADR revision authorizes that repository policy. The approved pilot backend is SQLite as the operational store plus committed schema-backed JSON/export artifacts for review.

Database evidence must remain inspectable without committing mutable authority. Preserve SQLite schema or migration notes, load/export commands, query transcript, checksums, SQL dumps, or equivalent evidence sufficient to verify behavior. Keep the mutable SQLite database file local/ignored unless a later ADR explicitly authorizes committing it.

## Projection invariants for `docs/adr/`

The pilot must define and validate projection invariants for the Markdown file under `docs/adr/`:

- Every projected Markdown ADR identifies its source record ID, schema ID/version, generation method, source-of-truth mode, and pilot-derivative/non-authoritative status.
- Projection output is deterministic for unchanged source record content.
- Projection preserves required ADR sections: status, context, decision, consequences, architecture spec, acceptance criteria, implementation brief, resolved open questions, non-goals, validation expectations, routing, and links when present.
- Generated projection must be distinguishable from hand-authored authority.
- If Markdown remains editable for review, the ingest direction and conflict rule must be explicit.
- A stale projection must be detectable by comparing source record metadata, content hash, or equivalent version field.
- `docs/adr/` remains review/navigation surface during the pilot; it is not removed or bulk replaced.
- The hand-authored source draft must not be overwritten as the generated projection unless explicitly approved. Prefer a generated projection path, projection diff, or clearly marked generated fixture while retaining the original Markdown draft as migration source evidence. If a pilot artifact is written under `docs/adr/`, it must carry explicit generated metadata and a conflict rule.

## Expected pilot-safe output paths

Use pilot-local, non-authoritative paths unless VULCAN proposes a better path before implementation:

- Primary JSON ADR export/checkpoint: `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.draft.json`
- Pilot manifest/config and evidence index: `dev/adr-json-database-one-adr-pilot/manifest.json`
- Pilot metadata/mapping evidence: `dev/adr-json-database-one-adr-pilot/mapping.md` or `.json`
- Generated Markdown projection fixture/diff: `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md`
- Database schema/load/export evidence: `dev/adr-json-database-one-adr-pilot/database-evidence.md` plus any SQL schema/dump text needed for review
- Generated SQLite database: temp/test output only; do not commit the mutable `.sqlite`/`.db` file.

Implementation package boundary, if code is added:

- Package: `src/python/projectkoios/bootstrap/adr_records/`
- Tests: `tests/projectkoios/bootstrap/adr_records/`

The implementation must include a narrow storage adapter boundary so ADR mapping, validation, projection, and equality logic do not depend directly on SQLite. SQLite is the approved pilot backend, but it must be implemented behind an adapter interface rather than becoming the system architecture.

Do not expand into a generic ingestion framework, generic database framework, product template architecture, or all-document migration package. Prefer narrow pilot code and evidence artifacts that clarify the ADR storage authority decision over reusable abstractions.

## Required pilot flow

VULCAN may implement the pilot only after this brief is accepted or explicitly approved.

Before coding, VULCAN must produce a short implementation plan with an explicit decision table and pause for user/Hermes approval. The plan must identify proposed file paths, storage adapter boundary, SQLite adapter/schema shape, JSON export/checkpoint shape, projection approach, validation commands, and any deviations from this brief or from `docs/architecture/architecture.json-adr-storage-topology.md`. The decision table must make the major implementation choices inspectable and easy for the user/Hermes to approve or revise. The plan should optimize for **decision evidence with minimal code**: enough implementation to compare authority models and git/review implications, without prematurely building a reusable framework. Coding begins only after that plan is approved.

The implementation flow must be limited to one ADR:

1. Inspect the source Markdown ADR `docs/adr/adr.json-database-for-adr-storage.draft.md` without changing its authority or overwriting it.
2. Map the ADR into a plain schema-backed JSON record compatible with `docs/schemas/adr.schema.json`. The source Markdown draft has prose/frontmatter-like provenance while the schema requires structured fields such as `delegated_operator`; apply the fixture mapping rules above, record every normalization/default/inference, and distinguish copied source claims from inferred pilot metadata.
3. Validate the JSON record against the ADR schema using the local schema registry or an equivalent offline validator.
4. Load the record into a generated local SQLite operational store through the storage adapter boundary. Mark the JSON record, SQLite representation, and Markdown projection as pilot derivatives/fixtures, not accepted ADR authority.
5. Export the stored record back through the adapter to schema-backed JSON checkpoint/export.
6. Render deterministic Markdown projection to a generated fixture/diff path that does not overwrite the source draft without explicit approval.
7. Parse or map the projection back to a schema-backed ADR record where feasible.
8. Define and apply the semantic equality policy below. Compare the original JSON record, database-exported JSON record, and projection-mapped record for semantic equality.
9. Record that the pilot implemented the database-operational / JSON-checkpointed model using SQLite as the operational store and JSON as committed review checkpoint. Any repository-authoritative database model remains recommendation-only unless a follow-up ADR authorizes it. If the pilot needs `database_row`/`database_document` projection metadata, report that `docs/schemas/schema.record-base.json` currently lacks that source-of-truth value and treat it as a schema/metadata revision need, not something to force through the current `schema_record`/`projection`/`unknown` enum.
10. Produce an implementation report or deviation report.

## Semantic equality policy

VULCAN must declare and implement a comparison policy before validating round trip equality. Minimum policy:

- Semantic fields include every field required by `docs/schemas/adr.schema.json` and optional schema fields present in the source-derived record.
- The approved normalization `routing.next_phase: proposed -> proposal` is semantic-preserving only if recorded in mapping evidence.
- Inferred `context.delegated_operator: HERMES` is allowed only as explicitly marked pilot metadata required to satisfy the current schema.
- Presentation-only Markdown whitespace, heading spacing, and generated banner text are not semantic.
- Projection-only metadata may be excluded from ADR content equality, but must itself survive projection metadata checks.
- Source/date metadata that is not part of `adr.schema.json` must be preserved in pilot metadata or mapping evidence and must not silently disappear from the implementation report.

## Concrete test and failure criteria

The pilot must include focused tests or an explicit deviation report for each item:

- Schema registry or equivalent offline validator loads `docs/schemas/adr.schema.json`.
- The named Markdown fixture maps to ADR JSON and validates.
- Invalid ADR JSON fails validation with inspectable errors.
- JSON -> generated local storage -> JSON preserves semantic equality.
- JSON -> Markdown projection is deterministic/byte-stable for unchanged input.
- Projection includes source record ID, schema ID/version, generation method, source-of-truth mode, and pilot derivative/non-authoritative status.
- Projection staleness can be detected by content hash, source record version, or equivalent metadata.
- Parser/projection mapping failures are distinguishable from JSON Schema validation failures.
- Tests or implementation guardrails prove only `docs/adr/adr.json-database-for-adr-storage.draft.md` is used as the ADR fixture.

Expected validation commands, adjusted only if VULCAN records the final package path:

```bash
uv run pytest tests/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/schema -q
uv run mypy src/python/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/adr_records
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/adr_records tests/projectkoios/bootstrap/adr_records
git diff --check
```

## Acceptance criteria

The pilot is acceptable only if all of the following are true:

- Exactly one ADR is migrated/tested as the pilot fixture.
- The primary produced ADR record is a plain `docs/schemas/adr.schema.json` instance, or VULCAN stops with a schema revision request/deviation report.
- The produced record validates against `docs/schemas/adr.schema.json` or a documented, reviewed schema revision request is produced.
- Pilot JSON, database, and projection artifacts are explicitly marked derived/non-authoritative and cite the source draft as migration source evidence.
- Implemented authority mode is the database-operational / JSON-checkpointed model, using SQLite as operational store and JSON as committed review checkpoint; repository-authoritative database mode is recommendation-only until a follow-up ADR authorizes it.
- Database behavior is explicit: committed authority, generated cache, local-only cache, or exported checkpoint.
- `docs/adr/` projection invariants are documented and tested for the representative ADR.
- Round-trip validation uses the declared comparison policy and demonstrates no semantic loss for required ADR fields.
- Git/review implications are documented before any database file is committed, and inspectable DB evidence is preserved without committing mutable authority unless later authorized.
- Existing Markdown ADRs outside the one representative fixture are not modified, and the representative hand-authored source draft is not overwritten by a generated projection without explicit approval.
- Any mismatch between the current draft ADR and the user's newer database-authoritative direction is reported as an architecture decision gap, not resolved by implementation convenience.
- Mapping from source Markdown to schema-backed ADR record records copied fields, normalized/defaulted fields, and inferred pilot metadata separately, including `delegated_operator`, `date`, and `proposed` -> `proposal`.
- Any need for `database_row`/`database_document` source-of-truth metadata is reported as a schema/projection revision need.
- A VULCAN implementation report records files changed, validation commands, authority model exercised, and residual risks.
- ATHENA reviews pilot conformance before any bulk ADR migration or ADR-authority promotion.

## Explicit non-goals

Do not do any of the following in this pilot:

- Bulk migrate ADRs.
- Rewrite all `docs/adr/*.md` files.
- Promote, accept, activate, or supersede `docs/adr/adr.json-database-for-adr-storage.draft.md`.
- Make a mutable database file canonical by implementation side effect.
- Remove Markdown ADR review surfaces.
- Build a general document-ingestion pipeline.
- Build a generic database framework.
- Change product-domain architecture for the `projectkoios` mothership.
- Treat generated projections as hand-authored ADR authority without explicit metadata and conflict rules.
- Infer schema validity from file presence without validator output.

## Expected output artifacts if implemented

The exact paths should be proposed by VULCAN before implementation if they differ, but the pilot should produce at minimum. Artifacts should emphasize decision evidence: authority-model comparison, git/review implications, SQLite operational behavior, JSON checkpoint reviewability, and projection conflict/staleness behavior.

- One pilot manifest/config artifact at `dev/adr-json-database-one-adr-pilot/manifest.json` declaring non-authoritative pilot status, source/checkpoint/projection paths, hashes, storage adapter policy, SQLite local/generated policy, conflict rule, and evidence index.
- One plain `adr.schema.json` ADR JSON record/export for the representative ADR, marked as a pilot derivative/fixture through the manifest/mapping/report unless a later ADR action changes authority.
- One mapping evidence artifact recording copied, normalized, defaulted, and inferred fields.
- One deterministic Markdown projection or projection diff for the representative ADR, preferably not overwriting the hand-authored source draft.
- Storage-backend notes or migration artifact sufficient to explain the generated local database/cache representation, plus inspectable DB evidence such as commands, schema/migration notes, query transcript, checksums, or dump/export evidence.
- Validation output proving schema validation and round-trip/semantic equality for the one ADR.
- VULCAN implementation report or deviation report.
- ATHENA conformance review after implementation.

## Follow-up architecture decision

After the pilot, ATHENA should revise, replace, or advance `docs/adr/adr.json-database-for-adr-storage.draft.md` only if the pilot evidence supports a clear authority model. The follow-up ADR must separate evidence from recommendation: pilot artifacts may be cited as evidence, but the pilot implementation itself must not become ADR authority by side effect.

The follow-up ADR decision must explicitly answer:

- Is the canonical ADR authority a JSON record, a database row/document, or a hybrid checkpoint model?
- What artifact is committed to git as durable review and history authority?
- What is the status of `docs/adr/*.md`: generated projection, editable projection, or transitional source?
- What validations are required before additional ADRs migrate?
