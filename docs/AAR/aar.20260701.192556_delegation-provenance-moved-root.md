# AAR 20260701.192556: Delegation provenance moved to root

## Scope

Moved the delegation/provenance reminder from `workspaces/hermes/AGENTS.md` into the repo root `AGENTS.md`.

## What happened

The user chose to centralize the represented-harness/delegation rule. I added the rule block to root AGENTS and removed the Hermes-local reminder.

## Process issues

- None observed.
- The user asked for better analysis before selecting the location, which was applied.

## Proposed follow-up improvements

- Keep represented-harness resolution rules in the root AGENTS file.
- Keep workspace files focused on workspace-only instructions.

## Candidate ADR or implementation topics

- Identity and delegation provenance policy
- AGENTS file scope split between root and workspaces
- Approval-gated edit workflow

## Current status

Delegation provenance guidance now lives in the repo root AGENTS file.
