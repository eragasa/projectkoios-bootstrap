```json
{
  "title": "ADR bidirectional object canary slice 0 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260711.134900Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.adr-bidirectional-objects.md",
  "source_brief": "docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md",
  "slice_name": "adr-bidirectional-object-canary-slice-0",
  "evidence_dir": "dev/adr-bidirectional-object-canary-slice-0/",
  "next_owner": "HERMES_USER_REVIEW"
}
```

# Implementation report 20260711.134900: ADR bidirectional object canary slice 0

## Summary

Implemented the bounded one-source `AdrBidirectionalObject` canary for:

```text
docs/adr/adr.json-schemas.draft.md
```

The slice creates candidate object evidence only. It does not change ADR source authority, schema authority, storage authority, lifecycle status, filenames, or repository-wide hierarchy.

## Changed files

Implementation and tests:

- `src/python/projectkoios/bootstrap/control_surface/adr/bidirectional.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrBidirectionalCanaryRunner__json_schemas.py`

Generated canary evidence:

- `dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json`
- `dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.projected.md`
- `dev/adr-bidirectional-object-canary-slice-0/conversion-evidence.json`
- `dev/adr-bidirectional-object-canary-slice-0/manifest.json`

## Implemented behavior

- Added `AdrBidirectionalCanaryRunner` for a file/evidence/projection-only canary.
- Uses exactly one source Markdown file: `docs/adr/adr.json-schemas.draft.md`.
- Produces a candidate `AdrBidirectionalObject` envelope, not a published schema.
- Keeps `classification` metadata outside `content`:
  - `category=template_schema_contract`
  - `secondary_aspect=architecture_blueprint`
  - `source_role=canary_source`
  - `source_authority_effect=none`
- Keeps `content` compatible with current `docs/schemas/adr.schema.json`.
- Preserves unsupported source material in `sidecar` and evidence, including `routing`, `links.related`, source status text, source date, source path/hash, schema path/hash, and projection path/hash.
- Generates deterministic Markdown projection evidence with explicit generated/projection-only marker text.
- Parses generated projection back to ADR content and validates semantic equality.
- Records source hash before/after as source-mutation proof.
- Does not implement hand-authored Markdown ingest.
- Does not use SQLite or create mutable `.sqlite`/`.db` evidence.

## Validation

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `14 passed in 0.18s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 13 file(s)`.

```bash
git status --short -- docs/adr/adr.json-schemas.draft.md
```

Result: no output; the exact canary source is unmodified.

```bash
git status --short -- docs/adr
git status --short -- docs/schemas
```

Current `docs/adr` output at closeout:

```text
?? docs/adr/adr.json-authoritative-adr-store.draft.md
```

`docs/schemas` output: no output. The untracked `docs/adr/adr.json-authoritative-adr-store.draft.md` file is not a VULCAN-owned artifact for this slice and is outside the exact canary source. Keep commit boundaries explicit.

```bash
find dev/adr-bidirectional-object-canary-slice-0 -type f \( -name '*.sqlite' -o -name '*.db' \) -print
```

Result: no output; no mutable database file exists in the canary evidence directory.

```bash
uv run python -m json.tool dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json >/dev/null
```

Result: passed.

```bash
git diff --check
```

Result: passed.

## Boundary confirmation

Preserved boundaries:

- No `docs/adr/` mutation.
- No `docs/schemas/` publication or change.
- No database/storage authority and no committed `.sqlite`/`.db` file.
- No bulk migration.
- No hand-authored Markdown ingest.
- No file moves or renames.
- No status normalization or draft supersession.
- No Petri-net, Operator Console, or workflow-object integration.

## Notes for review

The generated projection parse-back proof applies only to generated projection evidence. It is not a hand-authored Markdown importer and does not make generated projection evidence repository authority.

## Next owner

HERMES/USER review.
