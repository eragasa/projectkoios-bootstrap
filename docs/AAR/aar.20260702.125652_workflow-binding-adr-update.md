# AAR 20260702.125652Z: Workflow-binding ADR update

## Scope

Project Koios bootstrap ADR workflow vocabulary, binding note, template contract, lifecycle policy, and schema alignment.

## What happened

New `adr.workflow.draft.md` and `adr.adr-workflow.draft.md` notes were drafted to define the workflow ontology and ADR binding layer. Template, policy, lifecycle, and schema surfaces were updated to reflect optional workflow binding and explicit gate links.

## Process issues

- The first lifecycle ADR edit missed exact text matching and had to be retried.
- The template contract initially described the new binding surface as documentation-only; schema alignment was needed to keep the contract consistent.

## Proposed follow-up improvements

- Keep template, policy, and schema edits grouped when introducing new optional ADR fields.
- When adding a new control surface, update the source-of-truth ADR, the template contract, and the schema together.

## Candidate ADR or implementation topics

- Promote the workflow binding object from optional schema support into downstream rendering/tooling.
- Decide whether workflow-bound ADRs should eventually require explicit gate links when a gate is declared.

## Current status

The workflow ontology and ADR binding notes are drafted; template, policy, and schema surfaces now acknowledge optional workflow binding.
