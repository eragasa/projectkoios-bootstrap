```json
{
  "title": "ADR semantic rationalization slice 5 architecture-review brief",
  "artifact_type": "architecture-review-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.154300Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / JSON-authoritative ADR store",
  "slice_name": "adr-semantic-rationalization-six-entry-slice-5",
  "source_slice_4_acceptance": "docs/reviews/hermes-acceptance.20260711.154100_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
  "source_slice_4_evidence": "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-semantic-rationalization-after-slice-4.md",
  "next_owner": "HERMES_USER"
}
```

# Architecture-review brief 20260711.154300: ADR semantic rationalization six-entry slice 5

## Purpose

Perform a bounded ATHENA semantic rationalization review of the six Slice 4 ADR/control-surface entries, aligned to KOIOS semantic review ordering.

The goal is to decide, as review evidence only, whether each selected ADR/control surface still makes sense as current/project authority, needs revision, is superseded or source-only/provenance, is a template/control artifact, should be excluded, or should be deferred for domain review.

This slice is independent of JSON conversion mechanics. It uses Slice 4 dry-run evidence as input because Slice 4 exposed source-to-candidate incompleteness, omitted/source-preserved sections, blockers, and sidecar needs. It must not convert, rewrite, normalize, supersede, or mutate any source.

## Control inputs

Required inputs:

- Slice 4 HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.154100_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- KOIOS semantic rationalization input: `workspaces/koios/working/next-proof-input.20260711_adr-semantic-rationalization-after-slice-4.md`
- Slice 4 evidence: `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`
- Slice 4 implementation report: `docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md`
- Slice 4 ATHENA conformance review: `docs/reviews/architecture-conformance.20260711.153400_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- Slice 4 KOIOS provenance review: `workspaces/koios/working/provenance-review.20260711_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- Current selected source files listed below.

Use existing ADR lifecycle/authority documents as reference evidence where relevant, including but not limited to:

- `docs/adr/adr.json-authoritative-adr-store.draft.md`
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- `docs/adr/adr.adr-lifecycle.draft.md`
- `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`
- `docs/adr/README.md`

If lifecycle/authority references conflict, record the conflict as a rationalization finding; do not resolve it by changing source ADRs.

## Selected rationalization subset

Use exactly the six Slice 4 entries unless HERMES/USER explicitly changes the subset:

```text
docs/adr/README.md
docs/adr/adr.petrinet.20260705.132740Z.md
docs/adr/adr.adr-template-contract.md
docs/adr/adr.json-schemas.draft.md
docs/adr/adr.schema-base.md
docs/adr/adr.adr-lifecycle.draft.md
```

This is the same membership as Slice 4, reordered for semantic review per KOIOS input: directory/control-surface truth first, clear accepted/current decision second, accepted-like template/schema ambiguity third, draft schema namespace fourth, missing-status schema/base concept fifth, and source/provenance lifecycle draft last.

Do not add domain-review or product/future-system ADRs in this slice. Do not expand to all `docs/adr/*.md`.

## Required output artifact

Produce one ATHENA review artifact, preferred path:

```text
docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md
```

Alternative ATHENA-owned intake/review path, if HERMES prefers plan-surface naming:

```text
docs/plans/semantic-rationalization-intake.20260711_adr-six-entry-slice-5.md
```

The review artifact must include:

- JSON frontmatter with `artifact_type: architecture-review`, `scope: adr-semantic-rationalization-six-entry-slice-5`, and `status` such as `semantic-rationalization-review-only`.
- Exact selected subset list.
- Per-entry semantic classification table.
- Per-entry rationale and cited evidence.
- Cross-entry findings and contradictions.
- Recommended next actions, if any, as proposals only.
- Explicit non-authority/non-mutation statement.

## Semantic classification vocabulary

Use these labels unless a narrower label is clearly necessary:

- `current_coherent_authority_candidate` — source appears semantically coherent as current/project authority, pending normal approval gates.
- `current_but_needs_revision` — still relevant, but should be revised before being treated as clean current authority.
- `superseded_or_obsolete_candidate` — appears overtaken by later accepted decisions or implementation reality, but not formally superseded by this review.
- `source_only_provenance` — useful as historical/provenance/source evidence but should not become current authority without a separate promotion/revision.
- `template_or_schema_contract` — template/schema/control contract rather than ordinary project decision authority.
- `index_or_control_surface_exclude` — control/index artifact, not an ADR record.
- `defer_domain_review` — semantic authority depends on another domain/owner or product/future-system decision.
- `insufficient_evidence` — cannot classify safely from current artifacts.

