# AAR 20260704.000100: Document-state orchestration correction

## Scope

Follow-up correction to the mailbox/control-surface cleanup in `projectkoios-bootstrap`.

## What happened

The user clarified that Project Koios should be modeled as agents initialized from repository document state, running bounded transformations, and writing back modified document state. Separation of concerns means document-domain ownership, not message delivery or routing. Hermes should orchestrate by resolving inconsistencies between document domains rather than acting as a communication layer.

I updated the active control surfaces to use document-state orchestration language:

- repository documents and statuses are the durable workflow state
- agents own document domains
- Hermes owns cross-domain inconsistency resolution
- transport, routing, and mailbox mechanics are not authoritative workflow concepts

## Process issues

- The previous cleanup replaced mailbox language with role-routing language, which was still too transport/control-flow oriented.
- Several legacy ADRs and schema fields still use `routing`; those active surfaces were not broadly rewritten in this pass.
- Some compatibility code and legacy guard names still refer to routing/inbox concepts; these should be treated as compatibility identifiers until a deliberate migration is approved.

## Proposed follow-up improvements

- Create a focused ADR or architecture document for document-state orchestration if Zeus wants the model made durable.
- Decide whether legacy `routing` fields in ADR templates/schemas should be renamed to `document-state` or retained for compatibility.
- Decide whether handoff directories should remain as transitional provenance folders or be replaced by document-domain status indexes.

## Candidate ADR or implementation topics

- Document-state orchestration model.
- Hermes as cross-domain inconsistency resolver.
- Migration policy for legacy routing/handoff/inbox terminology.

## Current status

Active guidance and workspace bootstrap code now emphasize document-state orchestration. Targeted tests pass. Graphify update succeeded with `--force` after the first update refused to overwrite a smaller graph.
