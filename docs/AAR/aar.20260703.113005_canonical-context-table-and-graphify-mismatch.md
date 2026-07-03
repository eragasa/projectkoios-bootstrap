# AAR 20260703.113005: Canonical context table and graphify mismatch

## Scope
Updated the root `AGENTS.md` with a canonical context table for harness loads.

## What happened
Added a short table listing the canonical `[Context]` file order for global, repo, and role-workspace rules.

## Process issues
`graphify update . --no-cluster` still refused to overwrite the existing graph because of the node-count mismatch.

## Proposed follow-up improvements
Treat the graph mismatch as a standing tooling issue until the graph is rebuilt or the refresh path is changed.

## Candidate ADR or implementation topics
Canonical context loading order.

## Current status
Complete.
