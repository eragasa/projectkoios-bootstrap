# AAR 20260704.205637: Schema package policy remediation

## Scope

VULCAN remediated `src/python/projectkoios/bootstrap/schemas/` against the new Python policy validator rules.

## What happened

- Ran the new validator against the existing source tree and found 810 source findings, with 116 in the schema package.
- Chose the schema package as the first bounded remediation slice because it is newly added and reviewable.
- Added generated-docs-compatible docstrings, explicit local variable annotations, nearby purpose comments, and package-level JSON aliases to avoid local `Any` annotations.
- Added `types-jsonschema` as a development dependency so mypy can validate the package.
- Wrote `docs/implementation/implementation-report.20260704.205637_schema-package-policy-remediation.md`.

## Process issues

- Whole-repo remediation is too large for a single safe patch; the validator reported 1633 findings across all Python files before this slice.
- The local-variable comment rule creates substantial review noise if applied mechanically across older code.
- Mypy needed a stub package for `jsonschema`, which was not apparent until the schema package was type-checked directly.

## Proposed follow-up improvements

- Continue remediation package-by-package rather than by broad automatic rewrite.
- Consider whether tests need the same strict local-comment/docstring policy or a separate test profile.
- Add CLI integration for the validator before using it as a routine closeout gate.
- Track remaining baseline counts after each remediation slice.

## Candidate ADR or implementation topics

- Python policy exception/profile model for test code and legacy code.
- Package-by-package remediation plan for `src/python`.
- Validator CLI and baseline report command.

## Current status

`src/python/projectkoios/bootstrap/schemas/` now has zero Python policy validator findings. The remaining `src/python` baseline is 694 findings.
