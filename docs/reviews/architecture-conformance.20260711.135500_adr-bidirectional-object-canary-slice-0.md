```json
{
  "title": "Architecture conformance review: ADR bidirectional object canary slice 0",
  "artifact_type": "architecture-conformance-review",
  "status": "accepted-with-watchpoints",
  "datetime": "20260711.135500Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "reviewed_artifact": "docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md",
  "source_brief": "docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md",
  "source_architecture": "docs/architecture/architecture.adr-bidirectional-objects.md",
  "verdict": "conforms"
}
```

# Architecture conformance review 20260711.135500: ADR bidirectional object canary slice 0

## Verdict

Accepted with watchpoints.

The VULCAN implementation conforms to the approved canary brief and HERMES decision as an evidence-only `AdrBidirectionalObject` canary. It does not change ADR source authority, schema authority, storage authority, lifecycle status, filenames, or repository-wide hierarchy.

## Review basis

Reviewed:

- `docs/architecture/architecture.adr-bidirectional-objects.md`
- `docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md`
- `docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md`
- `docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md`
- `src/python/projectkoios/bootstrap/control_surface/adr/bidirectional.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrBidirectionalCanaryRunner__json_schemas.py`
- `dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json`
- `dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.projected.md`
- `dev/adr-bidirectional-object-canary-slice-0/conversion-evidence.json`
- `dev/adr-bidirectional-object-canary-slice-0/manifest.json`

## Conformance findings

- The implementation uses exactly one source: `docs/adr/adr.json-schemas.draft.md`.
- Candidate object evidence is isolated under `dev/adr-bidirectional-object-canary-slice-0/`.
- The envelope includes `content`, `classification`, `markdown_projection`, `conversion_evidence`, `source_refs`, `sidecar`, `validation`, and `conflict_policy`.
- Classification/disposition metadata remains outside ADR `content` and records:
  - `category=template_schema_contract`
  - `secondary_aspect=architecture_blueprint`
  - `source_role=canary_source`
  - `source_authority_effect=none`
- `content` is schema-valid against the current ADR schema and does not include envelope-only metadata.
- Unsupported source fields are preserved outside `content`, including `routing` and `links.related`.
- Generated Markdown projection is visibly marked as generated/projection-only evidence.
- Generated projection parse-back semantic equality is implemented and tested for generated projection only.
- Hand-authored Markdown ingest is not implemented.
- Source mutation proof records matching before/after hashes for `docs/adr/adr.json-schemas.draft.md`.
- No SQLite/database storage authority is introduced and no mutable DB files are generated in the canary evidence directory.
- No Petri-net, Operator Console, workflow-object, bulk migration, file move/rename, status normalization, or draft supersession behavior is introduced.

## ATHENA validation rerun

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
git status --short -- docs/adr/adr.json-schemas.draft.md
git status --short -- docs/adr
git status --short -- docs/schemas
find dev/adr-bidirectional-object-canary-slice-0 -type f \( -name '*.sqlite' -o -name '*.db' \) -print
uv run python -m json.tool dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json >/dev/null
git diff --check
```

Results:

- Focused pytest: `14 passed in 0.17s`.
- Python policy: `summary: 0 finding(s), 13 file(s)`.
- Exact canary source status: no output for `docs/adr/adr.json-schemas.draft.md`.
- `docs/adr` status: only unrelated ATHENA authority-change draft `?? docs/adr/adr.json-authoritative-adr-store.draft.md`.
- `docs/schemas` status: no output.
- Mutable DB check in canary evidence directory: no output.
- Candidate object JSON validity: passed.
- `git diff --check`: passed.

## Watchpoints

- This canary remains evidence/mechanics only. It is not repository-wide JSON authority, schema authority, storage authority, or Markdown authority demotion.
- `docs/adr/adr.json-authoritative-adr-store.draft.md` is an ATHENA authority-change draft created after the canary brief; it should be reviewed separately before mass conversion or JSON-authoritative cutover.
- The canary may become Phase 0 evidence for JSON-authoritative migration if HERMES/USER accepts that authority-change direction, but it does not itself authorize mass migration.
- Future work must preserve the precise language boundary: use `candidate object evidence`, `generated projection evidence`, and `current conformance artifact`; avoid ambiguous `active ADRs` wording unless specifically referring to ADR lifecycle status.
- Any hand-authored Markdown ingest, `docs/schemas/` publication/change, file moves/renames, status normalization, source ADR mutation, DB authority, or bulk migration still requires separate HERMES/USER approval.
