# ADR 20260630.171442: First-class interview phase in the Petri-net meta-harness

## Status

Implemented

## Context

Origin: archon
Created: 2026-06-30 17:14
From: Athena
To: Vulcan
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap

This ADR specifies Option 1: **Interview as a First-Class Petri Net Phase**.
It is scoped to `projectkoios-bootstrap` and does not implement code.

Primary source context:

- `AGENTS.md`
- `docs/meta-harness.md`
- `docs/petri-net-model.md`
- `docs/architecture/adr/adr.20260630.042202_colored-petri-net-meta-harness.md`
- `docs/architecture/adr/adr.20260630.170000_pending-athena-decisions.md`
- `archon/workflows/archon-piv-loop.yaml`
- `archon/workflows/athena-handoff-spec.yaml`
- `docs/architecture/adr/adr.20260630.171204_interactive-interview-petri-net-piv.md`

## Decision

Project Koios should split the existing `archon-piv-loop` exploration behavior
into a first-class, typed intake phase that runs before Athena specification.
The interview loop remains interactive, but it no longer implies that Archon is
running a full Plan-Implement-Validate workflow. Its sole authority is to turn
an underspecified user request into a durable `spec-intake` packet that Hermes
can route to Athena.

The target flow is:

```text
user-request
  -> intake.unclarified
  -> conduct_interview / intake.interviewing
  -> interview-summary + spec-intake
  -> athena.ready
  -> athena-handoff-spec
  -> architecture-spec + acceptance-criteria + implementation-brief
  -> Hermes route to Vulcan
```

`archon-piv-loop.yaml` remains source material, not the new authority boundary.
The reusable part is its EXPLORE loop: inspect the repo before questioning,
ask decision-oriented questions, iterate until explicit user convergence, and
then summarize. The new phase must stop before Athena planning/specification.

### Places

Add or document these logical places in the Petri-net/meta-harness model:

| Place | Meaning |
|---|---|
| `intake.unclarified` | Raw or underspecified `user-request` needs interview before Athena can consume it. |
| `intake.interviewing` | `conduct_interview` is active and may exchange question/response tokens with the user. |
| `intake.blocked` | Interview cannot continue because user input or required repository context is missing. |
| `intake.ready_for_review` | Interview loop produced a candidate summary but Hermes has not routed it yet. |
| `spec-intake.ready` | Durable `spec-intake` packet is complete and has no blocking open questions. |
| `athena.ready` | Hermes has accepted the packet and routed it to Athena. |
| `athena.specifying` | `athena-handoff-spec` is producing the downstream spec handoff. |
| `vulcan.ready` | Hermes has routed Athena's implementation brief to Vulcan. |
| `hermes.completion_review` | Vulcan has reported back and Hermes must decide completion, revision, or knowledge capture. |
| `revision.required` | A guard, Hermes review, Athena, or Vulcan found missing or contradictory information. |

The current evaluator may initially represent these as conceptual places over
handoff files rather than executable Petri-net places. Do not build a full
Petri-net engine for this slice.

### Colored Artifact Tokens

The interview phase introduces these token kinds:

| Token kind | Owner | Required colors / provenance |
|---|---|---|
| `user-request` | user or Hermes | original request, source channel, repository scope |
| `intake-classification` | Hermes | route decision, reason, target place |
| `interview-question-set` | conduct_interview | questions, rationale, blocking/nonblocking marker |
| `interview-response` | user | answer text, question-set reference |
| `interview-summary` | conduct_interview | consolidated goal, context, decisions, risks |
| `spec-intake` | conduct_interview, routed by Hermes | durable Athena input packet |
| `routing-decision` | Hermes | target harness/place and reason |
| `architecture-spec` | Athena | final spec artifact |
| `acceptance-criteria` | Athena | inspectable completion criteria |
| `implementation-brief` | Athena | Vulcan-ready instructions |
| `implementation-plan` | Vulcan | planned file-level changes |
| `patch` | Vulcan | repository modification |
| `test-results` | Vulcan | validation output |
| `implementation-report` | Vulcan | implementation summary and residual risks |
| `deviation-report` | Vulcan | mismatch between spec and repo reality |
| `completion-decision` | Hermes | complete, revise, or route to Koios |

