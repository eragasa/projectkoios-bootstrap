# AAR 20260705.173808: Petri-net follow-ups

## Scope

VULCAN follow-up work after ATHENA accepted the Petri-net separation ADR remediation with follow-ups.

## What happened

- Implemented direct `PetriNetFiringRequest` adoption in `PetriNetExecutor.fire()`.
- Updated the workflow executor test to use the request object.
- Added explicit current-control notes to the older workflow executor draft ADR and implementation plan, linking them to the accepted Petri-net separation ADR.
- Validated targeted workflow tests, full repository tests, mypy, and Python policy checks.

## Process issues

- Initial validation commands were run from `workspaces/vulcan/`, which caused path/module discovery failures. Re-running from the repository root produced valid results.
- The older workflow ADR/plan contained broad draft vocabulary that could remain misleading without an explicit control note.

## Proposed follow-up improvements

- Prefer repository-root command wrappers or shell aliases for recurring validation commands to avoid workspace-relative path mistakes.
- Keep reconciliation notes explicit when older draft/control surfaces are preserved as provenance but narrowed by later accepted ADRs.

## Candidate ADR or implementation topics

- If deterministic event timestamps become important, define an accepted clock-injection or event timestamp policy before changing runtime semantics.
- Broader workflow adapter, restart, persistence, and product-domain surfaces still need separate architecture authority before expansion.

## Current status

The bounded follow-ups are implemented and validated. Packaging should still avoid unrelated dirty ATHENA/KOIOS/root files unless explicitly directed.
