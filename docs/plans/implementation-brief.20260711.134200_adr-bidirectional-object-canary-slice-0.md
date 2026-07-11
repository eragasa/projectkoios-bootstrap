```json
{
  "title": "ADR bidirectional object canary slice 0 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.134200Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / bidirectional JSON-Markdown object architecture",
  "slice_name": "adr-bidirectional-object-canary-slice-0",
  "source_architecture": "docs/architecture/architecture.adr-bidirectional-objects.md",
  "next_owner": "HERMES_USER"
}
```

# Implementation brief 20260711.134200: ADR bidirectional object canary slice 0

## Purpose

Implement the first bounded canary for the ADR bidirectional JSON↔Markdown object path.

The slice should prove that one ADR source can be represented as a candidate `AdrBidirectionalObject` envelope with:

- ADR-schema-compatible `content` payload;
- classification/disposition metadata outside `content`;
- sidecar/evidence preservation for unsupported source fields;
- generated Markdown projection;
- parse-back semantic equality for generated projection only;
- source/projection/schema hashes and source-mutation proof.

This is a canary/evidence slice. It must not change repository-wide ADR authority.

## Source authority

Architecture direction:

- `docs/architecture/architecture.adr-bidirectional-objects.md`
- `docs/architecture/architecture.json-adr-storage-topology.md`

Source intake and KOIOS inputs:

- `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md`
- `workspaces/koios/working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`
- `workspaces/koios/working/candidate-schema.20260711_adr-bidirectional-json-md-object.md`
- `workspaces/koios/working/classification-proposal.20260711_adr-hierarchy-rationalization.md`

Prior conformance evidence:

- `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`
- `dev/adr-json-schemas-conformance/`

## Canary source

Exactly one source ADR may be used:

```text
docs/adr/adr.json-schemas.draft.md
```

No other `docs/adr/` source may be converted, rewritten, moved, renamed, status-normalized, accepted, superseded, or included as a second canary.

## Required evidence path

Create candidate canary evidence under a dedicated dev path, preferred:

```text
dev/adr-bidirectional-object-canary-slice-0/
```

Expected evidence artifacts may include:

```text
dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json
dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.projected.md
dev/adr-bidirectional-object-canary-slice-0/conversion-evidence.json
dev/adr-bidirectional-object-canary-slice-0/manifest.json
```

VULCAN may adjust filenames for consistency, but the evidence directory must remain a single canary directory and must be documented in the implementation report.

## Candidate object requirements

The candidate object must represent an `AdrBidirectionalObject` envelope, not a published schema.

Minimum envelope shape:

```text
AdrBidirectionalObject
├── object_type
├── object_version
├── authority_mode
├── content
├── classification
├── markdown_projection
├── conversion_evidence
├── source_refs
├── sidecar
├── validation
└── conflict_policy
```

Required values/semantics:

- `object_type`: identifies the envelope as an ADR bidirectional object.
- `object_version`: candidate version, e.g. `candidate-0`.
- `authority_mode`: candidate/evidence mode, not repository authority.
- `content`: ADR payload compatible with current `docs/schemas/adr.schema.json`.
- `classification`: envelope metadata outside `content`.
- `markdown_projection`: generated projection metadata, path, hash, and generated-only mode.
- `conversion_evidence`: source mutation flag, omitted/normalized/inferred fields, lossiness, and concise notes.
- `source_refs`: source Markdown, schema, projection, architecture, and evidence refs with hashes where applicable.
- `sidecar`: unsupported source fields preserved outside ADR content.
- `validation`: schema validation, projection parse-back equality, source-mutation proof, and no mutable database commit evidence.
- `conflict_policy`: generated projection only; no hand-authored Markdown ingest; bulk migration false.

## Classification/disposition requirements

Classification/disposition metadata must live outside the ADR `content` payload.

For this canary, record:

```text
category: template_schema_contract
secondary_aspect: architecture_blueprint
source_role: canary_source
source_authority_effect: none
```

The implementation must not use classification/disposition metadata to change source ADR status, filename, source-of-truth mode, schema authority, or lifecycle authority.

Avoid ambiguous wording such as `active ADRs` in generated artifacts, implementation reports, and comments. Use precise language such as:

- `current conformance artifact`;
- `documents marked active/accepted pending hierarchy review`;
- `source Markdown`;
- `candidate object evidence`;
- `generated projection evidence`.

## Content payload requirements

The `content` payload should conform to current ADR schema expectations without adding envelope-only material.

Rules:

- Do not put classification/disposition fields in `content`.
- Do not put source hashes, projection hashes, conversion warnings, or source filename suffixes in `content` unless already required by the current ADR schema.
- Do not add unsupported source fields such as `routing` or `links.related` to `content` if current schema rejects or omits them.
- Preserve unsupported source material in sidecar/evidence instead.

## Sidecar/evidence requirements

Preserve unsupported or schema-excluded source material in sidecar/evidence, including at minimum:

