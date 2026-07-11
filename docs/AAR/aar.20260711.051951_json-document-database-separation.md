# AAR 20260711.051951: JSON document database separation

## Scope

VULCAN implementation of the approved JSON document database separation slice for the one-ADR pilot.

## What happened

- ATHENA provided a bounded brief and approved VULCAN's paused plan.
- User clarified that enumerated semantic values must be scoped enums/types and that dangling semantic constants are not acceptable.
- VULCAN implemented a generic document-store substrate and ADR wrapper, regenerated pilot evidence, and validated the slice.

## Process issues

- The first planning pass used `DocumentKind` and free string examples; user corrected the desired naming and enum policy before coding.
- The coding policy did not previously state the enum and dangling-constant preference explicitly.

## Proposed follow-up improvements

- Continue enforcing enum/type-owned semantic values in future Python slices.
- Prefer approving enum/type names in implementation plans before coding when names are user-visible or policy-significant.
- Consider adding automated checks later if dangling semantic constants recur.

## Candidate ADR or implementation topics

- Decide whether generic document-store enum/type naming should be standardized across future control-surface packages.
- Decide whether replacement evidence schemas should be formalized if more pilot migrations follow.

## Current status

Implemented and validated. Awaiting ATHENA/user/Hermes review.
