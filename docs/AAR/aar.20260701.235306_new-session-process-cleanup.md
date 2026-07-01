# AAR 20260701.235306: New Session Process Cleanup

## Scope
Hermes session-start cleanup in the projectkoios-bootstrap repo.

## What happened
I tightened the session-start guidance so it is shorter and more ordered: Graphify first, then live repo state, then active orchestration state, then the highest-leverage next step.

## Process issues
The previous startup guidance had too much overlap between AGENTS and the session protocol, which made the first-pass session check feel noisier than needed. I also hit a small Archon JSON parsing snag while inspecting run state.

## Proposed follow-up improvements
Keep the startup path brief and deterministic. Prefer a single ordered checklist over repeated references to the same state.

## Candidate ADR or implementation topics
None.

## Current status
AGENTS and docs/session-protocol are aligned more closely. graphify update . was run after the docs edit.
