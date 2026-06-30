# AAR 20260701.034204: Human Review Agent ADR Proposal

## Scope

Created a Draft ADR proposal for a human-in-the-loop code review agent contract.

## What happened

The user supplied a review-agent prompt and asked for an ADR proposal based on
it. Codex used Graphify first, inspected ADR lifecycle conventions, checked the
opencode harness guidance, and wrote a bounded Draft ADR under
`docs/architecture/adr/`.

The ADR defines an advisory review contract and preserves the user's key
constraints: no automatic ADR generation, no broad rewrites, evidence-backed
findings, bounded human decision points, fixed severities, and fixed final
recommendations.

## Process issues

No blocking process issue was observed. The main routing risk was avoiding an
implementation task shape; the ADR was kept as a Draft architecture proposal.

## Proposed follow-up improvements

If this ADR is promoted, route it through Hermes/Athena review before Vulcan
implements any reusable prompt, command, or workflow surface.

## Candidate ADR or implementation topics

Possible follow-up implementation topic: a reusable opencode or Archon review
prompt that emits the fixed Markdown review format.

## Current status

Draft ADR created. No implementation performed.
