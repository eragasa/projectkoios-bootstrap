# AAR — koios harnesses auto Hermes startup

## Scope
Automatic Hermes session-marker startup when `koios harnesses start` runs.

## What happened
Updated the koios harness start path to invoke `./scripts/hermes-startup new`, so Hermes now self-announces a durable new session marker when the koios tmux session starts.

## Process issues
The first implementation pass focused on the Hermes launcher itself, but the real automation boundary lives in the koios harness start command.

## Proposed follow-up improvements
Consider a tiny smoke test or fixture that exercises the koios start path without requiring an interactive tmux attach.

## Candidate ADR or implementation topics
Startup automation smoke test for koios harness start.

## Current status
Automation is in place; validation was limited to syntax checks and direct launcher execution.
