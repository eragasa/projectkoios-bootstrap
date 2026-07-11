```json
{
  "title": "Operator Console preview CLI implementation plan",
  "artifact_type": "implementation-plan",
  "status": "implemented-posthoc-user-confirmed",
  "datetime": "20260711.094447Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "slice_name": "operator-console-preview-cli",
  "source_context": "user feedback that preview command should not require copying a long package directory",
  "implementation_report": "docs/implementation/operator-console-preview-cli.20260711.093303.md",
  "next_owner": "USER_OR_HERMES_OR_ATHENA_REVIEW"
}
```

# Implementation plan 20260711.094447: Operator Console preview CLI

## Status

Implemented post-hoc after direct user feedback and now formalized as its own bounded convenience slice.

## Source context

The user reported that manually running:

```bash
cd /Users/eugene/repos/projectkoios-bootstrap/src/typescript/projectkoios/ui/operator-console
npm install --ignore-scripts
npm run build
npm run preview -- --host 127.0.0.1
```

was inconvenient and error-prone when line wrapping split the long package path.

User direction: this should be part of the CLI.

## Objective

Provide one repo-root command that launches the Operator Console preview from the correct package directory and builds before previewing.

## Scope

In scope:

- Add a local bootstrap CLI wrapper for Operator Console preview.
- Keep the command under existing `projectkoios` CLI surface.
- Default to package path `src/typescript/projectkoios/ui/operator-console/`.
- Run `npm install --ignore-scripts`, `npm run build`, then `npm run preview` from that package directory.
- Support host/port overrides and repeat preview without install.
- Add focused Python tests for command dispatch and generated subprocess argv.

Out of scope:

- Changing Operator Console UI behavior.
- Adding dependencies.
- Starting live adapters, backend/API service, persistent storage, or product runtime.
- Changing package manager policy.
- Making preview a production deployment command.

## Implemented command

From repository root:

```bash
uv run projectkoios operator-console preview
```

Repeat run without reinstall:

```bash
uv run projectkoios operator-console preview --skip-install
```

Options:

- `--host`, default `127.0.0.1`.
- `--port`, default `4173`.
- `--skip-install`.
- `--package-dir`, test/developer override.

## Files changed

- `src/python/projectkoios/bootstrap/commands/operator_console.py`
- `src/python/projectkoios/cli/main.py`
- `tests/projectkoios/bootstrap/test__OperatorConsolePreviewCommand__run.py`
- `docs/implementation/operator-console-preview-cli.20260711.093303.md`
- `docs/plans/implementation-plan.20260711.094447_operator-console-preview-cli.md`
- `workspaces/vulcan/state.md`
- `workspaces/vulcan/active.md`

## Validation evidence

Already recorded in `docs/implementation/operator-console-preview-cli.20260711.093303.md`:

```bash
uv run pytest tests/projectkoios/bootstrap/test__OperatorConsolePreviewCommand__run.py
# 2 passed

uv run projectkoios operator-console preview --help
# displayed command help

uv run ruff check src/python/projectkoios/bootstrap/commands/operator_console.py src/python/projectkoios/cli/main.py tests/projectkoios/bootstrap/test__OperatorConsolePreviewCommand__run.py
# All checks passed

uv run mypy src/python/projectkoios/bootstrap/commands/operator_console.py src/python/projectkoios/cli/main.py tests/projectkoios/bootstrap/test__OperatorConsolePreviewCommand__run.py
# Success: no issues found in 3 source files
```

## Boundary statement

This is a developer convenience wrapper. It does not introduce product authority, live state, backend/API behavior, persistent storage, workflow mutation, messaging capability, or production deployment semantics.

## Next owner

USER/HERMES/ATHENA review.
