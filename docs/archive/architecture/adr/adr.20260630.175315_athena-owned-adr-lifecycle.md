# ADR 20260630.175315: Athena-owned ADR lifecycle

## Status

historic

## Context

Origin: user Athena revision request informed by promotion review
From: Codex
Acting-As: Athena
Scope: projectkoios-bootstrap ADR lifecycle and harness routing
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Athena promotion review run `91101d553c5ed959eae0a7735d58cf3e`
recommended `needs_athena_revision` because the deterministic JSON contract
requires each lifecycle phase object to include `entry_criteria` and
`exit_criteria`, but the prior draft did not define canonical values for those
fields.

The human architect selected Option 1 from the architecture interview:
Criteria Catalog In Lifecycle Schema. This revision updates the existing Draft
ADR instead of creating a new ADR. Codex is only the delegated operator
materializing the Athena artifact. Codex is not Hermes, Athena, Archon, Vulcan,
or Hermes, and this Draft status must be preserved unless an explicit workflow
grants authority to change it.

The current repository already distinguishes durable ADR file status from
meta-harness operational work. That distinction must remain explicit:

- status is the archival state recorded in the ADR file
- phase is the operational routing state used by Hermes, Athena, and Vulcan

`adr.20260630.170000_pending-athena-decisions.md` is Accepted and resolved the
pending Athena decisions known at that time, including command-shape guidance
for the handoff topics projection. It does not grant blanket future authority to
change lifecycle semantics without Athena. Future lifecycle changes remain
architecture decisions and must be routed through a new or superseding Athena
ADR unless an accepted ADR explicitly delegates a narrower mechanical change.

Project Koios needs the ADR lifecycle to separate these concerns:

- human-readable architecture decisions authored by Athena
- operational workflow phases coordinated by Hermes
- implementation and implementation review performed by Vulcan
- deterministic machine-readable lifecycle data consumed by CLI tooling and tests
- no-implementation decisions that still need validation and completion records

## Decision

### architecture-spec

ADRs keep the existing file status set:

| Status | Meaning |
|---|---|
| `Draft` | The decision is not yet authoritative. |
| `Accepted` | Athena has made the decision authoritative. |
| `Completed` | Hermes has validated that required implementation is complete, or recorded that no implementation was required. |
| `Superseded` | Athena has replaced the decision with a newer ADR. |
| `Rejected` | Athena has declined the proposal. |

Lifecycle tooling may normalize status values to lowercase identifiers in JSON,
but Markdown status text remains the human-facing ADR status.

ADRs also use operational lifecycle phases. Phases are persistent,
ObjectClass-like lifecycle objects: they have stable identifiers, owner
metadata, status mappings, required sections, criteria references, and allowed
next phases. They are not transition commands or execution events.

Criteria are Policy-like catalog entries. A phase's `entry_criteria` and
`exit_criteria` are ordered policy references resolved to criteria objects with
stable IDs and human descriptions. Criteria define inspectable conditions; they
do not execute work, mutate ADR files, persist traces, or advance lifecycle
state.

Future transition actions, execution records, trace persistence, workflow
runner behavior, ADR mutation commands, Petri-net behavior, database storage,
and vault integration are separate architecture surfaces. They are explicitly
deferred and must not be introduced in this implementation slice.

### Lifecycle Phases

Every phase has a canonical `allowed_next` set; no implementation may invent
extra transitions.

| Phase | Status | Owner | Purpose | Required sections | allowed_next |
|---|---|---|---|---|---|
| `intake` | `Draft` | Hermes | Capture request, provenance, scope, and decide whether an ADR is needed. | `context` | `proposed`, `rejected` |
| `proposed` | `Draft` | Athena | Produce architecture spec, criteria, non-goals, open-question resolution, and implementation brief or no-implementation statement. | `architecture-spec`, `acceptance-criteria`, `implementation-brief`, `resolved-open-questions`, `non-goals`, `validation-expectations`, `routing` | `review`, `rejected`, `superseded` |
| `review` | `Draft` | Hermes | Review scope, provenance, completeness, and routing before acceptance. | all `proposed` sections | `proposed`, `accepted`, `rejected` |
| `accepted` | `Accepted` | Athena | Mark the decision as authoritative architecture. | all `proposed` sections | `implementation_ready`, `validated`, `superseded` |
| `implementation_ready` | `Accepted` | Hermes | Route implementation-bearing ADRs to Vulcan with criteria and validation expectations. | all `proposed` sections | `implementing`, `validated` |
| `implementing` | `Accepted` | Vulcan | Apply the accepted implementation brief. | all `proposed` sections | `implementation_review`, `superseded` |
| `implementation_review` | `Accepted` | Vulcan | Review Vulcan's own implementation output, tests, and deviations before returning evidence to Hermes. | `implementation-report`, `test-results`, `implementation-review-result` or `deviation-report` | `implementing`, `validated`, `superseded` |
| `validated` | `Accepted` | Hermes | Compare Vulcan evidence, or no-implementation evidence, against acceptance criteria. | `validation-evidence` | `completed`, `implementing`, `proposed`, `superseded` |
| `completed` | `Completed` | Hermes | Record that validation is complete and no further action is required for this ADR. | `completion-record` | `superseded` |
| `superseded` | `Superseded` | Athena | Record replacement by a later ADR. | `superseded-by` | none |
| `rejected` | `Rejected` | Athena | Record that the proposal should not proceed. | `rejection-rationale` | none |

### Criteria Catalog

The deterministic lifecycle schema includes this canonical criteria catalog.
The IDs and descriptions are stable contract values for `schema_version` 1.
Ordering inside this catalog is deterministic, but phase-level
`entry_criteria` and `exit_criteria` order is defined by each phase below.

