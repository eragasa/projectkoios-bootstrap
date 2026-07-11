# AAR 20260711.153000: ADR JSON authority corpus dry-run inventory slice 4

## Scope

VULCAN implemented and validated `adr-json-authority-corpus-dry-run-inventory-slice-4` over the HERMES-approved six-entry subset.

## What happened

- Implemented a bounded corpus-style dry-run runner.
- Generated per-source results, aggregate counts, candidate objects, projections, sidecars, skipped/blocked evidence, and conflict/lossiness reporting under `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`.
- Preserved Slice 2 missing-status behavior and Slice 3 wrapped-list/status-casing behavior in multi-file mode.
- Kept README as index/control skipped and lifecycle draft as source/provenance skipped/blocked.
- Validated tests, mypy, Python policy, JSON validity, no DB files, source/schema non-mutation, aggregate count consistency, projection location, and diff hygiene.
- After KOIOS provenance review, corrected source-to-candidate omission visibility by enumerating omitted/source-preserved sections per source and in aggregates.

## Process issues

- Multi-file dry-run evidence increased the importance of aggregate/per-source consistency checks; explicit count validation was useful.
- The prior Slice 3 wrapped-list issue made it necessary to add direct source-to-candidate regression assertions rather than relying only on projection parse-back equality.
- The initial Slice 4 aggregate evidence still over-emphasized candidate/projection equality and did not enumerate all source sections omitted from reduced candidates.

## Proposed follow-up improvements

- Add a reusable aggregate-count checker if later slices expand subset reporting.
- Consider a shared evidence-only Markdown extraction helper before adding more dry-run sources.
- Continue requiring source-to-candidate regression assertions for any previously discovered lossiness pattern.
- Future reduced-candidate dry runs should require omitted-section inventories from the first implementation pass.

## Candidate ADR or implementation topics

- Whether future subset dry-runs should include a domain-review row remains a HERMES/ATHENA/KOIOS decision.
- Whether source/provenance drafts should have a dedicated non-ADR evidence record type remains unresolved.

## Current status

Slice 4 is implemented and validated. Next required state is KOIOS provenance review and ATHENA architecture/conformance review before HERMES final acceptance.
