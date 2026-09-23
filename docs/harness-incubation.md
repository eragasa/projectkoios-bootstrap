# Project Koios Pi harness incubation

## Status

Accepted boundary. See
[`HARNESS-ARCHITECTURE-01`](https://github.com/eragasa/projectkoios/issues/4).

## Purpose

This repository may incubate bounded Project Koios-specific Pi coordination
capabilities until their reuse and ownership are understood. Incubation must
not turn bootstrap into a workflow engine, runtime-state store, or owner of
component behavior.

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

- **Observed:** one bounded instance exists; recurrence is unproven.
- **Candidate:** intent, limitations, and sanitized artifacts are reviewable.
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

Before reusable harness code is promoted, its owner issue must show:

1. two independent bounded uses or one concrete recurring failure;
2. a normalized contract excluding private runtime state;
3. deterministic dry-run and replay behavior;
4. idempotent or explicitly recoverable partial execution;
5. public-record privacy checks;
6. owner routing and stop conditions;
7. synthetic or sanitized fixtures;
8. an awkward or failure-case test; and
9. an explicit retain-or-extract decision.