| ID | Description |
|---|---|
| `entry.lifecycle.request_scoped` | A user request or harness handoff identifies the ADR scope and repository boundary. |
| `entry.lifecycle.provenance_recorded` | The ADR context records relevant provenance fields such as Origin, From, Acting-As, Scope, Repository, and Delegated-Operator when they affect interpretation. |
| `entry.proposed.intake_complete` | Hermes has enough request, provenance, and scope context to route the item to Athena for a proposed architecture decision. |
| `entry.review.proposal_complete` | The Draft ADR contains the proposed machine-relevant sections required for Hermes review. |
| `entry.accepted.review_passed` | Hermes review found the Draft ADR complete enough for Athena acceptance. |
| `entry.implementation_ready.accepted_decision` | The ADR status is Accepted and the decision is authoritative for downstream routing. |
| `entry.implementing.routing_received` | Vulcan has received an Accepted implementation-bearing ADR with acceptance criteria and validation expectations. |
| `entry.implementation_review.implementation_reported` | Vulcan has produced implementation output, test results, and either a review result or a deviation report. |
| `entry.validated.evidence_available` | Hermes has implementation evidence or no-implementation evidence to compare against the ADR criteria. |
| `entry.completed.validation_passed` | Hermes validation has passed and no required lifecycle work remains for the ADR. |
| `entry.superseded.replacement_identified` | Athena has identified a replacement ADR that supersedes this ADR. |
| `entry.rejected.rationale_available` | Athena has enough rationale to reject the proposal. |
| `exit.intake.scope_decided` | Hermes has decided whether the request should proceed to an ADR proposal or be rejected. |
| `exit.proposed.spec_ready` | Athena has produced architecture-spec, acceptance-criteria, implementation-brief, resolved-open-questions, non-goals, validation-expectations, and routing. |
| `exit.review.disposition_recorded` | Hermes has recorded whether the Draft returns to Athena, proceeds to acceptance, or is rejected. |
| `exit.accepted.routing_path_chosen` | Athena or Hermes has identified whether the Accepted ADR is implementation-bearing, no-implementation, or superseded. |
| `exit.implementation_ready.vulcan_or_validation_routed` | Hermes has routed implementation-bearing work to Vulcan or routed an explicit no-implementation ADR to validation. |
| `exit.implementing.output_ready` | Vulcan has completed the implementation attempt or identified that the ADR has been superseded. |
| `exit.implementation_review.evidence_returned` | Vulcan has reviewed its output and returned implementation evidence, a fix loop, or a supersession signal. |
| `exit.validated.validation_disposition_recorded` | Hermes has recorded completion, a route back to Vulcan, a route back to Athena, or supersession. |
| `exit.completed.completion_recorded` | Hermes has recorded the completion record for the ADR lifecycle. |
| `exit.superseded.supersession_recorded` | Athena has recorded the replacement ADR reference. |
| `exit.rejected.rejection_recorded` | Athena has recorded the rejection rationale. |

### Phase Criteria

The JSON contract must resolve these references into ordered criteria objects in
each phase object. Each object must include at least `id` and `description`.
Vulcan must not invent additional criteria or reorder the arrays.

| Phase | entry_criteria IDs, in order | exit_criteria IDs, in order |
|---|---|---|
| `intake` | `entry.lifecycle.request_scoped`, `entry.lifecycle.provenance_recorded` | `exit.intake.scope_decided` |
| `proposed` | `entry.proposed.intake_complete`, `entry.lifecycle.provenance_recorded` | `exit.proposed.spec_ready` |
| `review` | `entry.review.proposal_complete`, `entry.lifecycle.provenance_recorded` | `exit.review.disposition_recorded` |
| `accepted` | `entry.accepted.review_passed` | `exit.accepted.routing_path_chosen` |
| `implementation_ready` | `entry.implementation_ready.accepted_decision` | `exit.implementation_ready.vulcan_or_validation_routed` |
| `implementing` | `entry.implementing.routing_received` | `exit.implementing.output_ready` |
| `implementation_review` | `entry.implementation_review.implementation_reported` | `exit.implementation_review.evidence_returned` |
| `validated` | `entry.validated.evidence_available` | `exit.validated.validation_disposition_recorded` |
| `completed` | `entry.completed.validation_passed` | `exit.completed.completion_recorded` |
| `superseded` | `entry.superseded.replacement_identified` | `exit.superseded.supersession_recorded` |
| `rejected` | `entry.rejected.rationale_available` | `exit.rejected.rejection_recorded` |

### Lifecycle Paths

The implementation-bearing path is:

1. `intake`
2. `proposed`
3. `review`
4. `accepted`
5. `implementation_ready`
6. `implementing`
7. `implementation_review`
8. `validated`
9. `completed`

The no-implementation ADR path is:

1. `intake`
2. `proposed`
3. `review`
4. `accepted`
5. `validated`
6. `completed`

`implementation_ready` may transition directly to `validated` only when Hermes
records that an Accepted ADR is explicitly no-implementation. `accepted` may
also transition directly to `validated` for no-implementation ADRs that do not
need a separate routing phase. In both cases, Hermes must record
no-implementation validation evidence before `completed`.

### implementation_review boundary

`implementation_review` is owned by Vulcan, not Hermes. It is the boundary where
Vulcan checks its own patch, tests, implementation report, and known deviations
against the accepted ADR before asking Hermes to validate completion.

Vulcan may leave `implementation_review` in three ways:

- return to `implementing` when Vulcan finds implementation defects it can fix
- advance to `validated` by handing Hermes an implementation report, test
  results, and implementation-review approval
- advance to `superseded` only when Athena replaces the ADR before validation

Hermes does not perform `implementation_review`. Hermes performs `validated`.
Hermes may reject Vulcan's evidence during validation and route the work back to
`implementing` or to `proposed` when the ADR itself needs Athena revision.

### no-implementation ADRs