All durable tokens must preserve the existing colors from the handoff model:
`kind`, `origin`, `sender`, `recipient`, `acting_as`, `delegated_operator`,
`repository`, `scope`, `status`, and source artifact references. Codex-mediated
artifacts must keep `Delegated-Operator` explicit and must not collapse Codex
into `pi`, `archon`, `opencode`, or `goose`.

### Transitions

| Transition | Consumes | Produces | Owner |
|---|---|---|---|
| `ClassifyIntake` | `user-request` | `intake-classification`, token in `intake.unclarified` or direct route | Hermes |
| `StartInterview` | `user-request`, `intake-classification` | `interview-question-set`, token in `intake.interviewing` | Hermes / interview workflow |
| `CollectInterviewResponse` | `interview-question-set` | `interview-response` | user / interview workflow |
| `UpdateInterviewState` | `interview-response`, prior summary | updated `interview-summary`, open/resolved questions | interview workflow |
| `ConvergeInterview` | `interview-summary`, open questions | `spec-intake`, token in `spec-intake.ready` | interview workflow |
| `RouteSpecIntakeToAthena` | `spec-intake` | `routing-decision`, token in `athena.ready` | Hermes |
| `ProduceAthenaHandoff` | `spec-intake` | `architecture-spec`, `acceptance-criteria`, `implementation-brief` | Athena via `athena-handoff-spec` |
| `RouteSpecToVulcan` | `implementation-brief` | `routing-decision`, token in `vulcan.ready` | Hermes |
| `ImplementBrief` | `implementation-brief` | `implementation-plan`, `patch`, `test-results`, `implementation-report` | Vulcan |
| `ReviewCompletion` | Vulcan reports | `completion-decision`, `revision-request`, or knowledge-capture route | Hermes |

### Guard Rules

1. `UnderspecifiedRequestsEnterIntake`
   - If Hermes determines that a request is exploratory, ambiguous, or missing
     decisions needed for Athena, it must route to `intake.unclarified` before
     Athena specification.

2. `InterviewCannotSpecify`
   - `conduct_interview` may produce `interview-summary` and `spec-intake`.
     It must not produce final `architecture-spec`, `acceptance-criteria`, or
     `implementation-brief`.

3. `SpecIntakeRequiresExplicitConvergence`
   - `ConvergeInterview` is enabled only when the latest user message clearly
     authorizes completion of interview, using a signal equivalent to
     `INTERVIEW_PACKET_READY`. Silence, partial answers, questions, or new
     areas to investigate are not convergence.

4. `BlockingQuestionsMustBeEmpty`
   - `RouteSpecIntakeToAthena` is enabled only when `spec-intake` contains an
     explicit `blocking-open-questions` section and that section is empty.

5. `HermesMustRouteSpecIntake`
   - A completed `spec-intake` packet cannot jump directly to Athena. Hermes
     must create a `routing-decision` that moves it to `athena.ready`.

6. `AthenaRequiresSpecIntake`
   - For this flow, `athena-handoff-spec` consumes `spec-intake`, not the raw
     `user-request` or chat transcript.

7. `NoImplementationBeforeAthenaBrief`
   - Vulcan cannot implement from `user-request`, `interview-summary`, or
     `spec-intake`. Vulcan requires Athena's `implementation-brief` unless
     Hermes explicitly routes a trivial non-architecture task under existing
     repo policy.

8. `CompletionReturnsToHermes`
   - Vulcan reports return to `hermes.completion_review`. Vulcan does not mark
     the meta-harness flow complete by itself.

9. `ProvenanceRequired`
   - Tokens missing required provenance colors are invalid for authority-bearing
     transitions and should be routed to `revision.required` or violation
     reporting.

