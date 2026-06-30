# AAR 20260701.032257: Daemon Liveness Logs

## Scope

Inspected the Graphify daemon behavior in `projectkoios-bootstrap` after the user reported that it "does one batch and then stops."

## What happened

Reproduced the daemon locally and confirmed it continues watching after the initial batch and subsequent filesystem updates. The main issue was that daemon/Ollama logs were buffered when redirected, so detached runs could look like they had stopped.

Updated daemon logging to flush immediately and added an explicit "watching" banner after the initial run.

## Process issues

The daemon was functionally still alive, but the lack of flushed output made its continued watch state easy to misread as a stop.

## Proposed follow-up improvements

Add a small runbook note for detached/redirected daemon launches and logging expectations.

## Candidate ADR or implementation topics

Daemon run visibility and launch ergonomics.

## Current status

Code updated and validated with the daemon test suite.
