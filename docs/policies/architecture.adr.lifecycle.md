# Architecture ADR Lifecycle Policy

## Purpose

This policy is a consumption aid for the active Project Koios bootstrap ADR lifecycle decision.

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this policy are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Source of truth

- Canonical architecture decision: `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- Review/proposal surface: `dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md`
- Prior lifecycle draft: `docs/adr/adr.adr-lifecycle.draft.md`
- Prior promotion-mechanics draft: `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`
- This policy is a consumption aid.
- If this policy conflicts with the active ADR, the active ADR wins.

## Canonical ADR record statuses

ADR records governed by the active lifecycle ADR MUST use these statuses:

1. `proposal`
2. `draft`
3. `accepted`
4. `active`
5. `superseded`

## Canonical status meanings

- `proposal` — candidate idea or review packet that is not yet shaped as a complete ADR.
- `draft` — complete enough to review as an ADR, but not accepted authority.
- `accepted` — approved document authority, but not necessarily enforced, implemented, or current as the active controlling surface.
- `active` — accepted and current controlling authority for work, enforcement, routing, or document interpretation.
- `superseded` — no longer current because another accepted or active record replaced or narrowed it.

## Canonical transitions

Allowed lifecycle transitions are:

- `proposal -> draft -> accepted -> active`
- `accepted -> superseded`
- `active -> superseded`
- `draft -> superseded`
- `proposal -> superseded`

## Compatibility mapping

Older lifecycle language MUST be read through this compatibility map unless a later accepted ADR changes it:

| Older term | Canonical status or meaning |
|---|---|
| `proposed` | `proposal` for candidate/review packets; `draft` when the document is complete enough for ADR review. |
| `completed` | `active` when the decision remains controlling after rollout; `superseded` when the completed work is no longer current. |
| `rejected` | no longer a canonical ADR status; preserve as review outcome/provenance or mark the candidate `superseded` when a durable record must remain. |
| `historical` | Usually `superseded`; otherwise an archive/provenance label, not ADR status. |
| active review | `proposal`, `draft`, or workspace-local `active.md`, depending on whether the review packet is an ADR record. |

ADR status `active` is canonical only for accepted records that are current controlling authority. Workspace-local `active.md` remains a separate live-work control surface and MUST NOT be confused with ADR status `active`.

## Spike and proposal surfaces

- A spike SHOULD be represented as a `proposal` or `draft` ADR plus `ADR_implementation_plan` under `spike/<spike-id>/` until the spike workflow is separately reconciled.
- A `proposal` ADR SHOULD be located under `dev/<proposal-id>/` when it is a candidate/review packet outside `docs/adr/`.
- An `accepted` or `active` ADR SHOULD be located under `docs/adr/`.

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

The active ADR intentionally does not settle these older draft elements:

- lifecycle state ownership by role
- required `proposal` or `draft` sections
- optional workflow gate fields
- deprecated `docs/incubator/` and `docs/spikes/` migration
- broader legacy-source index flow from idea through iterative implementation

Those elements MUST NOT become changed authority without separate acceptance, activation, or documentation handoff.
