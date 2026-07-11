```json
{
  "title": "KOIOS provenance review: ADR JSON authority messy canary slice 2",
  "artifact_type": "provenance-review",
  "status": "reviewed-accepted-with-watchpoints",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-messy-canary-slice-2",
  "reviewed_report": "docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md",
  "evidence_dir": "dev/adr-json-authority-messy-canary-slice-2/"
}
```

# KOIOS provenance review: ADR JSON authority messy canary slice 2

## Verdict

Reviewed: accept with watchpoints.

Slice 2 faithfully preserves the key messy-canary provenance constraints. It demonstrates a blocked/review-only conversion candidate for `docs/adr/adr.schema-base.md` without inventing ADR status or authority.

## Sources reviewed

- Source: `docs/adr/adr.schema-base.md`
- Brief: `docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md`
- Reviewed inventory: `dev/adr-json-authority-inventory-review-overrides-slice-1/`
- Evidence directory: `dev/adr-json-authority-messy-canary-slice-2/`
- Implementation report: `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`
- KOIOS pre-review checklist: `workspaces/koios/working/pre-review-checklist.20260711_adr-json-authority-messy-canary-slice-2.md`

## Provenance findings

- Exactly one source is represented: `docs/adr/adr.schema-base.md`.
- Source hash is preserved as `48a5fed34bec41b18885fdb57d7491895783f735c07efc33202098bbf61a2d51` and before/after source hashes match.
- The missing top-level Markdown/ADR status remains missing: candidate `content_candidate.status` is `null`, `observed_markdown_status` is `null`, and `missing_status` is `true`.
- Embedded JSON `status: draft` is preserved in `sidecar-provenance.json` as embedded metadata only; it is not promoted into ADR lifecycle/content status.
- Schema/implementation-contract ambiguity is explicit in sidecar and conflict/lossiness evidence.
- Outcome is visibly blocked/review-only: `conversion_candidate_blocked_pending_review`.
- Candidate object is marked `candidate_only: true`, `authority_change: false`, `authority_mode: candidate-evidence-only-not-repository-authority`, `source_mutation: false`, `schema_change: false`, and `database_authority: false`.
- Conflict/lossiness report states schema validation is blocked without invented status and records missing status plus manual-review/schema-contract ambiguity as blockers.
- No projection was generated, with rationale that projection could imply schema-valid ADR content or require invented status. This is provenance-safe.
- No `.sqlite` or `.db` files were found under the Slice 2 evidence path.
- `git status --short -- docs/adr docs/schemas` produced no output during KOIOS review, consistent with no ADR/schema mutation.

## Watchpoints

1. This is a successful messy canary precisely because it remains blocked pending review. Do not reinterpret it as a completed conversion or proof that `adr.schema-base.md` can be auto-migrated.
2. The embedded schema-record JSON may be useful input for a later schema/envelope design, but its `status: draft` must remain sidecar/source metadata unless ATHENA/USER explicitly defines a mapping.
3. The absence of generated projection is acceptable and should not be treated as missing implementation; it is the correct conservative outcome for this source.
4. Next slices still need to prove behavior for a messy record that can generate a projection without inventing authority, and eventually for source/projection conflict handling.

## Boundary confirmation

KOIOS found no evidence of:

- mutation of `docs/adr/adr.schema-base.md` or other ADR sources;
- `docs/schemas` mutation;
- conversion of a second source;
- authoritative JSON ADR record creation;
- replacement projection creation;
- file moves, renames, deletes, or archives;
- source status normalization;
- draft supersession;
- authority cutover;
- database/storage authority;
- committed mutable database files under the evidence path.

## Recommendation

HERMES/USER can accept Slice 2 as evidence that the migration machinery correctly stops on missing-status/schema-contract ambiguity and preserves sidecar provenance.

Do not proceed to corpus conversion from this alone. The next safe proof point should either test a messy-but-projectable source or extend conflict/lossiness handling while preserving the same candidate-only/no-mutation boundaries.
