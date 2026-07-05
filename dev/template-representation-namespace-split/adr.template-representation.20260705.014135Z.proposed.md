```json
{
  "title": "Template Representation and Namespace Split",
  "artifact_type": "adr-proposal",
  "status": "proposed",
  "datetime": "20260705.014135Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "docs/templates/, docs/implementation/; src/python/projectkoios/bootstrap/ as future implementation target only",
  "proposal_surface": "dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.proposed.md",
  "candidate_canonical_location": "docs/adr/adr.20260705.014135_template-representation-namespace-split.md",
  "source_artifacts": [
    "docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md",
    "docs/plans/template-representation-and-implementation-namespace-split.md",
    "docs/templates/templates.00.md",
    "docs/implementation/implementation.00.md",
    "docs/architecture/architecture.templates.md",
    "docs/adr/adr.templates.md",
    "docs/adr/adr.implementation.draft.md"
  ],
  "next_phase": "HERMES/user review for acceptance, revision, or rejection"
}
```

# ADR 20260705.014135Z: Template Representation and Namespace Split

## Status

proposed

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** in this ADR are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Provenance

Origin: Athena portfolio item started after ADR lifecycle/naming consolidation closeout
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap template/document transformation boundary; `src/python/projectkoios/bootstrap/` is a future implementation target only
Repository: projectkoios-bootstrap
Architecture-Domain: workflow/control-surface and implementation-brief boundary
Proposal-Review-Surface: `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.proposed.md`
Candidate-Accepted-Location: `docs/adr/adr.20260705.014135_template-representation-namespace-split.md`

Source artifacts:

- `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`
- `docs/plans/template-representation-and-implementation-namespace-split.md`
- `docs/templates/templates.00.md`
- `docs/implementation/implementation.00.md`
- `docs/architecture/architecture.templates.md`
- `docs/adr/adr.templates.md`
- `docs/adr/adr.implementation.draft.md`

## Context

The repository has a draft ADR and implementation plan for a narrow template/document transformation slice. The slice is useful because current docs distinguish reusable templates from implementation reports, but there is not yet an accepted architecture boundary for the JSON↔Markdown representation contract or for the code namespace that would implement it.

The term `ingestion` is overloaded in this repository. There is existing bootstrap code under `src/python/projectkoios/bootstrap/commands/ingestion.py`, and there are broader Graphify/source-ingestion concepts elsewhere. This ADR intentionally avoids authorizing a general ingestion framework.

The repository currently has `src/python/projectkoios/bootstrap/` and does not have `src/python/ingestion/`. Any implementation brief for this slice MUST target the existing bootstrap package boundary unless a separate accepted architecture decision changes the package layout.

`docs/templates/templates.00.md` and `docs/architecture/architecture.templates.md` identify `docs/adr/adr.templates.md` as their controlling draft. `docs/implementation/implementation.00.md` identifies `docs/adr/adr.implementation.draft.md` as its controlling draft. This proposal uses those predecessor surfaces as source context for namespace meaning; it does not accept those drafts wholesale or change their status.

## Decision

Project Koios bootstrap SHOULD adopt a narrow template representation and namespace split for this repository slice.

The slice MUST define the boundary for reusable template documents as:

- canonical template JSON representation
- Markdown rendering from canonical template representation
- Markdown parsing/import back to canonical template representation
- allowed Markdown presentation variance that does not change semantic meaning
- namespace-aware handling for `docs/templates/`
- namespace-aware handling for `docs/implementation/`

The slice MUST NOT define or authorize:

- a general repository ingestion framework
- Graphify ingestion behavior
- source acquisition or crawling pipelines
- vault, PDF, or evidence ingestion
- a new top-level `projectkoios.ingestion` package
- a new `src/python/ingestion/` tree
- product-domain template semantics for the `~/projectkoios/` mothership repository or any future product repository unless separately accepted there

Acceptance records a bootstrap architecture/control-surface boundary only. It does not implement code, create a general ingestion framework, define product-domain template semantics, or promote the implementation plan beyond the constraints explicitly restated here.

## Source traceability

| Claim | Source artifacts |
|---|---|
| JSON↔Markdown representation contract is the intended narrow slice | `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`; `docs/plans/template-representation-and-implementation-namespace-split.md`; `docs/architecture/architecture.templates.md` |
| Presentation-only Markdown variance may normalize when semantic meaning is preserved | `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`; `docs/plans/template-representation-and-implementation-namespace-split.md` |
| `docs/templates/` is the reusable template namespace | `docs/templates/templates.00.md`; `docs/architecture/architecture.templates.md`; `docs/adr/adr.templates.md` |
| `docs/implementation/` is the implementation-linked records namespace | `docs/implementation/implementation.00.md`; `docs/adr/adr.implementation.draft.md` |
| Existing bootstrap package is the future implementation target | repository source layout under `src/python/projectkoios/bootstrap/`; `docs/plans/template-representation-and-implementation-namespace-split.md` |
| Broad ingestion, Graphify, vault/PDF/evidence ingestion, and product-domain semantics are excluded | `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`; `docs/plans/template-representation-and-implementation-namespace-split.md` |
| Implementation-plan handoff remains conditional and constrained | `docs/plans/template-representation-and-implementation-namespace-split.md`; constraints restated in this ADR |

## Architecture contract

### Representation boundary

Template records SHOULD have a canonical structured representation that can render to Markdown and be reconstructed from Markdown when the Markdown preserves semantic meaning.

