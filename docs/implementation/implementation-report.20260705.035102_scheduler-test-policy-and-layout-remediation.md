# Implementation report 20260705.035102: Scheduler test policy and layout remediation

## Status

Implementation complete for a bounded daemon scheduler test-code Python policy and layout remediation slice.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Workspace: `workspaces/vulcan/`
- Branch: `master`
- Source request: user directed VULCAN to continue remaining remediation one file at a time
- Source policies: `docs/policies/python-coding.md`, `docs/policies/python-testing.md`
- Remediation source target: `tests/harness/daemon/__Scheduler__coalesce__tests.py`
- Remediation final target: `tests/projectkoios/bootstrap/harness/daemon/test__Scheduler__coalesce.py`

## Summary

Remediated the daemon scheduler coalescing tests against the Python policy validator and moved the file to the package-mirroring test tree.

Changed files:

- Removed `tests/harness/daemon/__Scheduler__coalesce__tests.py`.
- Added `tests/projectkoios/bootstrap/harness/daemon/test__Scheduler__coalesce.py`.
  - Moved the test under `tests/projectkoios/bootstrap/harness/daemon/` to mirror `projectkoios.bootstrap.harness.daemon.scheduler`.
  - Renamed the file from the legacy non-`test__` prefix pattern to a pytest-discoverable filename.
  - Added generated-docs-compatible docstrings to test and nested async helper functions.
  - Added explicit local annotations and nearby purpose comments for scheduler state, asyncio events, fired batches, and tasks.

## Validation evidence

Commands run from `/Users/eugene/repos/projectkoios-bootstrap`:

- `uv run projectkoios bootstrap validate-python-policy tests/projectkoios/bootstrap/harness/daemon/test__Scheduler__coalesce.py` => `summary: 0 finding(s), 1 file(s)`
- `uv run mypy tests/projectkoios/bootstrap/harness/daemon/test__Scheduler__coalesce.py` => `Success: no issues found in 1 source file`
- `uv run pytest tests/projectkoios/bootstrap/harness/daemon/test__Scheduler__coalesce.py -q` => `4 passed in 0.04s`
- `uv run pytest -q` => `215 passed in 1.13s`
- `uv run projectkoios bootstrap validate-python-policy --all` summary after this slice => `104 finding(s), 107 file(s)`
- `graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9392 nodes, 10128 edges, 832 communities`

## Deviations and deferred work

- This slice remediated and relocated only the daemon scheduler test file.
- Remaining test-code policy findings are outside this slice.
- Whole-repo policy validation remains incomplete; remaining findings should continue one file at a time.
- No architecture authority or product-domain decision is created by this remediation.

## Current status

`tests/projectkoios/bootstrap/harness/daemon/test__Scheduler__coalesce.py` now passes the Python policy validator with zero findings, mypy, focused pytest, and full pytest regression. Whole-repo policy validation decreased from `123 finding(s), 107 file(s)` to `104 finding(s), 107 file(s)` after this slice.
