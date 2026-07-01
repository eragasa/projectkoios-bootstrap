# AAR 20260701.143555: Policy baseline changes

## Scope

Updated the policy and review baselines to reflect the user's control-surface model.

## What happened

Applied the requested baseline changes: `architecture-baseline.md` now includes policy, Markdown/control, and review mechanics as observed surface areas, plus the policy target-assumption note. `review-baseline.md` now includes cross-surface coherence and improvement/debt discovery, debt triage, and the data-object/action-object separation. Added a new `docs/policies/policy-baseline.md` for vision-surface policy intent. `code-baseline.md` gained explicit data-object/action-object and dangling-function guidance.

## Process issues

The review-baseline update initially accumulated duplicate sections; it was rewritten cleanly.

## Proposed follow-up improvements

- Consider adding a dedicated review-matrix template if the review baseline grows further.
- Consider a policy-surface matrix if policy examples become more detailed.

## Candidate ADR or implementation topics

- Policy-baseline lifecycle and ownership.
- Review-matrix template.

## Current status

Policy and review baselines now reflect the user's control-surface framing.
