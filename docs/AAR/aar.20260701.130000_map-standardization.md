# AAR 20260701.130000: Map standardization

## Scope

Standardized the bootstrap workspace maps so they clearly separate repository ownership, package ownership, and vault paths.

## What happened

Rewrote `maps/repositories.md`, `maps/packages.md`, and `maps/vault_paths.md` to:
- point to `docs/agent-charter.md` for routing
- remove the vault directory from the repo list
- mark `projectkoios-notes` as a vault path, not a git repo
- align package ownership with the extracted repo layout

## Process issues

- The repo map still blended git repos and vault directories.
- The package map needed a clearer relationship to the canonical routing doc.

## Proposed follow-up improvements

- Keep workspace maps narrowly scoped: repos, packages, vault paths.
- Add a simple index page for the maps if more workspace categories appear.

## Candidate ADR or implementation topics

- Canonical workspace-map index
- Vault/repo distinction policy

## Current status

Complete.
