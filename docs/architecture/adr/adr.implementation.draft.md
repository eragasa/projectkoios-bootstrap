# ADR 20260702.181500Z: Implementation Document Surface

## Status

draft
date: 20260702.181500Z

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

Implementation artifacts need one canonical namespace so execution notes, plans, and brief-adjacent material do not drift into the architecture surface. The repository already has implementation-linked documents; what it lacks is a mothership decision that says where implementation documents live, how they are indexed, and how they relate back to architecture.

## Decision

Adopt `docs/implementation/` as the canonical namespace for implementation documents.

The implementation namespace has three rules:

- implementation documents live under `docs/implementation/`
- `docs/implementation/implementation.00.md` is the namespace index
- each implementation document links back to its controlling ADR, while the controlling ADR links forward to the implementation document when one exists

Implementation documents are execution surfaces, not architecture decisions. Architecture decisions stay under `docs/architecture/adr/`.

## Consequences

- implementation material has one obvious home
- architecture notes no longer need to host implementation blocks inline
- readers can navigate from ADR to implementation doc and back again
- future implementation docs can follow one template and one index

## architecture-spec

The implementation namespace should remain lightweight and reviewable:

- the index note is the primary navigation surface
- implementation docs should be readable on their own
- implementation docs should carry clear provenance and control links
- the implementation surface must not replace the ADR lifecycle

## acceptance-criteria

- implementation documents live under `docs/implementation/`
- `docs/implementation/implementation.00.md` exists as the namespace index
- current implementation docs are reachable from the index
- architecture notes can link to implementation docs without embedding them
- a reviewer can tell whether a document is architecture or implementation by path alone

## implementation-brief

If accepted, create `docs/implementation/implementation.00.md` as the namespace index, update the relevant workspace guidance to point implementation work at `docs/implementation/`, and migrate any implementation blocks currently embedded in architecture notes into implementation documents.

## resolved_open_questions

- Should every implementation document use the same front matter? Yes, once the namespace stabilizes.
- Should the implementation namespace have subfolders by topic? Not yet — keep the first version flat.

## non_goals

- Replacing ADRs as the decision surface
- Defining implementation validation tooling
- Forcing every implementation note to be the same length or shape

## validation_expectations

- A new implementation document can be placed in `docs/implementation/` without ambiguity
- The namespace index lists the known implementation docs
- Architecture notes can point to implementation docs instead of carrying the implementation text themselves

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Documentation-surface control object for implementation material.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
