# AAR 20260701.012317: Graphify daemon ADR session

## Scope

This after-action report reviews the process used to produce and refine the
Graphify daemon ADR and interview artifacts in `projectkoios-bootstrap`.

It focuses on process problems and possible improvements, not on whether the
final ADR content is architecturally correct.

## What happened

The session started with repository state assessment, then accepted two Draft
ADRs. The discussion moved to the superseded Koios proposal for a
Graphify-backed daemon. A new daemon ADR was drafted, then an
Athena-style interview refined it. The interview output was written as a
separate artifact and passed with the Draft ADR to Archon, which revised the ADR
in place.

## Process issues

### Interview protocol mismatch

The user expected the interview protocol to ask one question at a time. Each
question should present four alternatives, analyze them against the user's
architecture preferences, recommend one, then wait for the user's response and
comments.

The first attempt asked a batch of questions. That violated the expected
interactive shape and reduced the user's ability to steer the architecture one
decision at a time.

Improvement:

- Add an explicit interview protocol to the `athena-interview-user` skill:
  one question per turn, four alternatives, recommendation, wait for response.
- Treat any user correction of interview shape as a protocol update to preserve
  in the final interview artifact.

### Premature solution narrowing

Early questions overfit the daemon to code review before the user clarified
that Graphify is intended as a shared substrate for all agents.

Improvement:

- Ask first about intended consumers before asking about output format.
- In architecture interviews, avoid assuming the first named use case is the
  whole use case.
- Add an early question: "Which harnesses or agents must consume this output in
  the first slice?"

### ADR draft was broader than the user's eventual intent

The first Draft ADR preserved too much of the old Koios ingestion proposal:
vault ingestion, PDF provenance, directive outputs, and future ingestion-engine
concerns. The user later narrowed the slice to automatically updated Graphify
for `projectkoios-bootstrap`, with broader ingestion deferred.

Improvement:

- When extracting from superseded proposal ADRs, separate "historical proposed
  scope" from "candidate first slice" before writing a new ADR.
- Prefer a short interview before drafting if the source proposal is known to
  have been superseded or partially rejected.

### Source authority was correct but slow

The session repeatedly used Graphify, direct file reads, ADR status scans, and
Archon run inspection. This was rigorous, but the user wanted to move quickly
once the high-level direction was clear.

Improvement:

- At session start, summarize authoritative state once, then avoid repeating
  broad scans unless a new decision depends on them.
- For follow-on edits in the same session, use targeted checks against the
  changed files and the relevant accepted ADRs.

### Graphify update semantics remained confusing

`graphify update .` was run after meaningful file changes, but it reported that
doc/paper/image changes need a fuller update path. This creates ambiguity:
the session protocol says to run `graphify update .`, but the work was mostly
Markdown ADR/interview content.

Improvement:

- Clarify in session protocol whether Markdown-only architecture changes need
  semantic Graphify update, AST-only update, or both.
- Record when `graphify update .` is only a session-boundary refresh and does
  not fully index new document semantics.
- Consider making this a follow-up ADR or implementation task because it now
  directly relates to the Graphify daemon work.

### Archon workflow fit was imperfect

The desired action was "use this interview plus this existing Draft ADR to
update the ADR." The available `athena-revise-adr` workflow was too narrow
because it accepted only an ADR path and a directive shape. The
`athena-handoff-spec` workflow was used instead and successfully revised the
existing ADR, but its nominal description says it writes a finalized ADR.

Improvement:

- Add or revise an Athena workflow for "apply architecture interview to existing
  Draft ADR."
- Inputs should be:
  - existing ADR path
  - interview artifact path
  - revision mode: in-place or replacement
  - status preservation rule
- Output should state whether it updated in place or wrote a replacement ADR.

### Durable AAR storage did not exist

The repo had ADRs, handoff archives, and interviews, but no obvious place for
process after-action reports. That means process learnings risk being buried in
chat or conflated with architecture decisions.

Improvement:

- Establish `docs/AAR/` as the default durable location for
  process AARs.
- Use filename convention:
  `aar.YYYYMMDD.HHMMSS_kebab-topic.md`.
- Keep AARs non-authoritative unless later promoted into an ADR or skill update.

### Dirty worktree accumulated across lifecycle steps

The session accumulated accepted-status edits, a new Draft ADR, a new interview
artifact, and an Archon-produced ADR revision before any commit boundary.

Improvement:

- At clear lifecycle boundaries, offer a checkpoint summary:
  - files changed
  - status of each artifact
  - whether to continue accumulating or commit/checkpoint first
- For multi-stage architecture work, consider committing after stable accepted
  status changes before starting a new Draft ADR path.

## Proposed follow-up improvements

1. Update `agents/global/archon/skills/athena-interview-user/SKILL.md` to encode
   the one-question-at-a-time interview protocol.
2. Create an Athena workflow for applying an architecture interview to an
   existing Draft ADR.
3. Decide whether Markdown ADR/interview changes require semantic Graphify
   refresh beyond `graphify update .`.
4. Document `docs/AAR/` as the durable home for process AARs.
5. Add a session checkpoint convention for multi-stage artifact work.

## Candidate ADR or implementation topics

- Athena interview protocol refinement.
- Interview-to-ADR revision workflow.
- Graphify semantic refresh policy for Markdown architecture artifacts.
- AAR artifact convention and lifecycle.
- Session checkpoint discipline for multi-artifact architecture work.

## Current status

This AAR is a process observation artifact. It does not change architecture
authority, ADR status, or implementation routing by itself.