A follow-on implementation brief MUST define a minimal canonical template JSON representation before coding. That definition SHOULD include required fields, optional fields, ordering rules, and normalization behavior for the first supported template fixture.

Presentation-only Markdown variance MAY normalize to the same canonical representation. Meaning-changing Markdown differences SHOULD produce a typed parse or equivalence error rather than silent normalization.

### Namespace boundary

`docs/templates/` MUST remain the namespace for reusable template content, instructions, and boilerplate.

`docs/implementation/` MUST remain the namespace for implementation reports, implementation plans, and implementation-linked records.

Template documents MUST NOT be indexed as implementation reports solely because they can be rendered or ingested by code. Implementation reports MUST NOT be treated as reusable templates solely because they are Markdown files.

### Package boundary

Implementation, if authorized separately, SHOULD live under `src/python/projectkoios/bootstrap/` in a package/module name that describes template/document representation rather than broad ingestion.

The first implementation slice SHOULD use `src/python/projectkoios/bootstrap/template_representation/` unless the accepted implementation brief chooses another explicit non-ingestion name under `src/python/projectkoios/bootstrap/`.

Implementation names SHOULD prefer `templates`, `template_records`, `template_representation`, `rendering`, or `markdown` terminology over `ingestion` unless a later ADR resolves ingestion terminology.

Implementation MUST NOT depend on a nonexistent `src/python/ingestion/` tree. If implementers believe a new top-level ingestion package is required, they MUST stop and request architecture reconciliation before coding that package boundary.

## Acceptance criteria

- A reviewer can distinguish the template representation boundary from broader ingestion systems.
- A reviewer can identify `docs/templates/` and `docs/implementation/` as separate namespaces with separate meanings.
- A reviewer can identify the existing bootstrap Python package tree, with `src/python/projectkoios/bootstrap/template_representation/` as the preferred first-slice module target, for any follow-on work.
- A reviewer can identify that the accepted ADR filename should follow `adr.YYYYMMDD.HHMMSS_kebab-slug.md` convention.
- The proposal does not authorize code changes by itself.
- The proposal does not create a general ingestion framework or product-domain template architecture for `projectkoios-bootstrap`, `~/projectkoios/`, or any future product repository.
- The existing implementation plan can be used as a candidate Vulcan handoff only after acceptance or explicit user direction; acceptance does not promote the plan beyond constraints explicitly restated in this ADR.

## Implementation brief

No implementation is authorized by this proposal alone.

If this proposal is accepted and the user requests implementation handoff, Vulcan SHOULD use `docs/plans/template-representation-and-implementation-namespace-split.md` as a candidate starting implementation plan, not as accepted architecture authority beyond the constraints explicitly restated in this ADR:

1. keep the first implementation slice inside `src/python/projectkoios/bootstrap/`
2. define a minimal canonical template JSON representation before coding, including required fields, optional fields, ordering rules, and normalization behavior for the first fixture
3. prove one template can round-trip JSON → Markdown → JSON before expanding coverage
4. add tests for allowed Markdown presentation variance and typed parse/equivalence errors for meaning-changing Markdown differences
5. add namespace classification tests proving template docs are not classified as implementation reports and implementation reports are not classified as reusable templates; path SHOULD be necessary but not sufficient if frontmatter or metadata later exists
6. update `docs/templates/templates.00.md` and `docs/implementation/implementation.00.md` only as needed for namespace clarity and only under explicit documentation/implementation handoff authority
7. avoid changes to Graphify ingestion, source retrieval, vault ingestion, or product-domain code

### Verification method

A follow-on implementation SHOULD be validated with:

- round-trip tests for template JSON and Markdown
- fixture tests for allowed Markdown presentation variance
- typed parse/equivalence-error tests for meaning-changing Markdown differences
- namespace classification tests for `docs/templates/` and `docs/implementation/`
- link/path checks for `docs/templates/templates.00.md` and `docs/implementation/implementation.00.md`
- repository-path inspection confirming no dependency on `src/python/ingestion/` or `projectkoios.ingestion`

## Resolved open questions

- This slice uses the existing bootstrap package tree, not a new top-level ingestion package.
- This slice is about template/document transformation, not Graphify or source ingestion.
- Markdown presentation variance is allowed only when semantic meaning is preserved.

## Non-goals

- General-purpose ingestion architecture
- Repository-wide content crawling
- Vault, PDF, or evidence ingestion
- Replacing or expanding Graphify
- Creating `src/python/ingestion/`
- Creating `projectkoios.ingestion`
- Product-facing template architecture for the `~/projectkoios/` mothership repository or any future product repository
- Code implementation from Athena

## Validation expectations

- The proposal is bounded to a template/document representation contract.
- The implementation target is inspectably compatible with the current repository layout.
- The proposal is suitable for HERMES/user acceptance, revision, rejection, or routing to Vulcan after acceptance.

## Routing

- Owner: ATHENA
- Current phase: proposed
- Next owner: HERMES/user for review decision
- Notes: This is an architecture/control-surface proposal only.

## Links

- `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`
- `docs/plans/template-representation-and-implementation-namespace-split.md`
- `docs/templates/templates.00.md`
- `docs/implementation/implementation.00.md`
- `docs/architecture/architecture.templates.md`
- `docs/adr/adr.templates.md`
- `docs/adr/adr.implementation.draft.md`
