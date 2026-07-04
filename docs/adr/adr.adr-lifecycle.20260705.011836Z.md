```json
{
  "title": "ADR Lifecycle and Naming Consolidation",
  "artifact_type": "adr",
  "status": "accepted",
  "datetime": "20260705.011836Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "docs/adr/",
  "proposal_surface": "dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md",
  "canonical_location": "docs/adr/adr.adr-lifecycle.20260705.011836Z.md",
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
  "accepted_from": "dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md"
}
```

# ADR 20260705.011836Z: ADR Lifecycle and Naming Consolidation

## Status

accepted

## Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this ADR are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

Non-normative provenance, context, examples, and validation notes do not create requirements unless they use those capitalized key words.

## Provenance

Origin: Athena workspace next-action selection from `workspaces/athena/active.md`
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap ADR control surface
Repository: projectkoios-bootstrap
Architecture-Domain: workflow/control-surface
Proposal-Review-Surface: `dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md`
Accepted-Location: `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
Accepted-By: user direction "go" after HERMES, VULCAN, and KOIOS review clearance
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

| Claim in this ADR | Primary source(s) | Treatment |
|---|---|---|
| Lifecycle states and transitions require reconciliation before acceptance | `docs/adr/adr.adr-lifecycle.draft.md`; `docs/policies/architecture.adr.lifecycle.md`; `docs/schemas/schema.record-base.json` | Consolidates old lifecycle wording with current schema vocabulary. |
| Spike packaging is draft ADR plus `ADR_implementation_plan` under a spike directory | `docs/adr/adr.adr-lifecycle.draft.md`; `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`; `docs/architecture/architecture.lifecycle.00.md` | Preserved, normalized to repo-relative `spike/<spike-id>/`. |
| Proposed ADRs use `dev/<proposal-id>/` as review surface | `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`; `docs/architecture/architecture.lifecycle.00.md` | Preserved, with `active review` terminology mapped to `proposed`. |
| Title and filename are separate naming layers | `docs/adr/adr.adr-names.draft.md`; `docs/architecture/architecture.adr.names.md` | Promoted only as umbrella distinction. |
| Detailed title and filename rules remain child guidance | `docs/adr/adr.adr-title-naming-convention.draft.md`; `docs/adr/adr.adr-filename-naming-convention.draft.md` | Not promoted as canonical detailed rules by this ADR. |
| Source-draft disposition must preserve trace and avoid silent supersession | Source drafts listed above; HERMES/VULCAN/KOIOS review inputs | Accepted only as bounded consolidation unless separate handoff supersedes specific drafts. |

## Context

The ADR control surface contains related draft documents for lifecycle, promotion mechanics, and naming. This ADR consolidates only the compatible subset after compatibility reconciliation:

- lifecycle state is separate from file status and workspace-local live-work markers
- current accepted/schema-backed practice uses `accepted`, `completed`, `superseded`, and `rejected` as record statuses
- older lifecycle drafts used `active` and `historical` language that must be reconciled before acceptance
- promotion mechanics preserve proposal, accepted/completed, superseded/historical, and rejected traceability
- ADR title is semantic display identity
- ADR filename is storage identity
- umbrella naming guidance organizes title and filename rules without collapsing them

This ADR is a bounded consolidation decision. It MUST preserve the source drafts as provenance and MUST NOT perform a broad refactor by implication.

The following source elements are explicitly out of scope for this ADR: lifecycle state ownership by role, required `proposed` sections, optional workflow gate fields, deprecated `docs/incubator/` and `docs/spikes/` migration, and the broader legacy-source index flow `idea -> spike -> draft ADR -> proposed ADR -> active ADR -> implementation brief -> iterative implementation`. Those elements MUST NOT become changed authority without separate acceptance or a separate documentation handoff.

## Decision

Project Koios MUST adopt the compatible subset of ADR lifecycle and naming drafts as one consolidated ADR control-surface decision.

### Lifecycle contract

ADR records governed by this ADR MUST use the following canonical status vocabulary, aligned with the current accepted/schema surface:

1. `draft`
2. `proposed`
3. `accepted`
4. `completed`
5. `superseded`
6. `rejected`

ADR lifecycle transitions MUST be limited to the following transitions unless a later accepted ADR changes this contract:

- `draft -> proposed -> accepted`
- `proposed -> rejected`
- `accepted -> completed`
- `accepted -> superseded`
- `completed -> superseded`
- `draft -> rejected`

`accepted` MUST mean that the decision is adopted as ADR authority. `completed` MUST mean that implementation, rollout, or documentation reconciliation is complete when applicable. Live review or work-in-progress state MUST use `draft`, `proposed`, or workspace control surfaces such as `workspaces/<role>/active.md`; it MUST NOT use ADR status `active`.

### Compatibility and migration contract

Existing ADRs and schema-backed records with `status: accepted` MUST remain valid. Acceptance of this ADR MUST NOT invalidate recent accepted ADR metadata or the `docs/schemas/schema.record-base.json` `RecordStatus` enum.

Compatibility terms from older drafts map as follows:

| Older term | Canonical status or meaning | Migration rule |
|---|---|---|
| `active` | `accepted` when the decision is adopted as authority; `completed` only after applicable rollout is complete | Implementations MUST treat this as legacy wording unless a separate migration handoff rewrites records. |
| `historical` | umbrella description for no-longer-current records, usually `superseded`; sometimes `completed` for finished non-current work | Implementations MUST NOT use this as a new record status unless a future schema migration explicitly adds it. |
| active review | `proposed` or workspace-local `active.md` | Implementations MUST NOT encode this as ADR status `active`. |

This ADR defines the compatibility mapping only. It MUST NOT authorize schema changes, tooling changes, bulk record rewrites, mass status migration, or file renames without a separate accepted implementation/documentation handoff.

### Promotion mechanics

Promotion MUST preserve traceability:

- A spike MUST be represented as a draft ADR plus `ADR_implementation_plan` under `spike/<spike-id>/`.
- A proposed ADR MUST be the review surface and SHOULD be located under `dev/<proposal-id>/`.
- An accepted ADR MUST be the authoritative decision record and SHOULD be located under `docs/adr/`.
- A completed ADR MUST record applicable implementation, rollout, or documentation-reconciliation completion.
- Superseded and rejected records MUST remain available as trace.
- Structured links MUST be the primary machine-readable promotion trail.

When lifecycle tooling is introduced, the `status` field MUST be the source of truth for lifecycle state. Path location, `artifact_type`, and structured links MAY provide supporting context and traceability. If supporting context disagrees with `status`, tooling MUST report the disagreement for reconciliation and MUST NOT silently infer a lifecycle state.

Structured link keys SHOULD include, where applicable: `proposal_surface`, `candidate_canonical_location`, `canonical_location`, `supersedes`, `superseded_by`, `derived_from`, `source_artifacts`, `back_to`, and `implementation_plan`.

### Naming contract

ADR naming MUST distinguish the following two layers:

- **Title**: semantic display name and queryable label
- **Filename**: filesystem/storage locator

Titles and filenames MAY differ. Index surfaces SHOULD render the semantic title and SHOULD NOT render the raw storage path as the title.

This accepted ADR's filename MUST use the user-corrected convention `adr.<topic>.<YYYYMMDD.HHMMSSZ>.md`, as applied at `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`. This ADR MUST NOT establish detailed filename rules for other ADRs. The older draft filename model `adr.<name>.md` / `adr.<name>.<status>.md` remains non-canonical draft guidance until a separate naming-rule reconciliation accepts, revises, or rejects it. Metadata timestamps SHOULD use the existing schema-compatible forms `YYYYMMDD.HHMMSS` or `YYYYMMDD.HHMMSSZ`; timezone suffix forms such as `PST` are legacy/proposal-local and SHOULD NOT be introduced as new canonical machine-parseable formats.

Detailed naming rules MUST remain encapsulated by the source naming drafts unless and until they are promoted or superseded by a separate accepted action:

- `docs/adr/adr.adr-title-naming-convention.draft.md`
- `docs/adr/adr.adr-filename-naming-convention.draft.md`

### Source-draft disposition

By this acceptance:

- This ADR MUST be the canonical consolidation surface for lifecycle/status compatibility and only the umbrella distinction between title and filename.
- Lifecycle and promotion-mechanics drafts MUST remain source/provenance records with links to this accepted ADR unless a separate follow-on action explicitly supersedes them.
- Naming umbrella and child naming drafts MUST remain non-canonical detailed guidance unless a follow-on acceptance explicitly promotes or supersedes them.
- Existing accepted ADRs MUST remain valid during any lifecycle vocabulary migration.
- Policy and architecture-index updates MUST require a separate implementation or documentation handoff unless explicitly included in the acceptance request.

## Consequences

- Reviewers get one accepted surface for the lifecycle/naming model instead of rediscovering the relationship across five drafts.
- This ADR preserves the separation between lifecycle state, workspace live-work state, semantic title, and storage filename.
- Existing drafts remain useful provenance and detailed guidance.
- Existing accepted records and current schema status vocabulary remain valid.
- Acceptance MUST NOT itself authorize code changes, schema/tooling changes, status migrations, or mass file renames.
- Future JSON-backed ADR storage MAY use title as semantic display identity and filename/path as storage identity without changing the lifecycle contract.

## Acceptance criteria

- A reviewer can identify the allowed ADR lifecycle states and transitions from this ADR alone.
- A reviewer can distinguish `proposed` review state from `accepted` ADR authority and `completed` rollout completion.
- A reviewer can identify how legacy `active`/`historical` wording maps to current `accepted`/`completed`/`superseded` vocabulary.
- A reviewer can distinguish ADR semantic title from ADR storage filename.
- The ADR names the source drafts it consolidates.
- The ADR MUST NOT silently rename files, rewrite historical records, change schemas/tooling, or grant implementation authority.
- This ADR can be superseded or amended without touching implementation files.

## Implementation brief

This ADR alone MUST NOT authorize implementation work.

If the user requests follow-on documentation work, the next documentation slice SHOULD:

1. update `docs/policies/architecture.adr.lifecycle.md` to point at the accepted ADR as the controlling decision
2. update `docs/architecture/architecture.lifecycle.00.md` and `docs/architecture/architecture.adr.names.md` to point at the accepted ADR where appropriate
3. mark or link the source drafts as provenance/superseded only to the extent explicitly accepted

Acceptance records an architecture/control-surface decision only. Acceptance MUST NOT rename files, migrate archives, update schemas, or change tooling behavior without a separate implementation/documentation handoff.

### Verification method

Manual documentation validation:

- A reviewer SHOULD inspect the accepted ADR and confirm lifecycle states, transitions, naming layers, and source-draft links are present.
- A reviewer SHOULD inspect policy/index surfaces and confirm they point at the accepted ADR without introducing implementation authority.
- A reviewer SHOULD confirm `git diff` contains only architecture/documentation changes.

## Resolved open questions

- The consolidation MUST NOT collapse title and filename semantics.
- The consolidation MUST NOT introduce ADR status `active` as a replacement for `accepted`.
- The consolidation MUST NOT treat proposed review state or workspace `active.md` state as accepted ADR authority.
- Superseded and rejected records MUST remain trace, not dead files.
- Detailed title and filename rules MUST remain non-canonical draft guidance in their existing child drafts until a follow-on action promotes or supersedes them.

## Non-goals

- This ADR MUST NOT rename existing ADR files.
- This ADR MUST NOT rewrite historical ADRs.
- This ADR MUST NOT change ADR JSON schemas.
- This ADR MUST NOT implement promotion tooling.
- This ADR MUST NOT edit product or implementation code.
- This ADR MUST NOT replace all ADR lifecycle documentation in one step.

## Validation expectations

- The accepted ADR is internally consistent with the listed source drafts.
- The ADR preserves provenance rather than erasing draft history.
- The ADR is bounded to the architecture/control-surface decision accepted by the user.

## Routing

- Owner: ATHENA
- Current phase: accepted
- Next owner: ATHENA/HERMES only if the user requests follow-on documentation/control-surface reconciliation
- Notes: This is an accepted architecture/control-surface decision only; follow-on policy/index/source-draft edits remain separate.

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
