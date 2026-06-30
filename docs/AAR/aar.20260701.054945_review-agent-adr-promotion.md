# AAR 20260701.054945: Review agent ADR promotion

## Scope

Promotion review and acceptance of the human-in-the-loop review agent contract
ADR.

## What happened

Codex used Graphify first for broad context, checked git and Archon active run
state, then ran `athena_review-draft-for-promotion` on
`docs/architecture/adr/adr.20260701.034612_human-in-the-loop-review-agent-contract.md`.

The first promotion review returned `needs_athena_revision` because the Draft
ADR left implementation classification, target surface, validation depth, and
Hermes gate unresolved. Codex revised the ADR to make it implementation-bearing
after acceptance, selected
`agents/global/goose/skills/technical-debt-report/SKILL.md` as the bounded
Goose-owned implementation surface, selected template conformance as the first
validation slice, and selected `hermes.completion_review` with the Koios
technical debt report as required input.

After the revision was pushed, a fresh Athena promotion review returned
`ready_for_hermes_acceptance_review` with no required revisions. Codex then
promoted the ADR status to `Accepted`.

## Process issues

- `athena-revise-adr` could not accept the requested path plus revision
  directive because its `fetch-adr` bash node treats all `$ARGUMENTS` as a file
  path.
- `athena_review-draft-for-promotion` runs in an isolated worktree created from
  the pushed branch state, so it did not see local committed but unpushed ADR
  changes.
- Graphify was available in the main checkout but absent in Archon review
  worktrees, so Athena review treated source files as authoritative there.

## Proposed follow-up improvements

- Fix `athena-revise-adr` argument handling so it can receive an ADR path and a
  separate revision directive.
- Document that Archon promotion reviews require pushed branch state when the
  workflow enforces worktree isolation.
- Consider ensuring Graphify output is available or intentionally ignored in
  Archon review worktrees.

## Candidate ADR or implementation topics

- Implement the accepted review-agent contract through
  `agents/global/goose/skills/technical-debt-report/SKILL.md`.
- Repair `archon/workflows/athena-revise-adr.yaml` argument parsing.

## Current status

The review-agent contract ADR is accepted. Implementation remains pending.
