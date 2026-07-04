```json
{
  "title": "ADR Lifecycle and Naming Consolidation",
  "artifact_type": "adr-proposal",
  "status": "proposed",
  "datetime": "20260705.010958",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "docs/adr/",
  "proposal_surface": "dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md",
  "candidate_canonical_location": "docs/adr/adr.adr-lifecycle.20260705.011836Z.md",
  "source_artifacts": [
    "docs/adr/adr.adr-lifecycle.draft.md",
    "docs/adr/adr.adr-lifecycle-promotion-mechanics.md",
    "docs/adr/adr.adr-names.draft.md",
    "docs/adr/adr.adr-title-naming-convention.draft.md",
    "docs/adr/adr.adr-filename-naming-convention.draft.md",
    "docs/architecture/architecture.lifecycle.00.md",
    "docs/architecture/architecture.adr.names.md",
    "docs/policies/architecture.adr.lifecycle.md",
    "docs/schemas/schema.record-base.json"
  ],
  "review_inputs": [
    "HERMES review: revise-before-acceptance for lifecycle vocabulary compatibility",
    "VULCAN review: implementation-ready after accepted/active compatibility clarification",
    "KOIOS review: add claim-level provenance and tighten non-authority boundaries"
  ],
  "next_phase": "HERMES/user review for acceptance after revision"
}
```

# ADR 20260705.010958: ADR Lifecycle and Naming Consolidation

## Status

proposed

## Provenance

Origin: Athena workspace next-action selection from `workspaces/athena/active.md`
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap ADR control surface
Repository: projectkoios-bootstrap
Architecture-Domain: workflow/control-surface
Proposal-Review-Surface: `dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md`
Source ADR drafts:

- `docs/adr/adr.adr-lifecycle.draft.md`
- `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`
- `docs/adr/adr.adr-names.draft.md`
- `docs/adr/adr.adr-title-naming-convention.draft.md`
- `docs/adr/adr.adr-filename-naming-convention.draft.md`

Consumption/index/schema surfaces reviewed for compatibility:

- `docs/architecture/architecture.lifecycle.00.md`
- `docs/architecture/architecture.adr.names.md`
- `docs/policies/architecture.adr.lifecycle.md`
- `docs/schemas/schema.record-base.json`

Claim/source traceability:

| Claim in this proposal | Primary source(s) | Treatment |
|---|---|---|
| Lifecycle states and transitions require reconciliation before acceptance | `docs/adr/adr.adr-lifecycle.draft.md`; `docs/policies/architecture.adr.lifecycle.md`; `docs/schemas/schema.record-base.json` | Consolidates old lifecycle wording with current schema vocabulary. |
| Spike packaging is draft ADR plus `ADR_implementation_plan` under a spike directory | `docs/adr/adr.adr-lifecycle.draft.md`; `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`; `docs/architecture/architecture.lifecycle.00.md` | Preserved, normalized to repo-relative `spike/<spike-id>/`. |
| Proposed ADRs use `dev/<proposal-id>/` as review surface | `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`; `docs/architecture/architecture.lifecycle.00.md` | Preserved, with `active review` terminology mapped to `proposed`. |
| Title and filename are separate naming layers | `docs/adr/adr.adr-names.draft.md`; `docs/architecture/architecture.adr.names.md` | Promoted only as umbrella distinction. |
| Detailed title and filename rules remain child guidance | `docs/adr/adr.adr-title-naming-convention.draft.md`; `docs/adr/adr.adr-filename-naming-convention.draft.md` | Not promoted as canonical detailed rules by this proposal. |
| Source-draft disposition must preserve trace and avoid silent supersession | Source drafts listed above; HERMES/VULCAN/KOIOS review inputs | Accepted only as bounded consolidation unless separate handoff supersedes specific drafts. |

## Context

The ADR control surface has several related but still-draft documents for lifecycle, promotion mechanics, and naming. They express a coherent enough model to consolidate only after compatibility reconciliation:

- lifecycle state is separate from file status and workspace-local live-work markers
- current accepted/schema-backed practice uses `accepted`, `completed`, `superseded`, and `rejected` as record statuses
- older lifecycle drafts used `active` and `historical` language that must be reconciled before acceptance
- promotion mechanics preserve proposal, accepted/completed, superseded/historical, and rejected traceability
- ADR title is semantic display identity
- ADR filename is storage identity
- umbrella naming guidance organizes title and filename rules without collapsing them

