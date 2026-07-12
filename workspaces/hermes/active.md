```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260712",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_USER",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Hold at HERMES/USER decision after accepting `schema-record-envelope-schema-change-planning-slice-16` as proposal-only planning.
2. Preserve schema authority boundaries: `docs/schemas/schema.record-base.json` remains unchanged draft direction.
3. Do not activate `pi-skill-determinism-slice-0` unless HERMES/USER explicitly chooses to leave or pause the ADR/schema track.

## Active slice

No active queue item remains after Slice 16 acceptance.

Workflow fixture token:

```text
active_slice=none
```

Completed Slice 16 artifact:

```text
docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md
```

HERMES acceptance:

```text
docs/reviews/hermes-acceptance.20260712.023900_schema-record-envelope-schema-change-planning-slice-16.md
```

## Validation and review observed

ATHENA reported:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git status --short -- docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md
git diff --check
```

Reported result: no mutation to `docs/adr/`, `docs/schemas/`, or Slice 4 dry-run evidence; only the new plan appeared on the scoped plan path; diff hygiene passed.

HERMES independently observed the same scoped state and `git diff --check` passed.

KOIOS provenance review: provenance-adequate for HERMES proposal-only acceptance; no blockers. Watchpoints: acceptance must not approve schema JSON edits, schema authority promotion, status mirroring, projection requirements, or substantive reconciliation without later authority/tests.

VULCAN implementation-reality comments: no blockers for accepting proposal-only Option A/F. Keeping `schema.record-base.json` unchanged is implementation-safe and preserves current validator behavior. Main unchanged-schema risk is operator/agent authority confusion, not code breakage.

VULCAN watchpoints integrated:

- Do not ask implementation agents to validate new records against `schema.record-base.json` unless explicitly scoped as draft-envelope validation.
- A future minimal reference/comment slice should prefer `$comment` for tooling-neutral draft-boundary notes; `description` is more discoverable but can be mistaken as user-facing authority.
- Avoid normative wording like "must use" or "canonical" in future draft-boundary annotations.
- Any change to `required`, `additionalProperties`, `$defs`, enum values, timestamp pattern, `$id`, `$ref` behavior, or other validation-affecting keywords is semantic and out of scope for a reference/comment-only slice.

## Accepted recommendation

Keep `docs/schemas/schema.record-base.json` unchanged as draft record-envelope direction for now.

Defer substantive schema changes until renderer/ingester, family-schema composition, or migration needs become concrete.

If HERMES/USER wants a minimal next schema-edit slice, limit it to non-semantic reference/description/comment changes linking `docs/architecture/architecture.schema-record-envelope.md` while preserving validation semantics.

## Waiting on

HERMES/USER next decision:

1. Stop the ADR/schema planning track here and leave `schema.record-base.json` unchanged until implementation or migration pressure appears.
2. Activate a minimal non-semantic `schema-record-envelope-reference-comment-slice-17`.
3. Defer schema reconciliation and return to another explicitly chosen workflow item.

## Exit criteria

Hermes state is stable: the Slice 16 acceptance package is committed and the workflow fixtures report no active queue item / `active_slice=none`.
