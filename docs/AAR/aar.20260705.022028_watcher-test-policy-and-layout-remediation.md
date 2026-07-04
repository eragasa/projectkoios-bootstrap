# AAR 20260705.022028: Watcher test policy and layout remediation

## Scope

VULCAN bounded remediation of the daemon watcher tests against `docs/policies/python-coding.md`, `docs/policies/python-testing.md`, and the ongoing direction to fix touched test location and filename.

## What happened

- Moved `tests/harness/daemon/__Watcher__scan_mtimes__tests.py` to `tests/projectkoios/bootstrap/harness/daemon/test__Watcher__scan_mtimes.py`.
- Remediated the moved file with generated-docs-compatible docstrings, local annotations, purpose comments, and typed async watcher state.
- Validated the focused file with policy validation, mypy, focused pytest, full pytest, and refreshed Graphify.

## Process issues

- The daemon test layout is improving incrementally, but untouched legacy daemon tests remain until their slices are completed.

## Proposed follow-up improvements

- Continue daemon test remediation by moving each touched daemon test under `tests/projectkoios/bootstrap/harness/daemon/`.

## Candidate ADR or implementation topics

- No ADR is created by this AAR. Possible implementation topic: complete package-mirroring test layout migration for `tests/harness/daemon/`.

## Current status

The remediation slice is complete and recorded in `docs/implementation/implementation-report.20260705.022028_watcher-test-policy-and-layout-remediation.md`. Whole-repo policy validation remains incomplete at `264 finding(s), 107 file(s)`.
