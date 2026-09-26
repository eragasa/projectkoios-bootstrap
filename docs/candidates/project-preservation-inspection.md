# Project preservation inspection candidate

## Lifecycle

**Candidate.** The first bounded use is the preservation-first cleanup of the
12 repositories in `maps/repositories.md` plus the separately included
Frankenstein incubation repository and their registered worktrees. The existing
repository summary identifies counts but intentionally does not expose the
paths and commit reachability needed to preserve work before cleanup. One use
does not establish recurrence or authorize promotion.

## Purpose and contract

The executable entry point is `scripts/inspect-project-preservation`.
Per-repository evidence is implemented in
`projectkoios.bootstrap.worktree.preservation`; deterministic cross-repository
aggregation belongs to `projectkoios.bootstrap.repository.preservation`.

Invoke it with an explicit set of absolute canonical repository roots:

```bash
./scripts/inspect-project-preservation \
  /absolute/path/to/repository-a \
  /absolute/path/to/repository-b
```

The command emits one schema-versioned JSON document to stdout. For every
registered worktree it combines the existing inventory facts with:

- structured staged, unstaged, untracked, conflicted, renamed, and submodule
  status paths;
- a digest and category counts for the exact porcelain-v2 status payload;
- the exact locally known remote-tracking ref names, object IDs, symbolic
  targets, and a deterministic ref-set digest;
- commit reachability from each worktree HEAD against that ref set; and
- deterministic preservation signals for dirty state, commits not on known
  remotes, missing or prunable registrations, hidden index flags, locks,
  non-branch state, unavailable comparisons, and upstream relationships.

Up to 100 sorted object IDs not reachable from known remote-tracking refs are
included directly. The complete count and digest remain available when the list
is truncated. The aggregate count is a **worktree occurrence count** because
the same commit may be reachable from more than one worktree HEAD; it is not a
deduplicated project-wide commit count.

## Meaning and limits

A preservation signal identifies evidence needing inspection. It is not a
cleanup decision or severity ranking.

- `dirty` says Git reported status entries. It does not interpret their content
  or decide whether they are valuable.
- `commits_not_on_known_remotes` says commits are not reachable from any local
  remote-tracking ref. The command does not fetch, so stale local refs can
  produce conservative results.
- `remote_reachability_unknown` says the local evidence was insufficient; it
  does not mean the HEAD is unpublished.
- `missing` and `prunable` reproduce Git facts. Neither means safe to delete.
- `upstream_behind` is synchronization evidence, not authority to pull, merge,
  rebase, or reset.

The tool does not inspect ignored files because Git status deliberately excludes
them. It reports paths and Git object IDs but never emits or interprets file
content. The inherited inventory reads tracked and non-ignored untracked bytes
locally only to hash them for change-during-inspection detection. Output may
contain private local paths and untracked filenames; keep it in ephemeral
operational storage and do not commit it to this repository.

## Safety and stop behavior

The operation is read-only. It uses Git with optional locks, lazy fetching,
background maintenance, global configuration, system configuration, credential
prompts, and inherited `GIT_TRACE*` or repository-redirection variables
disabled. Commit traversal receives the captured remote-ref object IDs through
stdin instead of resolving the live remote namespace again. It does not fetch,
prune, delete, clean, reset, stash, stage, commit, push, open issues, contact
GitHub, or change worktree registration.

Repository paths must be explicit, absolute, canonical, unique, and point to
non-bare worktree roots. Inputs are sorted before inspection, so repository
argument order does not affect output bytes. The command validates the complete
result as JSON before writing stdout and emits no partial JSON if any repository
fails. Additive schema-version-1 values must therefore remain JSON-compatible.
It stops if required Git output is malformed or if
refs, worktree metadata, HEAD attachment, index flags, status, or tracked and
non-ignored untracked filesystem evidence changes during inspection.

The command writes no ledger, decision file, checkpoint, or task state. Re-run
it to obtain current facts. Cleanup and branch migration remain separately
authorized operations with their own authoritative preflight.

## Validation

Tests cover:

- ordinary, renamed, unmerged, and untracked porcelain-v2 records, including
  paths containing spaces;
- malformed or duplicate NUL/newline records, status characters, submodule
  fields, modes, object IDs, rename scores, refs, and option-shaped HEAD
  rejection;
- SHA-1 and SHA-256 status object IDs;
- simultaneous staged and unstaged changes;
- reachability against captured ref object IDs even when the live ref moves;
- lazy-fetch suppression using a promisor repository and observable local
  remote helper;
- commits not reachable from a configured remote;
- absent remote-tracking refs;
- missing/prunable worktree preservation;
- no mutation of status or refs;
- deterministic output under reversed repository input order;
- complete required-field and semantic validation, duplicate or unsorted
  worktree/status rejection, producer-contradiction rejection,
  JSON-compatible additive-field support, and pre-serialization;
- bounded expected CLI failure without partial JSON or traceback; and
- executable-wrapper behavior.

Run:

```bash
python3.14 -m pytest -q \
  tests/worktree/test_preservation.py \
  tests/repository/test_preservation.py
python3.14 -m ruff check python tests
python3.14 -m ruff format --check python tests
python3.14 -m mypy python tests
```

Tests use temporary repositories and local bare remotes. They do not establish
GitHub state, content value, deletion safety, migration readiness, or the
freshness of local remote-tracking refs.

## Owner routing and revisit criteria

This Project Koios-specific cross-repository inspection belongs in bootstrap
while it remains a candidate. Git owns status, refs, worktree registration, and
reachability semantics. Owner repositories retain their content and cleanup
decisions. Revisit extraction only after an independent use demonstrates a
stable generic contract.
