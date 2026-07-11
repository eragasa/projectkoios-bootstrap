```json
{
  "title": "Architecture conformance review: ADR JSON authority projectable messy canary slice 3",
  "artifact_type": "architecture-conformance-review",
  "status": "accepted-with-watchpoints-pending-koios-re-review",
  "datetime": "20260711.150300Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-projectable-messy-canary-slice-3",
  "reviewed_implementation": "docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md",
  "source_brief": "docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md",
  "next_owner": "HERMES_USER"
}
```

# Architecture conformance review 20260711.150300: ADR JSON authority projectable messy canary slice 3

## Verdict

Accepted with watchpoints, pending KOIOS re-review / HERMES final acceptance.

Initial ATHENA validation found the Slice 3 boundaries and status/projection markers conforming, but KOIOS provenance review identified an acceptance blocker: source-to-candidate conversion dropped continuation text from one wrapped acceptance-criteria list item while the evidence still reported candidate/projection parse-back equality. VULCAN corrected wrapped-list continuation preservation, regenerated evidence, updated the implementation report, and added a focused regression assertion.

ATHENA re-reviewed the corrected evidence and now finds the implementation conforming to the Slice 3 brief and HERMES decision. The corrected implementation uses exactly `docs/adr/adr.adr-template-contract.md`, preserves observed status casing `Accepted` separately from normalized candidate `accepted`, preserves the wrapped list continuation text, generates a non-authoritative projection under the Slice 3 `dev` path only, parses back only that generated projection, preserves template/schema-contract manual-review blockers, and does not perform source mutation, schema change, authority cutover, replacement projection, database/storage authority, or corpus conversion.

## Reviewed artifacts

- `docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md`
- `docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md`
- `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md`
- `docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md`
- `dev/adr-json-authority-projectable-messy-canary-slice-3/manifest.json`
- `dev/adr-json-authority-projectable-messy-canary-slice-3/candidate-object.json`
- `dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md`
- `dev/adr-json-authority-projectable-messy-canary-slice-3/projection-parseback-evidence.json`
- `dev/adr-json-authority-projectable-messy-canary-slice-3/conversion-evidence.json`
- `dev/adr-json-authority-projectable-messy-canary-slice-3/conflict-lossiness-report.json`
- `dev/adr-json-authority-projectable-messy-canary-slice-3/sidecar-provenance.json`
- `src/python/projectkoios/bootstrap/control_surface/adr/projectable_messy_canary.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrProjectableMessyCanaryRunner__template_contract.py`

## Conformance findings

### Exactly-one-source boundary

Conforms.

The manifest and candidate object name exactly one source:

```text
docs/adr/adr.adr-template-contract.md
```

The candidate object's `conversion_scope.sources` contains only that file. No evidence artifact indicates conversion or projection of another ADR file.

### Status-casing preservation

Conforms.

The implementation preserves observed source status casing:

- candidate object `content_candidate.observed_status_text` is `Accepted`;
- candidate object `content_candidate.status` remains `Accepted`;
- normalized status candidate `accepted` is recorded separately;
- `normalization_requires_review` is true;
- projection parse-back records `parseback_status_text: Accepted`;
- projection/parse-back reports `status_normalized_by_projection_or_parseback: false`.

This satisfies the brief requirement to preserve `Accepted` separately from any normalized candidate and not silently normalize source status.

### Projection and parse-back boundary

Conforms.

Generated projection exists only at:

```text
dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md
```

The projection is visibly marked as generated evidence and non-authoritative. Parse-back evidence states `parseback_source: generated_projection_only` and `hand_authored_source_parsed_as_replacement: false`. Projection parse-back semantic equality for candidate fields is true, but `projection_resolves_review_blockers` is false.

### Conflict/lossiness and review blockers

Conforms.

The conflict/lossiness report preserves the required blockers:

- `template_schema_contract_ambiguity: true`;
- `manual_review_required: true`;
- `status_casing_normalization_sensitive: true`;
- `blocked_from_authority_promotion: true`;
- outcome `projectable_candidate_blocked_pending_template_contract_and_status_review`.

Sidecar/provenance records Slice 1 reviewed values and preserves routing/manual-review/status-casing material outside the content candidate.

### No-authority boundary

Conforms.

Evidence markers preserve:

- `candidate_only: true`;
- `authority_change: false`;
- `conversion_completed_as_authoritative_record: false`;
- `database_authority: false`;
- `schema_change: false`;
- `source_mutation: false`.

This implementation does not authorize JSON authority promotion or status normalization.

### Source/schema/storage boundaries

Conforms.

ATHENA found no evidence of:

