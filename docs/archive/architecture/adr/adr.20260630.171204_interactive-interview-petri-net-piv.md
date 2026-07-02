# ADR 20260630.171204: Interactive interview phase for Petri-net PIV routing

## Status

historic

## Context

Origin: archon
Created: 2026-06-30 17:12
From: Athena
To: Vulcan
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap

This specification responds to the user request to break up the existing
`archon-piv-loop` so that an interactive interview/exploration loop can be
modeled inside the Project Koios colored-Petri-net/meta-harness workflow before
Athena specification begins.

Primary source context:

- `archon/workflows/archon-piv-loop.yaml`
- `archon/workflows/athena-handoff-spec.yaml`
- `docs/architecture/adr/adr.20260630.042202_colored-petri-net-meta-harness.md`
- `docs/architecture/adr/adr.20260630.170000_pending-athena-decisions.md`
- `docs/petri-net-model.md`
- `docs/meta-harness.md`
- `AGENTS.md`

This is scoped to `projectkoios-bootstrap`. It does not define product/domain
architecture for the mothership vault.

## Decision

The existing `archon-piv-loop` should not remain the only shape for guided
Plan-Implement-Validate work in Project Koios. Its useful behaviors should be
split into explicit meta-harness phases that can be represented as colored
Petri-net transitions:

1. `interview/explore`
2. `plan/spec`
3. `implementation`
4. `validation`
5. `routing/completion`

The first new slice is an interactive interview phase that runs before Athena
authors an architecture specification. The interview phase is not Athena
specification work. It is a bounded artifact-producing transition that gathers
user intent, repo context, scope boundaries, risks, and open questions until
the request is clear enough for Athena to consume.

### Design Intent

The user-facing flow should become:

```text
user-request
  -> Hermes classifies and starts interview when intent is underspecified
  -> Interview loop produces interview-summary and athena-input-packet
  -> Hermes routes athena-input-packet to Athena
  -> Athena handoff-spec produces architecture-spec, acceptance-criteria, and implementation-brief
  -> Hermes routes implementation-brief to Vulcan
  -> Vulcan implements and validates
  -> Hermes reviews reports and routes completion, revision, or knowledge capture
```

This keeps `archon-piv-loop` from acting as one opaque workflow that owns
exploration, planning, implementation, validation, push, and PR creation in a
single run. The workflow may still inspire prompts and interaction patterns,
but the Project Koios meta-harness should expose each phase as a separately
inspectable transition with typed input and output artifacts.

### Places

Add or document these logical places in the Petri-net model. The first
implementation may represent them through handoff files and evaluator
classification rather than a general Petri-net engine.

| Place | Purpose |
|---|---|
| `user_request_inbox` | Raw user request or Hermes-created request token. |
| `interview_ready` | Request needs interactive exploration before spec. |
| `interview_active` | Interview loop is in progress and may ask the user follow-up questions. |
| `interview_packet_ready` | Interview has produced a complete Athena input packet. |
| `athena_inbox` | Athena can consume an `athena-input-packet` through `athena-handoff-spec`. |
| `architecture_spec_ready` | Athena has produced spec artifacts. |
| `vulcan_inbox` | Vulcan can consume an implementation brief. |
| `implementation_report_ready` | Vulcan has produced implementation and validation artifacts. |
| `hermes_completion_review` | Hermes must route completion, revision, or knowledge capture. |
| `revision_needed` | A guard or review found missing information or failed validation. |
| `invalid_or_blocked` | A guard failure prevents the next transition. |

### Colored Tokens

The interview phase must produce typed artifacts, not only chat transcript.
Recommended token kinds:

