# AAR 20260702.004512: ADR Template Conformance

## Scope
Hermes normalized the live ADRs under `docs/architecture/adr/` to better match the canonical Markdown ADR template.

## What happened
Updated both live ADRs to use the template-style section names, added explicit provenance domain metadata in `Context`, and added a `links` section so the Markdown render better matches the canonical ADR schema shape.

## Process issues
The first pass briefly introduced an incorrect routing value on the draft workflow ADR; that was corrected immediately.

## Proposed follow-up improvements
Consider syncing the proposal template and the architecture schema note more explicitly around `architecture_domain` and `links` so future ADRs have one obvious render shape.

## Candidate ADR or implementation topics
- Template/schema alignment for ADR Markdown renders
- Whether archived ADRs should be normalized too

## Current status
Live ADRs in `docs/architecture/adr/` are now closer to the canonical template structure.