### Interview Loop Exit Criteria

The interview loop exits only when all of these are true:

- The user has explicitly indicated readiness to proceed from interview to
  specification.
- The packet restates the user's goal in implementation-neutral terms.
- Repository scope is confirmed as `projectkoios-bootstrap`.
- Scope-in and scope-out are explicit.
- User decisions are separated from Athena-resolvable assumptions.
- `blocking-open-questions` is empty.
- Risks and validation expectations are captured.
- The packet names source context inspected during interview.
- The workflow emits `INTERVIEW_PACKET_READY` or an equivalent completion signal.

If any criterion fails, the token remains in `intake.interviewing` or moves to
`intake.blocked`; it must not move to `athena.ready`.

### Required Markdown Conventions

The durable `spec-intake` artifact should be a markdown file, preferably written
by the interview workflow as `$ARTIFACTS_DIR/spec-intake.md` and then routed by
Hermes into a handoff when crossing the Athena boundary.

Required header:

```text
Origin: archon
Created: <YYYY-MM-DD HH:MM>
From: conduct_interview
To: Athena
Status: ready-for-routing
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap
Kind: spec-intake
```

Required sections:

- `# Spec Intake: <short title>`
- `## Source Request`
- `## Problem Statement`
- `## Repository Scope`
- `## Context Inspected`
- `## Decisions Made`
- `## Scope In`
- `## Scope Out`
- `## Interview Summary`
- `## Blocking Open Questions`
- `## Nonblocking Open Questions`
- `## Risks And Constraints`
- `## Candidate Artifact Contract`
- `## Validation Expectations`
- `## Provenance`

`Blocking Open Questions` must contain either `None` or a checklist of blocking
items. Hermes may route to Athena only when it is `None`.

### Composition With `athena-handoff-spec`

`athena-handoff-spec.yaml` remains the Athena composition point. It should read
a prepared `spec-intake` handoff and produce the established downstream handoff
sections:

- `architecture-spec`
- `acceptance-criteria`
- `implementation-brief`
- `resolved open questions`
- `non-goals`
- `validation expectations`
- `handoff routing back to Hermes after Vulcan reports`

Athena may resolve nonblocking questions from the packet. Athena must not treat
missing blocking information as a design decision; it should return a revision
request to Hermes if a packet reaches `athena.ready` with blocking gaps.

### Hermes Routing And Monitoring

Hermes owns routing and monitoring:

- On intake, classify the request as direct-to-Athena, direct-to-Vulcan,
  interview-needed, Koios knowledge work, or blocked.
- For interview-needed work, place the request in `intake.unclarified` and run
  the interview workflow in the foreground by default.
- Monitor the interview for explicit convergence and packet creation.
- Verify the `spec-intake` packet has no blocking open questions before routing.
- Create the `routing-decision` that moves `spec-intake.ready` to
  `athena.ready`.
- Invoke `athena-handoff-spec` with the packet path or handoff reference.
- After Athena produces an implementation brief, route it to Vulcan.
- After Vulcan reports, decide completion, revision to Vulcan, revision to
  Athena, or knowledge capture by Koios.

Hermes should treat orphaned or detached Archon runs as local runtime state to
inspect and clean up before relying on their output.

### Lifecycle Compatibility

The `intake.*` places defined here (`intake.unclarified`,
`intake.interviewing`, `intake.blocked`, `intake.ready_for_review`) are
**operational Petri-net places** for the interview workflow conduct. They are
distinct from the `intake` status field defined in the accepted ADR lifecycle
(`adr.20260630.175315_athena-owned-adr-lifecycle.md`), which is a lifecycle
status on ADR artifacts.

These operational places do not replace, override, or alias the ADR lifecycle
phases or their `allowed_next` rules. Model separation is preserved: workflow
places describe runtime conduct state; lifecycle status describes artifact
maturity.

