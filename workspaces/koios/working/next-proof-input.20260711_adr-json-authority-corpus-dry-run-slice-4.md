```json
{
  "title": "KOIOS next proof input: ADR JSON authority corpus dry-run slice 4",
  "artifact_type": "provenance-next-proof-input",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "next bounded ADR JSON authority proof point after accepted projectable messy canary slice 3"
}
```

# KOIOS next proof input: ADR JSON authority corpus dry-run slice 4

## Authority boundary

This note is KOIOS provenance input only. It does not authorize source mutation, schema changes, source status normalization, authoritative JSON ADR records, corpus-wide migration, file moves/renames, database/storage authority, or JSON authority cutover.

## Recommended slice shape

Recommended slice name:

```text
adr-json-authority-corpus-dry-run-inventory-slice-4
```

Recommended purpose:

- run a small bounded multi-file dry-run over selected `docs/adr/` sources;
- produce candidate-only per-file conversion/reporting/lossiness evidence under a dedicated `dev/` path;
- prove multi-file manifest/report behavior across different reviewed dispositions;
- keep every generated object/projection/sidecar non-authoritative;
- do not mutate source Markdown or schemas.

This should be a **subset dry-run**, not a corpus-wide migration. The word `corpus` should mean corpus-style reporting/manifest shape over a bounded subset, not all ADRs.

## Primary recommended subset

Use exactly these six entries unless HERMES/USER explicitly changes the subset:

| Role in proof | Source path | Slice 1 reviewed values / hash | Why include |
|---|---|---|---|
| Clean candidate control | `docs/adr/adr.json-schemas.draft.md` | `template_schema_contract`; `json_authority_candidate`; `authority_effect: candidate`; auto candidate `true`; hash `c95dfb0928ba1398eb058a7bb16b21f2dad77f4116169cbcc8075fb5186c2df5` | Good low-surprise candidate for ordinary candidate conversion/report rows; schema-adjacent and relevant to ADR JSON path. |
| Accepted/current decision candidate | `docs/adr/adr.petrinet.20260705.132740Z.md` | `template_schema_contract`; `json_authority_candidate`; `authority_effect: candidate`; auto candidate `true`; hash `7fd761c39056bf7a81032b98aabde038d053931e73cd161fb9a48934b2a700a3` | Tests accepted-decision candidate handling while remaining in bootstrap workflow scope; must remain candidate-only despite accepted source status. |
| Slice 3 regression / manual review | `docs/adr/adr.adr-template-contract.md` | `template_schema_contract`; `manual_review_required`; `authority_effect: candidate`; auto candidate `false`; hash `2876dfbe031105d383fa9e33cec7d5dd49cf569cea6f43eae59e8fa1da502895` | Reuses the accepted Slice 3 canary as a regression row for `Accepted` casing, wrapped-list preservation, generated projection labeling, and manual-review blockers. |
| Missing-status/manual review blocker | `docs/adr/adr.schema-base.md` | `template_schema_contract`; `manual_review_required`; `authority_effect: candidate`; auto candidate `false`; hash `48a5fed34bec41b18885fdb57d7491895783f735c07efc33202098bbf61a2d51` | Carries the Slice 2 missing-status/blocker risk into multi-file reporting; should produce blocked/lossiness evidence without invented status. |
| Source/provenance draft exclusion | `docs/adr/adr.adr-lifecycle.draft.md` | `template_schema_contract`; `source_only_provenance_candidate`; `authority_effect: candidate`; auto candidate `false`; hash `d9068c3a5d10efcf9ee2216e34272cc8399c91e5af67ce51b0f1e5e5b5464706` | Tests that source/provenance drafts are preserved/reportable but not auto-promoted or treated as current decision authority. |
| Index/control exclusion row | `docs/adr/README.md` | `index_or_control_surface`; `authority_effect: none`; auto candidate `false`; hash `9950799ed8c20d7980634fc086309cfd98fd3c065499d25f6aab965ec6dfef2e` | Tests manifest/report behavior for a docs/adr control surface that should not become an ADR record. If implementation tooling only accepts ADR Markdown records, this row should be reported as skipped/excluded rather than converted. |

## Rationale

This subset exercises the main reviewed dispositions without creating avoidable product/domain surprises:

- conversion-planning candidates that still remain candidate-only;
- accepted/current source status that must not imply JSON authority cutover;
- manual-review blockers from noncanonical status casing and template-contract ambiguity;
- missing-status blocker behavior;
- source-only/provenance draft handling;
- index/control-surface exclusion.

It also carries forward the two strongest prior proof points:

- Slice 2: missing-status records must block authority rather than invent status.
- Slice 3: projectable messy candidates can generate evidence while preserving observed status/casing and manual-review blockers.

## Optional domain-review canary, only if explicitly approved

KOIOS does **not** recommend including a product/future-system/domain-risk source in the default Slice 4 subset. If HERMES/USER wants to test domain-review row behavior explicitly, add exactly one flagged domain-review file and require the output to mark it skipped/blocked from conversion:

```text
docs/adr/adr.agent-windows-on-message-triggers.draft.md
```

Reviewed values: `product_future_system_draft`; `domain_review_required`; `authority_effect: domain_review_required`; auto candidate `false`; hash `102d63582fad9f26e5ee0c282b3cfaf5b62c2c270fc3c1f44ced67185b9c7193`.