| Token kind | Owner | Meaning |
|---|---|---|
| `user-request` | user/Hermes | Original request and immediate constraints. |
| `interview-question-set` | interview transition | Focused questions asked of the user. |
| `interview-response` | user | User answers to a question set. |
| `interview-summary` | interview transition | Consolidated understanding of goal, scope, context, and constraints. |
| `resolved-question-set` | interview transition | Questions answered during interview, with decisions captured. |
| `open-question-set` | interview transition | Remaining questions and whether they block Athena. |
| `athena-input-packet` | interview transition/Hermes route | The finalized typed packet Athena may consume. |
| `routing-decision` | Hermes | Decision to route the packet to Athena, Vulcan, Koios, or back to interview. |
| `architecture-spec` | Athena | Bounded architecture decision. |
| `acceptance-criteria` | Athena | Inspectable completion criteria. |
| `implementation-brief` | Athena | Concrete downstream instructions for Vulcan. |
| `implementation-plan` | Vulcan | Planned file-level implementation. |
| `patch` | Vulcan | Repository modification. |
| `test-results` | Vulcan | Validation output. |
| `implementation-report` | Vulcan | Summary of changes and residual risks. |
| `deviation-report` | Vulcan | Mismatch between spec and repo reality. |
| `completion-decision` | Hermes | Final route: complete, revise, or knowledge capture. |

Every token created by workflow automation must preserve the existing
provenance colors: `kind`, `origin`, `sender`, `recipient`, `acting_as`,
`delegated_operator`, `repository`, `status`, and source artifact references.

### Athena Input Packet

The interview loop's primary output is `athena-input-packet`. It is the only
interview artifact Athena must consume directly.

Required packet sections:

- `source-request`: the original user request or explicit reference to it
- `problem-statement`: the user's goal in implementation-neutral terms
- `repo-scope`: confirmation that the work is within `projectkoios-bootstrap`
- `context-read`: files, ADRs, workflows, and docs inspected during interview
- `decisions-made`: user decisions and inferred decisions accepted by the user
- `scope-in`: concrete inclusions
- `scope-out`: concrete exclusions
- `candidate-phases`: expected phase sequence and why each phase is needed
- `artifact-contract`: expected output artifacts from Athena and Vulcan
- `blocking-open-questions`: must be empty before `RouteToAthena` fires
- `nonblocking-open-questions`: items Athena may resolve in the spec
- `risks`: known risks and constraints
- `validation-expectations`: expected static, doc, and workflow validation

The packet should be written as a normal handoff artifact when crossing a
harness boundary. It may also live as an Archon workflow artifact during the
interactive run, but Hermes must route a durable handoff artifact to Athena
before `athena-handoff-spec` consumes it.

### Transitions

The split workflow should expose these transitions:

| Transition | Consumes | Produces | Owner |
|---|---|---|---|
| `ClassifyRequest` | `user-request` | `routing-decision` plus one target token | Hermes |
| `StartInterview` | `user-request`, `routing-decision` | `interview-question-set` | Hermes/interview workflow |
| `CollectInterviewResponse` | `interview-question-set` | `interview-response` | user/interview workflow |
| `UpdateInterviewState` | `interview-response`, prior interview state | `interview-summary`, `resolved-question-set`, optional `open-question-set` | interview workflow |
| `ConvergeInterview` | `interview-summary`, `open-question-set` | `athena-input-packet` | interview workflow |
| `RouteInterviewToAthena` | `athena-input-packet` | `routing-decision` to Athena | Hermes |
| `ProduceAthenaSpec` | `athena-input-packet` | `architecture-spec`, `acceptance-criteria`, `implementation-brief` | Athena |
| `RouteSpecToVulcan` | `implementation-brief` | `routing-decision` to Vulcan | Hermes |
| `ImplementBrief` | `implementation-brief` | `implementation-plan`, `patch`, `test-results`, `implementation-report` | Vulcan |
| `ValidateImplementation` | `patch`, `test-results`, `implementation-report` | validation status or `deviation-report` | Vulcan |
| `CompletionReview` | Vulcan reports | `completion-decision`, `revision-request`, or Koios route | Hermes |

`athena-handoff-spec` composes at `ProduceAthenaSpec`. It should not conduct
the interactive interview itself. It should read an already prepared
`athena-input-packet` and produce the established Athena handoff sections:
`architecture-spec`, `acceptance-criteria`, `implementation-brief`, resolved
questions, non-goals, validation expectations, and routing back to Hermes.

### Guards

Add guard rules to make the new phase explicit and prevent role collapse:

1. `RouteToAthenaRequiresPacket`
   - `RouteInterviewToAthena` is enabled only when an `athena-input-packet`
     exists and `blocking-open-questions` is empty.

