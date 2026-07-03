# AAR 20260704.000647: Koios agent policy identity cleanup

## Scope

Root `AGENTS.md` and Koios workspace `AGENTS.md` in `projectkoios-bootstrap`.

## What happened

The session corrected Koios workspace identity guidance and renamed the Koios workspace control file from `AGENT.md` to `AGENTS.md`.

The session rewrote root `AGENTS.md` toward RFC-style normative language.

The session removed Hermes-centered identity and authority language from root policy.

The session clarified that `projectkoios` is a knowledge-management and content-generation platform for scientific workflows.

The session clarified that `projectkoios-bootstrap` is the meta-harness repository used to build and maintain the harness for `projectkoios`.

The session added an extraction boundary for reusable bootstrap code that may move to `projectkoios` sub-repositories.

## Process issues

The assistant initially misidentified as Hermes while operating from the Koios workspace.

The root policy contained identity guidance that made runtime authority too easy to confuse with represented role identity.

The Koios workspace used `AGENT.md` while root policy expected workspace `AGENTS.md` files.

## Proposed follow-up improvements

Review other workspace policy files for the same RFC-style and one-sentence-per-line convention.

Review root `AGENTS.md` for further reduction after agents use the revised policy in practice.

Consider moving detailed ADR and AAR conventions into dedicated docs if root policy remains too long.

## Candidate ADR or implementation topics

A future workflow policy update may define the boundary between bootstrap extraction candidates and product-facing `projectkoios` sub-repositories.

A future implementation task may validate that all workspace policy files use `AGENTS.md` consistently.

## Current status

Root `AGENTS.md` has been rewritten but not validated beyond targeted text inspection.

Koios workspace policy now lives at `workspaces/koios/AGENTS.md`.
