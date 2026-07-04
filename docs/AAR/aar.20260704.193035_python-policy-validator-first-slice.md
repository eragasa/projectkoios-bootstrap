# AAR 20260704.193035: Python policy validator first slice

## Scope

VULCAN implemented the easy first slice of a Python policy validator from `docs/plans/implementation-plan.20260704.192620_python-policy-validator.md`.

## What happened

- Added AST rules for missing return annotations, unannotated local variable introductions, local variable annotations using `Any`, local variables missing purpose comments, missing public docstrings, and exception handlers returning generic sentinel values.
- Added target selection helpers for explicit, changed, and all Python file modes.
- Added a small mypy runner but did not wire it into CLI or combined validation yet.
- Added focused tests and wrote `docs/implementation/implementation-report.20260704.193035_python-policy-validator.md`.

## Process issues

- The new local-variable annotation policy is stricter than common Python style, so whole-repo enforcement would likely be noisy.
- Python syntax does not allow inline annotations for loop targets, `with/as` aliases, or exception aliases, so the validator requires a prior annotation for those names.
- The local-variable comment rule needs practical exemptions for simple predeclared loop variables; the validator currently skips comment findings for annotation-only declarations.
- The first implementation should stay path-targeted until legacy exceptions/remediation are defined.

## Proposed follow-up improvements

- Add CLI integration for `projectkoios bootstrap validate-python-policy`.
- Wire mypy results into `PythonPolicyValidator` and CLI output.
- Add changed-file target tests with a fake git adapter or isolated repository fixture.
- Decide whether parameter annotations and `typing.Any` imports should become enforced rules.

## Candidate ADR or implementation topics

- Python policy exception model for legacy files.
- CLI validation command for implementation closeout.
- Optional stricter mypy/ruff configuration once the validator is stable.

## Current status

The easy first slice is implemented and validated. No whole-repo enforcement or CLI integration has been added yet.