2. `InterviewCannotProduceSpec`
   - The interview phase may produce `interview-summary` and
     `athena-input-packet`; it must not produce final `architecture-spec`,
     `acceptance-criteria`, or `implementation-brief`.

3. `AthenaRequiresInterviewForUnderspecifiedWork`
   - If Hermes classifies a request as underspecified or exploratory, Athena
     must receive an `athena-input-packet`, not a raw user request.

4. `HermesMustRouteInterviewOutput`
   - A completed interview packet cannot jump directly to Athena without a
     Hermes `routing-decision`.

5. `NoImplementationBeforeSpec`
   - Vulcan cannot consume `interview-summary`, `athena-input-packet`, or raw
     `user-request` as authority for implementation. Vulcan requires an
     Athena `implementation-brief` unless Hermes explicitly routes a trivial
     non-architecture task under existing policy.

6. `VulcanOwnsImplementation`
   - Only Vulcan may produce `patch`, `test-results`, `implementation-plan`,
     `implementation-report`, or `deviation-report` after an
     `implementation-brief` reaches `vulcan_inbox`.

7. `CompletionReturnsToHermes`
   - Vulcan reports must route to `hermes_completion_review`; Vulcan does not
     self-complete the meta-harness flow.

8. `ProvenanceRequired`
   - Any Codex-mediated artifact must include `Delegated-Operator` provenance
     and must not collapse Codex into `Hermes`, `archon`, `opencode`, or `goose`.

### Workflow Shape

Vulcan should prefer adding a new workflow or a narrowly scoped workflow split
over heavily mutating `archon-piv-loop.yaml` in place. The recommended shape is:

- preserve `archon-piv-loop.yaml` as the existing full PIV workflow unless the
  user later asks to deprecate it
- add an interview-focused workflow, for example
  `archon/workflows/interactive-interview.yaml`, that stops after producing an
  `athena-input-packet`
- update or add documentation that explains how Hermes routes from interview
  output into `archon/workflows/athena-handoff-spec.yaml`
- optionally add a composed workflow only if Archon can express the handoff
  boundary without hiding phase outputs

The interactive loop may reuse the good parts of `archon-piv-loop`'s `explore`
node:

- read `AGENTS.md`
- inspect relevant files and ADRs before asking questions
- ask targeted decision questions instead of generic discovery questions
- iterate until the user explicitly says to proceed
- require an explicit signal before the phase completes

However, its completion signal should mean `INTERVIEW_PACKET_READY`, not
`PLAN_READY`. Planning and specification are Athena's responsibility after the
packet is routed.

## Consequences

This ADR is retained for provenance but has been replaced by the more precise
first-class interview phase decision in
`adr.20260630.171442_first-class-interview-petri-net-phase.md`. Its acceptance
criteria and implementation guidance remain historical context only.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

Vulcan's implementation is complete when:

1. The repo contains an explicit interactive interview workflow or equivalent
   workflow split that ends at an `athena-input-packet` and does not implement
   code, write Athena specs, push branches, or create PRs.
2. The new workflow requires explicit user convergence before producing the
   packet, using a completion signal equivalent to `INTERVIEW_PACKET_READY`.
3. The packet template includes the required sections listed in this spec,
   especially `blocking-open-questions`, `scope-in`, `scope-out`,
   `decisions-made`, and `validation-expectations`.
4. The workflow or documentation states that `blocking-open-questions` must be
   empty before Hermes routes the packet to Athena.
5. `athena-handoff-spec.yaml` remains the Athena composition point: it consumes
   prepared handoff/interview material and produces the final Athena handoff.
6. Documentation explains the phase sequence from interview to Athena to
   Vulcan to Hermes completion review.
7. The Petri-net model documentation or evaluator-facing notes include the new
   token kinds, places, transitions, and guards at the conceptual level.
8. Existing active workflows are not broken or silently repurposed; if
   `archon-piv-loop.yaml` is changed, the old full-PIV behavior remains
   discoverable or is explicitly documented as superseded.
9. No machine-local state, secrets, local Archon run history, or user-specific
   credentials are committed.
10. Vulcan returns an `implementation-report`, `test-results`, and, if reality
    differs from this spec, a `deviation-report`.

## implementation-brief

Vulcan should implement the smallest repo-local workflow/documentation slice
that makes the interview phase explicit.

