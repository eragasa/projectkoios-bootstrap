# AAR 20260703.010000: GraphRAG docs relocation

## Scope
Project Koios bootstrap repo, relocation of durable GraphRAG notes from `workspaces/athena/` into `docs/archive/incubator/graphrag/`.

## What happened
Stable GraphRAG planning notes, schema drafts, and the consolidated implementation brief were moved out of the Athena workspace and into a docs archive namespace so the durable project record lives under `docs/`.

## Process issues
- The Athena workspace had accumulated durable notes that were no longer just transient session state.
- The repository needed a clearer distinction between workspace-local scratch and repo-local durable project artifacts.

## Proposed follow-up improvements
- Keep durable planning artifacts in `docs/` from the start.
- Use workspace inbox/outbox only for temporary session coordination.
- Prefer archival namespaces for superseded drafts and iterative planning notes.

## Candidate ADR or implementation topics
- workspace-to-docs promotion rule
- durable artifact placement policy
- archive namespace conventions for iterative spec drafts

## Current status
Relocation complete. No authority change implied.
