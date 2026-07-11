```json
{
  "title": "Provenance/risk input: ADR JSON authority and mass conversion",
  "artifact_type": "provenance-risk-input",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "mass ADR Markdown to JSON conversion and JSON authority path",
  "requires_promotion_by": ["ATHENA", "USER/HERMES"]
}
```

# Provenance/risk input: ADR JSON authority and mass conversion

## Authority boundary

This is KOIOS provenance/risk input only. It does not authorize JSON authority, bulk conversion, schema edits, source ADR mutation, file moves/renames, or implementation.

USER clarified the desired end state: mass convert ADR Markdown to JSON and make JSON authoritative. That is an authority change and must be promoted through ATHENA/USER architecture decision before VULCAN implementation.

## Source basis

- `docs/adr/` current inventory and status scan.
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` — lifecycle/naming authority and non-silent migration boundary.
- `docs/architecture/architecture.adr-bidirectional-objects.md` — candidate object/envelope and generated-projection-first semantics.
- `docs/architecture/architecture.json-adr-storage-topology.md` — storage topology, deferred authority, SQLite pilot boundaries.
- `workspaces/koios/working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`.
- `workspaces/koios/working/candidate-schema.20260711_adr-bidirectional-json-md-object.md`.
- `workspaces/koios/working/classification-proposal.20260711_adr-hierarchy-rationalization.md`.
- Prior implementation evidence under `dev/adr-json-database-one-adr-pilot/` and `dev/adr-json-schemas-conformance/`.

## Current ADR mess classification

KOIOS previously inventoried 42 Markdown files under `docs/adr/`, including `README.md`. Observed status parsing found mixed status values/casing and unknown status cases:

- `draft`: 31
- `Draft`: 1
- `active`: active-like records observed
- `accepted` / `Accepted`: both observed
- unknown/no parsed status: 6

The ADR space currently mixes several document classes:

1. current decision records;
2. source/provenance drafts;
3. architecture blueprints in ADR space;
4. policy/process documents;
5. templates/schema/contracts;
6. implementation workflow support documents;
7. product/future-system drafts needing domain review.

Risk: mass conversion that treats all files as equivalent ADR decisions will silently promote drafts, templates, process notes, or architecture blueprints into uniform JSON authority.

## What could be lost or distorted in mass conversion

Potential losses/distortions:

- original Markdown formatting, comments, ordering, and human context;
- status casing and legacy vocabulary that may be meaningful provenance even if not canonical;
- filename-derived state such as `.draft.md` suffixes;
- source dates or timestamps not represented by `docs/schemas/adr.schema.json`;
- unsupported fields such as legacy `routing.*` or `links.related`;
- links expressed only in prose rather than schema fields;
- source-draft disposition relationships not yet structured;
- architecture/policy/template identity when mapped into a plain ADR schema payload;
- distinction between generated projection Markdown and hand-authored source Markdown;
- rejection/supersession history if records are normalized without sidecar trail.

## Status/lifecycle/casing ambiguity

The accepted lifecycle/naming ADR defines current lifecycle/status vocabulary and explicitly forbids silent schema/tooling changes, status migration, mass record rewrites, or file renames without separate handoff.

Before JSON authority:

- observed status and original casing must be preserved separately from normalized JSON status;
- unknown status files must not be guessed into accepted/active authority;
- source draft vs accepted/current decision must be classified before conversion;
- workspace `active.md` live-work state must not be confused with ADR lifecycle `active`;
- `active conformance artifact` must not be conflated with ADR status `active`.

## Unsupported fields and sidecar requirements

Mass conversion needs an explicit sidecar/envelope policy. Current evidence already shows plain ADR schema does not carry all source material.

Minimum preservation per source file:

- source path;
- source content hash;
- observed status and exact casing;
- observed source date/time where present;
- filename suffix/state such as `.draft.md`;
- omitted fields and original values;
- normalized fields and original values;
- inferred fields and rationale;
- parse warnings/lossiness classification;
- links/provenance not representable in ADR schema;
- generated JSON hash and projection hash;
- conversion tool version/command.

Recommendation: use an `AdrBidirectionalObject` envelope or companion sidecar, not plain `docs/schemas/adr.schema.json` alone, for authority migration evidence.

## Source/projection conflict policy needed

Before JSON becomes authoritative, conflict policy must answer:

- If hand-authored Markdown and generated JSON differ, which is authoritative during migration?
- When is Markdown frozen as source evidence?
- Are `docs/adr/*.md` files rewritten as generated projections, left as historical source, or replaced by generated projection files?
- How are human edits to Markdown after JSON authority detected and handled?
- What happens when generated projection parse-back differs semantically from JSON?
- What review gate is required before deleting or replacing hand-authored Markdown?

Minimum safe policy for first bulk attempt:

- do not mutate `docs/adr/` source Markdown during conversion;
- generate JSON plus projection/evidence in a separate review path;
- compare generated projection parse-back to JSON;
- report every lossy or unsupported conversion;
- require explicit USER/HERMES acceptance before flipping authority or replacing Markdown.

## Provenance and audit trail requirements

A mass conversion authority path should produce an auditable manifest/index with one row per source file:

| Required evidence | Purpose |
|---|---|
| source path + source hash | prove source identity and detect later edits |
| source classification/category | avoid promoting non-decision docs accidentally |
| observed status/casing + normalized status | preserve lifecycle ambiguity |
| conversion result path/hash | review generated JSON |
| projection path/hash | review generated Markdown rendering |
| sidecar path/hash | preserve unsupported/lossy material |
| validation result | prove schema and round-trip status |
| disposition | current decision / provenance draft / architecture candidate / policy candidate / domain review required |
| authority effect | none / candidate / proposed authority / accepted authority |

The conversion should be reproducible: same source inputs and schema/config should produce the same JSON/projection hashes.

## What must be validated before JSON authority

Minimum validation gates:

1. Full ADR inventory classification reviewed by ATHENA/USER.
2. Schema validity for every generated JSON authority candidate.
3. Sidecar preservation for every unsupported field or omitted source feature.
4. Generated Markdown projection is deterministic.
5. Generated projection parse-back is semantically equal to JSON for every generated projection.
6. Source Markdown unchanged during dry-run/migration review unless explicit rewrite approved.
7. No file moves/renames/status changes without separate accepted plan.
8. No mutable `.sqlite`/`.db` files committed as authority unless a later ADR explicitly promotes database authority.
9. JSON authority mode is explicit per record and in the corpus manifest.
10. Conflicts and lossy conversions block authority promotion until reviewed.
11. Tests cover clean ADRs, messy drafts, unknown status, unsupported fields, and architecture/policy/template-like files.
12. Human review confirms generated JSON did not collapse document class distinctions.

## Recommended staged path

1. **Dry-run corpus inventory**: parse/classify every `docs/adr/*.md`; emit manifest only.
2. **Canary conversion**: one file (`adr.json-schemas.draft.md`) using `AdrBidirectionalObject` envelope; no source mutation.
3. **Messy canary**: one high-ambiguity draft or unknown-status file; prove lossiness reporting.
4. **Corpus conversion dry-run**: generate JSON/projections/sidecars for all files under `dev/` or another review-only path.
5. **ATHENA/USER authority decision**: decide JSON authority, Markdown projection policy, and disposition categories.
6. **Bounded migration implementation**: only after accepted architecture/brief; preserve audit trail and rollback path.

## KOIOS watchpoints

Block premature implementation or bulk migration if any of these are unresolved:

- status normalization policy;
- unknown-status handling;
- classification/disposition of non-decision documents;
- sidecar/envelope authority;
- Markdown source vs generated projection policy;
- conflict/lossiness review gate;
- storage authority model: JSON files vs database vs hybrid;
- whether `dev/` artifacts can become durable authority or need a new location;
- whether `docs/adr/` remains review/navigation surface or becomes generated projection;
- how to preserve accepted lifecycle/naming ADR boundaries.

## KOIOS conclusion

JSON authority and mass conversion are plausible as an end state, but only after a staged dry-run/canary path proves no source context is lost and after ATHENA/USER explicitly accepts an authority model. The current ADR corpus is too heterogeneous for safe one-shot conversion into plain ADR schema payloads without envelope/sidecar provenance and classification/disposition review.
