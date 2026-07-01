# AAR 20260701.152548: Agent identity and ADR pause

## Scope

AGENTS.md session instructions for Project Koios bootstrap.

## What happened

The session clarified that harness identity, command authority, and delegated
operation were being conflated. The user established that each agent's apartment
is `./workspace/<identity>/`, that all non-ADR-governance ADRs are paused, and
that paused ADRs may only receive comments until HERMES, with ZEUS permission,
consolidates concerns into a new ADR proposal.

## Process issues

- Existing instructions put HERMES command authority near the top without first
  defining harness identity.
- Delegated operation could be mistaken for artifact voice.
- The active ADR surface had become chaotic because too many ADRs could continue
  moving while the ADR strategy itself was unstable.

## Proposed follow-up improvements

- Keep identity rules before migration and command-authority rules.
- Treat comment headings as role identity, not runtime or command runner.
- Keep paused ADR changes comment-only until the consolidated ADR proposal is
  ready.

## Candidate ADR or implementation topics

- Consolidated ADR strategy proposal for lifecycle, comments, consolidation, and
  archival.
- Workspace apartment contract for `./workspace/<identity>/`.

## Current status

AGENTS.md now includes top-level agent identity, migration, speaking attribution,
and ADR stabilization rules.
