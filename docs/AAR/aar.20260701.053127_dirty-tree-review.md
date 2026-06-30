# AAR 20260701.053127: Dirty tree review

## Scope

Reviewed the current dirty tree containing untracked human-in-the-loop
review-agent ADRs, policy files, and AARs.

## What happened

Codex used Graphify first for broad context, then inspected git status and the
untracked ADR, policy, and AAR files directly. The review found that the dirty
tree contains useful work, especially the refined review-agent contract ADR and
local policy surface, but also needs consolidation before commit.

## Process issues

The tree contains overlapping Draft ADRs for the same review-agent contract.
The older proposal remains Draft while the newer refined ADR names it as source
material, which can confuse current artifact authority.

The policy baseline files are useful but include template placeholders that
should be made explicit before the files are treated as durable policy state.

## Proposed follow-up improvements

Consolidate the review-agent ADR set by keeping the refined ADR as the active
Draft and either superseding, archiving, or otherwise demoting the older source
proposal.

Clarify whether `docs/policies/architecture-baseline.md` is a template or an
observed baseline, and remove placeholder rows or mark them as examples.

## Candidate ADR or implementation topics

- Review-agent ADR promotion or consolidation.
- Policy baseline/template ownership between `projectkoios-bootstrap` and
  `projectkoios-workflow`.

## Current status

No consolidation edits were made in this review session. The working tree
remains dirty with useful but uncommitted artifacts.
