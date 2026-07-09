# AAR 20260709.010828: KOIOS comments applied to skill brief

## Scope

ATHENA update to the template record round-trip skill implementation brief after receiving KOIOS provenance/process comments.

## What happened

- User requested KOIOS comments on the schema-backed template-record skill integration.
- KOIOS replied by intercom with concerns about status ambiguity, provisional schema-backed validation, and risk of making an incomplete contract reusable.
- ATHENA updated `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md` to require draft/gated skill status until durable VULCAN schema-backed parser report and ATHENA conformance review exist.

## Process issues

- The skill brief needed stronger language preventing future agents from treating a draft skill as stable completion evidence.
- File presence for `docs/schemas/template-record.schema.json` must not be treated as proof of schema-backed parser validation.

## Proposed follow-up improvements

- VULCAN should implement or update the schema-backed parser report before any stable skill registration.
- ATHENA should perform conformance review of the schema-backed parser revision and skill draft together.
- KOIOS should update process trace only after those artifacts exist.

## Candidate ADR or implementation topics

- Skill stability lifecycle tied to validation evidence.
- Schema-backed template-record parser validation gate.

## Current status

- KOIOS comments have been incorporated into the skill implementation brief.
- The skill remains a draft/gated implementation target.
- Packaging remains blocked until schema-backed parser validation is demonstrated and reviewed.