Recommended tasks:

1. Add a new Archon workflow for interactive interview packet creation.
   - Suggested path: `archon/workflows/interactive-interview.yaml`
   - Provider/model should match local Archon workflow conventions.
   - The workflow must be `interactive: true`.
   - It should loop over user questions and answers until explicit user
     convergence.
   - It should write a packet artifact, preferably
     `$ARTIFACTS_DIR/athena-input-packet.md`.

2. Define the packet template in the workflow prompt.
   - Include all required packet sections from this spec.
   - Make `blocking-open-questions` a hard gate.
   - Make clear that the workflow does not author Athena's final spec.

3. Document composition with Athena.
   - Update a repo-local doc or add a concise doc under `docs/` describing:
     `interactive interview -> Hermes route -> athena-handoff-spec -> Vulcan`.
   - Reference `docs/petri-net-model.md` and `docs/meta-harness.md`.

4. Update Petri-net model notes.
   - Add conceptual token/place/transition/guard entries for the interview
     phase.
   - Keep this documentation-level unless an existing evaluator change is
     clearly necessary and low-risk.

5. Keep code changes out of scope unless the existing test suite or evaluator
   depends on enumerated artifact kinds in code.
   - If code changes are necessary, keep them limited to parser/evaluator
     classification support and tests.
   - Do not build a general Petri-net execution engine.

6. Report back to Hermes.
   - Produce `implementation-report` and `test-results`.
   - Produce `deviation-report` if Vulcan changes workflow shape, file paths,
     or guard details from this brief.

## resolved-open-questions

1. Should the interview happen inside Athena?
   - Resolved: no. The interview phase precedes Athena. Athena consumes the
     resulting `athena-input-packet`.

2. Should the existing `archon-piv-loop` continue to be the primary model?
   - Resolved: no for Project Koios meta-harness routing. It remains useful
     source material, but the desired model splits PIV into explicit phases.

3. What artifact gates Athena?
   - Resolved: `athena-input-packet`, routed by Hermes, with no blocking open
     questions.

4. Who owns completion after Vulcan validates?
   - Resolved: Hermes. Vulcan reports implementation and validation results;
     Hermes decides completion, revision, or knowledge-capture routing.

5. Can Vulcan implement directly from interview output?
   - Resolved: no, except for trivial non-architecture tasks under existing
     Hermes policy. For this flow, Vulcan requires Athena's implementation
     brief.

6. Does this require a full Petri-net engine now?
   - Resolved: no. First implementation should be workflow/documentation plus
     conceptual evaluator alignment.

## non-goals

- Do not replace all Archon workflows.
- Do not remove `archon-piv-loop.yaml` unless separately requested.
- Do not implement product/domain architecture outside `projectkoios-bootstrap`.
- Do not build a general colored Petri-net execution engine.
- Do not let the interview phase produce final Athena spec artifacts.
- Do not let Vulcan implement from a raw user request or interview transcript
  in this flow.
- Do not push branches, create PRs, or modify machine-local Archon state.
- Do not commit secrets, local runtime state, or credentials.

## validation-expectations

Vulcan should run the smallest relevant validation for the actual changes made.
Expected validation set:

- YAML syntax validation for any changed workflow files.
- Markdown lint or formatting check if the repo has an established command for
  docs; otherwise perform a manual Markdown structure check.
- Existing Python/package validation only if code under `src/python/` changes.
- `projectkoios bootstrap handoff evaluate --dry-run` if available and safe in
  the current environment.
- `git diff --check` before reporting.

Validation results must be captured in `test-results`. If a validation command
is unavailable, Vulcan should record the attempted command and why it could not
run.

## routing

After implementation, Vulcan must route results back to Hermes, not directly to
Athena and not directly to Koios.

Required return artifacts:

- `implementation-report` addressed to Hermes
- `test-results` addressed to Hermes
- `deviation-report` addressed to Hermes if the implementation differs from
  this specification or exposes an unresolved architecture question

Hermes then decides one of:

- completion if the acceptance criteria and validation pass
- revision back to Vulcan if implementation or validation is incomplete
- revision back to Athena if the spec is insufficient or contradicted by repo
  reality
- knowledge-capture routing to Koios after completion if durable notes or
  provenance indexes are needed

- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260630.171204: Interactive interview phase for Petri-net PIV routing

## Status

historic

## Context

Origin: archon
Created: 2026-06-30 17:12
From: Athena
To: Vulcan
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap

This specification responds to the user request to break up the existing
`archon-piv-loop` so that an interactive interview/exploration loop can be
modeled inside the Project Koios colored-Petri-net/meta-harness workflow before
Athena specification begins.

Primary source context:

- `archon/workflows/archon-piv-loop.yaml`
- `archon/workflows/athena-handoff-spec.yaml`
- `docs/architecture/adr/adr.20260630.042202_colored-petri-net-meta-harness.md`
- `docs/architecture/adr/adr.20260630.170000_pending-athena-decisions.md`
- `docs/petri-net-model.md`
- `docs/meta-harness.md`
- `AGENTS.md`

This is scoped to `projectkoios-bootstrap`. It does not define product/domain
architecture for the mothership vault.

## Decision

The existing `archon-piv-loop` should not remain the only shape for guided
Plan-Implement-Validate work in Project Koios. Its useful behaviors should be
split into explicit meta-harness phases that can be represented as colored
Petri-net transitions:

1. `interview/explore`
2. `plan/spec`
3. `implementation`
4. `validation`
5. `routing/completion`

The first new slice is an interactive interview phase that runs before Athena
authors an architecture specification. The interview phase is not Athena
specification work. It is a bounded artifact-producing transition that gathers
user intent, repo context, scope boundaries, risks, and open questions until
the request is clear enough for Athena to consume.

### Design Intent

The user-facing flow should become:

```text
user-request
  -> Hermes classifies and starts interview when intent is underspecified
  -> Interview loop produces interview-summary and athena-input-packet
  -> Hermes routes athena-input-packet to Athena
  -> Athena handoff-spec produces architecture-spec, acceptance-criteria, and implementation-brief
  -> Hermes routes implementation-brief to Vulcan
  -> Vulcan implements and validates
  -> Hermes reviews reports and routes completion, revision, or knowledge capture
```

This keeps `archon-piv-loop` from acting as one opaque workflow that owns
exploration, planning, implementation, validation, push, and PR creation in a
single run. The workflow may still inspire prompts and interaction patterns,
but the Project Koios meta-harness should expose each phase as a separately
inspectable transition with typed input and output artifacts.

### Places

Add or document these logical places in the Petri-net model. The first
implementation may represent them through handoff files and evaluator
classification rather than a general Petri-net engine.

| Place | Purpose |
|---|---|
| `user_request_inbox` | Raw user request or Hermes-created request token. |
| `interview_ready` | Request needs interactive exploration before spec. |
| `interview_active` | Interview loop is in progress and may ask the user follow-up questions. |
| `interview_packet_ready` | Interview has produced a complete Athena input packet. |
| `athena_inbox` | Athena can consume an `athena-input-packet` through `athena-handoff-spec`. |
| `architecture_spec_ready` | Athena has produced spec artifacts. |
| `vulcan_inbox` | Vulcan can consume an implementation brief. |
| `implementation_report_ready` | Vulcan has produced implementation and validation artifacts. |
| `hermes_completion_review` | Hermes must route completion, revision, or knowledge capture. |
| `revision_needed` | A guard or review found missing information or failed validation. |
| `invalid_or_blocked` | A guard failure prevents the next transition. |

### Colored Tokens

The interview phase must produce typed artifacts, not only chat transcript.
Recommended token kinds:

| Token kind | Owner | Meaning |
|---|---|---|
| `user-request` | user/Hermes | Original request and immediate constraints. |
| `interview-question-set` | interview transition | Focused questions asked of the user. |
| `interview-response` | user | User answers to a question set. |
| `interview-summary` | interview transition | Consolidated understanding of goal, scope, context, and constraints. |
| `resolved-question-set` | interview transition | Questions answered during interview, with decisions captured. |
| `open-question-set` | interview transition | Remaining questions and whether they block Athena. |
| `athena-input-packet` | interview transition/Hermes route | The finalized typed packet Athena may consume. |
| `routing-decision` | Hermes | Decision to route the packet to Athena, Vulcan, Koios, or back to interview. |
| `architecture-spec` | Athena | Bounded architecture decision. |
| `acceptance-criteria` | Athena | Inspectable completion criteria. |
| `implementation-brief` | Athena | Concrete downstream instructions for Vulcan. |
| `implementation-plan` | Vulcan | Planned file-level implementation. |
| `patch` | Vulcan | Repository modification. |
| `test-results` | Vulcan | Validation output. |
| `implementation-report` | Vulcan | Summary of changes and residual risks. |
| `deviation-report` | Vulcan | Mismatch between spec and repo reality. |
| `completion-decision` | Hermes | Final route: complete, revise, or knowledge capture. |

