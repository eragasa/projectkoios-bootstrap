# Hermes handoff: Athena ADR-skill testing plan persistence

## Purpose
Persist the next-step question set for Athena so we do not spend chat context re-deriving the testing plan for a large ADR/skills surface.

## Context
- Repo has many ADRs and many skills.
- Broad rollout of the ADR skill boundary change needs a targeted test plan.
- KOIOS already said the boundary looks durable, but we still need a lightweight safety sweep before broader rollout.

## Request to Athena
Provide a **targeted testing plan** for the ADR skill boundary change.

### Required outputs
1. **Test surfaces first**
   - which ADR/skill/doc surfaces to test first
   - why those surfaces are highest risk

2. **Pass/fail criteria**
   - what counts as success
   - what counts as a regression

3. **Stale-reference detection at scale**
   - grep/search strategy
   - any path or naming patterns to check
   - how to avoid false positives

4. **Minimal proof of safety**
   - smallest sweep that would justify rollout
   - what evidence should be captured

### Constraints
- Keep it lightweight.
- Focus on highest-risk surfaces only.
- Avoid full-repo semantic review unless absolutely necessary.
- Prefer grepable checks and bounded sampling.

## Recommended next step
After Athena returns the plan, convert it into a short execution checklist and run only the minimum sweep needed to validate rollout safety.

## Success condition
A reviewer should be able to pick this up later and know:
- what was being tested
- why those tests matter
- what proof is enough to proceed
- what remains open
