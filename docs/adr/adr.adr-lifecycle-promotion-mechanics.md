# ADR 20260702.185000: ADR Lifecycle Promotion Mechanics

## Status

draft

## Accepted control

This draft is retained as source/provenance for accepted ADR `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`.

This draft is not canonical where it conflicts with the accepted ADR.

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The ADR lifecycle needs one concrete rule for promotion mechanics so reviewers and agents stop inventing their own draft-to-proposed behavior. The current model needs to capture three distinct things:

- how a spike is packaged
- how a draft becomes proposed
- how a proposed ADR becomes active in production

## Decision

Use explicit promotion mechanics for ADR work.

### Spike packaging

A draft ADR plus `ADR_implementation_plan` is a spike, and the spike lives in `reporoot/spike/<spike-id>/`.

### Draft-to-proposed promotion

When a draft ADR is promoted to proposed:

- the proposed ADR becomes the active review surface
- the proposed ADR represents the move to dev
- `reporoot/dev/<proposal-id>/` is the only dev location for ADR proposals that are not active yet
- monkey-patched classes may be used if needed to align the ADR with the current repository
- the draft remains historical context until it is superseded or replaced

### Proposed-to-active promotion

When a proposed ADR becomes active:

- the implementation plan is complete
- the ADR is in production
- the active ADR is the operational record of the decision
- active ADR filenames may later move toward `ADR.YYYYMMDDHHMMSS[a-z]` once the hierarchy stabilizes

### Historical and rejection mechanics

- `historical` means the ADR was superseded
- `rejected` means the ADR was archived and did not proceed
- historical records remain available as trace
- rejected records remain available as archived negative trace

### Traceability rule

The promotion mechanics must make the successor obvious from the file structure and links alone. The `links` section is the primary machine-readable trail; prose may restate the relationship, but it should not be the only place the relationship exists.

## Consequences

- there is a single active review surface after draft promotion
- there is a distinct production state after implementation-plan completion
- spikes have one packaging rule instead of local invention
- the repository can move toward human-facing Markdown renders of JSON without losing the lifecycle trail
- the dev location is explicit while bootstrapping, even if the final ADR naming hierarchy is still stabilizing

## architecture_spec

The promotion mechanics define:

- spike packaging in `reporoot/spike/<spike-id>/`
- draft-to-proposed promotion
- proposed-to-active promotion
- historical supersession
- rejection as terminal non-progression
- bidirectional trace links between draft, proposed, active, and superseded records when applicable

Stated negatively:
- do not promote by silently rewriting the draft in place
- do not collapse proposed and active into one state
- do not lose the historical draft when promoting
- do not require prose-only explanation for the promotion trail

## acceptance_criteria

- a reviewer can identify the active proposed ADR from the draft
- a reviewer can tell when an ADR has become active in production
- the archive path or historical marker preserves superseded records
- the promotion trail is visible in structured links
- spikes are consistently recognized as draft ADR + `ADR_implementation_plan`

## implementation_brief

If accepted, update lifecycle guidance so promotion uses the spike package rule, the proposed-to-active distinction, and the historical/rejected outcomes.

### Verification method

Promote a sample draft ADR, move it to proposed, complete the implementation plan, and confirm the ADR becomes active without losing the historical trail.

## resolved_open_questions

- Should `reporoot/spike` be the only allowed spike location? Yes, with a nested directory per spike.
- Should monkey-patched alignment be documented in the implementation plan or only in the proposal?
- Should active ADRs retain the proposed file path or move to a separate active surface?
- Should rejected ADRs stay in place or move to an archive path? Rejected ADRs are archived.
- Should active ADR filenames move to `ADR.YYYYMMDDHHMMSS[a-z]` once naming stabilizes?

## non_goals

- Redefining the full ADR lifecycle
- Changing the canonical ADR JSON schema
- Eliminating historical draft records
- Mandating a specific archive directory layout

## validation_expectations

- the active review surface is obvious after draft promotion
- the production record is obvious after implementation-plan completion
- the historical record is preserved
- the promotion rule stays compact enough to reuse across ADRs

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Promotion mechanics slice of the ADR lifecycle.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
