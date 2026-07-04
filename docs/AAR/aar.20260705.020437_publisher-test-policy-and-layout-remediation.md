# AAR 20260705.020437: Publisher test policy and layout remediation

## Scope

VULCAN bounded remediation of the daemon publisher tests against `docs/policies/python-coding.md`, `docs/policies/python-testing.md`, and the user request to fix the test location and filename.

## What happened

- Moved `tests/harness/daemon/__Publisher__publish_run__tests.py` to `tests/projectkoios/bootstrap/harness/daemon/test__Publisher__publish_run.py`.
- Remediated the moved file with generated-docs-compatible docstrings, local annotations, purpose comments, typed monkeypatch parameters, and typed JSON payload access.
- Validated the focused file with policy validation, mypy, focused pytest, full pytest, and refreshed Graphify.

## Process issues

- The current suite still contains multiple daemon test files in the legacy `tests/harness/daemon/` tree, so fixing one file's location creates a mixed layout until the remaining daemon tests are remediated.
- JSON payload assertions need explicit casts to satisfy mypy while preserving readable tests.

## Proposed follow-up improvements

- Continue daemon test remediation by moving each touched daemon test under `tests/projectkoios/bootstrap/harness/daemon/` when its policy slice is active.
- Consider a short implementation plan for consolidating legacy `tests/harness/` layout into package-mirroring `tests/projectkoios/bootstrap/harness/` groups.

## Candidate ADR or implementation topics

- No ADR is created by this AAR. Possible implementation topic: complete package-mirroring test layout migration for `tests/harness/`.

## Current status

The remediation slice is complete and recorded in `docs/implementation/implementation-report.20260705.020437_publisher-test-policy-and-layout-remediation.md`. Whole-repo policy validation remains incomplete at `376 finding(s), 107 file(s)`.
