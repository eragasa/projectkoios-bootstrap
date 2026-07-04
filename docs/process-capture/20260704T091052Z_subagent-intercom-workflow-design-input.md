# Design input: subagent/intercom workflow harness

## Metadata

- Type: design-input
- Status: advisory
- From: KOIOS
- Target reader: ATHENA
- Repository: projectkoios-bootstrap
- Created: 20260704T091052Z
- Next expected artifact: ATHENA architecture draft or rejection note

## Purpose

This note transfers process and provenance observations about using pi subagents, intercom, role workspaces, and git worktrees in Project Koios.

This note is not an ADR.

This note is not an architecture document.

This note is not an implementation brief.

This note is draft input for ATHENA to decide whether an architecture draft is warranted.

## Problem observed

Project Koios now uses multiple role workspaces and live intercom sessions.

Pi subagents can automate bounded work, review, and context-building.

Intercom can notify live sessions but should not become durable authority.

Git worktrees can isolate parallel edits but do not define Project Koios roles or authority.

The system needs a way to preserve artifact-chain continuity without creating hidden workflow authority.

## Converged model

The repo filesystem remains the durable coordination surface.

Subagents automate bounded labor or review.

Intercom transports notifications and questions.

Git worktrees provide optional isolation for parallel or risky edits.

Role-owned artifacts remain the source of workflow authority.

A small workflow ledger may help reconciliation if it stays append-only and evidence-linked.

## Role feedback summary

### ATHENA feedback

Subagents should be treated as implementation-detail workers or role-local automation by default.

Subagents should not be treated as independent Project Koios role actors by default.

Role identity should be determined by durable workspace and artifact ownership, not by subprocess, model, cwd, or worktree.

Subagent output should remain advisory until promoted into a role-owned artifact.

Every subagent run should declare represented role, source artifact, output artifact, status marker, and promotion target.

### VULCAN feedback

Independent cwd or worktree subagents can hide implementation state unless outputs are copied back into durable artifacts.

Parallel implementation workers can create merge conflicts, duplicate fixes, or divergent validation assumptions.

Every subagent task should name cwd or worktree, consumed source artifact, allowed files or scope, validation command or review criterion, expected output artifact, and next expected artifact.

One merger or committer should own each integration surface.

Before merging worktree output, the parent or VULCAN should inspect the diff, run relevant tests, record results, and link back to the source artifact.

Intercom messages should not be completion evidence.

### HERMES feedback

The design should remain a thin workflow harness, not an orchestration platform.

`start-task` and `close-task` should be artifact-chain helpers, not lifecycle authorities.

The task contract should be schema-first.

The task contract should include `validator_of_record`.

Validation evidence should be stored as references only.

Intercom should remain optional and non-authoritative.

Both commands should support dry-run output.

The helper should refuse or require confirmation when source artifacts are missing, owner role is ambiguous, cwd or worktree state is unsafe, or closeout would imply authority promotion.

### KOIOS feedback

The ledger should preserve traceability, not become narrative memory.

Claims should be linked to source artifacts, validation evidence, reviews, commits, or explicit user decisions.

Hermes should not become validator of record.

Process capture should remain separate from ADRs, architecture documents, implementation reports, AARs, and durable knowledge notes.

## Candidate task contract

Every automated task should declare:

- represented role
- source artifact
- expected output artifact
- status marker
- next expected artifact
- cwd or worktree
- scope or allowed files
- validator of record
- validation evidence references
- writer or merger owner when relevant

## Candidate outcome vocabulary

- `started`
- `closed-clean`
- `closed-gap`
- `route-needed`
- `blocked`
- `aborted`

## Candidate first slice

Add a thin repo-local workflow helper with two commands.

```text
projectkoios workflow start-task
projectkoios workflow close-task
```

`start-task` should validate required task fields.

`start-task` should append a ledger entry.

`start-task` may print or run an exact pi-subagent launch command.

`start-task` may create or record a git worktree when requested.

`close-task` should check that the expected output artifact exists.

`close-task` should record validation evidence references.

`close-task` should mark the task outcome.

`close-task` may send an intercom notification that an artifact is ready.

The first slice should not perform automatic merge.

The first slice should not promote authority.

The first slice should not declare validation except by citing the validator of record.

## Candidate ledger role

The ledger should be append-only.

The ledger should index artifact-chain state.

The ledger should not become an ADR, architecture document, implementation report, AAR, or knowledge note.

The ledger should record enough information to reconstruct what artifact was consumed, what artifact was produced, what validation evidence exists, and who owns the next step.

## Open questions for ATHENA

Should the workflow helper be specified as an architecture document, a policy, or a workflow-control surface?

What schema should define the task envelope and ledger entry?

Where should the append-only ledger live?

Should subagent launch be part of the first slice or should the first slice only print commands?

Which role owns reconciliation when the ledger detects a gap or conflict?

What is the minimum dry-run contract for safe adoption?

## Non-authority statement

This note is advisory process/provenance synthesis only.

This note does not create architecture authority.

This note does not authorize implementation.

This note does not define validator-of-record authority.

ATHENA owns any architecture draft or rejection note that follows from this input.