When `spec-intake.ready` is routed by Hermes to `athena.ready` and
`athena-handoff-spec` produces `architecture-spec`, `acceptance-criteria`, and
`implementation-brief`, the resulting ADR artifact enters the accepted ADR
lifecycle at the `proposed` phase. Athena proposes; Hermes (as the message bus)
routes to `review`. This mapping is conceptual for the first implementation
slice and does not require a Petri-net engine or automatic status edits.

Future Hermes will operate as the message bus with a single UI controlling the
meta-harness. The operational places defined here are forward-compatible with
that model: Hermes routes tokens between places, while the ADR lifecycle tracks
artifact status independently.

## Consequences

This decision makes interactive intake an explicit Petri-net phase before
Athena specification, rather than burying exploration inside the monolithic
`archon-piv-loop`. Acceptance criteria, implementation guidance, validation
expectations, and Hermes return routing are below.

## architecture-spec

Split the existing `archon-piv-loop` exploration behavior into a first-class,
typed intake phase that runs before Athena specification. The interview loop
remains interactive but no longer implies Archon is running a full
Plan-Implement-Validate workflow. Its sole authority is to turn an underspecified
user request into a durable `spec-intake` packet that Hermes routes to Athena.

The target flow is:
`user-request -> intake.unclarified -> conduct_interview / intake.interviewing -> interview-summary + spec-intake -> athena.ready -> athena-handoff-spec -> architecture-spec + acceptance-criteria + implementation-brief -> Hermes route to Vulcan`.

`archon-piv-loop.yaml` remains source material, not the new authority boundary.
The reusable part is its EXPLORE loop: inspect the repo before questioning, ask
decision-oriented questions, iterate until explicit user convergence, then
summarize. The new phase stops before Athena planning/specification.

The `intake.*` places are operational Petri-net places, distinct from the ADR
lifecycle `intake` status (see Lifecycle Compatibility above). When
`spec-intake.ready` routes to `athena.ready` and `athena-handoff-spec` produces
the downstream spec, the resulting ADR artifact enters the accepted lifecycle
at the `proposed` phase.

## acceptance-criteria

Vulcan's implementation is acceptable when:

1. A first-class interactive interview workflow or equivalent split exists and
   stops at `spec-intake`; it does not implement code, author final Athena
   specs, validate patches, push branches, or create PRs.
2. The workflow models the desired place flow:
   `user-request -> intake.unclarified -> conduct_interview / intake.interviewing -> interview-summary/spec-intake -> athena.ready`.
3. The workflow includes an explicit convergence signal equivalent to
   `INTERVIEW_PACKET_READY`.
4. The `spec-intake` markdown template includes all required sections and
   provenance headers.
5. The workflow or docs state that `Blocking Open Questions` must be `None`
   before Hermes routes to Athena.
6. Documentation or evaluator-facing notes define the new places, colored
   tokens, transitions, guards, and exit criteria at the conceptual level.
7. `athena-handoff-spec.yaml` remains the only workflow responsible for turning
   `spec-intake` into `architecture-spec`, `acceptance-criteria`, and
   `implementation-brief`.
8. Existing `archon-piv-loop.yaml` behavior is preserved or explicitly
   documented as legacy/source material; it is not silently repurposed.
9. No machine-local config, secrets, run history, or credentials are modified or
   committed.
10. Vulcan returns `implementation-report`, `test-results`, and, if needed,
     `deviation-report` to Hermes.
11. Documentation includes a lifecycle compatibility note distinguishing
    `intake.*` operational places from the ADR lifecycle `intake` status, and
    mapping `spec-intake.ready -> athena.ready` to the lifecycle `proposed`
    phase.

## implementation-brief

Vulcan should implement the smallest repo-local slice that makes the interview
phase explicit.

Recommended work:

1. Add a new Archon workflow, suggested path
   `archon/workflows/conduct-interview.yaml` or
   `archon/workflows/spec-intake-interview.yaml`.
   - It must be interactive.
   - It should reuse the EXPLORE behavior from `archon-piv-loop.yaml`.
   - It must stop after writing `$ARTIFACTS_DIR/spec-intake.md`.
   - It must emit `INTERVIEW_PACKET_READY` only after explicit user readiness.