An ADR is no-implementation only when its implementation brief explicitly says
no code, config, documentation, workflow, or test change is required.

A no-implementation ADR must still include:

- acceptance criteria that Hermes can inspect
- validation expectations that explain what evidence proves no implementation is
  required
- routing back to Hermes for validation and completion

No-implementation ADRs skip Vulcan phases unless Hermes identifies downstream
work during review or validation. If downstream work is found, Hermes routes the
ADR back to Athena for revision or to Vulcan only after an Accepted ADR contains
an implementation-bearing brief.

### Machine-relevant ADR section conventions

The repository ADR header convention remains mandatory:

- `# ADR YYYYMMDD.HHMMSS: Title`
- `## Status`
- `## Context`
- `## Decision`
- `## Consequences`

When an ADR reaches `proposed`, these machine-relevant sections are required
using exact lowercase, hyphenated headings or subheadings:

- `architecture-spec`
- `acceptance-criteria`
- `implementation-brief`
- `resolved-open-questions`
- `non-goals`
- `validation-expectations`
- `routing`

For normal ADR prose, these may appear as second-level headings after
`Consequences` or as third-level headings under `Decision` when they are part of
the architectural decision. Tooling must treat the exact normalized section IDs
above as canonical, regardless of Markdown heading depth.

Implementation-bearing ADRs must include an actionable `implementation-brief`.
No-implementation ADRs must put the explicit no-implementation statement inside
`implementation-brief`.

When provenance affects interpretation, `Context` must include fields such as:

- `Origin`
- `From`
- `Acting-As`
- `Scope`
- `Repository`
- `Delegated-Operator`

### Deterministic JSON CLI surface

Vulcan should implement one deterministic CLI surface for lifecycle data:

```text
projectkoios adr lifecycle --format json
```

The command should emit only deterministic JSON by default. It must not include
generated timestamps, machine-local paths outside the repository, runtime
process state, credentials, user-specific configuration, database state, trace
state, vault state, or workflow runner state.

The JSON contract is:

- `schema`: `projectkoios.adr_lifecycle`
- `schema_version`: an integer starting at `1`
- `status_values`: status identifiers in deterministic order
- `criteria_catalog`: criteria objects in the order defined by this ADR, each
  with stable `id` and `description`
- `phases`: phase objects in lifecycle order
- each phase object includes `phase`, `status`, `owner`, `purpose`,
  `entry_criteria`, `exit_criteria`, `required_sections`, and `allowed_next`
- `entry_criteria` and `exit_criteria` contain ordered criteria objects resolved
  from `criteria_catalog`, not bare strings
- no generated timestamps by default
- deterministic key ordering at the CLI boundary

The Markdown ADR is the human source of architectural intent. The JSON CLI
surface is the tooling contract and must match this ADR.

### Repository Boundary

`projectkoios-bootstrap` owns this first deterministic ADR lifecycle schema
because the slice concerns bootstrap repository ADR metadata, harness routing,
and the `projectkoios adr lifecycle --format json` CLI surface.

Future workflow/control-plane execution may require a later ADR and may belong
in another Project Koios repository if it introduces runtime orchestration,
durable traces, databases, vault synchronization, or cross-repository execution
semantics. This ADR does not decide that future repository placement.

### Future authority

Lifecycle phases, statuses, ownership, required sections, criteria catalog
entries, per-phase criteria references, transition rules, and the deterministic
JSON shape are architecture decisions. Future changes must be routed to Athena
as a new or superseding ADR.

Hermes may coordinate the request, validate evidence, and mark lifecycle work
completed when criteria pass. Vulcan may implement accepted decisions and report
constraints or deviations. Codex may invoke Archon or relay artifacts as a
delegated operator. None of those actions replaces Athena's authority to make or
revise lifecycle architecture.

## Consequences

The ADR lifecycle has a complete canonical transition graph. Tooling and tests
can reject missing, unordered, or unauthorized transitions.

The JSON contract now has deterministic `entry_criteria` and `exit_criteria`
values for every phase. Vulcan can implement the JSON surface without inventing
criteria IDs, descriptions, ordering, or phase semantics.

The model remains separated:

- phases are persistent lifecycle objects
- criteria are policy catalog entries and ordered per-phase references
- future actions are transition or mutation behavior outside this slice
- future traces are execution evidence outside this slice

The Vulcan-owned `implementation_review` phase prevents implementation output
from being mistaken for Hermes validation.

No-implementation ADRs have a first-class path to completion without artificial
Vulcan work, while still requiring Hermes validation evidence.

Machine-relevant section IDs are normalized enough for deterministic parsing
without replacing the existing human-readable ADR convention.

The CLI target is intentionally narrow: one JSON lifecycle surface that Vulcan
can implement and test without redesigning the broader CLI, workflow runner,
database, vault, or control plane.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

- The ADR remains in `Draft` status until Hermes review and explicit workflow
  authority changes it.
- Every lifecycle phase defines canonical `allowed_next` transitions.
- Every lifecycle phase defines ordered `entry_criteria` and `exit_criteria`
  references.
- Every referenced criterion exists in the canonical criteria catalog.
- Every criterion has a stable ID and human description.
- The deterministic JSON contract requires phase-level `entry_criteria` and
  `exit_criteria` arrays to contain ordered criteria objects resolved from the
  catalog.
- `implementation_review` is explicitly owned by Vulcan and is distinct from
  Hermes validation.
- The ADR defines both implementation-bearing and no-implementation lifecycle
  flows.
- The no-implementation path requires explicit implementation-brief language and
  Hermes validation evidence before completion.
- Future lifecycle authority is reconciled with
  `adr.20260630.170000_pending-athena-decisions.md`: that ADR remains accepted
  for its resolved decisions, but future lifecycle changes require Athena.
- Machine-relevant required section IDs are normalized and documented.
- The intended deterministic JSON CLI surface is named as
  `projectkoios adr lifecycle --format json`.
