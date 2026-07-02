# AAR 20260702.174927: Spike Taxonomy and Draft ADR Alignment

## Scope

ATHENA session in `projectkoios-bootstrap` updating spike/ADR language without changing `AGENTS.md`.

## What happened

- Aligned spike policy text to the rule that a spike is a draft ADR plus an implementation attachment
- Updated the spike entry-conditions ADR to remove the idea of spikes as a separate artifact class
- Updated the brainstorm/incubator ADR to route topics into draft ADRs or out-of-scope rejection
- Updated the reusable incubator template to match the same promotion rule

## Process issues

- Initial spike wording was still carrying a separate artifact-class mental model
- The repo needed the policy expressed in ADR/template surfaces rather than in `AGENTS.md`

## Proposed follow-up improvements

- Mirror the same spike wording into any remaining spike guidance surfaces if they diverge
- Check for older docs that still describe spikes as standalone artifacts

## Candidate ADR or implementation topics

- Standardize the spike package wording across docs/templates
- Review any remaining spike guidance pages for taxonomy drift

## Current status

Policy text updated in-place. Working tree now includes ADR/template edits plus this AAR.
