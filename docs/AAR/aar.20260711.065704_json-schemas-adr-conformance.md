# AAR 20260711.065704: JSON schemas ADR conformance

## Scope

VULCAN implementation of the approved one-document active conformance slice for `docs/adr/adr.json-schemas.draft.md`.

## What happened

- VULCAN implemented a target-specific conformance runner using the existing ADR parser/validator, ADR storage adapter, and generic document store.
- The run generated `dev/adr-json-schemas-conformance/` artifacts for the active conformed record, projection, manifest, mapping, database evidence, and conversion sidecar.
- Source-only `routing.*` and `links.related` data were preserved in sidecars and omitted from the schema record.
- Validation passed across focused and full test suites plus type/lint/policy checks.

## Process issues

- The existing projection renderer assumed a `pilot` manifest block. The implementation needed a small compatibility adjustment so it can render both pilot and conformance manifests without creating a new projection policy.
- Python policy comments required additional local-purpose comments in the new conformance runner and tests.

## Proposed follow-up improvements

- If more single-ADR conformance slices are approved, consider extracting a small target configuration model for repeated conformance runs, while avoiding reusable repository-level storage authority until approved.
- ATHENA should review whether `links.related` should eventually be represented in the ADR schema or remain sidecar-only.

## Candidate ADR or implementation topics

- ADR schema treatment for related links.
- Projection vocabulary for active JSON checkpoints versus generated Markdown review artifacts.
- Target-local conformance manifest vocabulary if this pattern repeats.

## Current status

Implemented and validated. Awaiting ATHENA/user/Hermes review.
