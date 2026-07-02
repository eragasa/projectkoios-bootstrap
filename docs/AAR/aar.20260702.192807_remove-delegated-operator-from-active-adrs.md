# AAR 20260702.192807: Remove Delegated-Operator from Active ADRs

## Scope

ATHENA session in `projectkoios-bootstrap` normalizing active ADR provenance so `Delegated-Operator` is no longer used in active ADRs or the ADR proposal template.

## What happened

- Removed `Delegated-Operator` from active ADR files under `docs/architecture/adr/`
- Removed `Delegated-Operator` from `docs/templates/ADR.proposal.template.md`
- Left implementation-specific references to `pi` only where the ADR content was explicitly discussing implementation/runtime details

## Process issues

- The provenance block still carried historical harness-mediation language after the repo had moved to a harness-agnostic model
- The active-doc rule needed to be applied consistently across all active ADRs, not just the lifecycle docs

## Proposed follow-up improvements

- Consider a repo-wide pass for other historical harness-mediation language in active surfaces
- Decide whether future active ADR templates should explicitly omit any harness-mediation field entirely

## Candidate ADR or implementation topics

- Provenance-field policy for active ADRs
- Harness-agnostic active ADR rendering rules

## Current status

Active ADRs and the ADR proposal template no longer include `Delegated-Operator`.