- source `routing` block from `docs/adr/adr.json-schemas.draft.md`;
- source `links.related` value;
- observed source status text/casing;
- observed source date;
- source path and source hash;
- current schema path and schema hash;
- generated projection path and projection hash.

The sidecar is evidence for this canary. It must not be treated as a published schema or repository-wide ADR sidecar authority.

## Bidirectional behavior

Only generated projection round-trip is in scope:

```text
candidate object content
  -> generated Markdown projection
  -> parse generated Markdown projection
  -> semantic equality against candidate object content
```

Requirements:

- Generated Markdown projection must be deterministic for unchanged object content.
- Projection must carry enough marker/metadata to distinguish generated projection evidence from hand-authored source Markdown.
- Parse-back equality must be semantic equality for the generated projection only.
- Hand-authored Markdown ingest is out of scope.
- Source Markdown must not be overwritten or regenerated.

## Source mutation proof

The implementation must prove `docs/adr/adr.json-schemas.draft.md` was not modified.

Required evidence:

- source hash before/after or source hash recorded and validated after generation;
- `git status --short -- docs/adr` output in the implementation report;
- tests or validation command that fails if the source Markdown is mutated by canary generation.

## Storage and database boundary

This slice should be file/evidence/projection only unless VULCAN identifies an unavoidable reason to touch storage code and pauses for approval.

Rules:

- Do not promote database/storage authority.
- Do not create or commit mutable `.sqlite` or `.db` files.
- Do not require SQLite for this canary.
- Do not weaken SQLite durability settings or add storage behavior.
- Preserve existing generic document-store separation.

## Scope

In scope:

```text
docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md
dev/adr-bidirectional-object-canary-slice-0/
src/python/projectkoios/bootstrap/control_surface/adr/        # only if needed for reusable ADR object/projection behavior
tests/projectkoios/bootstrap/control_surface_adr/             # focused tests for canary behavior
docs/implementation/<implementation-report>.md
docs/AAR/<aar-if-useful>.md
workspaces/vulcan/state.md
workspaces/vulcan/active.md
```

Out of scope:

```text
docs/adr/** mutation
docs/schemas/** publication or change
bulk conversion of docs/adr/
database authority or committed DB files
hand-authored Markdown ingest
Petri-net workflow integration
Operator Console integration
workflow-object integration
repository-wide ADR hierarchy migration
file moves or renames
status normalization or status changes
marking drafts as superseded
```

## Acceptance criteria

1. Exactly one source is used: `docs/adr/adr.json-schemas.draft.md`.
2. Candidate `AdrBidirectionalObject` envelope evidence exists under one dev evidence directory.
3. Envelope includes `content`, `classification`, `markdown_projection`, `conversion_evidence`, `source_refs`, `sidecar`, `validation`, and `conflict_policy` or clear equivalent fields.
4. Classification/disposition metadata is outside ADR `content`.
5. `content` remains compatible with current `docs/schemas/adr.schema.json` and does not include envelope-only metadata.
6. Unsupported source fields are preserved in sidecar/evidence, including `routing` and `links.related`.
7. Generated Markdown projection exists as evidence and is visibly generated/projection-only.
8. Generated projection parse-back semantic equality is tested or otherwise validated.
9. Hand-authored Markdown ingest is not implemented.
10. `docs/adr/adr.json-schemas.draft.md` is not mutated.
11. No other `docs/adr/` file is mutated.
12. No `docs/schemas/` file is added or changed.
13. No mutable `.sqlite` or `.db` file is committed.
14. No bulk migration, file moves, file renames, status normalization, or draft supersession occurs.
15. Implementation report uses precise authority language and avoids ambiguous `active ADRs` wording.

## Suggested validation

From repository root, VULCAN should run focused validation appropriate to the implementation plus:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
git status --short -- docs/adr
git status --short -- docs/schemas
find dev/adr-bidirectional-object-canary-slice-0 -type f \( -name '*.sqlite' -o -name '*.db' \) -print
uv run python -m json.tool dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json >/dev/null
git diff --check
```

If artifact filenames differ, adjust the JSON validation command and document the difference.

## Pause triggers

Pause and ask HERMES/USER before proceeding if implementation would require:

- mutating any `docs/adr/` file;
- adding or changing any `docs/schemas/` file;
- converting more than `docs/adr/adr.json-schemas.draft.md`;
- moving or renaming ADR files;
- normalizing status text/casing;
- marking drafts as superseded;
- adding hand-authored Markdown ingest;
- adding database/storage authority;
- committing a mutable `.sqlite` or `.db` file;
- relying on SQLite for this canary;
- changing generic document-store schema;
- creating repository-wide ADR hierarchy migration machinery;
- adding Petri-net, Operator Console, or workflow-object integration;
- using ambiguous authority language that suggests this canary changes ADR authority.

## Handoff

This is a brief only. Pause for HERMES/USER approval before VULCAN routing or implementation.
