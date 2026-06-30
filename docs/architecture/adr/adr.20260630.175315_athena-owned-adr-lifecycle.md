# ADR 20260630.175315: Athena-owned ADR lifecycle

## Status

Draft

## Context

Origin: user decision request
From: Codex
Acting-As: Athena
Scope: projectkoios-bootstrap ADR lifecycle and harness routing
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

The current working tree contains uncommitted Codex-authored changes that define
an ADR lifecycle in Markdown and Python JSON. Those changes are draft input
only. They are not accepted architecture, because Codex is an access and
operator layer for invoking Archon and relaying artifacts. Codex is not the
architecture decision maker.

Project Koios needs a lifecycle that separates four concerns:

- human-readable architecture decisions authored by Athena
- operational workflow phases coordinated by Hermes
- implementation and review work performed by Vulcan
- deterministic machine-readable lifecycle data consumed by tools

The lifecycle must also preserve the existing distinction between ADR file
status and operational phase. Status is the durable archival state of the ADR
file. Phase is the meta-harness workflow position of the decision and any
downstream implementation work.

## Decision

### architecture-spec

ADRs use the existing file status set:

| Status | Meaning |
|---|---|
| `draft` | The decision is not yet authoritative. |
| `accepted` | Athena has made the decision authoritative. |
| `completed` | Hermes has validated that required implementation is complete, or recorded that no implementation was required. |
| `superseded` | Athena has replaced the decision with a newer ADR. |
| `rejected` | Athena has declined the proposal. |

ADRs also use an operational phase lifecycle:

| Phase | Status | Owner | Meaning |
|---|---|---|---|
| `intake` | `draft` | Hermes | Capture the request, bound scope, and decide whether an ADR is needed. |
| `proposed` | `draft` | Athena | Write the architecture decision, acceptance criteria, and implementation brief. |
| `review` | `draft` | Hermes | Check scope, completeness, provenance, and routing before acceptance. |
| `accepted` | `accepted` | Athena | Mark the decision as authoritative architecture. |
| `implementation_ready` | `accepted` | Hermes | Route the accepted ADR to Vulcan with acceptance criteria and validation expectations. |
| `implementing` | `accepted` | Vulcan | Apply the implementation described by the ADR. |
| `implementation_review` | `accepted` | Vulcan | Review Vulcan's implementation output before Hermes validation. |
| `validated` | `accepted` | Hermes | Compare Vulcan's report and evidence against the ADR acceptance criteria. |
| `completed` | `completed` | Hermes | Record that implementation and validation are done. |
| `superseded` | `superseded` | Athena | Record replacement by a later ADR. |
| `rejected` | `rejected` | Athena | Record that the proposal should not proceed. |

`implementation_review` is required for ADRs that route work to Vulcan. It may
be brief, but it must be explicit. Hermes validates acceptance criteria only
after Vulcan has either approved its implementation output, reported requested
fixes, or filed a deviation report.

ADRs that require no implementation may move from `accepted` to `completed`
through Hermes review without entering the Vulcan phases, but the ADR must say
that no implementation is required.

### Human-readable ADR content

Every ADR must keep the repository header convention:

- `# ADR YYYYMMDD.HHMMSS: Title`
- `## Status`
- `## Context`
- `## Decision`
- `## Consequences`

Any ADR that reaches `proposed` must also include:

- `architecture-spec`
- `acceptance-criteria`
- `implementation-brief`, or an explicit statement that no implementation is required
- `non-goals`
- `resolved open questions`
- `validation expectations`
- routing instructions for the next owner

When provenance affects interpretation, the context must include fields such as
`Origin`, `From`, `Acting-As`, `Scope`, `Repository`, and
`Delegated-Operator`.

### Deterministic JSON representation

The lifecycle must have one deterministic JSON representation suitable for CLI
output and tests. The JSON must:

- use a stable schema name such as `projectkoios.adr_lifecycle`
- include a lifecycle schema version
- include `status_values` in deterministic order
- include `phases` in lifecycle order
- include, for each phase, `phase`, `status`, `owner`, `purpose`,
  `entry_criteria`, `exit_criteria`, `required_sections`, and `allowed_next`
- omit generated timestamps and local machine state
- serialize with deterministic key ordering at the CLI boundary

The Markdown ADR is the human source of architectural intent. The JSON is the
tooling contract that must match that intent.

### Codex operator boundary