The next useful architecture step is not a broad refactor. It is a bounded consolidation slice that makes the compatible subset explicit as one reviewable proposal, while preserving the source drafts as provenance.

Deferred source elements remain out of scope for this proposal: lifecycle state ownership by role, required `proposed` sections, optional workflow gate fields, deprecated `docs/incubator/` and `docs/spikes/` migration, and the broader `idea -> spike -> draft ADR -> proposed ADR -> active ADR -> implementation brief -> iterative implementation` index flow. Those elements require separate acceptance or documentation handoff before becoming changed authority.

## Decision

Adopt the ADR lifecycle and naming drafts as one consolidated ADR control-surface proposal.

### Lifecycle contract

The canonical ADR record statuses are aligned with the current accepted/schema surface:

1. `draft`
2. `proposed`
3. `accepted`
4. `completed`
5. `superseded`
6. `rejected`

The canonical transitions are:

- `draft -> proposed -> accepted`
- `proposed -> rejected`
- `accepted -> completed`
- `accepted -> superseded`
- `completed -> superseded`
- `draft -> rejected`

`accepted` means the decision is adopted as ADR authority. `completed` means implementation, rollout, or documentation reconciliation is complete when applicable. Live review/work-in-progress MUST use `draft`, `proposed`, or workspace control surfaces such as `workspaces/<role>/active.md`, not ADR status `active`.

### Compatibility and migration contract

Existing ADRs and schema-backed records with `status: accepted` remain valid. Acceptance of this ADR MUST NOT invalidate recent accepted ADR metadata or the `docs/schemas/schema.record-base.json` `RecordStatus` enum.

Compatibility terms from older drafts map as follows:

| Older term | Canonical status or meaning | Migration rule |
|---|---|---|
| `active` | `accepted` when the decision is adopted as authority; `completed` only after applicable rollout is complete | Treat as legacy wording unless a separate migration handoff rewrites records. |
| `historical` | umbrella description for no-longer-current records, usually `superseded`; sometimes `completed` for finished non-current work | Do not use as a new record status unless a future schema migration explicitly adds it. |
| active review | `proposed` or workspace-local `active.md` | Never encode as ADR status `active`. |

This proposal defines the compatibility mapping only. It does not authorize schema/tooling changes, bulk record rewrites, mass status migration, or file renames without a separate accepted implementation/documentation handoff.

### Promotion mechanics

Promotion MUST preserve traceability:

- a spike is a draft ADR plus `ADR_implementation_plan` under `spike/<spike-id>/`
- a proposed ADR is the review surface and moves to `dev/<proposal-id>/`
- an accepted ADR is the authoritative decision record, normally under `docs/adr/`
- a completed ADR records applicable implementation/rollout completion
- superseded and rejected records remain available as trace
- structured links are the primary machine-readable promotion trail

When lifecycle tooling is introduced, the status field is the source of truth for lifecycle state. Path location, `artifact_type`, and structured links provide supporting context and traceability; if they disagree with `status`, the record requires reconciliation rather than silent inference.

Expected structured link keys include, where applicable: `proposal_surface`, `candidate_canonical_location`, `canonical_location`, `supersedes`, `superseded_by`, `derived_from`, `source_artifacts`, `back_to`, and `implementation_plan`.

### Naming contract

ADR naming has two layers:

- **Title**: semantic display name and queryable label
- **Filename**: filesystem/storage locator

Titles and filenames MAY differ. Index surfaces SHOULD render the semantic title, not the raw storage path.

Canonical accepted ADR filenames for this accepted artifact use the user-corrected convention `adr.<topic>.<YYYYMMDD.HHMMSSZ>.md`, yielding `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`. The older draft filename model `adr.<name>.md` / `adr.<name>.<status>.md` remains non-canonical draft guidance until a separate naming-rule reconciliation accepts, revises, or rejects it. Metadata timestamps SHOULD prefer the existing schema-compatible forms `YYYYMMDD.HHMMSS` or `YYYYMMDD.HHMMSSZ`; timezone suffix forms such as `PST` are legacy/proposal-local and SHOULD NOT be introduced as new canonical machine-parseable formats.

Detailed naming rules remain encapsulated by the source naming drafts unless and until they are promoted or superseded:

- `docs/adr/adr.adr-title-naming-convention.draft.md`
- `docs/adr/adr.adr-filename-naming-convention.draft.md`

### Source-draft disposition

If this proposal is accepted:

