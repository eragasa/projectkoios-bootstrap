# AAR 20260709.014124: ADR JSON/database pilot brief

## Scope

ATHENA response to HERMES/user architecture-intake requesting a bounded one-ADR schema-backed JSON/database pilot before any bulk ADR migration.

## What happened

- ATHENA inspected the existing draft ADR `docs/adr/adr.json-database-for-adr-storage.draft.md`.
- ATHENA used Graphify for broad repository context and confirmed existing schema/projection concepts in `docs/schemas/schema.record-base.json` and `docs/schemas/adr.schema.json`.
- ATHENA wrote `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`.
- The brief scopes a one-ADR pilot using `docs/adr/adr.json-database-for-adr-storage.draft.md` and requires explicit authority-model comparison before any migration.
- KOIOS reviewed the brief for provenance safety via intercom session `subagent-chat-019f4487`. ATHENA incorporated watchpoints for source-request provenance, derivative/non-authoritative pilot artifacts, source draft preservation, schema/projection metadata gaps, mapping normalization, inspectable DB evidence, round-trip equality policy, and evidence-vs-recommendation separation.
- VULCAN reviewed the brief for implementability via intercom session `subagent-chat-019f4471`. ATHENA incorporated clarifications on plain ADR schema shape, fixture normalization rules, pilot-safe output paths, implemented authority mode, test expectations, semantic equality, validation commands, and package boundary.

## Process issues

- The user direction intentionally conflicts with the current draft ADR's cache-only database posture. The brief preserves that as an architecture decision gap instead of silently resolving it.
- The source request is currently intercom/session-relayed rather than a durable committed request artifact; the brief now marks that provenance limitation for follow-up ADR use.
- The existing ADR schema is a plain ADR object while the record-base schema has envelope/projection concepts; the brief now prevents VULCAN from being asked to satisfy both schemas with one artifact implicitly.
- Current repo state already had uncommitted KOIOS workspace artifacts unrelated to this Athena brief; ATHENA did not package or commit from this workspace.

## Proposed follow-up improvements

- After pilot implementation evidence exists, revise or replace the draft ADR so the authority model is no longer ambiguous.
- Keep ADR JSON/database work separated into pilot, conformance review, and only then migration planning.

## Candidate ADR or implementation topics

- ADR storage authority model: JSON file, database row/document, or hybrid checkpoint.
- Projection metadata and stale-projection detection for `docs/adr/`.
- Repository policy for committing or regenerating database artifacts.

## Current status

A bounded Athena brief exists with KOIOS provenance and VULCAN implementability watchpoints incorporated. No ADR migration or implementation has started.
