# AAR 20260701.033848: Session Start Graphify Schema Warning

## Scope

Session-start state check for `projectkoios-bootstrap`.

## What happened

Codex used Graphify first, then git, ADR, and Archon run state. Graphify printed
a pre-`#1504` node-ID scheme warning during query execution.

Codex initially weighted that warning too strongly in the session summary. The
user clarified that the graph appears to be using the current practical query
surface and is returning good results.

## Process issues

Graphify compatibility warnings should be reported as warnings, not treated as
evidence that the graph is stale or low-quality without additional validation.

## Proposed follow-up improvements

When Graphify emits a schema or compatibility warning, distinguish three states:

- query quality appears good
- graph output has a compatibility warning
- a rebuild is required because source verification or query behavior shows a
  concrete problem

## Candidate ADR or implementation topics

None.

## Current status

No architecture or implementation issue was found. The graph warning remains a
low-priority maintenance signal, not a blocker.
