# Project Koios Pi harness incubation

## Status

Accepted boundary. See
[`HARNESS-ARCHITECTURE-01`](https://github.com/eragasa/projectkoios/issues/4).

## Purpose

This repository may incubate bounded Project Koios-specific Pi coordination
capabilities and tool candidates extracted from operator-provided source drops
until their reuse and ownership are understood. Incubation must not turn
bootstrap into a workflow engine, runtime-state store, generic tool warehouse,
or owner of component behavior.

## Intake boundary

A raw intake is a local, untracked observation used to discover reusable
mechanics. It may be incomplete, generated, product-specific, or unsuitable for
execution. Its presence does not make bootstrap its owner and does not imply
that missing packaging or companion files are defects. Initial inspection is
static and bounded. Execution, dependency installation, external transmission,
and owner-repository mutation remain separate operations subject to their own
trust and authority checks.

Do not promote or copy a raw intake wholesale. Extract a normalized behavior,
replace source-specific material with sanitized fixtures, and route product
behavior to its component owner. Raw intake paths are ignored by Git and are
not durable records.

## Candidate boundary

A candidate may include bounded source or Pi configuration, sanitized fixtures,
tests, deterministic expected outputs, limitations, and extraction criteria.
Tracked material must be reviewable without credentials, private paths,
protected excerpts, transcripts, generated handoffs, or copied task state.

Do not incubate product implementation, component code with an established
owner, replicated issue or roadmap state, daemons, telemetry, installers,
schema catalogs, operator consoles, generic workflow engines, named-role
systems, or stable generic Pi extensions.

## Lifecycle

A local intake precedes the lifecycle and is not itself a lifecycle status or
artifact.

- **Observed:** one bounded reusable mechanic has been identified; recurrence is
  unproven.
- **Candidate:** intent, limitations, sanitized artifacts, and owner routing are
  reviewable independently of the intake.
- **Repeated:** an independent task exercises substantially the same mechanics.
- **Validated:** deterministic normal and failure/recovery checks pass, with
  privacy, idempotence, authority, and owner routing explicit.
- **Extracted or retained:** generic capabilities move to an accepted owner;
  Project Koios-specific coordination may remain here.

A lifecycle transition grants no authority to commit, push, install, release,
deploy, or publish.

## Evidence and authority

Private or machine-bound observations belong in managed operational state
outside this repository and may be referenced only by safe content identity.
GitHub issues remain authoritative for mutable tasks. Git commits and owning
repository artifacts remain authoritative for implementation.

## Promotion gate

Before reusable harness code is promoted beyond candidate status, its owner
issue must show:

1. two independent bounded uses or one concrete recurring failure;
2. a normalized contract excluding private runtime state;
3. deterministic dry-run and replay behavior;
4. idempotent or explicitly recoverable partial execution;
5. public-record privacy checks;
6. owner routing and stop conditions;
7. synthetic or sanitized fixtures;
8. an awkward or failure-case test; and
9. an explicit retain-or-extract decision.
