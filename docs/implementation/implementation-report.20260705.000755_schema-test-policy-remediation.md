# Implementation report 20260705.000755: Schema test policy remediation

## Status

Implementation complete for the first bounded test-code Python policy remediation slice.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Workspace: `workspaces/vulcan/`
- Branch: `master`
- Source request: user directed VULCAN to continue after Python policy validator CLI integration
- Source follow-up: `docs/implementation/implementation-report.20260704.235829_python-policy-validator-cli.md`
- Source policies: `docs/policies/python-coding.md`, `docs/policies/python-testing.md`
- Remediation target: `tests/projectkoios/bootstrap/schema/`
- Next expected artifact: review, commit packaging, or next bounded test-code remediation slice

## Summary

Remediated schema package tests against the Python policy validator.

Changed files:

- `tests/projectkoios/bootstrap/schema/test__SchemaRegistry__validate.py`
  - Added generated-docs-compatible docstrings and return annotations to public fixtures/tests.
  - Added explicit local annotations and nearby purpose comments.
  - Added precise types for local registry lookup assertions.
- `tests/projectkoios/bootstrap/schema/test__DraftAdrRecord__markdown.py`
  - Added generated-docs-compatible docstrings and return annotations to tests.
  - Added explicit local annotations and nearby purpose comments.
  - Replaced direct assignment to frozen dataclass property in an immutability assertion with `setattr` so mypy accepts the intentional runtime failure check.

## Validation evidence

Commands run from `/Users/eugene/repos/projectkoios-bootstrap`:

- `uv run projectkoios bootstrap validate-python-policy tests/projectkoios/bootstrap/schema` => `summary: 0 finding(s), 2 file(s)`
- `uv run mypy tests/projectkoios/bootstrap/schema` => `Success: no issues found in 2 source files`
- `uv run pytest tests/projectkoios/bootstrap/schema -q` => `19 passed in 0.13s`
- `uv run mypy src/python tests/projectkoios/bootstrap/schema` => `Success: no issues found in 65 source files`
- `uv run pytest -q` => `213 passed in 1.02s`
- `uv run projectkoios bootstrap validate-python-policy --all` summary after this slice => `753 finding(s), 107 file(s)`

## Deviations and deferred work

- This slice remediated only schema tests.
- Remaining test-code policy findings are outside `tests/projectkoios/bootstrap/schema/` and should continue by bounded test package or file group.
- No architecture authority or product-domain decision is created by this remediation.

## Current status

Schema tests now pass the Python policy validator with zero findings, mypy, and full pytest regression. Test-code policy remediation remains incomplete outside the schema test package.
