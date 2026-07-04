# AAR 20260705.021601: Daemon run-once test policy and layout remediation

## Scope

VULCAN bounded remediation of the daemon run-once tests against `docs/policies/python-coding.md`, `docs/policies/python-testing.md`, and the ongoing direction to fix touched test location and filename.

## What happened

- Moved `tests/harness/daemon/__Daemon__run_once__tests.py` to `tests/projectkoios/bootstrap/harness/daemon/test__Daemon__run_once.py`.
- Remediated the moved file with generated-docs-compatible docstrings, local annotations, purpose comments, and typed subprocess fixtures.
- Validated the focused file with policy validation, mypy, focused pytest, full pytest, and refreshed Graphify.

## Process issues

- The daemon tests remain partially split between legacy `tests/harness/daemon/` and package-mirroring `tests/projectkoios/bootstrap/harness/daemon/` until all daemon files are remediated.
- Ad hoc dynamic result objects were convenient for tests but poor for static checking; typed `subprocess.CompletedProcess[str]` fixtures resolved this cleanly.

## Proposed follow-up improvements

- Continue daemon test remediation by moving each touched daemon test under `tests/projectkoios/bootstrap/harness/daemon/`.
- Consider extracting shared typed subprocess fixtures if daemon tests accumulate repeated command-patching setup.

## Candidate ADR or implementation topics

- No ADR is created by this AAR. Possible implementation topic: complete package-mirroring test layout migration for `tests/harness/daemon/`.

## Current status

The remediation slice is complete and recorded in `docs/implementation/implementation-report.20260705.021601_daemon-run-once-test-policy-and-layout-remediation.md`. Whole-repo policy validation remains incomplete at `300 finding(s), 107 file(s)`.
