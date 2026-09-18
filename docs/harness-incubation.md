# Project Koios Pi harness incubation

## Status

Accepted boundary. See
[`HARNESS-ARCHITECTURE-01`](https://github.com/eragasa/projectkoios/issues/4).

## Purpose

`projectkoios-bootstrap` incubates bounded, Project Koios-specific Pi
coordination capabilities that do not yet have a stable generic extraction
boundary. Incubation preserves enough source, fixtures, tests, and limitations
to compare independent uses without turning bootstrap into a workflow engine or
runtime state store.

## Allowed tracked artifacts

- bounded coordination-helper source;
- Project Koios-specific Pi skills and prompt templates;
- deterministic repository, issue, session, and recovery utilities;
- sanitized fixtures derived from public or synthetic evidence;
- tests and deterministic expected outputs;
- candidate manifests, limitations, and extraction criteria; and
- documentation explaining why the capability belongs in bootstrap.

Tracked fixtures must not contain private machine paths, credentials, signed
URLs, protected source excerpts, session transcripts, or copied owner-task
state.

## Prohibited artifacts

- product or scientific-domain implementation;
- component code with an established owner repository;
- roadmap or task databases and replicated issue state;
- session transcripts, persistent queues, checkpoints, or generated handoffs;
- daemons, telemetry services, generic workflow engines, schema catalogs,
  installers, or operator consoles;
- the historical Hermes/Athena/Vulcan/Koios role system;
- credentials or machine-specific configuration; and
- generic stable Pi extensions better owned by the operator installation or an
  accepted extracted repository.

## Candidate lifecycle

### Observed

One bounded coordination instance exists. Private evidence may be retained in
managed operational state with a content-derived identity. Observation does not
establish recurrence.

### Candidate

The common intent, exact limitations, sanitized source or pseudocode, and
synthetic/public fixtures are reviewable. A candidate is not production tooling
and is not installed automatically.

### Repeated

A second independent Project Koios task exercises substantially the same
coordination sequence. The comparison identifies common mechanics and rejects
task-specific coincidence.

### Validated

Deterministic tests pass for normal execution and at least one partial-failure
or recovery case. Privacy, idempotence, authority, and owner-routing boundaries
are explicit.

### Extracted or retained

Stable generic capabilities move to the operator Pi installation or an
accepted owner repository. Capabilities whose semantics remain specific to
Project Koios multi-repository coordination may remain in bootstrap.

## Operational evidence

Private, generated, machine-bound observations belong under managed `.koios`
state outside this repository. An owner issue may record a content identity,
file count, validation result, and limitations without publishing the private
path or contents.

GitHub issues remain authoritative for mutable tasks. Git commits and owning
repository artifacts remain authoritative for implementation. A harness
candidate must not recreate either authority locally.

## Promotion gate

Before a candidate becomes reusable harness code, its owner issue must show:

1. at least two independent bounded uses, or one concrete recurring failure;
2. a normalized input/output contract that excludes private runtime state;
3. deterministic dry-run and replay behavior;
4. idempotent or explicitly recoverable partial execution;
5. public-record privacy checks;
6. owner-repository routing and stop conditions;
7. synthetic or sanitized fixtures;
8. tests for at least one awkward or failure case; and
9. a decision to retain the capability here or extract it.

No candidate lifecycle transition grants commit, push, installation, release,
or execution authorization.

## First observation

The first observation is the references adversarial-review issue campaign
tracked by:

- https://github.com/eragasa/projectkoios-references/issues/3
- https://github.com/eragasa/projectkoios-bootstrap/issues/2

It generated bounded child issues, created them with resumable local progress,
updated a classified parent, cross-linked owner repositories, and verified
completeness and privacy. The hardcoded one-off helpers are preserved privately
as `OBSERVED_UNVALIDATED` evidence. They are not tracked production source and
do not establish recurrence.