A source may receive a primary classification plus secondary flags, for example:

```text
primary: template_or_schema_contract
flags: [current_but_needs_revision, source_to_candidate_incomplete]
```

## Per-entry review requirements

For each selected entry, record:

- source path;
- observed status/casing or explicit absence;
- Slice 4 final outcome;
- omitted/source-preserved sections summary from Slice 4;
- semantic classification;
- rationale grounded in source text and repository control inputs;
- whether it appears to be current/project authority, candidate authority, source-only/provenance, template/control, excluded, or deferred;
- conflicts with accepted ADR lifecycle/authority documents or current architecture, if any;
- recommended follow-up: no action, revise, promote through ADR lifecycle, exclude from JSON authority migration, consolidate, or defer.

Required specific watchpoints:

1. `docs/adr/README.md` — review first as the directory-level control surface and semantic yardstick; classify as index/control surface, not ADR decision authority, unless the review finds a separate control-surface role to preserve.
2. `docs/adr/adr.petrinet.20260705.132740Z.md` — accepted status must not automatically imply JSON-authority readiness; evaluate whether its Petri-net authority still matches current workflow-engine work without broadening it into product/runtime authority.
3. `docs/adr/adr.adr-template-contract.md` — determine whether it is a current template/schema contract, stale template proposal, or revision candidate; preserve Slice 3/4 status-casing and template-contract ambiguity as evidence.
4. `docs/adr/adr.json-schemas.draft.md` — determine whether the schema-adjacent draft is still current enough to guide ADR JSON authority work or needs revision after `routing` removal and later JSON-authority direction; do not treat clean conversion candidacy as semantic authority.
5. `docs/adr/adr.schema-base.md` — missing top-level ADR status must not be invented; evaluate whether it is source-only/schema-base material, obsolete, or needs explicit lifecycle repair.
6. `docs/adr/adr.adr-lifecycle.draft.md` — evaluate last as source/provenance draft without promoting, superseding, or demoting current lifecycle authority; compare against accepted lifecycle/naming consolidation authority.

## Review method

1. Read the six selected source files and only the lifecycle/authority references needed to classify them.
2. Compare each selected entry against Slice 4 evidence, especially omitted/source-preserved sections and `source_to_candidate_complete: false`.
3. Identify whether each source still has coherent current/project authority, is template/control/source-only, or needs revision/defer/exclusion.
4. Record findings as review evidence only.
5. Do not edit source ADRs, schema files, generated evidence, or code.

## Non-authorizations

This slice does not authorize:

- source Markdown mutation;
- status changes or status normalization;
- formal supersession, acceptance, rejection, promotion, or demotion of any ADR;
- file moves, renames, deletes, archives, or draft supersession;
- schema changes;
- JSON conversion or projection generation;
- authoritative JSON ADR records;
- database/storage authority;
- bulk/corpus migration;
- authority cutover;
- treating `dev/` evidence as durable authority.

The review may recommend future actions, but those recommendations are proposal input only and require HERMES/USER approval before execution.

## Acceptance criteria for this review slice

HERMES/USER may accept the review only if:

1. It covers exactly the selected six entries or explicitly records any HERMES/USER-approved subset change.
2. It classifies every selected entry using the semantic vocabulary or a justified refinement.
3. It distinguishes semantic authority from JSON conversion readiness.
4. It preserves Slice 4 evidence boundaries: source-to-candidate incomplete, candidate-only, no authority cutover.
5. It does not mutate `docs/adr/`, `docs/schemas/`, `dev/`, or implementation code.
6. It does not silently change ADR lifecycle status, supersede drafts, or promote source-only material.
7. It records recommended follow-ups as proposals only.

## Validation / closeout

Because this is a document-domain review slice with no implementation changes expected, validation should include:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

If the review accidentally requires code, schema, source ADR, or evidence mutation, stop and return to HERMES/USER for a new slice.

## Pause gate

After this revised brief is drafted, pause for HERMES/USER approval before performing the actual semantic rationalization review.
