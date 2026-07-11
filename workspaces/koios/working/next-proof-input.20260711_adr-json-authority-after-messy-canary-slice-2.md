```json
{
  "title": "KOIOS next proof input: ADR JSON authority after messy canary slice 2",
  "artifact_type": "provenance-next-proof-input",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "next bounded ADR JSON authority proof point after messy canary slice 2"
}
```

# KOIOS next proof input: ADR JSON authority after messy canary slice 2

## Authority boundary

This note is KOIOS provenance input only. It does not authorize source mutation, schema changes, conversion authority, file moves/renames, or JSON authority cutover.

## Current state

`adr-json-authority-messy-canary-slice-2` proved the migration machinery can preserve a source with missing top-level ADR status and block authority rather than invent a status. The next useful proof should test a source that is messy but likely projectable, so the workflow can exercise projection/parse-back and conflict/lossiness reporting without relying on a fully clean record.

## Recommended next proof point

### Primary recommendation: `docs/adr/adr.adr-template-contract.md`

Slice 1 reviewed values:

- `source_hash`: `2876dfbe031105d383fa9e33cec7d5dd49cf569cea6f43eae59e8fa1da502895`
- `category_candidate`: `template_schema_contract`
- `disposition_candidate`: `manual_review_required`
- `authority_effect`: `candidate`
- `automatic_conversion_eligibility_candidate`: `false`
- `exclusion_blocking_reasons`: `manual_review_required`, `status_casing_or_text_would_normalize`
- `owner_domain_review_flags.manual_review_required`: `true`

Why this is the best next proof:

- It is messy but likely projectable: it has a parseable `## Status` section, but the observed status is `Accepted` with non-canonical casing.
- It directly concerns ADR schema/template authority, so it is relevant to the JSON-authoritative ADR store path.
- It exercises status casing preservation and normalization policy without the missing-status blocker from `adr.schema-base.md`.
- It has template/contract ambiguity, so the candidate object must preserve classification/disposition outside ADR `content`.
- It is not primarily a product/future-system/domain file, so it is safer than agent/UI/training candidates.

Expected outcome:

- `candidate_object_generated_with_review_flags` or equivalent, not authority cutover.
- Generated projection may be appropriate if content can be represented without inventing fields.
- Original observed status casing `Accepted` must be preserved in sidecar/provenance.
- Any normalized content status candidate such as `accepted` must be explicitly marked as normalization requiring review, not as a source rewrite.
- Projection equality must not resolve the status-casing authority question by itself.

Required watchpoints:

- Do not mutate `docs/adr/adr.adr-template-contract.md`.
- Do not silently normalize source status casing.
- Do not treat `Accepted` as final accepted JSON authority without HERMES/USER review.
- Preserve that this is a template/schema contract surface, not a plain decision record.
- Preserve source hash, title, observed status/casing, reviewed Slice 1 values, normalization warning, and sidecar evidence.
- If projection is generated, it must live under a dedicated `dev/` evidence path and be marked generated evidence only.

## Safer alternative if HERMES/USER wants lower authority risk

### `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`

Slice 1 reviewed values:

- `source_hash`: `d8f468f9ed031223067c48c677e82b7d962314083b9b1cf0cff276a9b8ae4e77`
- `category_candidate`: `template_schema_contract`
- `disposition_candidate`: `manual_review_required`
- `authority_effect`: `candidate`
- `automatic_conversion_eligibility_candidate`: `false`
- `exclusion_blocking_reasons`: `manual_review_required`

Why it is safer:

- It has lower-case `draft` status, so it avoids accepted-status authority ambiguity.
- It is likely projectable and can test mixed template/ingestion scope handling.
- It still requires manual review because template/ingestion boundaries can touch product-domain ingestion vocabulary.

Tradeoff:

- It is less useful for proving status casing normalization/preservation, which remains an important migration risk.

## Candidate to defer

### `docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md`

Although Slice 1 listed it as alternate messy canary, KOIOS recommends deferring it until after a template/schema contract canary because it is `product_future_system_draft` / `domain_review_required` and has training/product implications. It is valuable later for domain-review behavior, not as the immediate next proof after `adr.schema-base.md`.

## Recommended next slice shape

Candidate slice name:

```text
adr-json-authority-projectable-canary-slice-3
```

Minimum scope:

- exactly one source, preferably `docs/adr/adr.adr-template-contract.md`;
- candidate-only object evidence under `dev/`;
- preserve observed status/casing separately from normalized candidate;
- sidecar/provenance for template-contract classification and normalization warning;
- generated projection and parse-back only if no fields must be invented;
- conflict/lossiness report that explicitly names status-casing normalization and template-contract ambiguity;
- no source mutation, no schema mutation, no authority cutover, no database authority.

## KOIOS recommendation

Proceed with `docs/adr/adr.adr-template-contract.md` if the goal is to prove messy-but-projectable behavior. Use the template-representation draft only if HERMES/USER wants a lower-risk projectable source before testing noncanonical accepted-status casing.
