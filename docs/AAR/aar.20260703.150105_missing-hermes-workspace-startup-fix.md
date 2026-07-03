# AAR 20260703.150105: Missing Hermes workspace startup fix

## Scope
Project Koios bootstrap workspace initialization and Hermes session startup recovery.

## What happened
A Hermes/pi launch was failing with `ENOENT: process.cwd failed... uv_cwd`, indicating the shell or process had been started from a directory that no longer existed. In this checkout, `workspaces/hermes/` was also absent, so the Hermes workspace layout was not materialized.

## Process issues
- The missing workspace path was not obvious until filesystem inspection.
- A dead cwd produces a startup crash before the harness can explain its own state.
- The repo already has a bootstrap command for workspaces, but the failure mode did not point there directly.

## Proposed follow-up improvements
- Add a preflight check that verifies the current cwd exists before launching harness commands.
- Emit a clearer recovery hint when `workspaces/hermes/` is missing.
- Consider a startup guard that auto-suggests `projectkoios bootstrap workspaces init --agents hermes`.

## Candidate ADR or implementation topics
- Workspace startup preflight and cwd recovery behavior.
- Better Hermes harness boot diagnostics.

## Current status
Hermes workspace materialized locally with the bootstrap command; the session should be restarted from a valid existing directory.
