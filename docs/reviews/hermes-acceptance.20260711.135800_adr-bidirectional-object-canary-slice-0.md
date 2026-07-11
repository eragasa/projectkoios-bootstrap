```json
{
  "title": "HERMES acceptance: ADR bidirectional object canary slice 0",
  "artifact_type": "acceptance-review",
  "status": "accepted-with-watchpoints",
  "datetime": "20260711.135800Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-bidirectional-object-canary-slice-0",
  "implementation_report": "docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md"
}
```

# HERMES acceptance 20260711.135800: ADR bidirectional object canary slice 0

## Verdict

Accepted with watchpoints.

## Reviewed artifacts

- `docs/architecture/architecture.adr-bidirectional-objects.md`
- `docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md`
- `docs/reviews/hermes-decision.20260711.134500_adr-bidirectional-object-canary-slice-0.md`
- `docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md`
- `docs/reviews/architecture-conformance.20260711.135500_adr-bidirectional-object-canary-slice-0.md`
- `dev/adr-bidirectional-object-canary-slice-0/`

## Independent HERMES validation

From repository root, HERMES reran:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
git status --short -- docs/adr/adr.json-schemas.draft.md
git status --short -- docs/schemas
find dev/adr-bidirectional-object-canary-slice-0 -type f \( -name '*.sqlite' -o -name '*.db' \) -print
uv run python -m json.tool dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json >/dev/null
git diff --check
```

Observed results:

- focused tests passed: `14 passed`;
- Python policy passed: `0 finding(s), 13 file(s)`;
- exact canary source `docs/adr/adr.json-schemas.draft.md` is unmodified;
- `docs/schemas` has no changes;
- no `.sqlite` or `.db` files exist under the canary evidence directory;
- candidate object JSON is valid;
- `git diff --check` passed.

## Acceptance basis

The slice satisfies the approved brief and HERMES decision:

- exactly one source is used: `docs/adr/adr.json-schemas.draft.md`;
- evidence is isolated under `dev/adr-bidirectional-object-canary-slice-0/`;
- the candidate object envelope includes `content`, `classification`, `markdown_projection`, `conversion_evidence`, `source_refs`, `sidecar`, `validation`, and `conflict_policy`;
- classification/disposition metadata remains outside ADR `content`;
- unsupported source fields including `routing` and `links.related` are preserved in sidecar/evidence;
- generated Markdown projection is marked projection-only;
- parse-back semantic equality applies only to generated projection evidence;
- source hash before/after proves the source Markdown was not mutated;
- no `docs/adr` source mutation, `docs/schemas` mutation, database/storage authority, mutable DB file, bulk migration, hand-authored Markdown ingest, file move/rename, status normalization, or draft supersession is introduced.

## Watchpoints

This canary is evidence/mechanics only. It does not make JSON repository-wide ADR authority, publish an envelope schema, demote Markdown authority, promote database/storage authority, or authorize mass conversion.

The separate authority-change draft `docs/adr/adr.json-authoritative-adr-store.draft.md` must be reviewed and accepted before any JSON-authoritative cutover, mass conversion, schema publication, source ADR mutation, file move/rename, or status normalization.