- Codex delegated-operator provenance remains explicit in `Context`.
- The first implementation slice excludes ActionClass transition definitions,
  ActionInstance execution, Trace persistence, ADR mutation commands, databases,
  Petri-net engines, vault integration, workflow runner behavior, and automatic
  status edits.

## implementation-brief

Do not implement code until Hermes reviews this Draft ADR and routes accepted
work to Vulcan.

If Hermes accepts and routes implementation, Vulcan should:

- add or update a deterministic ADR lifecycle model matching this ADR
- expose `projectkoios adr lifecycle --format json`
- emit `schema`, `schema_version`, `status_values`, `criteria_catalog`, and
  lifecycle-ordered `phases`
- include for every phase `phase`, `status`, `owner`, `purpose`,
  `entry_criteria`, `exit_criteria`, `required_sections`, and `allowed_next`
- emit `entry_criteria` and `exit_criteria` as ordered criteria objects with
  stable `id` and `description`
- ensure every phase-level criteria object matches the catalog entry for the
  same ID
- keep output free of generated timestamps, local machine state, database state,
  trace state, vault state, and workflow runner state by default
- serialize with stable key ordering
- add tests for status values, phase order, status mapping, required sections,
  `allowed_next` transitions, criteria catalog IDs, criteria order,
  descriptions, per-phase criteria references, no-implementation routing, and
  byte-stable JSON
- avoid changing machine-local harness config, secrets, unrelated CLI behavior,
  ADR status mutation behavior, workflow execution behavior, vault behavior, or
  repository control-plane behavior

Vulcan must return an implementation report, test results, and either an
implementation-review approval or a deviation report before Hermes validation.

The implementation-bearing path implies Vulcan work only after acceptance and
Hermes routing. The no-implementation path implies Hermes validation evidence
and completion record without Vulcan phases unless Hermes identifies downstream
work that requires Athena revision or later Vulcan routing.

## resolved-open-questions

- Canonical `allowed_next` transitions are required for every lifecycle phase.
- Canonical `entry_criteria` and `exit_criteria` are required for every
  lifecycle phase.
- The selected criteria design is Criteria Catalog In Lifecycle Schema.
- Criteria are Policy-like catalog entries or per-phase policy references, not
  actions or traces.
- Phases remain persistent ObjectClass-like lifecycle objects.
- `implementation_review` is a Vulcan-owned self-review and evidence boundary,
  not Hermes validation.
- No-implementation ADRs skip Vulcan phases only when the implementation brief
  explicitly says no implementation is required.
- `adr.20260630.170000_pending-athena-decisions.md` remains accepted for the
  decisions it resolved; it does not authorize future lifecycle changes without
  Athena.
- Required machine-relevant section IDs use lowercase hyphenated names.
- The intended deterministic JSON CLI surface is
  `projectkoios adr lifecycle --format json`.
- `projectkoios-bootstrap` owns this first deterministic lifecycle schema.
- Future workflow/control-plane execution requires a later ADR and may belong in
  another Project Koios repository.
- Codex remains a delegated operator and must preserve provenance when relaying
  Athena artifacts.

## non-goals

- This ADR does not implement Python code, CLI commands, tests, or documentation
  changes outside this ADR.
- This ADR does not accept the existing uncommitted lifecycle implementation, if
  any exists.
- This ADR does not define ActionClass transition definitions.
- This ADR does not define ActionInstance execution.
- This ADR does not define Trace persistence or trace storage.
- This ADR does not define ADR mutation commands or automatic status edits.
- This ADR does not introduce a database.
- This ADR does not introduce a Petri-net engine.
- This ADR does not integrate the Obsidian vault or any vault synchronization
  behavior.
- This ADR does not define workflow runner behavior or control-plane execution.
- This ADR does not redesign the whole Project Koios meta-harness.
- This ADR does not alter machine-local harness configuration or secrets.
- This ADR does not define product or domain architecture outside
  projectkoios-bootstrap.

## validation-expectations

Hermes should validate that any Vulcan implementation:

- preserves the ADR filename and header convention
- emits deterministic JSON from `projectkoios adr lifecycle --format json`
- includes all statuses, phases, owners, required sections, and `allowed_next`
  transitions defined in this ADR
- includes `criteria_catalog` with the exact IDs, order, and descriptions
  defined in this ADR
- includes phase-level `entry_criteria` and `exit_criteria` arrays for every
  phase
- emits each phase criterion as an object with stable `id` and `description`
- preserves the exact per-phase criteria order defined in this ADR
- ensures every phase criterion ID resolves to exactly one catalog entry
- ensures every phase criterion description matches the catalog description for
  that ID
- maps every phase to exactly one archival status
- keeps generated timestamps, machine-local state, database state, trace state,
  vault state, and workflow runner state out of default JSON output
- covers implementation-bearing and no-implementation flows in tests
- covers criteria IDs, order, descriptions, catalog resolution, and per-phase
  references in tests
- keeps `implementation_review` separate from Hermes validation
- avoids implementing ActionClass, ActionInstance, Trace persistence, ADR
  mutation commands, database storage, Petri-net behavior, vault integration,
  workflow runner behavior, or automatic status edits in this slice
- preserves Codex delegated-operator provenance in ADR artifacts when Codex is
  the relay

## routing

Hermes reviews this Draft ADR first. If Hermes accepts it, Hermes may route the
implementation brief to Vulcan.

After implementation, Vulcan returns:

- implementation report
- test results
- implementation-review result or deviation report

Hermes then validates the evidence against this ADR. If evidence passes, Hermes
may move the lifecycle work to `validated` and then `completed`. If evidence
fails, Hermes routes the work back to Vulcan for fixes. If the implementation
reveals a mismatch in the ADR itself, Hermes routes the issue back to Athena for
a revised or superseding ADR.

- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260630.175315: Athena-owned ADR lifecycle

## Status

historic

## Context

Origin: user Athena revision request informed by promotion review
From: Codex
Acting-As: Athena
Scope: projectkoios-bootstrap ADR lifecycle and harness routing
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Athena promotion review run `91101d553c5ed959eae0a7735d58cf3e`
recommended `needs_athena_revision` because the deterministic JSON contract
requires each lifecycle phase object to include `entry_criteria` and
`exit_criteria`, but the prior draft did not define canonical values for those
fields.

The human architect selected Option 1 from the architecture interview:
Criteria Catalog In Lifecycle Schema. This revision updates the existing Draft
ADR instead of creating a new ADR. Codex is only the delegated operator
materializing the Athena artifact. Codex is not Hermes, Athena, Archon, Vulcan,
or Hermes, and this Draft status must be preserved unless an explicit workflow
grants authority to change it.

The current repository already distinguishes durable ADR file status from
meta-harness operational work. That distinction must remain explicit:

- status is the archival state recorded in the ADR file
- phase is the operational routing state used by Hermes, Athena, and Vulcan

`adr.20260630.170000_pending-athena-decisions.md` is Accepted and resolved the
pending Athena decisions known at that time, including command-shape guidance
for the handoff topics projection. It does not grant blanket future authority to
change lifecycle semantics without Athena. Future lifecycle changes remain
architecture decisions and must be routed through a new or superseding Athena
ADR unless an accepted ADR explicitly delegates a narrower mechanical change.

Project Koios needs the ADR lifecycle to separate these concerns:

- human-readable architecture decisions authored by Athena
- operational workflow phases coordinated by Hermes
- implementation and implementation review performed by Vulcan
- deterministic machine-readable lifecycle data consumed by CLI tooling and tests
- no-implementation decisions that still need validation and completion records

## Decision

### architecture-spec

ADRs keep the existing file status set:

| Status | Meaning |
|---|---|
| `Draft` | The decision is not yet authoritative. |
| `Accepted` | Athena has made the decision authoritative. |
| `Completed` | Hermes has validated that required implementation is complete, or recorded that no implementation was required. |
| `Superseded` | Athena has replaced the decision with a newer ADR. |
| `Rejected` | Athena has declined the proposal. |

Lifecycle tooling may normalize status values to lowercase identifiers in JSON,
but Markdown status text remains the human-facing ADR status.

ADRs also use operational lifecycle phases. Phases are persistent,
ObjectClass-like lifecycle objects: they have stable identifiers, owner
metadata, status mappings, required sections, criteria references, and allowed
next phases. They are not transition commands or execution events.

Criteria are Policy-like catalog entries. A phase's `entry_criteria` and
`exit_criteria` are ordered policy references resolved to criteria objects with
stable IDs and human descriptions. Criteria define inspectable conditions; they
do not execute work, mutate ADR files, persist traces, or advance lifecycle
state.

Future transition actions, execution records, trace persistence, workflow
runner behavior, ADR mutation commands, Petri-net behavior, database storage,
and vault integration are separate architecture surfaces. They are explicitly
deferred and must not be introduced in this implementation slice.

### Lifecycle Phases

Every phase has a canonical `allowed_next` set; no implementation may invent
extra transitions.

| Phase | Status | Owner | Purpose | Required sections | allowed_next |
|---|---|---|---|---|---|
| `intake` | `Draft` | Hermes | Capture request, provenance, scope, and decide whether an ADR is needed. | `context` | `proposed`, `rejected` |
| `proposed` | `Draft` | Athena | Produce architecture spec, criteria, non-goals, open-question resolution, and implementation brief or no-implementation statement. | `architecture-spec`, `acceptance-criteria`, `implementation-brief`, `resolved-open-questions`, `non-goals`, `validation-expectations`, `routing` | `review`, `rejected`, `superseded` |
| `review` | `Draft` | Hermes | Review scope, provenance, completeness, and routing before acceptance. | all `proposed` sections | `proposed`, `accepted`, `rejected` |
| `accepted` | `Accepted` | Athena | Mark the decision as authoritative architecture. | all `proposed` sections | `implementation_ready`, `validated`, `superseded` |
| `implementation_ready` | `Accepted` | Hermes | Route implementation-bearing ADRs to Vulcan with criteria and validation expectations. | all `proposed` sections | `implementing`, `validated` |
| `implementing` | `Accepted` | Vulcan | Apply the accepted implementation brief. | all `proposed` sections | `implementation_review`, `superseded` |
| `implementation_review` | `Accepted` | Vulcan | Review Vulcan's own implementation output, tests, and deviations before returning evidence to Hermes. | `implementation-report`, `test-results`, `implementation-review-result` or `deviation-report` | `implementing`, `validated`, `superseded` |
| `validated` | `Accepted` | Hermes | Compare Vulcan evidence, or no-implementation evidence, against acceptance criteria. | `validation-evidence` | `completed`, `implementing`, `proposed`, `superseded` |
| `completed` | `Completed` | Hermes | Record that validation is complete and no further action is required for this ADR. | `completion-record` | `superseded` |
| `superseded` | `Superseded` | Athena | Record replacement by a later ADR. | `superseded-by` | none |
| `rejected` | `Rejected` | Athena | Record that the proposal should not proceed. | `rejection-rationale` | none |

### Criteria Catalog

The deterministic lifecycle schema includes this canonical criteria catalog.
The IDs and descriptions are stable contract values for `schema_version` 1.
Ordering inside this catalog is deterministic, but phase-level
`entry_criteria` and `exit_criteria` order is defined by each phase below.

