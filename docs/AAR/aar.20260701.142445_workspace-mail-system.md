# AAR 20260701.142445: Workspace mail system

## Scope

Converted the per-agent workspaces to use explicit `inbox/` and `outbox/`
folders and updated the runtime instructions so Hermes delivers mail.

## What happened

- Added `inbox/` and `outbox/` to each workspace layout.
- Updated `workspaces/<agent>/AGENT.md` instructions to say each agent reads
  inbox first and writes outgoing items to outbox.
- Codified Hermes as the mail-delivery role.
- Updated the workspace bootstrap skill and docs to match the mail system.

## Process issues

- Shared `handoffs/` alone was not enough to make the delivery path obvious.
- The runtime instructions needed a simple mailbox model per workspace.

## Proposed follow-up improvements

- Add a command for showing mail status in each workspace.
- Consider a tiny mail-delivery helper if Hermes mail routing becomes repetitive.

## Candidate ADR or implementation topics

- Workspace mail status command.
- Hermes mail delivery helper.

## Current status

Complete.
