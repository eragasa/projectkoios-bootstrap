# ADR Lifecycle Policy

## Purpose

This policy states the canonical ADR lifecycle for Project Koios bootstrap so reviewers and agents stop inventing lifecycle rules.

## Source of truth

- Canonical architecture decision: `docs/architecture/adr/adr.20260630.175315_athena-owned-adr-lifecycle.md`
- This policy is a consumption aid.
- If this policy conflicts with the accepted ADR, the ADR wins.

## File status values

ADR files keep these human-facing statuses:

- `Draft`
- `Accepted`
- `Completed`
- `Superseded`
- `Rejected`

## Operational lifecycle phases

These are the canonical operational phases:

1. `intake`
2. `proposed`
3. `review`
4. `accepted`
5. `implementation_ready`
6. `implementing`
7. `implementation_review`
8. `validated`
9. `completed`

## Canonical phase ownership

- `intake` — Hermes
- `proposed` — Athena
- `review` — Hermes
- `accepted` — Athena
- `implementation_ready` — Hermes
- `implementing` — Vulcan
- `implementation_review` — Vulcan
- `validated` — Hermes
- `completed` — Hermes

## Required ADR sections at `proposed`

When an ADR reaches `proposed`, it must include these machine-relevant sections:

- `architecture-spec`
- `acceptance-criteria`
- `implementation-brief`
- `resolved-open-questions`
- `non-goals`
- `validation-expectations`
- `routing`

## Canonical transitions

### Implementation-bearing path

`intake -> proposed -> review -> accepted -> implementation_ready -> implementing -> implementation_review -> validated -> completed`

### No-implementation path

`intake -> proposed -> review -> accepted -> validated -> completed`

## Rules

- Do not invent new lifecycle phases.
- Do not invent new allowed-next transitions.
- Do not use `implementation_review` as Hermes validation.
- Do not treat draft comments as acceptance.
- Do not mark an ADR complete without Hermes validation.
- Do not change lifecycle semantics without a new or superseding Athena ADR.
- Use `graphify update .` for session-boundary rebuilds; do not substitute a semantic refresh.

## Notes

- `Draft` / `Accepted` / `Completed` / `Superseded` / `Rejected` are ADR file statuses.
- `intake` / `proposed` / `review` / etc. are operational routing phases.
- Draft ADRs are commentable before they move to `proposed`.
