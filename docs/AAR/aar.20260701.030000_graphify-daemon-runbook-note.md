# AAR 20260701.030000: Graphify Daemon Runbook Note

## Scope

Verified the current Graphify daemon launch path in `projectkoios-bootstrap`.

## What happened

Confirmed `./scripts/koios ingestion daemon --once` runs successfully from the repo root.
The daemon CLI is present and the background watcher entrypoint exists.

## Process issues

None observed.

## Proposed follow-up improvements

Add a short runbook section for foreground and detached daemon launch, plus log handling.

## Candidate ADR or implementation topics

Daemon launch documentation and supervision helpers.

## Current status

The daemon is runnable today; the main gap is discoverability and a clearer launch recipe.
