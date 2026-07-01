# ADR 20260630.220700: Athena draft promotion review workflow

## Status

historic

## Context

Origin: user request
From: Codex
Acting-As: delegated operator
Scope: projectkoios-bootstrap Archon workflow surface
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Project Koios needs a repeatable way to decide whether a Draft ADR should be
promoted toward implementation. Acceptance of architecture and promotion for
implementation are separate decisions: Athena owns architecture review, Hermes
owns routing and promotion decisions, and Vulcan implements only after Hermes
routes accepted work.

The immediate task was to create an Archon workflow named
`athena_review-draft-for-promotion` that lets Athena review a Draft ADR and
return a structured recommendation to Hermes without editing files, changing
ADR status, routing to Vulcan, or implementing code.

The `athena_` prefix is an ownership marker. It follows the naming shape
`athena_<action-in-this-mode>` and means only Athena runs the workflow in the
harness sense. A delegated operator may invoke the Archon CLI, but the workflow
output remains an Athena artifact.

## Decision

Create `archon/workflows/athena_review-draft-for-promotion.yaml` as a
read-only Athena review workflow.

The workflow:

- requires an ADR path as input
- is named with the Athena-owned `athena_<action-in-this-mode>` convention
- reads the target ADR
- reads repo-level harness and meta-harness context
- checks promotion-readiness criteria
- returns a structured Markdown promotion review for Hermes
- distinguishes implementation-required, no-implementation, unclear, and
  non-candidate cases
- recommends the next Hermes action

The workflow is explicitly not allowed to:

- edit files
- change ADR status
- route directly to Vulcan
- implement code
- create a PR
- run validation loops

The workflow recommendation values are:

- `ready_for_hermes_acceptance_review`
- `needs_athena_revision`
- `no_implementation_required`
- `not_an_implementation_candidate`
- `blocked`

The implementation classification values are:

- `implementation_required`
- `no_implementation_required`
- `unclear`
- `not_applicable`

## Consequences

Hermes now has an explicit Athena workflow for reviewing Draft ADRs before
promotion toward implementation. This keeps architecture review separate from
Hermes routing and Vulcan implementation.

The workflow does not itself promote, accept, reject, supersede, complete, or
implement an ADR. It produces advisory review output that Hermes can use as
input to a later routing or acceptance decision.

The naming convention also gives Hermes a routing guard: `athena_` workflows are
not generic Archon utilities. They are Athena role actions whose artifacts must
be handled as Athena-authored proposal or review material.

## acceptance-criteria

- `archon/workflows/athena_review-draft-for-promotion.yaml` exists.
- The workflow name is exactly `athena_review-draft-for-promotion`.
- The workflow follows the `athena_<action-in-this-mode>` naming convention and
  records that only Athena runs it in the harness sense.
- The workflow reads one ADR path and returns a structured promotion review.
- The workflow is read-only and does not implement code or mutate ADR state.
- The workflow includes promotion gate criteria for scope, acceptance criteria,
  implementation brief, validation expectations, non-goals, open questions,
  provenance, accepted-ADR conflicts, Vulcan suitability, and
  no-implementation validation.
- The workflow validates with Archon.

## implementation-brief

Implemented in this task. No further Vulcan implementation is required for this
ADR unless Hermes requests refinements to the workflow contract.

Changed file:

- `archon/workflows/athena_review-draft-for-promotion.yaml`

## validation-expectations

Validation for this completed ADR is:

- `archon validate workflows athena_review-draft-for-promotion`

This command completed successfully with:

- `athena_review-draft-for-promotion ok`
- `Results: 1 valid, 0 with errors`

## routing

No Vulcan routing is required for this completed ADR. Hermes may request the
Athena review by causing Athena/Archon to run:

```bash
archon workflow run athena_review-draft-for-promotion \
  "docs/architecture/adr/<draft-adr>.md"
```

If Hermes, Codex, or another delegated operator invokes that command, it is
still acting as the access layer for Athena. The resulting promotion review is
not a Hermes routing decision.

If future use shows that the promotion gate needs different outcomes, extra
context files, or machine-readable output, route a new Athena revision request.
