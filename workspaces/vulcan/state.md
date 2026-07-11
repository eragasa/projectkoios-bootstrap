```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "adr-bidirectional-object-canary-slice-0-implemented-validated",
  "datetime": "20260711.134900Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_architecture": "docs/architecture/architecture.adr-bidirectional-objects.md",
  "source_brief": "docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md",
  "slice_name": "adr-bidirectional-object-canary-slice-0",
  "latest_report": "docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md",
  "latest_aar": "docs/AAR/aar.20260711.134900_adr-bidirectional-object-canary-slice-0.md",
  "evidence_dir": "dev/adr-bidirectional-object-canary-slice-0/",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_USER_REVIEW",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated ADR bidirectional object canary Slice 0.
- Slice name: `adr-bidirectional-object-canary-slice-0`.
- Source: `docs/adr/adr.json-schemas.draft.md` only.
- Architecture: `docs/architecture/architecture.adr-bidirectional-objects.md`.
- Brief: `docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md`.
- Report: `docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md`.

## Current status

- Candidate `AdrBidirectionalObject` envelope evidence exists under `dev/adr-bidirectional-object-canary-slice-0/`.
- Generated projection evidence exists and parse-back semantic equality is validated for generated projection only.
- Classification/disposition metadata is outside ADR `content`.
- Unsupported source fields, including `routing` and `links.related`, are preserved in sidecar/evidence.
- Source/projection/schema hashes and source-mutation proof are recorded.
- No hand-authored Markdown ingest, database/storage authority, schema publication, bulk migration, source mutation, file move/rename, status normalization, draft supersession, Petri-net, Operator Console, or workflow-object integration was added.

## Validation evidence

From repository root:

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` => `14 passed in 0.18s`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 13 file(s)`.
- `git status --short -- docs/adr/adr.json-schemas.draft.md` => no output; exact canary source unmodified.
- `git status --short -- docs/adr` => `?? docs/adr/adr.json-authoritative-adr-store.draft.md` at closeout; not VULCAN-owned for this slice.
- `git status --short -- docs/schemas` => no output.
- `find dev/adr-bidirectional-object-canary-slice-0 -type f \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `uv run python -m json.tool dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json >/dev/null` => passed.
- `git diff --check` => passed.

## Dirty tree caution

Treat VULCAN-owned changes for this slice as:

- `dev/adr-bidirectional-object-canary-slice-0/`
- `src/python/projectkoios/bootstrap/control_surface/adr/bidirectional.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrBidirectionalCanaryRunner__json_schemas.py`
- `docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md`
- `docs/AAR/aar.20260711.134900_adr-bidirectional-object-canary-slice-0.md`
- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

Known ATHENA/HERMES/KOIOS architecture, review, provenance, or unrelated `docs/adr` files may also exist in the dirty tree. Keep commit boundaries explicit.

## Next transition

- Owner: HERMES/USER review.
- Expected action: review or request closeout/commit.
- Blockers: none from VULCAN.
