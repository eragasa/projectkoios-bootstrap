# AAR 20260705.111255: Workspace ADR consolidation

## Scope

Athena session consolidating workspace-state authority into a single effective workspace ADR in `projectkoios-bootstrap`.

## What happened

- User clarified that `workspace/state.md` needs a durable ADR-level purpose, not only policy wording.
- Athena drafted and accepted a consolidated workspace ADR at `docs/adr/adr.workspaces.20260705.105021Z.md`.
- The ADR defines `state.md` as the required role-local cold-start resume/control surface and `active.md` as the current priority filter.
- The ADR incorporates KOIOS provenance concerns: classify claims where useful as validated facts, working assumptions, or unresolved questions; link to durable artifacts; do not duplicate full review, implementation, or chat history.
- Prior workspace-state ADR files were archived under `docs/archive/architecture/adr/` and retained as provenance.
- Workspace policy and architecture index/control notes were updated to point at the consolidated workspace ADR.

## Process issues

- Athena first updated `docs/policies/workspace-layout.md` before placing the normative update in the effective ADR surface. The user corrected the target.
- Some historical AAR/report links had to be rewritten after archival to avoid stale paths.

## Proposed follow-up improvements

- When defining or changing workspace contracts, start with the controlling ADR and then update policy/index surfaces.
- Keep `state.md` concise and use ADR/review/report/provenance links instead of embedding historical detail.
- Consider future validation that checks `state.md` exists, includes required cold-start fields, and avoids obvious stale controlling-ADR links.

## Candidate ADR or implementation topics

- Workspace-state validator for required fields and stale-path detection.
- Bootstrap workspace initializer update if any generated workspace templates still reference superseded workspace ADRs.

## Current status

- Consolidated workspace ADR exists at `docs/adr/adr.workspaces.20260705.105021Z.md`.
- Previous workspace-state ADR and draft are archived under `docs/archive/architecture/adr/`.
- Working tree has uncommitted consolidation changes ready for packaging.
