# AAR 20260701.123101: Cross-repo routing confusion

## Scope

Reviewed the bootstrap repo and the mothership/extracted Project Koios repos to identify why agents are getting mixed signals.

## What happened

Found multiple active repositories in mixed states, with inconsistent branch naming, partial extraction work, and several overlapping architecture documents in the mothership.

## Process issues

- Repo-local instructions are missing in most extracted repos.
- Architecture guidance is split across multiple files and not fully synchronized with the extraction ADRs.
- Several repos are dirty with local-only or generated files, which makes it hard to tell what is authoritative.

## Proposed follow-up improvements

- Add a minimal repo-specific README/AGENTS marker to each extracted repo.
- Collapse architecture guidance to one canonical index per repo.
- Separate local config/generated files from durable repo changes.

## Candidate ADR or implementation topics

- Cross-repo routing matrix
- Canonical architecture-doc index
- Repo-local agent instruction template

## Current status

Observed and reported; no repository changes made beyond this note.
