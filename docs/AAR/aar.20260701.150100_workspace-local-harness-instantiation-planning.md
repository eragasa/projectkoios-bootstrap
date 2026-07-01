# AAR 20260701.150100: Workspace-local harness instantiation planning

## Scope

Planned the next stage for moving harness instantiation into per-agent workspaces.

## What happened

Reviewed existing bootstrap ADRs and archived handoffs around global/local asset splitting, runtime-vs-role separation, and AST-only session rebuilds. Drafted a new ADR to define workspace-local harness instantiation as the next planning boundary.

## Process issues

None observed beyond the usual ambiguity between runtime names and role names, which remains an open planning question.

## Proposed follow-up improvements

Clarify naming and ownership boundaries before implementation begins.

## Candidate ADR or implementation topics

- Workspace root naming model
- Workspace-local state inventory
- Bootstrap template/materialization boundary
- Migration order and compatibility window

## Current status

Planning complete for this stage; implementation should wait on a follow-up brief.
