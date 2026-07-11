# AAR 20260711.150000: ADR JSON authority projectable messy canary slice 3

## Scope

VULCAN implemented and validated `adr-json-authority-projectable-messy-canary-slice-3` for exactly one source: `docs/adr/adr.adr-template-contract.md`.

## What happened

- Implemented a projectable messy-canary runner and focused tests.
- Generated candidate-only evidence under `dev/adr-json-authority-projectable-messy-canary-slice-3/`.
- Preserved observed status `Accepted` separately from normalized candidate `accepted`.
- Generated non-authoritative projection evidence under `dev/` only and parse-back evidence that reads only that projection.
- Validated tests, mypy, Python policy, JSON validity, no DB files, source/schema non-mutation, projection location, and diff hygiene.
- After KOIOS provenance review, corrected wrapped-list continuation preservation and regenerated evidence.

## Process issues

- The Python policy local-variable comment rule required a second pass after the initial implementation. This was caught before closeout and corrected.
- The existing ADR Markdown parser is intentionally narrow and did not directly parse the template-contract ADR's hyphenated headings; Slice 3 used a local bounded parser to avoid broadening parser behavior beyond the brief.
- The initial local bullet parser missed indented continuation text, showing that projectability evidence needs source-to-candidate lossiness checks beyond candidate/projection parse-back equality.

## Proposed follow-up improvements

- Consider extracting reusable evidence-only Markdown section parsing if future canary slices need similar handling.
- Add explicit source-to-candidate assertions for wrapped Markdown constructs in future canary tests.
- Consider adding a command wrapper for Slice 2/Slice 3 evidence generation if these canaries become a repeated migration workflow.
- Keep projection/parse-back helpers explicit about evidence-only authority to reduce review ambiguity.

## Candidate ADR or implementation topics

- Whether status casing normalization should be schema-level, migration-level, or review-level policy remains an architecture/review decision.
- Whether template/schema-contract ADRs should become normal ADR records or stay excluded/manual-review remains unresolved.

## Current status

Slice 3 is implemented and validated. Next required state is KOIOS provenance review and ATHENA architecture/conformance review before HERMES final acceptance.
