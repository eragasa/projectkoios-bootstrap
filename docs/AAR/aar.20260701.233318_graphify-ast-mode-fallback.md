# AAR 20260701.233318: Graphify AST-mode fallback

## Scope

Repo-local graphify refresh in Hermes session.

## What happened

A full `graphify .` attempt failed because the repo includes doc files and no LLM key/backend was configured for semantic extraction. I then used `graphify update . --no-cluster`, which completed the AST/code extraction successfully.

## Process issues

The initial command choice was too broad for a code-only refresh goal.

## Proposed follow-up improvements

Document the preferred fallback for AST-only refreshes when semantic backends are unavailable.

## Candidate ADR or implementation topics

Graphify runbook guidance for code-only vs full corpus refreshes.

## Current status

No durable issue observed beyond the initial tool mismatch.
