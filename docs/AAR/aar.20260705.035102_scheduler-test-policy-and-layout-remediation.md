# AAR 20260705.035102: Scheduler test policy and layout remediation

## Scope

VULCAN bounded remediation of daemon scheduler tests against Python policy and package-mirroring test layout.

## What happened

- Moved `tests/harness/daemon/__Scheduler__coalesce__tests.py` to `tests/projectkoios/bootstrap/harness/daemon/test__Scheduler__coalesce.py`.
- Remediated the moved file with docstrings, local annotations, purpose comments, and typed asyncio tasks.
- Validated with policy validation, mypy, focused pytest, full pytest, and Graphify refresh.

## Process issues

- No new process issue beyond the ongoing legacy test layout migration.

## Proposed follow-up improvements

- Continue one-file-at-a-time policy remediation and preserve package-mirroring layout for touched files.

## Candidate ADR or implementation topics

- No ADR is created by this AAR.

## Current status

The remediation slice is complete and recorded in `docs/implementation/implementation-report.20260705.035102_scheduler-test-policy-and-layout-remediation.md`.
