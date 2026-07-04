```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "watcher-test-policy-and-layout-remediation-complete",
  "datetime": "20260705.022028",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/implementation-report.20260705.022028_watcher-test-policy-and-layout-remediation.md",
    "docs/implementation/implementation-report.20260705.021601_daemon-run-once-test-policy-and-layout-remediation.md",
    "docs/implementation/implementation-report.20260705.021059_ollama-test-policy-and-layout-remediation.md"
  ],
  "scratch_directory": "scratch/",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md"
}
```

# Vulcan active work

## Current priority stack

1. Request HERMES/user review of `docs/implementation/implementation-report.20260705.022028_watcher-test-policy-and-layout-remediation.md`.
2. Continue remaining test-code Python policy remediation by bounded test file group if directed.
3. Package current implementation slices for commit/push if directed, avoiding concurrent non-VULCAN dirty files.

## Working material

- Watcher test remediation report: `docs/implementation/implementation-report.20260705.022028_watcher-test-policy-and-layout-remediation.md`.
- Current VULCAN AAR: `docs/AAR/aar.20260705.022028_watcher-test-policy-and-layout-remediation.md`.
- Latest moved/remediated file:
  - deleted `tests/harness/daemon/__Watcher__scan_mtimes__tests.py`.
  - added `tests/projectkoios/bootstrap/harness/daemon/test__Watcher__scan_mtimes.py`.
- Latest remaining all-target policy baseline: `264 finding(s), 107 file(s)` from `uv run projectkoios bootstrap validate-python-policy --all`.

## Latest validation evidence

- `uv run projectkoios bootstrap validate-python-policy tests/projectkoios/bootstrap/harness/daemon/test__Watcher__scan_mtimes.py` => `summary: 0 finding(s), 1 file(s)`.
- `uv run mypy tests/projectkoios/bootstrap/harness/daemon/test__Watcher__scan_mtimes.py` => `Success: no issues found in 1 source file`.
- `uv run pytest tests/projectkoios/bootstrap/harness/daemon/test__Watcher__scan_mtimes.py -q` => `7 passed in 0.24s`.
- `uv run pytest -q` => `215 passed in 1.13s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 264 finding(s), 107 file(s)`.

## Ignore for now

- Product architecture changes.
- Broad workflow refactors outside active handoff scope.
- ATHENA/HERMES/KOIOS-owned workspace files unless explicitly directed.
- Source-authority changes.
- Claims that whole-repo or all-test policy remediation is complete.
- Concurrent KOIOS dirty files unrelated to this VULCAN slice.

## Next expected artifact

- HERMES/user review response, next bounded test-code remediation report, or commit/push instruction.