Rationale: it exercises domain-review disposition without the training-data implications of `adr.20260702.144539_agent-production-trace-and-training-capture.draft.md`. Still, it should be included only with explicit HERMES/USER approval because it touches future agent/runtime behavior.

## Expected evidence path

Recommended dedicated evidence path:

```text
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/
```

Expected evidence should include, names adjustable for implementation consistency:

- `manifest.json` — slice metadata, selected source list, source hashes, artifact hashes, no-authority markers;
- `selected-sources.json` — frozen selected subset and reviewed Slice 1 values consumed;
- `per-source-results.json` — one row per selected source with outcome and blocker/lossiness summary;
- `candidate-objects/` — candidate JSON objects only for sources safely representable without inventing authority; if omitted for a blocked/skipped source, record why;
- `generated-projections/` — generated evidence only, under `dev/`, never replacement Markdown;
- `sidecars/` — per-source sidecar/provenance preserving observed status/casing, source hash, unsupported/omitted/inferred fields, reviewed disposition, and blockers;
- `conflict-lossiness-report.json` — aggregate and per-source lossiness/blocker report;
- `projection-parseback-report.json` — parse-back evidence for generated projections only;
- `skipped-or-blocked-sources.json` — explicit list for README/index, missing-status, source-only, manual-review, or domain-review rows as applicable.

## Per-source outcome expectations

- `adr.json-schemas.draft.md`: candidate evidence may be generated if no source facts are invented; still `candidate_only: true` and `authority_change: false`.
- `adr.petrinet.20260705.132740Z.md`: candidate evidence may be generated; accepted source status must not imply accepted JSON authority.
- `adr.adr-template-contract.md`: preserve `Accepted` exactly and normalized candidate separately; keep manual-review/template-contract blockers; preserve wrapped-list continuations from Slice 3.
- `adr.schema-base.md`: do not invent a top-level ADR status; record missing-status blocker and either skip projection or generate only clearly blocked candidate evidence if safe.
- `adr.adr-lifecycle.draft.md`: report as source/provenance draft; do not promote as current lifecycle authority or supersede accepted lifecycle ADR.
- `README.md`: report as index/control surface; do not convert to ADR candidate object unless tooling has an explicit non-ADR control-surface record type, and even then it remains non-authoritative evidence only.

## Required watchpoints

- Preserve exact source path and source hash for every selected file.
- Preserve observed status text/casing separately from normalized candidates.
- Never infer missing status as `draft`, `accepted`, or `active`.
- Distinguish source/provenance drafts from current decisions.
- Distinguish index/control surfaces from ADR records.
- Keep candidate object equality separate from source-to-candidate lossiness; Slice 3 showed this can otherwise hide dropped source content.
- Require sidecars for unsupported, omitted, inferred, normalized, or sidecar-only fields.
- Generated projection parse-back must parse generated projections only, not hand-authored source Markdown as replacement.
- Projection/parse-back equality must not resolve manual-review, domain-review, source-only, index/control, or status-normalization blockers.
- Aggregates must count skipped/blocked/review-required rows separately from projectable candidate rows.
- The subset must remain bounded; no globbing all `docs/adr/*.md` unless HERMES/USER explicitly changes the brief.

## Recommended acceptance criteria for ATHENA/HERMES brief

A Slice 4 implementation should be acceptable only if evidence shows:

1. Exactly the approved subset was inspected/attempted; no silent expansion to all ADRs.
2. `docs/adr/`, `docs/schemas/`, and ADR index/control Markdown were not mutated.
3. Every selected source has a per-source result row with source hash, reviewed Slice 1 values, observed status/casing, outcome, blockers, and artifact references or skip reason.
4. Candidate objects/projections/sidecars are under the dedicated `dev/` path only and marked generated evidence / non-authoritative.
5. Missing-status, manual-review, source-only, and index/control rows remain blocked/skipped as appropriate.
6. Accepted/current source statuses do not become accepted JSON authority.
7. Aggregate reports distinguish projectable, blocked, skipped, manual-review, source-only, and index/control outcomes.
8. JSON evidence validates, no `.sqlite`/`.db` files are created under the evidence path, and `git diff --check` passes.
9. Tests are added or updated if code changes, including regression for Slice 3 wrapped-list continuation preservation in multi-file mode.

## Non-authorizations

This Slice 4 input does not authorize:

- mutation of any `docs/adr/` file;
- mutation or publication of `docs/schemas/`;
- source status normalization;
- authoritative JSON ADR records;
- conversion of all ADRs;
- JSON authority cutover;
- database/storage authority;
- committed mutable `.sqlite` or `.db` files;
- file moves, renames, deletes, archives, or draft supersession;
- treating `dev/` evidence as durable authority;
- resolving template/schema-contract, source-only, index/control, or domain-review dispositions;
- product/future-system domain authority.

## KOIOS recommendation

Proceed with the six-entry primary subset for Slice 4. It is large enough to test multi-file corpus-style reporting and different reviewed dispositions, but small enough to keep provenance review tractable and avoid accidental product/domain authority. Add the optional domain-review canary only if HERMES/USER explicitly wants that risk exercised in this slice.
