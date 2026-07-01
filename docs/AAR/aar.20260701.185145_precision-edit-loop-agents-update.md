# AAR 20260701.185145: Precision-edit loop instruction added

## Scope

Updated `workspaces/hermes/AGENTS.md` to explicitly slow the Hermes workflow for precision edits.

## What happened

Added a session-protocol rule that, when the user requests precision edits or asks to slow down, Hermes should use a read → critique → propose-one-change → stop loop, avoid batching multiple edits, and wait for explicit approval before the next atomic change.

## Process issues

- None observed.

## Proposed follow-up improvements

- If this workflow proves useful, move it into the shared harness charter or a dedicated editing skill.

## Candidate ADR or implementation topics

- Precision-edit approval workflow
- One-change-at-a-time review protocol
- Harness instruction hierarchy for slow-mode editing

## Current status

The repo instruction now explicitly supports slower, approval-gated editing sessions.
