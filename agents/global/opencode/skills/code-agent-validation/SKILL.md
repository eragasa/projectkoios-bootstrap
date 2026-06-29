---
name: code-agent-validation
description: Run the validation suite and report results against acceptance criteria
metadata:
  agent: code-agent
  harness_role: producer
  consumes:
    - patch
    - acceptance-criteria
  produces:
    - test-results
---

## When to use this skill

After producing a patch, when validation must be run against acceptance criteria before knowledge capture or completion gating.

## Agent responsibility

The code agent (opencode/Vulcan) runs the validation gates and reports results truthfully. Do not skip failing tests. Do not suppress diagnostic output.

## Inputs

- `patch` — the repository modification
- `acceptance-criteria` — the criteria to validate against

## Procedure

1. Run the project's test suite.
2. Run lint checks.
3. Run type checking.
4. Cross-reference each result against acceptance criteria.
5. Report pass/fail for each criterion with diagnostic output.
6. If validation fails, diagnose and report root cause.

## Output artifact

- `test-results` — pass/fail per acceptance criterion with diagnostic output

## Failure modes

- Validation infrastructure is missing or broken — mark as unresolved, do not fabricate results
- Tests fail but spec is satisfied — report deviation, do not silently pass

## Escalation rule

If validation infrastructure is missing or broken and cannot be fixed in scope, escalate to meta-harness (pi).
