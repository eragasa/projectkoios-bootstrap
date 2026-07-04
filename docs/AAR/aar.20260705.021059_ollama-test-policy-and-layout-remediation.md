# AAR 20260705.021059: Ollama test policy and layout remediation

## Scope

VULCAN bounded remediation of the daemon Ollama tests against `docs/policies/python-coding.md`, `docs/policies/python-testing.md`, and the ongoing user direction to fix touched test location and filename.

## What happened

- Moved `tests/harness/daemon/__Ollama__generate_cards__tests.py` to `tests/projectkoios/bootstrap/harness/daemon/test__Ollama__generate_cards.py`.
- Remediated the moved file with generated-docs-compatible docstrings, local annotations, purpose comments, typed captured-output fixtures, and typed mocks.
- Validated the focused file with policy validation, mypy, focused pytest, full pytest, and refreshed Graphify.

## Process issues

- The daemon tests remain partially split between legacy `tests/harness/daemon/` and package-mirroring `tests/projectkoios/bootstrap/harness/daemon/` until all daemon files are remediated.
- Mock call assertions required an explicitly typed `MagicMock` fixture to satisfy both policy validation and mypy.

## Proposed follow-up improvements

- Continue daemon test remediation by moving each touched daemon test under `tests/projectkoios/bootstrap/harness/daemon/`.
- Consider consolidating repeated daemon test fixture setup once the layout migration is complete.

## Candidate ADR or implementation topics

- No ADR is created by this AAR. Possible implementation topic: complete package-mirroring test layout migration for `tests/harness/daemon/`.

## Current status

The remediation slice is complete and recorded in `docs/implementation/implementation-report.20260705.021059_ollama-test-policy-and-layout-remediation.md`. Whole-repo policy validation remains incomplete at `338 finding(s), 107 file(s)`.