Every token created by workflow automation must preserve the existing
provenance colors: `kind`, `origin`, `sender`, `recipient`, `acting_as`,
`delegated_operator`, `repository`, `status`, and source artifact references.

### Athena Input Packet

The interview loop's primary output is `athena-input-packet`. It is the only
interview artifact Athena must consume directly.

Required packet sections:

- `source-request`: the original user request or explicit reference to it
- `problem-statement`: the user's goal in implementation-neutral terms
- `repo-scope`: confirmation that the work is within `projectkoios-bootstrap`
- `context-read`: files, ADRs, workflows, and docs inspected during interview
- `decisions-made`: user decisions and inferred decisions accepted by the user
- `scope-in`: concrete inclusions
- `scope-out`: concrete exclusions
- `candidate-phases`: expected phase sequence and why each phase is needed
- `artifact-contract`: expected output artifacts from Athena and Vulcan
- `blocking-open-questions`: must be empty before `RouteToAthena` fires
- `nonblocking-open-questions`: items Athena may resolve in the spec
- `risks`: known risks and constraints
- `validation-expectations`: expected static, doc, and workflow validation

The packet should be written as a normal handoff artifact when crossing a
harness boundary. It may also live as an Archon workflow artifact during the
interactive run, but Hermes must route a durable handoff artifact to Athena
before `athena-handoff-spec` consumes it.

### Transitions

The split workflow should expose these transitions:

| Transition | Consumes | Produces | Owner |
|---|---|---|---|
| `ClassifyRequest` | `user-request` | `routing-decision` plus one target token | Hermes |
| `StartInterview` | `user-request`, `routing-decision` | `interview-question-set` | Hermes/interview workflow |
| `CollectInterviewResponse` | `interview-question-set` | `interview-response` | user/interview workflow |
| `UpdateInterviewState` | `interview-response`, prior interview state | `interview-summary`, `resolved-question-set`, optional `open-question-set` | interview workflow |
| `ConvergeInterview` | `interview-summary`, `open-question-set` | `athena-input-packet` | interview workflow |
| `RouteInterviewToAthena` | `athena-input-packet` | `routing-decision` to Athena | Hermes |
| `ProduceAthenaSpec` | `athena-input-packet` | `architecture-spec`, `acceptance-criteria`, `implementation-brief` | Athena |
| `RouteSpecToVulcan` | `implementation-brief` | `routing-decision` to Vulcan | Hermes |
| `ImplementBrief` | `implementation-brief` | `implementation-plan`, `patch`, `test-results`, `implementation-report` | Vulcan |
| `ValidateImplementation` | `patch`, `test-results`, `implementation-report` | validation status or `deviation-report` | Vulcan |
| `CompletionReview` | Vulcan reports | `completion-decision`, `revision-request`, or Koios route | Hermes |

`athena-handoff-spec` composes at `ProduceAthenaSpec`. It should not conduct
the interactive interview itself. It should read an already prepared
`athena-input-packet` and produce the established Athena handoff sections:
`architecture-spec`, `acceptance-criteria`, `implementation-brief`, resolved
questions, non-goals, validation expectations, and routing back to Hermes.

### Guards

Add guard rules to make the new phase explicit and prevent role collapse:

1. `RouteToAthenaRequiresPacket`
   - `RouteInterviewToAthena` is enabled only when an `athena-input-packet`
     exists and `blocking-open-questions` is empty.

2. `InterviewCannotProduceSpec`
   - The interview phase may produce `interview-summary` and
     `athena-input-packet`; it must not produce final `architecture-spec`,
     `acceptance-criteria`, or `implementation-brief`.

