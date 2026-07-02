# Idea: AAR Extraction to Vault

## Brainstorm

Treat repo AARs as raw process records and extract the durable lessons into the vault.

## Goal

Preserve only the long-term useful parts of AARs:
- recurring friction
- workflow mistakes
- boundary confusion
- candidate ADRs
- process improvements

## Current thinking

AARs are valuable as session memory, but not as the final storage form.
The repo keeps the operational record; the vault keeps the distilled knowledge.

## Spike requirements

- Should vault notes be one per AAR or one per theme?
- Should extracted lessons be tagged by role, workflow, or repo area?
- Should the vault note include a source link back to the AAR?

## Ideas considered

- Vault each AAR verbatim
- Vault only distilled lessons
- Vault recurring themes across multiple AARs
- Keep AARs repo-local and export summaries to the vault

## Objections / risks

- Vault clutter from raw session noise
- Duplicate notes if each AAR becomes a vault entry
- Losing operational provenance if summaries get too thin

## Open questions

- Should vault notes be one per AAR or one per theme?
- Should extracted lessons be tagged by role, workflow, or repo area?
- Should the vault note include a source link back to the AAR?
- Should repeated AAR themes trigger an ADR or a workflow update?

## Preferred direction

Use AARs as source material, but vault only the distilled lessons and recurring patterns.

## Anything to keep out

- raw session noise
- operational commands
- one-off debugging chatter
- implementation details that do not generalize

## Promotion target

Vault extraction workflow or ADR candidate
