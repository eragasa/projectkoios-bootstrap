```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.180700Z",
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

1. Package/commit stable ADR filename convention, Slice 10 path corrections, and corrected retrospective Slice 12 acceptance if USER approves.
2. Decide whether to activate `adr-template-schema-contract-successor-draft-slice-11` for ATHENA.
3. Create a separate ATHENA-owned naming-policy/documentation reconciliation slice for remaining active guidance if USER approves.

## Stabilized control-surface state

- Future Slice 11 successor draft path is now the stable semantic path:

```text
docs/adr/adr.adr-template-schema-contract.draft.md
```

- Root `AGENTS.md` ADR filename convention is updated in the working tree to avoid timestamped ADR filenames by default.
- Invalid uncommitted Slice 12 VULCAN implementation decision was removed.
- Slice 12 implementation is accepted only through corrected retrospective review:
  - VULCAN report: `docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md`
  - ATHENA conformance: `docs/reviews/architecture-conformance.20260711.180500_adr-heading-parser-stable-format-slice-12.md`
  - KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-heading-parser-stable-format-slice-12.md`
  - HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.180700_adr-heading-parser-stable-format-slice-12.md`
- Process AARs:
  - `docs/AAR/aar.20260711_premature-vulcan-tooling-handoff.md`
  - `docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md`

## Accepted Slice 12 meaning

- Stable `# ADR: Title` headings are accepted by control-surface ADR parser tooling.
- Legacy prefixed headings remain accepted for compatibility/provenance.
- Legacy heading-prefix normalization is recorded only for legacy prefixed headings.
- No `docs/adr`, `docs/schemas`, lifecycle/status policy, successor ADR, supersession, migration, projection replacement, storage authority, or cutover boundary changed.

## Current boundaries

Future document-policy/tooling implementation should start with ATHENA-owned brief/acceptance criteria unless USER explicitly waives that order.

Current work does not authorize creating the successor ADR draft, editing existing `docs/adr/` files, editing `docs/schemas/`, changing source status or casing, supersession, lifecycle changes, migration, generated projection replacement, database/storage authority, or cutover.

## Waiting on

- USER decision to package/commit current control-surface corrections and retrospective Slice 12 acceptance.
- USER decision whether next work is ATHENA Slice 11 successor draft creation, naming-policy/documentation reconciliation, or another bounded action.

## Exit criteria

Hermes state is stable when the current control-surface corrections and retrospective Slice 12 acceptance are packaged or explicitly revised, and any next work is assigned to the correct document-domain owner before implementation begins.
