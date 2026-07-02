# AAR 20260702.192138: Inline Supersession Markers for Promotion Mechanics

## Scope

ATHENA session in `projectkoios-bootstrap` refining ADR lifecycle promotion wording so supersession is marked inline in affected lines and the mechanics live in the promotion-mechanics ADR.

## What happened

- Updated `adr.adr-lifecycle-promotion-mechanics.md` to define inline supersession markers in human-facing Markdown
- Updated `adr.draft-comment-and-promotion-workflow.draft.md` to annotate affected sentences and lines with `superseded_by: adr.adr-lifecycle-promotion-mechanics`
- Kept the structured links model as the machine-readable trail while making the rendered text easier to scan

## Process issues

- The lifecycle wording needed a compact line-local marker instead of a separate supersession block
- The user clarified that the marker should live at the end of each affected line rather than in a footnote or separate list

## Proposed follow-up improvements

- Fold remaining promotion-comment wording into the promotion-mechanics ADR if it becomes fully redundant
- Decide whether the inline marker should also be standardized for other lifecycle-related ADRs

## Candidate ADR or implementation topics

- Supersession marker syntax for human-facing ADR renders
- Lifecycle doc consolidation into the promotion mechanics ADR

## Current status

Promotion mechanics and draft comment workflow text updated with inline supersession markers.
