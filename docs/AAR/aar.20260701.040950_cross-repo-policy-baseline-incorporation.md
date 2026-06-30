# AAR 20260701.040950: Cross-Repo Policy Baseline Incorporation

## Scope

Incorporated review baseline documents from the sibling
`projectkoios-workflow` repository into the human-in-the-loop review agent ADR
draft in `projectkoios-bootstrap`.

## What happened

The user clarified that the policy baseline documents live at:

`/Users/eugene/repos/projectkoios-workflow/docs/policies`

Codex inspected the four policy files there:

- `architecture-baseline.md`
- `review-baseline.md`
- `review-template.md`
- `code-baseline.md`

The sibling repo had a Graphify graph, but the new policy documents were not
discoverable through the graph query, so Codex used direct file reads as the
authoritative source.

Codex then ran `athena-handoff-spec` to revise the existing Draft ADR:

`docs/architecture/adr/adr.20260701.034612_human-in-the-loop-review-agent-contract.md`

Archon revised the ADR in place. It also copied the policy files into
`projectkoios-bootstrap/docs/policies/`; Codex initially removed those local
copies and preserved the sibling-repo paths as provenance/source material in the
ADR.

The user later clarified that the provenance had been moved into
`docs/policies/` and that those local documents are the editable policy surface.
Codex restored the policy documents in `docs/policies/`, cleaned the malformed
`code-baseline.md` source into a stable policy document, and updated the ADR to
point at local policy paths.

## Process issues

The policy source moved across repository boundaries during the session. That
made it important to distinguish editable policy provenance from accepted
bootstrap architecture.

`code-baseline.md` contained draft/proposal framing and a stray terminal escape
sequence, so it was treated as lower-confidence source material. The ADR
extracts only stable policy intent from it.

## Proposed follow-up improvements

When asking Archon to use cross-repo source material, explicitly state whether
the source documents should be copied, referenced, summarized, or treated as
the new editable local policy surface.

## Candidate ADR or implementation topics

Potential follow-up: clarify ownership and synchronization rules between
`projectkoios-bootstrap/docs/policies/` and any policy material that remains in
`projectkoios-workflow`.

## Current status

Draft ADR revised in place. Local policy documents restored under
`docs/policies/`. No implementation performed.
