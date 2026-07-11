```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-bidirectional-object-canary-slice-0-implemented-validated",
  "datetime": "20260711.134900Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/architecture/architecture.adr-bidirectional-objects.md",
    "docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md",
    "docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md",
    "docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md",
    "dev/adr-bidirectional-object-canary-slice-0/",
    "src/python/projectkoios/bootstrap/control_surface/adr/bidirectional.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrBidirectionalCanaryRunner__json_schemas.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md",
  "latest_aar": "docs/AAR/aar.20260711.134900_adr-bidirectional-object-canary-slice-0.md"
}
```

# Vulcan active work

## Current priority stack

1. `adr-bidirectional-object-canary-slice-0`: implemented and validated.
2. Parent effort: ADR rationalization / bidirectional JSON-Markdown object architecture.
3. Boundaries preserved: exactly one canary source; no `docs/adr` mutation; no `docs/schemas` mutation/publication; no database/storage authority; no committed `.sqlite`/`.db`; no bulk migration; no hand-authored Markdown ingest; no file moves/renames/status normalization/draft supersession; no Petri-net, Operator Console, or workflow-object integration.

## Latest working material

- Architecture: `docs/architecture/architecture.adr-bidirectional-objects.md`.
- Brief: `docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md`.
- Implementation report: `docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md`.
- AAR: `docs/AAR/aar.20260711.134900_adr-bidirectional-object-canary-slice-0.md`.

## Implemented outputs

- `AdrBidirectionalCanaryRunner` and exported helper `run_adr_bidirectional_object_canary`.
- Candidate canary evidence directory: `dev/adr-bidirectional-object-canary-slice-0/`.
- Candidate envelope: `adr.json-schemas.bidirectional-object.json`.
- Generated projection: `adr.json-schemas.projected.md`.
- Sidecar/conversion evidence: `conversion-evidence.json`.
- Manifest: `manifest.json`.
- Focused tests covering candidate envelope, sidecar preservation, generated projection parse-back equality, source-mutation proof, and no database files.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `14 passed in 0.18s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 13 file(s)`.

```bash
git status --short -- docs/adr/adr.json-schemas.draft.md
git status --short -- docs/adr
git status --short -- docs/schemas
find dev/adr-bidirectional-object-canary-slice-0 -type f \( -name '*.sqlite' -o -name '*.db' \) -print
uv run python -m json.tool dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json >/dev/null
git diff --check
```

Passed for the exact canary source, `docs/schemas`, DB-file check, object JSON, and diff whitespace. At closeout, `git status --short -- docs/adr` also shows unrelated untracked `docs/adr/adr.json-authoritative-adr-store.draft.md`, which is not VULCAN-owned for this slice.

## Next expected artifact

- HERMES/USER review or closeout/commit direction.
