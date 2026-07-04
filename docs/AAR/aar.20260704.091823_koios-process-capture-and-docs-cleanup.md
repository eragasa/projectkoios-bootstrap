# AAR 20260704.091823: Koios process capture and docs cleanup

## Scope

Koios workspace guidance, process-capture documentation, and docs cleanup in `projectkoios-bootstrap`.

## What happened

KOIOS captured advisory design input for a thin subagent/intercom workflow harness under `docs/process-capture/`.

KOIOS adjusted the Koios workspace control plane to remove mail-system assumptions and use filesystem artifact-chain language.

KOIOS reviewed the `docs/` tree for dangling or weird files.

KOIOS deleted the deprecated `docs/architecture/harness-boundaries.md` pointer.

KOIOS archived the superseded mailbox/intercom bridge plan under `docs/archive/plans/`.

KOIOS fixed broken active Markdown links and added `docs/architecture/architecture.adversarial-two-plane-gate.md` as an architecture pointer surface.

KOIOS renamed malformed AAR filenames from `aar.260701.*` to `aar.20260701.*`.

KOIOS ran `graphify update /Users/eugene/repos/projectkoios-bootstrap` at session closeout.

## Process issues

The session exposed residual mail-system and Hermes-router assumptions after the repo had moved toward filesystem-visible artifact chains.

The active docs tree contained stale compatibility pointers and broken links after recent ADR/schema namespace moves.

Multiple roles were changing related documentation concurrently, so KOIOS avoided claiming ownership over all dirty-tree changes.

## Proposed follow-up improvements

Add a lightweight active-docs link check to closeout or validation scripts.

Add a docs namespace index that identifies active, archived, process-capture, schema, implementation, and policy surfaces.

Clarify which role owns committing multi-role doc batches when changes span Athena, Vulcan, Hermes, and Koios surfaces.

## Candidate ADR or implementation topics

A future Athena architecture draft may define the thin workflow task-envelope helper for subagents, intercom notifications, and append-only ledger reconciliation.

A future Vulcan implementation slice may add `projectkoios workflow start-task` and `projectkoios workflow close-task` after architecture approval.

A future Koios process-capture convention may require every cross-role design input to name its source artifacts and next expected artifact.

## Current status

The Koios-owned process-capture design input has been written.

The Koios workspace guide no longer assumes a mail system.

The active-docs broken Markdown link check reported zero missing active links after cleanup.

The working tree still contains uncommitted changes from multiple roles and should be reviewed before a broad commit.
