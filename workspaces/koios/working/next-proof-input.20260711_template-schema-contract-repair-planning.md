```json
{
  "title": "KOIOS next proof input: ADR template/schema contract repair planning",
  "artifact_type": "provenance-next-proof-input",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "repair/revision planning for docs/adr/adr.adr-template-contract.md after Slice 5"
}
```

# KOIOS next proof input: ADR template/schema contract repair planning

## Authority boundary

This note is KOIOS provenance input only. It does not authorize source mutation, status normalization, formal supersession/promotion/demotion, schema changes, JSON authority cutover, generated projection replacement, file moves/renames, or migration.

The next slice should help ATHENA/HERMES decide a safe repair/revision path for `docs/adr/adr.adr-template-contract.md` as an accepted-like but semantically mixed/stale template/schema contract.

## Recommended slice shape

Recommended slice name:

```text
adr-template-schema-contract-repair-planning-slice-6
```

Recommended purpose:

- review `docs/adr/adr.adr-template-contract.md` as a template/schema contract and authority-relevant source;
- identify exactly which claims remain current, stale, ahead-of-authority, or ambiguous;
- propose safe repair paths without editing the source or changing lifecycle state;
- decide what later ATHENA/HERMES brief should repair: a replacement ADR, architecture note, schema contract, README/control-surface update, or provenance-only disposition;
- preserve `Accepted` casing and all source/provenance evidence.

## Primary source under review

```text
docs/adr/adr.adr-template-contract.md
```

Observed high-risk source claims to evaluate:

- status heading says `Accepted` with capital `A`;
- `docs/schemas/adr.schema.json` is declared canonical;
- Markdown is declared a render target, not source of truth;
- schema is said to include `routing`;
- architecture spec lists `dcn` and `routing` as canonical schema fields;
- `workflow_binding` is optional;
- routing section says the ADR governs the JSON ADR source-of-truth surface.

## Provenance/control sources to consult

### Direct source and local control

- `docs/adr/adr.adr-template-contract.md` — source under review.
- `docs/adr/README.md` — ADR directory boundary: ADRs vs architecture docs, policies, templates, implementation reports, process-capture.
- `docs/schemas/adr.schema.json` — current schema surface. KOIOS spot-check notes: current schema contains status vocabulary `proposal`, `draft`, `accepted`, `active`, `superseded`; it includes `workflow_binding`; it does **not** contain a top-level `routing` property.
- `docs/adr/adr.adr.md` — ADR namespace/control-surface relationship if needed.

### Lifecycle/status authority

- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` — active lifecycle/naming authority; preserve source drafts and avoid silent status/schema/tooling changes.
- `docs/policies/architecture.adr.lifecycle.md` — lifecycle consumption aid if needed.
- `workspaces/koios/working/provenance-audit.20260709T012117Z_adr-lifecycle-followon-reconciliation.md` — prior KOIOS audit of lifecycle/naming reconciliation.

### JSON authority and object/projection context

- `docs/adr/adr.json-authoritative-adr-store.draft.md` — accepted staged direction for JSON-authoritative ADR migration planning; no execution/cutover by itself.
- `docs/architecture/architecture.adr-bidirectional-objects.md` — candidate object/projection semantics and no-authority boundaries.
- `docs/architecture/architecture.json-adr-storage-topology.md` — JSON storage topology and deferred storage/database authority.
- `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md` — ATHENA intake for JSON↔Markdown object path.
- `workspaces/koios/working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`.
- `workspaces/koios/working/provenance-risk.20260711_adr-json-authority-mass-conversion.md`.

### Prior slice evidence and reviews

- `docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md` — ATHENA semantic review identifying this file as authority-relevant but needing revision.
- `workspaces/koios/working/provenance-review.20260711_adr-semantic-rationalization-six-entry-slice-5.md` — KOIOS clearance and watchpoints.
- `docs/reviews/hermes-acceptance.20260711.155200_adr-semantic-rationalization-six-entry-slice-5.md` if accepted/committed — review-only acceptance and next recommended decision.
- `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/` — provenance only, especially omitted/source-preserved section list for `adr.adr-template-contract.md`; do not treat generated projection as authority.
- `workspaces/koios/working/provenance-review.20260711_adr-json-authority-corpus-dry-run-inventory-slice-4.md` — no-authority and source-incomplete boundaries.

## Risks and watchpoints

### Status casing: `Accepted`

Risk:

- The source uses `Accepted`, while accepted lifecycle vocabulary is lower-case `accepted` / `active` and prior conversion slices preserve observed casing separately from normalized candidates.

Watchpoints:

- Preserve observed source status exactly as `Accepted`.
- Do not normalize to `accepted` or change to `active` in this planning slice.
- If a future repair recommends status normalization, it must be an explicit HERMES/USER-approved lifecycle/status repair, not a side effect.
- Do not infer that `Accepted` means clean current authority for every claim in the document.

### Stale `routing` claims

Risk:

- The source says the schema should include `routing` and lists `routing` in architecture-spec.
- Current `docs/schemas/adr.schema.json` does not have a top-level `routing` property.
- Later work preserves routing as sidecar/provenance in candidate conversion evidence.

Watchpoints:

- Mark `routing` as a likely stale or sidecar/provenance-only claim pending ATHENA/HERMES decision.
- Do not edit the schema or source to add/remove routing.
- If routing remains needed, identify whether it belongs in ADR schema, workflow binding, sidecar/envelope, README/control surface, or lifecycle/policy surface.

### JSON vs Markdown source-of-truth claims

Risk:

- The source declares Markdown is a render target and not source of truth.
- Later JSON-authoritative ADR store direction is staged and explicitly does not demote Markdown authority or execute migration yet.
- Current repository still has hand-authored Markdown ADR sources and candidate-only dev evidence.

Watchpoints:

- Treat the source-of-truth claim as ahead-of-current-repository-state unless HERMES/USER has accepted a specific per-record migration/cutover.
- Separate end-state direction from current authority.
- Do not use this file to justify generated projection replacement or Markdown demotion.

### Schema canonicality

Risk:

- The source declares `docs/schemas/adr.schema.json` canonical, but current schema and ADR object architecture have evolved; sidecars/envelopes are needed for omitted/provenance fields.
- Plain ADR schema does not carry all migration evidence, routing/source facts, or conversion sidecar material.

Watchpoints:

- Distinguish current schema file from future bidirectional object envelope.
- Identify whether repair should update the template contract to say: ADR schema governs content payload, while sidecar/envelope preserves migration/provenance facts.
- Do not publish or mutate schemas in this planning slice.

### Template/control artifact vs ordinary ADR decision

Risk:

- The source is an accepted-like decision record but semantically behaves as a template/schema contract/control surface.
- Treating it as an ordinary ADR decision can hide template/schema authority and migration policy complexity.

Watchpoints:

- Classify role explicitly: ordinary ADR decision, template contract, schema contract, ADR source-of-truth policy, or mixed authority-relevant source.
- Decide whether future repair should be a new ADR, architecture note, schema-contract doc, README/control-surface update, or source-provenance disposition.
- Preserve original file as source/provenance unless a future slice explicitly supersedes or replaces it.

### Slice 4 source incompleteness

Risk:

- Slice 4 candidate evidence for this source was source-to-candidate incomplete and listed omitted/source-preserved sections: `architecture_spec`, `context`, `implementation_brief`, `links`, `non_goals`, `resolved_open_questions`, `routing`, `validation_expectations`.

Watchpoints:

- Repair planning must inspect full source Markdown, not reduced candidate object/projection.
- Generated projection parse-back equality must not be treated as semantic completeness.

## Recommended output artifact

Recommended output path:

```text
docs/plans/architecture-review-brief.20260711_adr-template-schema-contract-repair-planning-slice-6.md
```

or, if ATHENA performs the review directly:

```text
docs/reviews/template-schema-contract-repair-plan.20260711_adr-template-contract-slice-6.md
```

Expected output sections:

1. **Source claim inventory** — table of claims from `adr.adr-template-contract.md`, with source quote/section.
2. **Current support check** — for each claim: supported, stale, ahead-of-authority, ambiguous, or needs owner decision.
3. **Control-source references** — schema, lifecycle ADR, JSON-authority staged direction, bidirectional object architecture, Slice 4/5 review evidence.
4. **Repair options** — at least three safe options:
   - preserve as source/provenance and write replacement contract later;
   - draft a successor ADR/template-contract revision without mutating current file;
   - extract schema/object architecture content into architecture/schema surface and leave this ADR as historical/source evidence.
5. **Recommended path** — proposal only, with required owner decisions.
6. **Non-authorizations** — explicit no mutation/no status/no schema/no cutover boundaries.

## Suggested claim inventory columns

- source section;
- exact claim or paraphrase;
- observed status/source wording;
- current supporting source(s);
- conflict/staleness evidence;
- proposed classification: `current`, `stale`, `ahead_of_authority`, `ambiguous`, `source_provenance_only`, `requires_owner_decision`;
- safe repair recommendation;
- required owner/role decision.

## Candidate repair options to evaluate

### Option A: Replacement/successor contract proposal

Create a future successor ADR or template/schema contract proposal that states current truth clearly, then later decide whether to supersede the old file.

Pros:

- Avoids editing accepted-like source in place.
- Keeps provenance clear.
- Allows status/supersession decision to be explicit.

Risks:

- Requires careful relationship to accepted lifecycle ADR and JSON authority staged direction.
- Must not silently demote current file before acceptance.

### Option B: Architecture/schema contract extraction

Extract current durable schema/object semantics into an architecture/schema surface, leaving `adr.adr-template-contract.md` as authority-relevant source/provenance until separately superseded.

Pros:

- Fits README boundary if the document is more blueprint/contract than bounded decision.
- Can distinguish ADR content schema from bidirectional object envelope and sidecar policy.

Risks:

- Requires later ADR or policy decision if architecture surface should control ADR schema authority.
- Must avoid hidden status transition.

### Option C: Minimal errata/reconciliation note

Produce a review-only errata/reconciliation note listing stale claims (`routing`, source-of-truth timing, status casing) without changing source.

Pros:

- Lowest mutation risk.
- Useful for later migration planning.

Risks:

- Leaves current readers with a confusing accepted-like file unless README/index points to the note in a later approved slice.

## KOIOS preliminary recommendation

Prefer **Option A or B**, not in-place mutation, for the first repair path.

The safest immediate slice should produce a repair plan/decision brief, not edit the source. It should likely recommend a successor template/schema contract or architecture/schema extraction that reconciles:

- ADR content schema vs bidirectional object envelope;
- Markdown current authority vs future generated projection state;
- `routing` as stale schema content vs sidecar/provenance/workflow metadata;
- status casing and lifecycle vocabulary;
- whether this file remains current authority, source/provenance, or later superseded by an explicit successor.

## Non-authorizations

This planning slice must not authorize:

- edits to `docs/adr/adr.adr-template-contract.md`;
- edits to any `docs/adr/` source;
- edits to `docs/schemas/`;
- status normalization or status changes;
- formal supersession, acceptance, activation, rejection, promotion, or demotion;
- file moves, renames, deletes, archives, or splits;
- JSON conversion/projection generation;
- generated projection replacement of hand-authored Markdown;
- authoritative JSON ADR records;
- JSON authority cutover;
- database/storage authority;
- product/domain authority decisions;
- treating `dev/` evidence as durable authority;
- implementation work beyond producing the review/planning artifact.
