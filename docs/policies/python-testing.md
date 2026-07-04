```json
{
  "title": "Python testing rules",
  "artifact_type": "implementation-policy",
  "status": "draft",
  "datetime": "20260704.175900",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "Python tests and validation in projectkoios-bootstrap",
  "owner": "VULCAN",
  "review_roles": ["KOIOS", "ATHENA"],
  "controls": ["tests/", "src/python/", "pyproject.toml"],
  "does_not_control": ["architecture decisions", "product domain policy", "non-Python implementation"]
}
```

# Python testing rules

## Status

Draft implementation policy.

## Purpose

This document defines testing and validation rules for Vulcan-owned Python work in `projectkoios-bootstrap`.

The key words `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative.

## Scope

These rules apply to Python tests and validation for code under:

- `src/python/`
- `tests/`

These rules complement `docs/policies/python-coding.md`. When a Python implementation slice changes runtime behavior, the implementation report MUST identify the relevant test command output.

## Test ownership

- New Python behavior MUST include focused tests in the same implementation slice.
- Tests MUST be owned by VULCAN as implementation/validation artifacts.
- Tests MUST validate behavior from the controlling source artifact, brief, ADR, or accepted work item.
- Tests MUST NOT create new architecture authority by encoding behavior not present in the controlling artifact unless the deviation is explicitly reported.

## Test structure

- Test files SHOULD live under `tests/projectkoios/` mirroring the package or feature surface under test.
- Test names SHOULD follow the repository convention and describe the behavior under test.
- Test fixtures SHOULD be minimal and explicit.
- Tests SHOULD prefer direct object/service testing before CLI testing unless CLI behavior is the target.
- Tests SHOULD isolate one behavior per assertion group when practical.

## Determinism and isolation

- Tests MUST avoid external network, model-provider, or machine-local credential dependencies unless explicitly marked and isolated.
- Tests MUST NOT depend on hidden chat state, intercom state, local untracked files, or developer-specific paths.
- Tests SHOULD use temporary directories for generated files.
- Tests SHOULD use fake adapters or fixtures for backend behavior.
- Tests for deterministic artifacts MUST compare stable serialized output or stable parsed structures.
- Tests MUST clean up temporary state or keep it inside pytest-managed temporary directories.

## Validation commands

- Every implementation report MUST list the exact validation commands run and their outcomes.
- Focused tests for the changed surface MUST run before closeout.
- Broader regression tests SHOULD run when the change touches shared code, config, package dependencies, schemas, validation behavior, CLI behavior, or persistence behavior.
- Static type checking MUST be part of validation when the changed surface adds or changes typed Python code.
- Static type checking MUST verify function and method return values against declared return types.
- If static type checking is not run, the implementation report MUST record the reason and the residual risk.

## Negative and regression tests

- Validation, parsing, schema, path, serialization, and CLI changes MUST include negative tests for expected failure modes.
- Bug fixes SHOULD include regression tests that fail before the fix and pass after it.
- Tests for strict validation MUST prove both accepted valid input and rejected invalid input.
- Tests for compatibility behavior MUST prove canonical and non-canonical paths or modes are distinguished.

## Assertions and error evidence

- Tests SHOULD assert observable behavior rather than private implementation details.
- Error-path tests SHOULD assert the exception type and enough message/context to prove the intended failure occurred.
- Tests SHOULD avoid broad `Exception` assertions unless the implementation surface intentionally delegates exact exception type to a third-party validator.
- Snapshot-style assertions MUST be deterministic and small enough for review.

## Dependency and fixture control

- New test dependencies MUST be justified in the implementation report or controlling brief.
- Test-only dependencies SHOULD be added to the development dependency group.
- Runtime dependencies introduced only to satisfy tests MUST NOT be added unless the runtime code also requires them.
- Shared fixtures SHOULD remain simple; complex fixture builders SHOULD be treated as test support code and reviewed for correctness.

## Closeout expectations

- Implementation reports MUST include focused test output.
- Implementation reports SHOULD include broader regression output when feasible.
- Known skipped, xfailed, or unrun tests MUST be documented with reason and residual risk when relevant to the changed surface.
- Validation failures outside the changed surface SHOULD be reported separately and MUST NOT be hidden.

## Non-goals

This document does not define:

- architecture acceptance criteria;
- product-domain validation policy;
- non-Python test policy;
- release certification policy;
- benchmark or performance-test requirements unless a controlling artifact asks for them.

## Promotion path

This draft MAY be promoted after it is exercised across multiple Vulcan implementation slices.

Repeated validation gaps SHOULD be used to revise this policy before promotion.
