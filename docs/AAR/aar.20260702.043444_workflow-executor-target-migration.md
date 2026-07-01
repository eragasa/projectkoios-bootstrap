# AAR 20260702.043444: Workflow executor target and migration framing

## Scope
Project Koios bootstrap repo, Petri-net workflow executor ADR and implementation plan.

## What happened
The workflow executor ADR and implementation plan were updated to target `src/python/projectkoios/workflow` in `projectkoios-bootstrap` and to treat the existing read-only handoff/evaluator code under `src/python/projectkoios/bootstrap/harness/` as migration or compatibility-shim material under the new architecture.

## Process issues
None.

## Proposed follow-up improvements
Use the migration-first framing to preserve current behavior while the new workflow substrate is introduced.

## Candidate ADR or implementation topics
- Workflow executor migration detail for current harness code
- Compatibility shim design
- Persistence/restart sub-ADR if needed

## Current status
Target and migration path updated.