Codex may:

- invoke Archon workflows when direct pi ownership is unavailable
- relay Athena artifacts into this repository
- materialize an Athena-authored ADR artifact when explicitly acting as the
  delegated operator
- report filesystem, git, validation, and workflow state to Hermes

Codex may not:

- accept, reject, supersede, or complete ADRs on its own authority
- treat Codex-authored draft code or Markdown as accepted architecture
- bypass Athena for lifecycle policy changes
- bypass Hermes validation after Vulcan implementation
- present itself as pi, Hermes, Archon, Athena, or Vulcan when it is only
  mediating access

When Codex writes an ADR while acting for Athena, the ADR must preserve
delegated-operator provenance so later readers can distinguish the architecture
role from the access layer.

### Future lifecycle changes

Future changes to ADR lifecycle phases, statuses, ownership, required sections,
or deterministic JSON shape must be routed to Athena as a new or superseding
ADR. Hermes may identify the need and coordinate the request. Vulcan may report
implementation constraints or deviations. Codex may relay the request or invoke
Archon. None of those actions replaces Athena's architecture decision.

## Consequences

The lifecycle has a mandatory implementation review boundary before Hermes
validation, which prevents "implemented" from being treated as "validated."

Statuses remain compact archival file states. Phases become the inspectable
workflow state used for routing, ownership, and gates.

The existing uncommitted lifecycle changes can be evaluated against this ADR,
but they must not be treated as accepted merely because they exist in the
working tree.

## acceptance-criteria

- A lifecycle ADR exists under `docs/architecture/adr/` and is explicitly in
  `Draft` status until reviewed through the meta-harness.
- The lifecycle includes `implementation_review` between `implementing` and
  `validated` for Vulcan-routed work.
- The ADR defines the difference between statuses and phases.
- The ADR defines required human-readable ADR sections for proposed decisions.
- The ADR defines deterministic JSON requirements without timestamps or local
  machine state.
- The ADR defines Codex's delegated-operator permissions and prohibitions.
- The ADR routes future lifecycle changes back to Athena.
- The ADR defines that Hermes validates only after Vulcan reports implementation
  review results.

## implementation-brief

Do not implement code from this ADR until Hermes reviews and accepts routing.

When routed to Vulcan, compare the existing uncommitted lifecycle Markdown,
Python model, CLI command, and tests against this ADR. Keep changes scoped to:

- the lifecycle data model
- the deterministic lifecycle JSON command
- tests for phase order, status mapping, required sections, allowed transitions,
  and deterministic serialization
- documentation updates that reflect the accepted lifecycle

Vulcan must produce an implementation report, test results, and either an
implementation-review approval or a deviation report before returning the work
to Hermes.

## resolved open questions

- Vulcan/opencode must have an explicit `implementation_review` phase before
  Hermes validation for implementation-bearing ADRs.
- ADR status and ADR phase are separate. Status is archival file state; phase is
  workflow state.
- Deterministic JSON is required for tooling and must not include generated
  timestamps by default.
- Codex is only a delegated operator/access layer when invoking Archon or
  relaying Athena artifacts.
- Lifecycle changes are architecture changes and must be routed to Athena.

## non-goals

- This ADR does not implement the lifecycle in Python.
- This ADR does not accept the existing uncommitted Codex-authored lifecycle
  changes.
- This ADR does not redesign the whole meta-harness.
- This ADR does not change machine-local harness configuration.
- This ADR does not define product or domain architecture outside
  projectkoios-bootstrap.

## validation expectations

Hermes should validate that any implementation:

- preserves the ADR filename and header convention
- emits deterministic JSON with stable ordering and no generated timestamp
- maps every lifecycle phase to exactly one archival status
- includes the required `implementation_review` phase for Vulcan-routed work
- prevents Codex-authored draft artifacts from being interpreted as accepted
  architecture without Athena acceptance
- includes tests covering lifecycle order, allowed transitions, and JSON
  stability

## routing back to Hermes after Vulcan reports

After Vulcan implements and reviews the lifecycle changes, Vulcan returns an
implementation report, test results, and implementation-review result to
Hermes. Hermes then checks the evidence against this ADR's acceptance criteria.
If the evidence passes, Hermes may mark the lifecycle work `validated` and then
`completed`. If evidence fails or scope diverges, Hermes routes the work back to
Vulcan for fixes or to Athena for a revised decision.
