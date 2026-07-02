# Architecture ADR Lifecycle Policy

## Purpose

This policy states the canonical ADR lifecycle for Project Koios bootstrap so reviewers and agents stop inventing lifecycle rules.

## Source of truth

- Canonical architecture decision: `docs/architecture/adr/adr.adr-lifecycle.draft.md`
- This policy is a consumption aid.
- If this policy conflicts with the ADR, the ADR wins.

## File status values

ADR files keep these human-facing statuses:

- `Draft`
- `Proposed`
- `Active`
- `Historical`
- `Rejected`

## Operational lifecycle states

These are the canonical operational states for ADR work:

1. `draft`
2. `proposed`
3. `active`
4. `historical`
5. `rejected`

## Canonical state meanings

- `draft` — comment-open working record
- `proposed` — active review surface and moving to dev
- `active` — implementation plan complete and ADR in production
- `historical` — superseded record after replacement
- `rejected` — archived record that did not proceed

## Canonical state ownership

- `draft` — Hermes
- `proposed` — Athena
- `active` — Vulcan
- `historical` — Athena
- `rejected` — Athena

## Required ADR sections at `proposed`

When an ADR reaches `proposed`, it must include these machine-relevant sections:

- `architecture-spec`
- `acceptance-criteria`
- `implementation-brief`
- `resolved-open-questions`
- `non-goals`
- `validation-expectations`
- `routing`

## Spike packaging rule

A draft ADR plus `ADR_implementation_plan` is a spike, and the spike lives in `reporoot/spike/<spike-id>/`.

## Canonical transitions

### Draft-to-production path

`draft -> proposed -> active`

### Replacement path

`active -> historical`

### Terminal rejection path

`draft -> rejected`

## Rules

- Do not invent new lifecycle states.
- Do not invent new allowed-next transitions.
- Do not use `active` as a synonym for `proposed`.
- Do not treat draft comments as acceptance.
- Do not mark an ADR complete without implementation-plan completion.
- Do not change lifecycle semantics without a new or superseding Athena ADR.
- `docs/incubator/` and `docs/spikes/` are deprecated and should be migrated out and deleted.

## Notes

- `Draft` / `Proposed` / `Active` / `Historical` / `Rejected` are ADR file statuses.
- `draft` / `proposed` / `active` / etc. are operational routing states.
- Draft ADRs are commentable before they move to `proposed`.
