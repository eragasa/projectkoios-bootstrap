# AAR 20260701.132048: ADR metadata block

## Scope

Normalized the ADR proposal template metadata into a top block.

## What happened

Updated `docs/templates/ADR.proposal.template.md` so `## Status` and `## Context` live inside a top `---` block, then aligned the governing ADR, active architecture note, and `create-adr` workflow prompt to the same structure.

## Process issues

No durable process issue observed.

## Proposed follow-up improvements

- Consider whether other ADR variants should use the same metadata block format.

## Candidate ADR or implementation topics

- ADR format normalization across archived ADRs.

## Current status

The canonical ADR template now uses a top metadata block for status/context.
