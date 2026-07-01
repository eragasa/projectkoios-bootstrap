---
status: draft
date: 20260701.131500Z
---

# Repository projections

See `[architecture.00](architecture.00.md)`.

## Context


Project Koios treats each git repository as both:
- a source repository with branches, commits, and diffs
- an Obsidian-like repository of Markdown architecture notes, decisions, and
  durable process artifacts

This allows architecture documents to live with the repo they describe while
still being tracked through git.

The bootstrap repo needs a small, filesystem-oriented layer for working with
both surfaces at once:
- git state and repo identity
- Markdown note layout and vault-like directory conventions
- per-agent workspace state that projects repo activity into session artifacts

## Decision


Use a bootstrap-side projection layer under:

```text
src/python/projectkoios/bootstrap/
├── workspace/
│   └── ...
├── repos/
│   ├── __init__.py
│   ├── git.py
│   └── obsidian.py
└── actions/
    └── ...
```

See:
- [architecture.workspaces.00](architecture.workspaces.00.md)
- [architecture.workspaces.git](architecture.workspaces.git.md)
- [architecture.workspaces.obsidian](architecture.workspaces.obsidian.md)
- [architecture.repos.00](architecture.repos.00.md)
- [architecture.repos.git](architecture.repos.git.md)
- [architecture.repos.obsidian](architecture.repos.obsidian.md)

### Package responsibilities

| Package | Responsibility |
|---|---|
| `projectkoios.bootstrap.workspace` | persistent per-agent workspace state |
| `projectkoios.bootstrap.repos.git` | git repository identity, branch, status, and file ownership |
| `projectkoios.bootstrap.repos.obsidian` | Markdown-note projection, architecture-note location, and vault-style conventions |
| `projectkoios.bootstrap.actions` | action objects that write or update workspace and repo artifacts |

## Consequences

- The bootstrap repo can model repo state and note state without forcing that
  concern into the mothership domain packages.
- Architecture notes can be treated as first-class Markdown artifacts while
  still being managed through git.
- The design stays small enough to incubate before extraction.

## Non-goals

- Not a replacement for `maps/`
- Not the product architecture model
- Not a full Obsidian sync engine
- Not a git wrapper for arbitrary repository operations

## Follow-up questions

- Should `obsidian.py` read only Markdown structure, or also frontmatter and
  wikilinks?
- Should `git.py` expose just state, or also helpers for writing repo-local
  notes?
- Should architecture-note indexing live in `repos/obsidian.py` or a dedicated
  `notes.py` module later?
