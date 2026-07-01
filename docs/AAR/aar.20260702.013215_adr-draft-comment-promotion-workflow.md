# AAR 20260702.013215: ADR Draft Comment Promotion Workflow

## Scope

Added a draft ADR and template updates to define comment handling for ADR drafts and promotion into proposed/accepted states.

## What happened

Created `docs/architecture/adr/adr.draft-comment-and-promotion-workflow.draft.md`, added a `Comments` section to `docs/templates/ADR.proposal.template.md`, and updated lifecycle guidance to distinguish draft, proposed, and accepted ADR states.

## Process issues

`graphify update .` rebuilt the graph but skipped `graph.html` because the node count exceeded the HTML visualization limit.

## Proposed follow-up improvements

Consider whether the proposed/accepted/archive transitions should also be spelled out in a small workflow note or promotion checklist.

## Candidate ADR or implementation topics

- ADR promotion checklist
- Comment retention rules for draft vs proposed ADRs
- Archive behavior for superseded draft ADRs

## Current status

Draft ADR and template updates are in place; graphify refreshed.
