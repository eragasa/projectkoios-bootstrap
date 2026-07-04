# ADR 20260702.000551: Idea → Spike → ADR → Implementation Workflow

## Status

draft

## Context

Origin: user request
From: Hermes
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The current workflow tends to push exploratory work into ADRs too early. That makes the decision log volatile and mixes brainstorming, uncertainty reduction, and durable architecture decisions.

The legacy staging directories `docs/incubator/` and `docs/spikes/` are deprecated. New work must not be added there; existing material should be migrated out and those directories deleted.

## Decision

Use a four-surface workflow:

- idea notes are separate documents that point at an ADR by stable fields
- `reporoot/spike/<spike-id>/` is the only spike location, and each spike gets its own nested directory
- `reporoot/dev/<proposal-id>/` is the only dev location for ADR proposals that are not active yet, and each proposal gets its own nested directory
- implementation briefs and tasks are separate delivery work

ADRs are encapsulated decision records and must remain independently readable.
Hierarchy, readiness level, and promotion ordering are represented by `architecture.00`, not by nested ADR body structure.

The intended lifecycle is:

`idea -> spike -> draft ADR -> proposed ADR -> active ADR -> implementation brief -> iterative implementation`

## Consequences

- brainstorming becomes low-friction without dedicated incubator directories
- spikes remain bounded and file-local
- ADRs stay short and durable
- iterative implementation can proceed without repeatedly reopening architecture decisions
- legacy staging directories can be removed after migration

## architecture-spec

This ADR introduces the workflow boundary and the deprecation of the old staging directories.

The boundary is:

- ideas are exploratory
- spikes are draft-ADR-plus-implementation-plan bundles in `reporoot/spike/<spike-id>/`
- draft ADRs are comment-open working records
- proposed ADRs are the active review surface and move to dev in `reporoot/dev/<proposal-id>/`
- active ADRs are production records
- implementation briefs translate decisions into build work

Stated negatively:
- do not add new work to `docs/incubator/`
- do not add new work to `docs/spikes/`
- do not keep the legacy staging dirs alive after migration

## acceptance_criteria

- raw ideas can be captured without using `docs/incubator/`
- spike artifacts live under `reporoot/spike/<spike-id>/`
- proposed ADR work lives under `reporoot/dev/<proposal-id>/`
- ADRs are only used for durable decisions
- the legacy staging dirs are clearly deprecated and removable after migration

## implementation_brief

If accepted, migrate any remaining content out of `docs/incubator/` and `docs/spikes/`, delete those directories, and update related workflow guidance so new work uses the repo-root spike/dev surfaces and ADR-linked separate documents.

## resolved_open_questions

- Should `docs/incubator/` and `docs/spikes/` be formal directories, or just conventions? They are deprecated and should be removed after migration.
- Where do spike packages live? `reporoot/spike/<spike-id>/`.
- Where do ADR proposals live before activation? `reporoot/dev/<proposal-id>/`.

## non_goals

- Replacing ADRs as the durable decision surface
- Forcing every idea into a formal process
- Making spikes as heavyweight as ADRs
- Preserving the legacy incubator/spike directories

## validation_expectations

- Review the workflow for clarity and low friction
- Confirm the proposal reduces ADR volatility rather than adding more ceremony
- Confirm the legacy staging dirs are no longer required

## routing

- Owner: Hermes
- Next phase: proposed
- Notes: Process/workflow control surface.
