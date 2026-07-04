# AAR 20260704.000000: Remove mailbox control surfaces

## Scope

Project Koios bootstrap control-surface cleanup for removing the workspace mailbox model from active guidance, templates, workspace bootstrap code, and related tests.

## What happened

The user directed that the mailbox system was too complicated and asked to remove it from the control surfaces. I replaced mailbox and sandbox-message-delivery language with role routing, explicit handoff artifacts, and provenance-preserving coordination. I also removed the bootstrap mailbox helper and its direct test, and updated workspace initialization so new workspaces no longer create `inbox/` or `outbox/` directories.

## Process issues

- Earlier in the session I delivered an Athena outbox file into a Hermes inbox immediately before the user rejected the mailbox model. That was consistent with the old guidance but exposed the workflow friction the cleanup addresses.
- The repo had many pre-existing uncommitted changes, including ADR moves and broad generated/documentation edits. I limited this pass to mailbox-related control surfaces and did not try to normalize unrelated changes.
- Full test validation still has unrelated ingestion fixture failures around `docs/adr/**/*.md` resolution in temporary test roots.

## Proposed follow-up improvements

- Decide whether legacy Petri-net place names such as `pi_inbox` should be renamed in code or retained as compatibility identifiers.
- Add an explicit migration note for old workspace `inbox/` and `outbox/` artifacts so agents preserve provenance without treating directory placement as authority.
- Consider removing empty workspace `inbox/` and `outbox/` directories from the working tree if they are not needed as historical placeholders.

## Candidate ADR or implementation topics

- Role-routing and explicit handoff artifacts as the canonical replacement for mailbox transport.
- Compatibility policy for legacy place identifiers in the handoff evaluator.
- Workspace bootstrap schema versioning for future control-surface changes.

## Current status

Targeted workspace and handoff tests pass. Full test suite was run and failed only in existing ingestion tests that cannot find `docs/adr/**/*.md` in temporary fixture roots.
