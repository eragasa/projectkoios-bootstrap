# Implementation report 20260704.193035: Python policy validator first slice

## Status

Implementation complete for the easy first slice; ready for review.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Worktree: `/Users/eugene/repos/projectkoios-bootstrap-schema-record-base`
- Branch: `vulcan/schema-record-base`
- Source artifact: `docs/plans/implementation-plan.20260704.192620_python-policy-validator.md`
- Source policies: `docs/policies/python-coding.md`, `docs/policies/python-testing.md`
- Previous artifact: user request to implement the easy portion of the validator
- Next expected artifact: review or follow-up implementation brief for CLI/mypy-runner integration

## Summary

Implemented the easy core of the Python policy validator without CLI integration. A follow-up update added checks for local-variable purpose comments, generated-docs-compatible docstrings on public classes/functions/methods, and broad exception handlers that return generic sentinel values.

Changed files:

- `src/python/projectkoios/bootstrap/python_policy/__init__.py`
  - Exposes the Python policy validator API.
- `src/python/projectkoios/bootstrap/python_policy/ast_rules.py`
  - Adds AST-based findings for missing return annotations, unannotated local variable introductions, local annotations that use `Any`, annotated locals without nearby purpose comments, missing public docstrings, and exception handlers returning generic sentinel values.
- `src/python/projectkoios/bootstrap/python_policy/targets.py`
  - Adds explicit, all, and changed target selection helpers for Python files.
- `src/python/projectkoios/bootstrap/python_policy/mypy_runner.py`
  - Adds a small mypy runner that can execute `python -m mypy` against validation targets.
- `src/python/projectkoios/bootstrap/python_policy/validator.py`
  - Adds a coordinator that validates selected targets with AST rules.
- `tests/projectkoios/bootstrap/python_policy/test__PythonPolicyAstValidator__validate_source.py`
  - Covers accepted annotated locals/returns and rejected missing returns, unannotated assignments, loop targets, `with/as`, exception aliases, assignment expressions, direct/nested `Any` annotations, nested function isolation, missing purpose comments, missing public docstrings, and generic exception-handler returns.
- `tests/projectkoios/bootstrap/python_policy/test__TargetSelector__targets.py`
  - Covers explicit file/directory target selection and cache/venv exclusion.

## Validation evidence

Commands run from `/Users/eugene/repos/projectkoios-bootstrap-schema-record-base`:

```bash
uv run pytest tests/projectkoios/bootstrap/python_policy -q
```

Result:

```text
17 passed in 0.07s
```

Static type checking for the new validator package:

```bash
uv run mypy src/python/projectkoios/bootstrap/python_policy
```

Result:

```text
Success: no issues found in 5 source files
```

Self-check with the new AST validator:

```bash
uv run python - <<'PY'
from pathlib import Path
from projectkoios.bootstrap.python_policy import PythonPolicyValidator, TargetSelector
paths = (Path('src/python/projectkoios/bootstrap/python_policy'),)
targets = TargetSelector(repo_root=Path.cwd()).explicit_targets(paths)
result = PythonPolicyValidator().validate_targets(targets)
for finding in result.findings:
    print(finding.format())
print(f'findings={len(result.findings)}')
raise SystemExit(1 if result.findings else 0)
PY
```

Result:

```text
findings=0
```

Broader regression:

```bash
uv run pytest -q
```

Result:

```text
209 passed in 0.94s
```

Validation note: `uv run` continued to warn that the parent shell's `VIRTUAL_ENV=/Users/eugene/repos/projectkoios-bootstrap/.venv` did not match the worktree-local `.venv`. The warning did not affect validation results.

## Deviations and deferred work

- CLI integration was deferred. The core validator can be called from Python, but there is no `projectkoios bootstrap validate-python-policy` command yet.
- The mypy runner is implemented but not yet coordinated into `PythonPolicyValidator.validate_targets`; this first slice validated mypy separately as a command.
- Whole-repo enforcement was not enabled to avoid noisy historical violations.
- Alias analysis for `Any` was not implemented. The AST rule detects direct `Any`, `typing.Any`, string annotations containing `Any`, and nested annotations such as `dict[str, Any]`.
- Whole-repo enforcement should still wait until existing code has documented exceptions or remediation plans.

## Current status

The easy first slice is implemented and validated. The next useful slice is CLI integration plus wiring mypy results into the combined validation result.
