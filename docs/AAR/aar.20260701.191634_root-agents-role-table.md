# AAR 20260701.191634: Root AGENTS role table moved

## Scope

Moved the role identity reference table from `workspaces/hermes/AGENTS.md` into the repo root `AGENTS.md`.

## What happened

The user requested the shared identity table be centralized in the repo root and ordered as Identity / Workspace / Harness / Role. I added the table to the root file and removed the duplicated table from the Hermes workspace file.

## Process issues

- None observed.
- The user requested a finer analysis format, which was applied during the line-by-line pass.

## Proposed follow-up improvements

- Keep shared identity metadata in the root AGENTS file only.
- Keep Hermes workspace instructions focused on Hermes-specific behavior, not the full identity matrix.

## Candidate ADR or implementation topics

- Repo-vs-workspace AGENTS boundary
- Canonical identity metadata table
- Precision-edit approval workflow

## Current status

The identity table now lives in the repo root AGENTS file.
