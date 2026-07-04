# ADR 20260702.030200: Implementation Plan Ownership

## Status

draft

## Context

Origin: role boundary gap
From: VULCAN
Acting-As: VULCAN
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

Implementation plans currently have no home. They are improvised during Vulcan sessions or crammed into ADR `implementation-brief` sections that belong to Athena. This creates three problems:

1. No role owns the transition from architecture decision to file-level implementation plan
2. No storage surface exists for plans, so they are lost between sessions
3. No escalation path exists when an ADR brief is too vague to plan against

Coding standards per language are also unowned. Vulcan determines them implicitly during implementation, but Koios (code reviewer) and Athena (ADR validator) have no documented surface to reference those standards.

## Decision

Vulcan owns implementation plans. Plans are stored at `docs/plans/` and derive from an accepted ADR or implementation brief.

Each plan must include:

- **Source** — which ADR, brief, or request the plan derives from
- **Scope** — bounded implementation boundary
- **Verification method** — how Vulcan validates completion (per ADR 20260702.030000)
- **Task breakdown** — file-level changes in dependency order
- **Escalation note** — what would block this plan (optional, filled when vague)

When an ADR brief is too vague to plan against, concerns should be framed in the form of a question in open questions.

**Coding standards flow:**

- Vulcan determines per-language coding standards from ADR intent, language conventions, and existing codebase patterns
- Koios reviews code against those standards
- Athena validates implementation against the ADR

## Consequences

- Implementation plans have an explicit owner and storage location
- Plans persist across sessions and are visible to all agents
- Coding standards per language are determined deliberately, not improvised
- Vague ADR briefs get escalated instead of silently worked around
- Koios and Athena have a documented standard to review and validate against

## architecture-spec

**Plan storage:** `docs/plans/<scope>-<topic>.md`

Example: `docs/plans/vulcan-graphify-skill-registration.md`

**Escalation protocol:**

1. ADR brief or request arrives too vague to plan against
4. Revised ADR arrives → Vulcan builds the plan → implements

**Coding standards authority order:**

1. ADR architecture intent (Athena)
2. Language ecosystem conventions (community standard)
3. Existing codebase patterns (project consistency)

## acceptance-criteria

- Every implementation derives from a plan at `docs/plans/`
- Plans are visible to Hermes, Athena, and Koios
- A vague ADR brief produces a handoff, not silent improvisation
- Coding standards per language are documented and reviewable by Koios
- Athena can validate implementation against the originating ADR

## implementation-brief

If accepted, create the `docs/plans/` directory and add a brief usage note in the workspace guidance. Existing ADR briefs may be planned retroactively; new ones require a plan before implementation starts.

## resolved-open-questions

- Should plans have an explicit approval step before implementation? Not yet — YAGNI. If plan rejection becomes common, add it later.
- Should plans expire? Not yet — YAGNI. Plans are snapshots tied to their source ADR.

## non-goals

- Replacing ADRs or the architecture surface
- Defining every possible plan field
- Creating plan validation tooling
- Mandating plan review before implementation

## validation-expectations

- A new ADR brief produces a plan at `docs/plans/` before any code changes
- An overly vague brief produces a handoff instead of an improvised plan
- Koios can name the coding standards for a given language from the plan
- Athena can find the plan that derives from a given ADR

## routing

- Owner: Vulcan
- Next phase: proposed
- Notes: Implementation surface — defines plan ownership, storage, coding standards flow, and escalation protocol.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- VULCAN: Proposed from the observed gap — plans were improvised, coding standards unowned, no escalation existed. YAGNI scope keeps it to the concrete problems.