2. Add the `spec-intake` packet template to the workflow prompt.
   - Include the required markdown header and sections.
   - Separate blocking questions from nonblocking questions.
   - Forbid final Athena spec language in the interview artifact.

3. Document the Petri-net phase.
   - Update `docs/petri-net-model.md` or a narrow adjacent doc with the new
     places, tokens, transitions, and guards.
   - Keep the first implementation documentation-level unless current code
     enumerates token kinds and would reject the new packet.

4. Document Hermes composition.
   - Add or update concise docs describing:
     `spec-intake interview -> Hermes route -> athena-handoff-spec -> Vulcan -> Hermes completion review`.
   - Make foreground Archon runs the default recommendation.

5. Update evaluator/parser code only if required.
   - If the existing handoff evaluator infers artifact kind from title/header
     and accepts unknown kinds, avoid code changes.
   - If it rejects or misclassifies `spec-intake`, add the narrowest parser or
     guard support plus focused tests.

6. Return artifacts to Hermes.
   - Produce `implementation-report` with files changed and decisions made.
   - Produce `test-results` with validation commands and outputs.
   - Produce `deviation-report` for any intentional variance from this spec.

## blocking-open-questions

None.

## resolved-open-questions

1. Should the interview be embedded inside Athena specification?
   - Resolved: no. It is a pre-Athena intake phase.

2. Should the full `archon-piv-loop` remain the unit of orchestration?
   - Resolved: no for this flow. Its EXPLORE prompt is reusable, but the
     meta-harness needs inspectable phase outputs.

3. What artifact gates Athena?
   - Resolved: `spec-intake`, routed by Hermes to `athena.ready`.

4. Can Athena consume a packet with blocking open questions?
   - Resolved: no. Blocking questions must return to interview or Hermes
     revision before Athena spec work begins.

5. Can Vulcan implement from interview output?
   - Resolved: no. Vulcan needs Athena's `implementation-brief` for this flow.

6. Is a general Petri-net execution engine required now?
   - Resolved: no. First slice is workflow/documentation plus narrow evaluator
     alignment only if needed.

7. Who owns final completion?
   - Resolved: Hermes. Vulcan reports; Hermes completes, revises, or routes to
     Koios for knowledge capture.

## non-goals

- Do not implement code as part of this Athena pass.
- Do not define Project Koios product/domain architecture.
- Do not remove or rewrite every Archon workflow.
- Do not build a general colored-Petri-net runtime engine.
- Do not make the interview phase produce Athena's final spec artifacts.
- Do not let Vulcan implement directly from `spec-intake`.
- Do not push branches, create PRs, or modify machine-local Archon state.
- Do not commit secrets, local runtime state, or credentials.

## validation-expectations

Vulcan should run the smallest relevant validation for the files changed:

- YAML syntax validation for changed workflow files.
- Markdown structure/format validation for changed docs, using repo tooling if
  present or manual inspection if no tool exists.
- Focused tests for parser/evaluator changes if any code under `src/python/`
  changes.
- `projectkoios bootstrap handoff evaluate --dry-run` if available and safe.
- `git diff --check`.

If a validation command is unavailable, record the command attempted and the
reason it could not run in `test-results`.

## routing

Vulcan must return to Hermes, not directly to Athena or Koios.

Required return artifacts:

- `implementation-report` addressed to Hermes
- `test-results` addressed to Hermes
- `deviation-report` addressed to Hermes if implementation differs from this
  specification or uncovers an unresolved architecture issue

Hermes then chooses one route:

- complete if acceptance criteria and validation pass
- revise to Vulcan if implementation is incomplete
- revise to Athena if this spec is insufficient or contradicted by repo reality
- route to Koios after completion if durable knowledge capture is needed