- the accepted ADR becomes the canonical consolidation surface for lifecycle/status compatibility and only the umbrella distinction between title and filename
- lifecycle and promotion-mechanics drafts remain source/provenance records with links to the accepted ADR unless a separate follow-on action explicitly supersedes them
- naming umbrella and child naming drafts remain non-canonical detailed guidance unless a follow-on acceptance explicitly promotes or supersedes them
- existing accepted ADRs remain valid during any lifecycle vocabulary migration
- policy and architecture-index updates require separate implementation or documentation handoff unless explicitly included in the acceptance request

## Consequences

- Reviewers get one proposed surface for the lifecycle/naming model instead of rediscovering the relationship across five drafts.
- The proposal preserves the separation between lifecycle state, workspace live-work state, semantic title, and storage filename.
- Existing drafts remain useful provenance and detailed guidance.
- Existing accepted records and current schema status vocabulary remain valid.
- Acceptance does not itself authorize code changes, schema/tooling changes, status migrations, or mass file renames.
- Future JSON-backed ADR storage can use title as semantic display identity and filename/path as storage identity without changing the lifecycle contract.

## Acceptance criteria

- A reviewer can identify the allowed ADR lifecycle states and transitions from this proposal alone.
- A reviewer can distinguish `proposed` review state from `accepted` ADR authority and `completed` rollout completion.
- A reviewer can identify how legacy `active`/`historical` wording maps to current `accepted`/`completed`/`superseded` vocabulary.
- A reviewer can distinguish ADR semantic title from ADR storage filename.
- The proposal names the source drafts it consolidates.
- The proposal does not silently rename files, rewrite historical records, change schemas/tooling, or grant implementation authority.
- The proposal can be accepted, revised, or rejected without touching implementation files.

## Implementation brief

No implementation is authorized by this proposal alone.

If HERMES/user accepts the proposal and requests follow-on documentation work, the next documentation slice should:

1. create an accepted ADR in `docs/adr/` from this proposal using the user-corrected filename convention `adr.<topic>.<YYYYMMDD.HHMMSSZ>.md`
2. update `docs/policies/architecture.adr.lifecycle.md` to point at the accepted ADR as the controlling decision
3. update `docs/architecture/architecture.lifecycle.00.md` and `docs/architecture/architecture.adr.names.md` to point at the accepted ADR where appropriate
4. mark or link the source drafts as provenance/superseded only to the extent explicitly accepted

Acceptance records an architecture/control-surface decision only. It does not rename files, migrate archives, update schemas, or change tooling behavior without a separate implementation/documentation handoff.

### Verification method

Manual documentation validation:

- inspect the accepted ADR and confirm lifecycle states, transitions, naming layers, and source-draft links are present
- inspect policy/index surfaces and confirm they point at the accepted ADR without introducing implementation authority
- confirm `git diff` contains only architecture/documentation changes

## Resolved open questions

- The consolidation should not collapse title and filename semantics.
- The consolidation should not introduce ADR status `active` as a replacement for `accepted`.
- The consolidation should not treat proposed review state or workspace `active.md` state as accepted ADR authority.
- Superseded and rejected records remain trace, not dead files.
- Detailed title and filename rules remain non-canonical draft guidance in their existing child drafts until a follow-on action promotes or supersedes them.

## Non-goals

- Renaming existing ADR files
- Rewriting historical ADRs
- Changing ADR JSON schemas
- Implementing promotion tooling
- Editing product or implementation code
- Replacing all ADR lifecycle documentation in one step

## Validation expectations

- The consolidated proposal is internally consistent with the listed source drafts.
- The proposal preserves provenance rather than erasing draft history.
- The proposal is suitable for HERMES/user acceptance, revision, or rejection as a bounded architecture slice.

## Routing

- Owner: ATHENA
- Current phase: proposed
- Next owner: HERMES/user for review decision
- Notes: This is an architecture/control-surface proposal only.

## Links

- `docs/adr/adr.adr-lifecycle.draft.md`
- `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`
- `docs/adr/adr.adr-names.draft.md`
- `docs/adr/adr.adr-title-naming-convention.draft.md`
- `docs/adr/adr.adr-filename-naming-convention.draft.md`
- `docs/architecture/architecture.lifecycle.00.md`
- `docs/architecture/architecture.adr.names.md`
- `docs/policies/architecture.adr.lifecycle.md`
- `docs/schemas/schema.record-base.json`
