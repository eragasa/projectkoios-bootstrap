# ADR 20260702.121432Z: Unified Diff Review Surface

## Status

draft
date: 20260702.121432Z

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The current review flow does not make exact file diffs easy to inspect in a stable way. When the agent summarizes changes in prose, the user cannot reliably see the literal file-level edit that is being proposed.

This makes approval, correction, and commit gating harder than they need to be. A review surface should show the actual diff, not a paraphrase of it.

## Decision

Adopt a unified diff review surface that shows the literal file diff before commit or status approval.

The review surface must:
- display exact diff hunks
- preserve file names and line context
- allow the user to review changes before commit
- support explicit approval or rejection of the proposed file status
- keep the diff visible while the associated discussion continues

## Consequences

- the user can inspect the actual file-level change instead of a summary
- approval becomes grounded in visible evidence
- commit gating becomes clearer
- the review surface can be implemented as a skill without changing the ADR review model itself

## architecture-spec

This ADR defines a workflow/review control surface.

The surface is not a replacement for the ADR lifecycle. It is the review mechanism that makes a proposed file change legible enough to approve, reject, or revise.

Minimum required behavior:
- render a literal unified diff
- keep the diff tied to the file path
- expose enough context to understand the change without leaving the review surface
- support incremental review of multiple files

## acceptance-criteria

- a reviewer can see the actual diff text for a file
- the diff includes enough context to understand the change
- the review surface can be used before commit
- approval or rejection is based on visible file changes, not prose paraphrase

## implementation-brief

If accepted, implement a diff-viewer skill or equivalent review tool that renders literal unified diffs and supports review-before-commit.

verification_method: open a changed file in the review surface and confirm the literal diff hunk matches the underlying file edit before approval.

## resolved_open_questions

- Should the diff surface live as a skill, an extension, or both?
- Should it support side-by-side and unified modes?
- Should approval be a status action or a separate review action?

## non_goals

- replacing git diff itself
- creating a new ADR schema field
- changing the commit command semantics

## validation_expectations

- the user can inspect literal diffs before committing
- the review surface reduces confusion about what changed
- the implementation can be tested against a known file edit

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Review/control surface for literal diff inspection.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
