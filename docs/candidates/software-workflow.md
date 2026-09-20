# Project Koios software-development workflow candidate

## Status

`OBSERVED_UNVALIDATED` candidate. It is documentation only, is not installed,
and is not an executable workflow, runtime, Git adapter, GitHub adapter, task
database, or source of repository authority. No owner issue or architecture
acceptance is implied.

The first observation is the bounded development of the Petri-independent
workflow core:

- owner task: [`projectkoios-workflow#1`](https://github.com/eragasa/projectkoios-workflow/issues/1);
- immutable implementation evidence: commit
  `5002923807b195f612eeb1ad65d1e3939f7a78f9`; and
- review surface: draft
  [`projectkoios-workflow#2`](https://github.com/eragasa/projectkoios-workflow/pull/2).

Those owner-repository records remain authoritative. This candidate does not
copy their mutable state.

## Observation

The development sequence repeatedly distinguished four things that an informal
checklist can easily collapse:

1. a technical recommendation;
2. an operator authorization for one exact protected action;
3. the attempted repository operation; and
4. immutable evidence that the operation completed or failed.

For example, authorization to implement did not authorize commit; authorization
to commit did not authorize push; authorization to push did not authorize a
pull request, merge, release, or architecture acceptance. Technical review
success did not grant any of those permissions.

This is one observation. It justifies preserving a candidate contract, not
building mandatory orchestration machinery.

## Ownership and dependency direction

The candidate separates responsibilities as follows:

- `projectkoios-workflow` owns reusable workflow records, validation, runtime,
  persistence, and engine-adapter protocols;
- `projectkoios-bootstrap` may incubate the Project Koios-specific coordination
  definition and bounded Git/GitHub adapter behavior;
- each component repository owns its source, tests, branches, commits, issues,
  and pull requests; and
- `projectkoios` owns cross-repository product architecture decisions.

A future implementation would consume `projectkoios-workflow`; it must not
reimplement a workflow engine in this repository. The generic workflow core
must not import this candidate.

## Candidate purpose

`SoftwareWorkflow` would coordinate a bounded software change while preserving:

- owner-repository authority;
- exact expected revision and idempotency evidence;
- separate technical-review, operator-authorization, architecture-decision,
  and repository-operation outcomes;
- dry-run before any external mutation;
- append-only transition evidence;
- deterministic replay without repeating external effects; and
- privacy-safe public records.

It would not decide product intent, technical correctness, architecture
acceptance, scientific validity, release readiness, or publication authority.

## Normalized operations

| Operation | Required input evidence | Successful evidence | Explicit non-authority |
|---|---|---|---|
| `prepare_change` | owner task or bounded operator intent | exact repository, base revision, and scope references | does not authorize file mutation |
| `implement` | implementation authority scoped to the change | changed-tree identity and validation plan | does not authorize commit |
| `validate` | changed-tree identity and declared checks | command identities and bounded pass/fail references | does not authorize technical acceptance |
| `review` | exact changed-tree and validation identities | typed review outcome and findings | does not authorize correction or repository mutation |
| `correct` | accepted findings and correction authority | successor changed-tree and repeated validation references | does not authorize commit |
| `commit` | exact commit authority and expected tree/revision | commit identity and clean/dirty worktree observation | does not authorize push |
| `push` | exact remote, branch, commit, and push authority | remote branch and commit identity | does not authorize PR creation |
| `open_pull_request` | exact head/base and public-action authority | pull-request identity and sanitized request evidence | does not authorize merge or close an issue |
| `record_architecture_decision` | human-owned decision with affected-owner review | decision-record identity | is not inferred from tests or PR status |
| `merge` | exact PR revision, required reviews/checks, and merge authority | merge commit or closed failure evidence | does not authorize release or deployment |

Recommendation records are evidence for a later human decision; they are never
authority references themselves.

## Candidate state

State remains a compact set of typed references rather than a copied work queue
or repository snapshot. A future run may reference:

- owner repository and task identity;
- expected base, tree, commit, branch, and pull-request identities;
- validation and review evidence;
- scoped authorization and architecture-decision evidence;
- the current operational phase; and
- predecessor transition or recovery evidence.

It must not contain source files, patches, logs, credentials, private paths,
session transcripts, issue bodies, pull-request bodies, or mutable GitHub task
state.

## Protected-action protocol

Every external mutation follows the same boundary:

1. resolve the exact owner repository and expected revision;
2. produce a deterministic dry-run describing the proposed action;
3. obtain separately recorded authority scoped to that action and revision;
4. revalidate the expected revision immediately before execution;
5. execute through a thin Git or GitHub adapter;
6. record success, conflict, rejection, or infrastructure failure evidence; and
7. advance workflow state only from that supplied evidence.

A changed expected revision produces a conflict and requires a new dry-run. An
infrastructure failure is not a business rejection. Replaying retained evidence
must never repeat Git or GitHub effects.

## Deterministic attempt ordering

Within one workflow revision, each attempted action uses its immutable request
identity as the attempt identity. The deterministic comparison key is workflow
revision, request identity, and event identity. A future append-only runtime may
also preserve occurrence order, but it must not use wall-clock time or random
values to reconstruct transition identity.

## Recovery expectations

A future adapter must reconcile before retrying:

- commit: inspect whether the expected tree already has the intended commit;
- push: compare local and remote branch commit identities;
- pull request: find an existing request only by validated owner, repository,
  head, and base identity;
- merge: inspect the exact pull-request head and merge result; and
- ambiguous infrastructure failure: stop for reconciliation rather than repeat
  a potentially completed mutation.

Idempotency prevents duplicate intent; it does not prove an external action did
or did not occur.

## Privacy and public-record boundary

Before a public GitHub action, the adapter must reject credentials, private
filesystem paths, private document excerpts, session transcripts, runtime
payloads, and unbounded command output. Public descriptions use repository
identities, task identifiers, commit identities, bounded validation summaries,
and explicitly selected review evidence.

Raw tool output and private operational observations remain outside Git in
managed local state. Their content identities may be referenced when policy
allows.

## Sanitized first-observation trace

The reusable mechanics of the first observation are:

```text
implementation authority
  -> implement
  -> validate
  -> independent technical review
  -> correct bounded findings
  -> revalidate
  -> review outcome: no blocking findings
  -> commit authority
  -> commit evidence
  -> push authority
  -> push evidence
  -> pull-request authority
  -> draft pull-request evidence
```

The trace deliberately omits prompts, transcripts, machine paths, credentials,
command output, and private state. It is descriptive evidence, not an
executable fixture or claim that every software change requires every step.

## Limitations

- Only one bounded use has been observed.
- The proposed workflow-core contract remains unaccepted.
- No workflow runtime, append-only persistence, adapter protocol, or public wire
  format is available yet.
- The candidate has no executable definition, parser, serializer, dispatcher,
  Git adapter, GitHub adapter, or automated recovery implementation.
- No CPN mapping or authority is implied.
- The operation table may be too detailed or too coarse for a second use.
- Repository-specific policies remain authoritative and may prohibit an action
  even when this candidate can represent it.

## Next experiment

After the workflow-core proposal is reviewed, represent the sanitized trace as
immutable workflow-core objects and replay it with no external effects. That
experiment must remain a test or candidate fixture until `WF.2` supplies an
accepted runtime/persistence boundary.

Do not add live Git/GitHub mutation, persistent workflow state, automatic
installation, or mandatory coordination rules after this single observation.

## Promotion condition

Revisit implementation only after a second independent Project Koios software
change exercises substantially the same authority and recovery sequence, or a
concrete recurring failure demonstrates that native Pi and Git are
insufficient. Promotion then requires every gate in
[`docs/harness-incubation.md`](../harness-incubation.md), including a sanitized
fixture, deterministic dry-run/replay, recovery coverage, privacy checks,
owner-repository routing, and an explicit retain-or-extract decision.