| ID | Description |
|---|---|
| `entry.lifecycle.request_scoped` | A user request or harness handoff identifies the ADR scope and repository boundary. |
| `entry.lifecycle.provenance_recorded` | The ADR context records relevant provenance fields such as Origin, From, Acting-As, Scope, Repository, and Delegated-Operator when they affect interpretation. |
| `entry.proposed.intake_complete` | Hermes has enough request, provenance, and scope context to route the item to Athena for a proposed architecture decision. |
| `entry.review.proposal_complete` | The Draft ADR contains the proposed machine-relevant sections required for Hermes review. |
| `entry.accepted.review_passed` | Hermes review found the Draft ADR complete enough for Athena acceptance. |
| `entry.implementation_ready.accepted_decision` | The ADR status is Accepted and the decision is authoritative for downstream routing. |
| `entry.implementing.routing_received` | Vulcan has received an Accepted implementation-bearing ADR with acceptance criteria and validation expectations. |
| `entry.implementation_review.implementation_reported` | Vulcan has produced implementation output, test results, and either a review result or a deviation report. |
| `entry.validated.evidence_available` | Hermes has implementation evidence or no-implementation evidence to compare against the ADR criteria. |
| `entry.completed.validation_passed` | Hermes validation has passed and no required lifecycle work remains for the ADR. |
| `entry.superseded.replacement_identified` | Athena has identified a replacement ADR that supersedes this ADR. |
| `entry.rejected.rationale_available` | Athena has enough rationale to reject the proposal. |
| `exit.intake.scope_decided` | Hermes has decided whether the request should proceed to an ADR proposal or be rejected. |
| `exit.proposed.spec_ready` | Athena has produced architecture-spec, acceptance-criteria, implementation-brief, resolved-open-questions, non-goals, validation-expectations, and routing. |
| `exit.review.disposition_recorded` | Hermes has recorded whether the Draft returns to Athena, proceeds to acceptance, or is rejected. |
| `exit.accepted.routing_path_chosen` | Athena or Hermes has identified whether the Accepted ADR is implementation-bearing, no-implementation, or superseded. |
| `exit.implementation_ready.vulcan_or_validation_routed` | Hermes has routed implementation-bearing work to Vulcan or routed an explicit no-implementation ADR to validation. |
| `exit.implementing.output_ready` | Vulcan has completed the implementation attempt or identified that the ADR has been superseded. |
| `exit.implementation_review.evidence_returned` | Vulcan has reviewed its output and returned implementation evidence, a fix loop, or a supersession signal. |
| `exit.validated.validation_disposition_recorded` | Hermes has recorded completion, a route back to Vulcan, a route back to Athena, or supersession. |
| `exit.completed.completion_recorded` | Hermes has recorded the completion record for the ADR lifecycle. |
| `exit.superseded.supersession_recorded` | Athena has recorded the replacement ADR reference. |
| `exit.rejected.rejection_recorded` | Athena has recorded the rejection rationale. |

### Phase Criteria

The JSON contract must resolve these references into ordered criteria objects in
each phase object. Each object must include at least `id` and `description`.
Vulcan must not invent additional criteria or reorder the arrays.

| Phase | entry_criteria IDs, in order | exit_criteria IDs, in order |
|---|---|---|
| `intake` | `entry.lifecycle.request_scoped`, `entry.lifecycle.provenance_recorded` | `exit.intake.scope_decided` |
| `proposed` | `entry.proposed.intake_complete`, `entry.lifecycle.provenance_recorded` | `exit.proposed.spec_ready` |
| `review` | `entry.review.proposal_complete`, `entry.lifecycle.provenance_recorded` | `exit.review.disposition_recorded` |
| `accepted` | `entry.accepted.review_passed` | `exit.accepted.routing_path_chosen` |
| `implementation_ready` | `entry.implementation_ready.accepted_decision` | `exit.implementation_ready.vulcan_or_validation_routed` |
| `implementing` | `entry.implementing.routing_received` | `exit.implementing.output_ready` |
| `implementation_review` | `entry.implementation_review.implementation_reported` | `exit.implementation_review.evidence_returned` |
| `validated` | `entry.validated.evidence_available` | `exit.validated.validation_disposition_recorded` |
| `completed` | `entry.completed.validation_passed` | `exit.completed.completion_recorded` |
| `superseded` | `entry.superseded.replacement_identified` | `exit.superseded.supersession_recorded` |
| `rejected` | `entry.rejected.rationale_available` | `exit.rejected.rejection_recorded` |

### Lifecycle Paths

The implementation-bearing path is:

1. `intake`
2. `proposed`
3. `review`
4. `accepted`
5. `implementation_ready`
6. `implementing`
7. `implementation_review`
8. `validated`
9. `completed`

The no-implementation ADR path is:

1. `intake`
2. `proposed`
3. `review`
4. `accepted`
5. `validated`
6. `completed`

`implementation_ready` may transition directly to `validated` only when Hermes
records that an Accepted ADR is explicitly no-implementation. `accepted` may
also transition directly to `validated` for no-implementation ADRs that do not
need a separate routing phase. In both cases, Hermes must record
no-implementation validation evidence before `completed`.

### implementation_review boundary

`implementation_review` is owned by Vulcan, not Hermes. It is the boundary where
Vulcan checks its own patch, tests, implementation report, and known deviations
against the accepted ADR before asking Hermes to validate completion.

Vulcan may leave `implementation_review` in three ways:

- return to `implementing` when Vulcan finds implementation defects it can fix
- advance to `validated` by handing Hermes an implementation report, test
  results, and implementation-review approval
- advance to `superseded` only when Athena replaces the ADR before validation

Hermes does not perform `implementation_review`. Hermes performs `validated`.
Hermes may reject Vulcan's evidence during validation and route the work back to
`implementing` or to `proposed` when the ADR itself needs Athena revision.

### no-implementation ADRs

An ADR is no-implementation only when its implementation brief explicitly says
no code, config, documentation, workflow, or test change is required.

