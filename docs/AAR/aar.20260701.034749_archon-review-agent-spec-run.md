# AAR 20260701.034749: Archon Review Agent Spec Run

## Scope

Ran Archon/Athena workflows to turn the human-in-the-loop code review agent
proposal into a spec-ready Draft ADR.

## What happened

The user requested an Archon interview on the proposal followed by an Archon
spec. Codex first attempted `design-review`, but that workflow did not receive
the ADR path in its bash node and reviewed the default missing path instead.

Codex then attempted `athena_review-draft-for-promotion`, which failed because
its bash node also did not receive the ADR path through `$ARGUMENTS`.

Codex then ran `athena-handoff-spec` with the source proposal path and explicit
interview-style instructions in the prompt node. That workflow completed and
wrote:

`docs/architecture/adr/adr.20260701.034612_human-in-the-loop-review-agent-contract.md`

Codex applied a mechanical heading normalization from `resolved open questions`
to `resolved-open-questions` so the generated ADR follows the repository's
machine-relevant section convention.

## Process issues

Two Archon workflows that use bash nodes failed or degraded because argument
passing did not populate the shell variable shape expected by the workflow.

The successful workflow used a prompt node and therefore avoided the bash
argument issue.

## Proposed follow-up improvements

Review repo-local Archon workflows that read `$ARGUMENTS` or shell positional
arguments in bash nodes. Add a small validation or fixture to confirm workflow
arguments reach bash nodes as expected.

## Candidate ADR or implementation topics

Possible implementation topic: harden `design-review` and
`athena_review-draft-for-promotion` argument handling.

## Current status

Archon produced the refined Draft ADR/spec. No code implementation was
performed.
