```json
{
  "title": "HERMES decision: Schema record-envelope architecture housekeeping slice 18",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-edit",
  "datetime": "20260712.030127Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-record-envelope-architecture-housekeeping-slice-18",
  "source_architecture": "docs/architecture/architecture.schema-record-envelope.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260712.020742_adr-schema-record-envelope-architecture-slice-14.md",
  "post_slice_reviews": [
    "KOIOS post-Slice 17 consistency review received by HERMES",
    "ATHENA post-Slice 17 consistency review received by HERMES"
  ],
  "target_surfaces": [
    "docs/architecture/architecture.schema-record-envelope.md"
  ],
  "user_authorization": "USER said proceed after HERMES recommended an optional bounded metadata/doc cleanup",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260712.030127: Schema record-envelope architecture housekeeping slice 18

## Decision

HERMES records USER authorization to activate a bounded housekeeping slice:

```text
schema-record-envelope-architecture-housekeeping-slice-18
```

ATHENA is the next owner because the target artifact is an architecture surface.

## Scope

ATHENA may edit only:

```text
docs/architecture/architecture.schema-record-envelope.md
```

The edit should be a small non-semantic housekeeping update that addresses reader-confusion watchpoints raised after Slices 14-17:

- align or clarify the frontmatter/status wording now that HERMES accepted the architecture surface in Slice 14;
- update provenance/acceptance basis to acknowledge Slices 15-17 and the post-Slice-17 ATHENA/KOIOS no-blocker consistency reviews;
- optionally add a short note that later README and schema `$comment` references were added by separate bounded slices without changing validation semantics or authority.

## Required boundaries

The edit must not create or imply any new authority beyond existing accepted surfaces.

The edit must not authorize or imply:

- machine-readable schema authority promotion;
- universal `metadata` + `content` emitted-record authority;
- status mirroring policy;
- generated projection requirements;
- renderer/ingester behavior;
- migration or source rewrite;
- database/storage authority;
- JSON authority cutover;
- validation semantics changes;
- edits to `docs/schemas/`, `docs/adr/`, generated projections, or implementation files.

Any historical Slice 14 boundary wording may be clarified only as a boundary of what the architecture artifact itself authorized, while preserving that later Slices 15 and 17 separately authorized bounded README/schema-comment edits.

## Required review before HERMES acceptance

Before HERMES accepts this slice, KOIOS should review the resulting architecture edit for provenance and authority-boundary consistency.

VULCAN review is not required unless the edit unexpectedly touches implementation, schemas, validation behavior, renderer/ingester behavior, migration, or generated projections.

## Closeout expectations

ATHENA/HERMES closeout should verify:

```bash
git diff -- docs/architecture/architecture.schema-record-envelope.md
git diff --check
```

HERMES acceptance, if any, must state that this slice is metadata/provenance/doc housekeeping only and does not promote schema-envelope authority.