A no-implementation ADR must still include:

- acceptance criteria that Hermes can inspect
- validation expectations that explain what evidence proves no implementation is
  required
- routing back to Hermes for validation and completion

No-implementation ADRs skip Vulcan phases unless Hermes identifies downstream
work during review or validation. If downstream work is found, Hermes routes the
ADR back to Athena for revision or to Vulcan only after an Accepted ADR contains
an implementation-bearing brief.

### Machine-relevant ADR section conventions

The repository ADR header convention remains mandatory:

- `# ADR YYYYMMDD.HHMMSS: Title`
- `## Status`
- `## Context`
- `## Decision`
- `## Consequences`

When an ADR reaches `proposed`, these machine-relevant sections are required
using exact lowercase, hyphenated headings or subheadings:

- `architecture-spec`
- `acceptance-criteria`
- `implementation-brief`
- `resolved-open-questions`
- `non-goals`
- `validation-expectations`
- `routing`

For normal ADR prose, these may appear as second-level headings after
`Consequences` or as third-level headings under `Decision` when they are part of
the architectural decision. Tooling must treat the exact normalized section IDs
above as canonical, regardless of Markdown heading depth.

Implementation-bearing ADRs must include an actionable `implementation-brief`.
No-implementation ADRs must put the explicit no-implementation statement inside
`implementation-brief`.

When provenance affects interpretation, `Context` must include fields such as:

- `Origin`
- `From`
- `Acting-As`
- `Scope`
- `Repository`
- `Delegated-Operator`

### Deterministic JSON CLI surface

Vulcan should implement one deterministic CLI surface for lifecycle data:

```text
projectkoios adr lifecycle --format json
```

The command should emit only deterministic JSON by default. It must not include
generated timestamps, machine-local paths outside the repository, runtime
process state, credentials, user-specific configuration, database state, trace
state, vault state, or workflow runner state.

The JSON contract is:

- `schema`: `projectkoios.adr_lifecycle`
- `schema_version`: an integer starting at `1`
- `status_values`: status identifiers in deterministic order
- `criteria_catalog`: criteria objects in the order defined by this ADR, each
  with stable `id` and `description`
- `phases`: phase objects in lifecycle order
- each phase object includes `phase`, `status`, `owner`, `purpose`,
  `entry_criteria`, `exit_criteria`, `required_sections`, and `allowed_next`
- `entry_criteria` and `exit_criteria` contain ordered criteria objects resolved
  from `criteria_catalog`, not bare strings
- no generated timestamps by default
- deterministic key ordering at the CLI boundary

The Markdown ADR is the human source of architectural intent. The JSON CLI
surface is the tooling contract and must match this ADR.

### Repository Boundary

`projectkoios-bootstrap` owns this first deterministic ADR lifecycle schema
because the slice concerns bootstrap repository ADR metadata, harness routing,
and the `projectkoios adr lifecycle --format json` CLI surface.

Future workflow/control-plane execution may require a later ADR and may belong
in another Project Koios repository if it introduces runtime orchestration,
durable traces, databases, vault synchronization, or cross-repository execution
semantics. This ADR does not decide that future repository placement.

### Future authority

Lifecycle phases, statuses, ownership, required sections, criteria catalog
entries, per-phase criteria references, transition rules, and the deterministic
JSON shape are architecture decisions. Future changes must be routed to Athena
as a new or superseding ADR.

Hermes may coordinate the request, validate evidence, and mark lifecycle work
completed when criteria pass. Vulcan may implement accepted decisions and report
constraints or deviations. Codex may invoke Archon or relay artifacts as a
delegated operator. None of those actions replaces Athena's authority to make or
revise lifecycle architecture.

## Consequences

The ADR lifecycle has a complete canonical transition graph. Tooling and tests
can reject missing, unordered, or unauthorized transitions.

The JSON contract now has deterministic `entry_criteria` and `exit_criteria`
values for every phase. Vulcan can implement the JSON surface without inventing
criteria IDs, descriptions, ordering, or phase semantics.

The model remains separated:

- phases are persistent lifecycle objects
- criteria are policy catalog entries and ordered per-phase references
- future actions are transition or mutation behavior outside this slice
- future traces are execution evidence outside this slice

The Vulcan-owned `implementation_review` phase prevents implementation output
from being mistaken for Hermes validation.

No-implementation ADRs have a first-class path to completion without artificial
Vulcan work, while still requiring Hermes validation evidence.

Machine-relevant section IDs are normalized enough for deterministic parsing
without replacing the existing human-readable ADR convention.

The CLI target is intentionally narrow: one JSON lifecycle surface that Vulcan
can implement and test without redesigning the broader CLI, workflow runner,
database, vault, or control plane.

## acceptance-criteria

- The ADR remains in `Draft` status until Hermes review and explicit workflow
  authority changes it.
- Every lifecycle phase defines canonical `allowed_next` transitions.
- Every lifecycle phase defines ordered `entry_criteria` and `exit_criteria`
  references.
- Every referenced criterion exists in the canonical criteria catalog.
- Every criterion has a stable ID and human description.
- The deterministic JSON contract requires phase-level `entry_criteria` and
  `exit_criteria` arrays to contain ordered criteria objects resolved from the
  catalog.
- `implementation_review` is explicitly owned by Vulcan and is distinct from
  Hermes validation.
- The ADR defines both implementation-bearing and no-implementation lifecycle
  flows.
- The no-implementation path requires explicit implementation-brief language and
  Hermes validation evidence before completion.
- Future lifecycle authority is reconciled with
  `adr.20260630.170000_pending-athena-decisions.md`: that ADR remains accepted
  for its resolved decisions, but future lifecycle changes require Athena.
- Machine-relevant required section IDs are normalized and documented.
- The intended deterministic JSON CLI surface is named as
  `projectkoios adr lifecycle --format json`.
