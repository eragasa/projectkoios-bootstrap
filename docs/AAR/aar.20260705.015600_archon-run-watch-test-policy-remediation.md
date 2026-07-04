# AAR 20260705.015600: Archon run watch test policy remediation

## Scope

VULCAN bounded remediation of `tests/test__archon_run_watch_skill.py` against `docs/policies/python-coding.md` and the Python policy validator.

## What happened

- Selected `tests/test__archon_run_watch_skill.py` because it had the largest remaining per-file policy finding count: 98 findings.
- Added missing test docstrings, explicit local annotations, nearby local-variable purpose comments, and mypy import ignores for dynamically loaded helper scripts.
- Validated the focused file with policy validation, mypy, focused pytest, full pytest, and refreshed Graphify.

## Process issues

- The first validator attempt using `--format json` failed because the CLI does not support that flag. The session recovered by parsing text output.
- The policy validator surfaced purpose-comment findings after annotations were added, so remediation required a second validator pass.
- Mypy could not resolve helper modules loaded by runtime `sys.path` insertion. The implementation preserved existing runtime behavior and documented the dynamic import boundary with import-not-found ignores.

## Proposed follow-up improvements

- Consider adding a machine-readable output mode to `projectkoios bootstrap validate-python-policy` if future prioritization workflows should avoid ad hoc text parsing.
- Consider refining test-policy remediation tooling so docstring, annotation, and purpose-comment fixes can be applied in one predictable pass.
- Consider an architecture or implementation brief for packaging Archon helper scripts if dynamic `sys.path` imports become a repeated validation cost.

## Candidate ADR or implementation topics

- Optional validator JSON output for policy finding prioritization.
- Dynamic helper script import strategy for testability and static checking.

## Current status

The remediation slice is complete and recorded in `docs/implementation/implementation-report.20260705.015600_archon-run-watch-test-policy-remediation.md`. Whole-repo policy validation remains incomplete at `421 finding(s), 107 file(s)`.
