# AAR — Hermes new-session launcher

## Scope
Hermes restart/autostart behavior and session-note creation.

## What happened
Added a `new` mode to `scripts/hermes-startup` so Hermes can create a durable timestamped session marker, print `new session`, and then read the standard resume surface. Also updated the Hermes workspace instructions and bootstrap template so fresh workspaces inherit the same restart contract.

## Process issues
The first launcher version only resumed from existing notes and accidentally treated the template file as the newest session. That made the restart surface less autonomous than intended.

## Proposed follow-up improvements
Consider wiring the launcher into the tmux/session bootstrap path so Hermes start-up can happen automatically when the workspace opens.

## Candidate ADR or implementation topics
Workspace startup automation and tmux bootstrap hook.

## Current status
The restart surface is now explicit and durable; further automation is optional.