- Codex delegated-operator provenance remains explicit in `Context`.
- The first implementation slice excludes ActionClass transition definitions,
  ActionInstance execution, Trace persistence, ADR mutation commands, databases,
  Petri-net engines, vault integration, workflow runner behavior, and automatic
  status edits.

## implementation-brief

Do not implement code until Hermes reviews this Draft ADR and routes accepted
work to Vulcan.

If Hermes accepts and routes implementation, Vulcan should:

- add or update a deterministic ADR lifecycle model matching this ADR
- expose `projectkoios adr lifecycle --format json`
- emit `schema`, `schema_version`, `status_values`, `criteria_catalog`, and
  lifecycle-ordered `phases`
- include for every phase `phase`, `status`, `owner`, `purpose`,
  `entry_criteria`, `exit_criteria`, `required_sections`, and `allowed_next`
- emit `entry_criteria` and `exit_criteria` as ordered criteria objects with
  stable `id` and `description`
- ensure every phase-level criteria object matches the catalog entry for the
  same ID
- keep output free of generated timestamps, local machine state, database state,
  trace state, vault state, and workflow runner state by default
- serialize with stable key ordering
- add tests for status values, phase order, status mapping, required sections,
  `allowed_next` transitions, criteria catalog IDs, criteria order,
  descriptions, per-phase criteria references, no-implementation routing, and
  byte-stable JSON
- avoid changing machine-local harness config, secrets, unrelated CLI behavior,
  ADR status mutation behavior, workflow execution behavior, vault behavior, or
  repository control-plane behavior

Vulcan must return an implementation report, test results, and either an
implementation-review approval or a deviation report before Hermes validation.

The implementation-bearing path implies Vulcan work only after acceptance and
Hermes routing. The no-implementation path implies Hermes validation evidence
and completion record without Vulcan phases unless Hermes identifies downstream
work that requires Athena revision or later Vulcan routing.

## resolved-open-questions

- Canonical `allowed_next` transitions are required for every lifecycle phase.
- Canonical `entry_criteria` and `exit_criteria` are required for every
  lifecycle phase.
- The selected criteria design is Criteria Catalog In Lifecycle Schema.
- Criteria are Policy-like catalog entries or per-phase policy references, not
  actions or traces.
- Phases remain persistent ObjectClass-like lifecycle objects.
- `implementation_review` is a Vulcan-owned self-review and evidence boundary,
  not Hermes validation.
- No-implementation ADRs skip Vulcan phases only when the implementation brief
  explicitly says no implementation is required.
- `adr.20260630.170000_pending-athena-decisions.md` remains accepted for the
  decisions it resolved; it does not authorize future lifecycle changes without
  Athena.
- Required machine-relevant section IDs use lowercase hyphenated names.
- The intended deterministic JSON CLI surface is
  `projectkoios adr lifecycle --format json`.
- `projectkoios-bootstrap` owns this first deterministic lifecycle schema.
- Future workflow/control-plane execution requires a later ADR and may belong in
  another Project Koios repository.
- Codex remains a delegated operator and must preserve provenance when relaying
  Athena artifacts.

## non-goals

- This ADR does not implement Python code, CLI commands, tests, or documentation
  changes outside this ADR.
- This ADR does not accept the existing uncommitted lifecycle implementation, if
  any exists.
- This ADR does not define ActionClass transition definitions.
- This ADR does not define ActionInstance execution.
- This ADR does not define Trace persistence or trace storage.
- This ADR does not define ADR mutation commands or automatic status edits.
- This ADR does not introduce a database.
- This ADR does not introduce a Petri-net engine.
- This ADR does not integrate the Obsidian vault or any vault synchronization
  behavior.
- This ADR does not define workflow runner behavior or control-plane execution.
- This ADR does not redesign the whole Project Koios meta-harness.
- This ADR does not alter machine-local harness configuration or secrets.
- This ADR does not define product or domain architecture outside
  projectkoios-bootstrap.

## validation-expectations

Hermes should validate that any Vulcan implementation:

- preserves the ADR filename and header convention
- emits deterministic JSON from `projectkoios adr lifecycle --format json`
- includes all statuses, phases, owners, required sections, and `allowed_next`
  transitions defined in this ADR
- includes `criteria_catalog` with the exact IDs, order, and descriptions
  defined in this ADR
- includes phase-level `entry_criteria` and `exit_criteria` arrays for every
  phase
- emits each phase criterion as an object with stable `id` and `description`
- preserves the exact per-phase criteria order defined in this ADR
- ensures every phase criterion ID resolves to exactly one catalog entry
- ensures every phase criterion description matches the catalog description for
  that ID
- maps every phase to exactly one archival status
- keeps generated timestamps, machine-local state, database state, trace state,
  vault state, and workflow runner state out of default JSON output
- covers implementation-bearing and no-implementation flows in tests
- covers criteria IDs, order, descriptions, catalog resolution, and per-phase
  references in tests
- keeps `implementation_review` separate from Hermes validation
- avoids implementing ActionClass, ActionInstance, Trace persistence, ADR
  mutation commands, database storage, Petri-net behavior, vault integration,
  workflow runner behavior, or automatic status edits in this slice
- preserves Codex delegated-operator provenance in ADR artifacts when Codex is
  the relay

## routing

Hermes reviews this Draft ADR first. If Hermes accepts it, Hermes may route the
implementation brief to Vulcan.

After implementation, Vulcan returns:

- implementation report
- test results
- implementation-review result or deviation report

Hermes then validates the evidence against this ADR. If evidence passes, Hermes
may move the lifecycle work to `validated` and then `completed`. If evidence
fails, Hermes routes the work back to Vulcan for fixes. If the implementation
reveals a mismatch in the ADR itself, Hermes routes the issue back to Athena for
a revised or superseding ADR.