3. `AthenaRequiresInterviewForUnderspecifiedWork`
   - If Hermes classifies a request as underspecified or exploratory, Athena
     must receive an `athena-input-packet`, not a raw user request.

4. `HermesMustRouteInterviewOutput`
   - A completed interview packet cannot jump directly to Athena without a
     Hermes `routing-decision`.

5. `NoImplementationBeforeSpec`
   - Vulcan cannot consume `interview-summary`, `athena-input-packet`, or raw
     `user-request` as authority for implementation. Vulcan requires an
     Athena `implementation-brief` unless Hermes explicitly routes a trivial
     non-architecture task under existing policy.

6. `VulcanOwnsImplementation`
   - Only Vulcan may produce `patch`, `test-results`, `implementation-plan`,
     `implementation-report`, or `deviation-report` after an
     `implementation-brief` reaches `vulcan_inbox`.

7. `CompletionReturnsToHermes`
   - Vulcan reports must route to `hermes_completion_review`; Vulcan does not
     self-complete the meta-harness flow.

8. `ProvenanceRequired`
   - Any Codex-mediated artifact must include `Delegated-Operator` provenance
     and must not collapse Codex into `Hermes`, `archon`, `opencode`, or `goose`.

### Workflow Shape

Vulcan should prefer adding a new workflow or a narrowly scoped workflow split
over heavily mutating `archon-piv-loop.yaml` in place. The recommended shape is:

- preserve `archon-piv-loop.yaml` as the existing full PIV workflow unless the
  user later asks to deprecate it
- add an interview-focused workflow, for example
  `archon/workflows/interactive-interview.yaml`, that stops after producing an
  `athena-input-packet`
- update or add documentation that explains how Hermes routes from interview
  output into `archon/workflows/athena-handoff-spec.yaml`
- optionally add a composed workflow only if Archon can express the handoff
  boundary without hiding phase outputs

The interactive loop may reuse the good parts of `archon-piv-loop`'s `explore`
node:

- read `AGENTS.md`
- inspect relevant files and ADRs before asking questions
- ask targeted decision questions instead of generic discovery questions
- iterate until the user explicitly says to proceed
- require an explicit signal before the phase completes

However, its completion signal should mean `INTERVIEW_PACKET_READY`, not
`PLAN_READY`. Planning and specification are Athena's responsibility after the
packet is routed.

## Consequences

This ADR is retained for provenance but has been replaced by the more precise
first-class interview phase decision in
`adr.20260630.171442_first-class-interview-petri-net-phase.md`. Its acceptance
criteria and implementation guidance remain historical context only.

## Acceptance-Criteria

Vulcan's implementation is complete when:

1. The repo contains an explicit interactive interview workflow or equivalent
   workflow split that ends at an `athena-input-packet` and does not implement
   code, write Athena specs, push branches, or create PRs.
2. The new workflow requires explicit user convergence before producing the
   packet, using a completion signal equivalent to `INTERVIEW_PACKET_READY`.
3. The packet template includes the required sections listed in this spec,
   especially `blocking-open-questions`, `scope-in`, `scope-out`,
   `decisions-made`, and `validation-expectations`.
4. The workflow or documentation states that `blocking-open-questions` must be
   empty before Hermes routes the packet to Athena.
5. `athena-handoff-spec.yaml` remains the Athena composition point: it consumes
   prepared handoff/interview material and produces the final Athena handoff.
6. Documentation explains the phase sequence from interview to Athena to
   Vulcan to Hermes completion review.
7. The Petri-net model documentation or evaluator-facing notes include the new
   token kinds, places, transitions, and guards at the conceptual level.
8. Existing active workflows are not broken or silently repurposed; if
   `archon-piv-loop.yaml` is changed, the old full-PIV behavior remains
   discoverable or is explicitly documented as superseded.
9. No machine-local state, secrets, local Archon run history, or user-specific
   credentials are committed.
10. Vulcan returns an `implementation-report`, `test-results`, and, if reality
    differs from this spec, a `deviation-report`.

## Implementation-Brief

Vulcan should implement the smallest repo-local workflow/documentation slice
that makes the interview phase explicit.

Recommended tasks:

