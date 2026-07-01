# AAR 20260701.154234: Sandbox Message Delivery Terminology

## Scope

Project Koios bootstrap documentation and active harness instruction surfaces.

## What happened

The user corrected the term "routing" as confusing and directed that the model
be described as sending or putting a message in the recipient's sandbox.

Active docs and harness-facing instructions were updated to use "sandbox
message delivery" in prose. Existing machine-facing identifiers such as
`routing-decision`, `routing-recommendation`, workflow node IDs, and file names
were preserved where renaming them would be a compatibility or behavior change.

## Process issues

The previous wording encouraged agents to treat "routing" as an abstract
authority operation rather than a concrete mailbox/sandbox message delivery
step.

## Proposed follow-up improvements

Consider a later compatibility ADR or migration brief if the project wants to
rename machine-facing identifiers away from `routing-*`.

## Candidate ADR or implementation topics

- Compatibility plan for renaming `routing-decision` and
  `routing-recommendation`.
- Workspace mailbox contract for recipient sandbox inbox/outbox semantics.

## Current status

Active prose has been updated. Historical archives and ADR bodies were not
rewritten during this cleanup pass.