- `docs/adr` mutation;
- `docs/schemas` changes;
- conversion/projection of any source except `docs/adr/adr.adr-template-contract.md`;
- authoritative JSON ADR record creation;
- replacement projection creation;
- file moves/renames/deletes/archives;
- source status normalization;
- draft supersession;
- authority cutover;
- database/storage authority;
- mutable `.sqlite` or `.db` files under the Slice 3 evidence path.

## ATHENA validation rerun

Commands rerun from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `30 passed in 0.28s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `Success: no issues found in 21 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 21 file(s)`.

```bash
find dev/adr-json-authority-projectable-messy-canary-slice-3 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-projectable-messy-canary-slice-3 \( -name '*.sqlite' -o -name '*.db' \) -print
git status --short -- docs/adr docs/schemas
find dev/adr-json-authority-projectable-messy-canary-slice-3 -name 'generated-projection.md' -print
git diff --check
```

Result: JSON validity passed; DB-file scan produced no output; `git status --short -- docs/adr docs/schemas` produced no output; projection location scan returned only `dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md`; `git diff --check` passed.

Additional ATHENA spot checks confirmed:

- source path is exactly `docs/adr/adr.adr-template-contract.md`;
- candidate source list contains only that file;
- observed status `Accepted` and normalized candidate `accepted` are separate;
- normalization requires review;
- projection is generated under the Slice 3 dev path only;
- parse-back uses generated projection only;
- projection does not normalize status or resolve blockers;
- template/schema-contract ambiguity and manual-review blockers remain active;
- all core evidence objects preserve `candidate_only: true` and `authority_change: false`.

## KOIOS provenance blocker and remediation

KOIOS provenance review exists at:

```text
workspaces/koios/working/provenance-review.20260711_adr-json-authority-projectable-messy-canary-slice-3.md
```

KOIOS found the slice not yet provenance-adequate for final HERMES acceptance because candidate/projection evidence dropped source text from one wrapped list item.

Source acceptance criterion:

```text
- Workflow-bound ADRs can render optional gate fields without losing schema
  consistency.
```

VULCAN remediated by fixing wrapped-list continuation preservation, regenerating Slice 3 evidence, and updating the implementation report. ATHENA verified that candidate and projection evidence now preserve:

```text
Workflow-bound ADRs can render optional gate fields without losing schema consistency.
```

The prior source-to-candidate lossiness blocker is resolved from ATHENA's architecture/conformance perspective. HERMES should still obtain/confirm KOIOS re-review or acceptance of the regenerated evidence before final acceptance, because KOIOS raised the blocker.

## Correction validation addendum

ATHENA reran validation after VULCAN's correction:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `30 passed in 0.29s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `Success: no issues found in 21 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 21 file(s)`.

```bash
find dev/adr-json-authority-projectable-messy-canary-slice-3 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-projectable-messy-canary-slice-3 \( -name '*.sqlite' -o -name '*.db' \) -print
git status --short -- docs/adr docs/schemas
find dev/adr-json-authority-projectable-messy-canary-slice-3 -name 'generated-projection.md' -print
git diff --check
```

Result: JSON validity passed; DB-file scan produced no output; `git status --short -- docs/adr docs/schemas` produced no output; projection-location scan returned only `dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md`; `git diff --check` passed.

Additional correction spot checks confirmed the corrected acceptance-criteria text appears in both `candidate-object.json` and `generated-projection.md`, observed `Accepted` status remains separate from normalized `accepted`, parse-back semantic equality remains true for candidate fields, and projection/parse-back does not normalize status.

## Watchpoints after remediation

1. This slice proves one projectable messy canary only; it does not authorize corpus conversion, schema publication, source mutation, JSON authority cutover, or migration.
2. Projection/parse-back equality is candidate-field evidence only and does not resolve template/schema-contract or status-casing authority questions.
3. The generated projection contains a candidate JSON block and a rendered status section, but it remains dev-path evidence only and must not be consumed as source ADR authority.
4. Remaining migration proof points still need review strategy for corpus dry-run selection, conflict handling across multiple records, and final authority-location/cutover decisions.
5. `manifest.json` still carries pre-closeout `pending closeout validation` labels; the implementation report and ATHENA validation provide closeout validation evidence, but remediation should refresh evidence/report state.

## Non-authorizations preserved

This acceptance does not authorize:

- corpus conversion;
- conversion or projection of any file beyond this one selected source;
- authoritative JSON ADR records;
- final per-file authority decisions;
- schema publication or schema changes;
- source Markdown mutation;
- source status normalization;
- file moves or renames;
- draft supersession;
- database/storage authority;
- committed mutable DB files;
- authority cutover;
- product/future-system or template/schema-contract authority resolution.

## Next owner

HERMES/USER for final acceptance consideration after KOIOS re-review or explicit KOIOS/HERMES confirmation that the regenerated evidence resolves the provenance blocker.