1. Add a new Archon workflow for interactive interview packet creation.
   - Suggested path: `archon/workflows/interactive-interview.yaml`
   - Provider/model should match local Archon workflow conventions.
   - The workflow must be `interactive: true`.
   - It should loop over user questions and answers until explicit user
     convergence.
   - It should write a packet artifact, preferably
     `$ARTIFACTS_DIR/athena-input-packet.md`.

2. Define the packet template in the workflow prompt.
   - Include all required packet sections from this spec.
   - Make `blocking-open-questions` a hard gate.
   - Make clear that the workflow does not author Athena's final spec.

3. Document composition with Athena.
   - Update a repo-local doc or add a concise doc under `docs/` describing:
     `interactive interview -> Hermes route -> athena-handoff-spec -> Vulcan`.
   - Reference `docs/petri-net-model.md` and `docs/meta-harness.md`.

4. Update Petri-net model notes.
   - Add conceptual token/place/transition/guard entries for the interview
     phase.
   - Keep this documentation-level unless an existing evaluator change is
     clearly necessary and low-risk.

5. Keep code changes out of scope unless the existing test suite or evaluator
   depends on enumerated artifact kinds in code.
   - If code changes are necessary, keep them limited to parser/evaluator
     classification support and tests.
   - Do not build a general Petri-net execution engine.

6. Report back to Hermes.
   - Produce `implementation-report` and `test-results`.
   - Produce `deviation-report` if Vulcan changes workflow shape, file paths,
     or guard details from this brief.

## Resolved Open Questions

1. Should the interview happen inside Athena?
   - Resolved: no. The interview phase precedes Athena. Athena consumes the
     resulting `athena-input-packet`.

2. Should the existing `archon-piv-loop` continue to be the primary model?
   - Resolved: no for Project Koios meta-harness routing. It remains useful
     source material, but the desired model splits PIV into explicit phases.

3. What artifact gates Athena?
   - Resolved: `athena-input-packet`, routed by Hermes, with no blocking open
     questions.

4. Who owns completion after Vulcan validates?
   - Resolved: Hermes. Vulcan reports implementation and validation results;
     Hermes decides completion, revision, or knowledge-capture routing.

5. Can Vulcan implement directly from interview output?
   - Resolved: no, except for trivial non-architecture tasks under existing
     Hermes policy. For this flow, Vulcan requires Athena's implementation
     brief.

6. Does this require a full Petri-net engine now?
   - Resolved: no. First implementation should be workflow/documentation plus
     conceptual evaluator alignment.

## Non-Goals

- Do not replace all Archon workflows.
- Do not remove `archon-piv-loop.yaml` unless separately requested.
- Do not implement product/domain architecture outside `projectkoios-bootstrap`.
- Do not build a general colored Petri-net execution engine.
- Do not let the interview phase produce final Athena spec artifacts.
- Do not let Vulcan implement from a raw user request or interview transcript
  in this flow.
- Do not push branches, create PRs, or modify machine-local Archon state.
- Do not commit secrets, local runtime state, or credentials.

## Validation Expectations

Vulcan should run the smallest relevant validation for the actual changes made.
Expected validation set:

- YAML syntax validation for any changed workflow files.
- Markdown lint or formatting check if the repo has an established command for
  docs; otherwise perform a manual Markdown structure check.
- Existing Python/package validation only if code under `src/python/` changes.
- `projectkoios bootstrap handoff evaluate --dry-run` if available and safe in
  the current environment.
- `git diff --check` before reporting.

Validation results must be captured in `test-results`. If a validation command
is unavailable, Vulcan should record the attempted command and why it could not
run.

## Handoff Routing Back To Hermes

After implementation, Vulcan must route results back to Hermes, not directly to
Athena and not directly to Koios.

Required return artifacts:

- `implementation-report` addressed to Hermes
- `test-results` addressed to Hermes
- `deviation-report` addressed to Hermes if the implementation differs from
  this specification or exposes an unresolved architecture question

Hermes then decides one of:

- completion if the acceptance criteria and validation pass
- revision back to Vulcan if implementation or validation is incomplete
- revision back to Athena if the spec is insufficient or contradicted by repo
  reality
- knowledge-capture routing to Koios after completion if durable notes or
  provenance indexes are needed
