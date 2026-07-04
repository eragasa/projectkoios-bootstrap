# Architecture ADR Lifecycle Policy

## Purpose

This policy is a consumption aid for the accepted Project Koios bootstrap ADR lifecycle decision.

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this policy are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Source of truth

- Canonical architecture decision: `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- Review/proposal surface: `dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md`
- Prior lifecycle draft: `docs/adr/adr.adr-lifecycle.draft.md`
- Prior promotion-mechanics draft: `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`
- This policy is a consumption aid.
- If this policy conflicts with the accepted ADR, the accepted ADR wins.

## Canonical ADR record statuses

ADR records governed by the accepted lifecycle ADR MUST use these statuses:

1. `draft`
2. `proposed`
3. `accepted`
4. `completed`
5. `superseded`
6. `rejected`

## Canonical status meanings

- `draft` — working record not yet adopted as a review surface.
- `proposed` — review surface pending acceptance or rejection.
- `accepted` — adopted ADR authority.
- `completed` — accepted decision with applicable implementation, rollout, or documentation reconciliation complete.
- `superseded` — no longer current because another accepted record replaced it.
- `rejected` — record that did not proceed.

## Canonical transitions

Allowed lifecycle transitions are:

- `draft -> proposed -> accepted`
- `proposed -> rejected`
- `accepted -> completed`
- `accepted -> superseded`
- `completed -> superseded`
- `draft -> rejected`

## Compatibility mapping

Older lifecycle language MUST be read through this compatibility map unless a later accepted ADR changes it:

| Older term | Canonical status or meaning |
|---|---|
| `active` | `accepted` when the decision is adopted as authority; `completed` only after applicable rollout is complete. |
| `historical` | Usually `superseded`; sometimes `completed` for finished non-current work. |
| active review | `proposed` or workspace-local `active.md`, not ADR status `active`. |

ADR status `active` MUST NOT be introduced as a canonical record status by this policy.

## Spike and proposal surfaces

- A spike MUST be represented as a draft ADR plus `ADR_implementation_plan` under `spike/<spike-id>/`.
- A proposed ADR SHOULD be located under `dev/<proposal-id>/` when it is a review surface outside `docs/adr/`.
- An accepted ADR SHOULD be located under `docs/adr/`.

## Traceability

Promotion and disposition SHOULD preserve traceability with structured links such as:

- `proposal_surface`
- `candidate_canonical_location`
- `canonical_location`
- `supersedes`
- `superseded_by`
- `derived_from`
- `source_artifacts`
- `back_to`
- `implementation_plan`

If lifecycle tooling is introduced, the `status` field MUST be the lifecycle source of truth. Path location, `artifact_type`, and structured links MAY provide context. Tooling MUST report disagreement between these surfaces and MUST NOT silently infer lifecycle state from path or link context.

## Deferred surfaces

The accepted ADR intentionally does not settle these older draft elements:

- lifecycle state ownership by role
- required `proposed` sections
- optional workflow gate fields
- deprecated `docs/incubator/` and `docs/spikes/` migration
- broader legacy-source index flow from idea through iterative implementation

Those elements MUST NOT become changed authority without separate acceptance or documentation handoff.
