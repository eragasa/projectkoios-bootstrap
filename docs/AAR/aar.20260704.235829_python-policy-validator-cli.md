# AAR 20260704.235829: Python policy validator CLI integration

## Scope

VULCAN added a first-class bootstrap CLI command for the Python policy validator after closeout packaging identified that `python -m projectkoios.bootstrap.python_policy` was unavailable.

## What happened

- Added `projectkoios bootstrap validate-python-policy` under the existing bootstrap CLI surface.
- Added tests for passing and failing command runs.
- Revalidated policy, mypy, and pytest baselines.

## Process issues

- The earlier validator workflow depended on copy-pasted Python snippets, which made validation less discoverable and caused an attempted `python -m` invocation to fail.
- The policy validator still intentionally separates AST policy checks from mypy; the CLI name and help text should keep that distinction clear.

## Proposed follow-up improvements

- Decide whether to add a combined validation command that runs both Python policy checks and mypy.
- Decide whether tests should be included in routine policy validation or remediated under a test-specific rule profile.

## Candidate ADR or implementation topics

- Implementation topic: test-code Python policy remediation.
- Implementation topic: combined source validation command or CI hook.

## Current status

CLI integration is implemented, tested, and documented in `docs/implementation/implementation-report.20260704.235829_python-policy-validator-cli.md`.
