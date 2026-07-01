# AAR 20260701.131000: Repo projection architecture

## Scope

Updated the bootstrap architecture docs to treat each repository as both a git repository and an Obsidian-like Markdown repository.

## What happened

Created `docs/architecture.repo-projections.md` and rewrote `docs/architecture.00.md` to define the bootstrap-side workspace, repo projection, and action layers under `src/python/projectkoios/bootstrap/`.

## Process issues

- The bootstrap architecture needed a clearer boundary between workspace persistence and repo projection behavior.
- The previous architecture note was malformed and needed a full rewrite.

## Proposed follow-up improvements

- Decide whether `repos/obsidian.py` should stay a single module or split into markdown/frontmatter/wikilink helpers.
- Add a minimal bootstrap helper that initializes the workspace layout on disk.

## Candidate ADR or implementation topics

- Workspace bootstrap and repo projection lifecycle.
- Markdown repository projection helpers.

## Current status

Complete.
