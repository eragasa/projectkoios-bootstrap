# AAR 20260701.105808: athena-revise-adr argument parsing fix

## Scope

Repair the `athena-revise-adr` Archon workflow so it can accept both an ADR
path and a revision directive in a single `$ARGUMENTS` message, resolving the
process failure recorded in `aar.20260701.054945_review-agent-adr-promotion.md`.

## What happened

Session started clean on `master`, no active Archon runs, no Draft ADRs
pending review. The highest-leverage pending item from the prior AAR was the
`athena-revise-adr` argument-handling bug, so the user routed to it directly.

Investigation confirmed the root cause: the `fetch-adr` bash node assigned the
entire `$ARGUMENTS` string to `path` and ran `[ ! -f "$path" ]`. When the
caller passed a path plus a revision directive as one message string, the whole
blob was treated as a file path and the existence check failed. This killed
run `0a15a5c78ea4` during the prior review-agent ADR revision.

The Archon CLI accepts only a single `[msg]` per `workflow run` with no
named-argument flag, so path and directive must be separated by a convention
inside `$ARGUMENTS`. A delimiter convention was chosen via user question:
first line = ADR path, remaining lines = revision directive.

Changes applied to `archon/workflows/athena-revise-adr.yaml` only:
- `fetch-adr` now splits `$ARGUMENTS` into `ADR_PATH` (line 1) and
  `REVISION_DIRECTIVE` (lines 2+), keeps the empty-path and existence guards,
  adds an empty-directive guard, and emits labeled output
  (`ADR_PATH=...`, `## Revision Directive`, `## ADR Content`).
- `revise-adr` prompt no longer re-injects raw `$ARGUMENTS`; it consumes
  `$fetch-adr.output` with an explicit map of the three labeled sections.
- `description` block documents the invocation contract and the real-newline
  requirement for shell callers.

Verification:
- `archon validate workflows athena-revise-adr` reports `ok`.
- Five dry-run cases of the bash split logic all behaved correctly:
  well-formed two-line input, path-only (clean directive error), single-line
  blob (clean not-found error replacing the old opaque failure), empty args,
  and multi-line directive capture.

## Process issues

- The original workflow shipped with an implicit single-input assumption that
  did not match its documented two-input purpose (path + directive). The
  `description` said it reads both, but the `fetch-adr` node only handled one.
  This is a spec/implementation drift that survived because no end-to-end
  revise run had been exercised until the review-agent promotion cycle.
- Archon's CLI offers no named-argument mechanism for `workflow run`, so
  multi-input workflows are forced into ad-hoc in-band parsing conventions.
  There is no repo-wide convention for this today; each workflow that needs
  multiple inputs must invent and document its own split rule.

## Proposed follow-up improvements

- Consider a repo-local convention document for Archon workflow `$ARGUMENTS`
  shapes (single-line, first-line-plus-rest, JSON) so future multi-input
  workflows do not reinvent the split rule ad hoc.
- Consider adding a smoke-test harness for Archon workflow bash nodes so
  fetch/parse nodes can be exercised without a live model run. The dry runs
  in this session were hand-rolled; a reusable script would lower the cost of
  validating future workflow changes.

## Candidate ADR or implementation topics

- Repo-local Archon `$ARGUMENTS` convention (small ADR, only if a second
  multi-input workflow appears; otherwise the per-workflow `description`
  contract is sufficient).
- The remaining pending item from `aar.20260701.054945`: implement the
  accepted review-agent contract through
  `agents/global/goose/skills/technical-debt-report/SKILL.md`.

## Current status

Fix complete and validated. Working tree dirty with the single workflow file
change. Not committed (awaiting user direction). Graphify AST refresh pending.
