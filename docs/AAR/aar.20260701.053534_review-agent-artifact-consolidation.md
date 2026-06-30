# AAR 20260701.053534: Review agent artifact consolidation

## Scope

Consolidated the dirty-tree human-in-the-loop review-agent documentation
artifacts before committing them.

## What happened

Codex reviewed the untracked ADR, policy, and AAR files, then made three
targeted documentation edits:

- Marked the older review-agent ADR proposal as superseded by the refined
  review-agent contract ADR.
- Clarified that `docs/policies/architecture-baseline.md` is an empty
  evidence-backed template, not a current observed architecture claim.
- Added an explicit guard that Codex must not invoke the opencode harness
  directly and that any opencode/Vulcan surface requires Hermes routing.

## Process issues

The dirty tree had useful artifacts but overlapping Draft authority. The older
ADR proposal and newer refined ADR could both appear active without an explicit
supersession marker.

The architecture baseline file mixed template shape with observed-state
language, which risked treating placeholders as durable architecture evidence.

## Proposed follow-up improvements

When a generated ADR supersedes a source proposal, update the source proposal's
status in the same session so later harnesses do not treat both as active
Drafts.

Keep empty baseline templates clearly labeled until populated with
evidence-backed observations.

## Candidate ADR or implementation topics

- Decide whether the review-agent contract should remain document-only or move
  to a Hermes-routed implementation surface.
- Decide whether policy templates in `docs/policies/` need synchronization rules
  with sibling repositories.

## Current status

The review-agent artifact set is consolidated and ready for validation and
commit.
