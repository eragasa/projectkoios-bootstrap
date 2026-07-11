```json
{
  "title": "Architecture conformance review: ADR heading parser stable format slice 12",
  "artifact_type": "architecture-conformance-review",
  "status": "accepted-with-watchpoints-retrospective",
  "datetime": "20260711.180500Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-heading-parser-stable-format-slice-12",
  "reviewed_implementation": "docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md",
  "authority_change": false,
  "source_mutation": false,
  "schema_mutation": false,
  "retrospective_review": true,
  "next_owner": "HERMES_USER"
}
```

# Architecture conformance review 20260711.180500: ADR heading parser stable format slice 12

## Verdict

ATHENA retrospectively accepts `adr-heading-parser-stable-format-slice-12` with watchpoints.

The patch conforms to the stable ADR filename/heading policy direction and is acceptable as a bounded tooling-compatibility adjustment.

## Process note

The initial VULCAN workpackage was premature and invalid as control authority because HERMES routed implementation before ATHENA produced the owning brief/acceptance criteria for the document-policy/tooling boundary.

This review supplies the missing ATHENA-owned retrospective conformance basis. It does not make the premature routing pattern acceptable for future slices.

Future tooling changes that interpret document policy should still begin with the owning architecture/specification brief or explicit ATHENA acceptance criteria unless USER/HERMES explicitly waives that order.

## Conformance basis

Current USER/HERMES direction is that ADR filenames should use stable semantic names by default and that timestamps should live in metadata, provenance/review artifacts, and git history rather than ADR storage filenames.

For heading parsing, this establishes the current parser target as:

```text
# ADR: Title
```

Legacy headings remain compatibility inputs only:

```text
# ADR <prefix>: Title
# ADR 20260711.000000Z: Title
```

The implementation report states the patch:

- accepts stable `# ADR: Title` headings;
- preserves legacy prefixed heading compatibility;
- records legacy heading-prefix stripping only when a legacy prefixed heading is parsed;
- updates projectable messy canary parsing to accept both forms;
- corrects a stale implementation docstring that described timestamped ADR filenames;
- adds focused parser test coverage;
- preserves `docs/adr/` and `docs/schemas/` unchanged.

ATHENA reran focused validation during retrospective review:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Observed: `35 passed`.

ATHENA also checked:

```bash
git status --short -- docs/adr docs/schemas
git diff --check
```

Observed: no `docs/adr` or `docs/schemas` output, and diff hygiene passed.

## Retrospective acceptance criteria

If ATHENA had authored the brief before implementation, the acceptance criteria would have been:

1. `AdrMarkdownRecordParser` accepts stable `# ADR: Title` headings.
2. Stable headings parse without recording a legacy heading-prefix normalization note.
3. Legacy prefixed headings such as `# ADR 20260711.000000Z: Title` continue to parse.
4. Legacy prefixed headings record that a legacy heading prefix was removed before the title.
5. `AdrProjectableMessyCanaryRunner` title parsing accepts both stable and legacy heading forms.
6. Stale implementation guidance that claims timestamped ADR filenames as the current convention is corrected to stable semantic filenames such as `adr.<topic>.md` or `adr.<topic>.<status>.md`.
7. No existing source ADR under `docs/adr/` is edited, renamed, normalized, generated, projected, superseded, or migrated.
8. No machine-readable schema under `docs/schemas/` is edited.
9. The patch does not change ADR lifecycle/status policy, source disposition, JSON authority, storage authority, migration gates, or cutover behavior.
10. Focused control-surface ADR tests pass.
11. Type checking and python policy validation pass for the touched Python surfaces.
12. `git diff --check` passes.

The implemented patch satisfies these criteria based on VULCAN's report and ATHENA's focused rerun.

## Authority boundaries

This review and the implementation do not authorize:

- rewriting source ADR headings;
- normalizing source status or source heading/date text;
- renaming ADR files;
- changing existing ADR lifecycle state;
- superseding, accepting, activating, rejecting, promoting, demoting, moving, deleting, archiving, or splitting ADR files;
- editing `docs/schemas/`;
- changing schema authority;
- creating or replacing generated Markdown projections;
- converting ADR Markdown to authoritative JSON;
- database/storage authority;
- bulk migration;
- JSON authority cutover.

Legacy prefixed headings remain accepted parser inputs for compatibility and provenance. They are not the preferred target format for newly authored ADRs unless USER/HERMES later changes the policy.

## Watchpoints

- Heading parsing logic now exists in both `AdrMarkdownRecordParser` and `AdrProjectableMessyCanaryRunner`; if additional ADR parsers or conversion runners are introduced, the heading parser should be centralized to avoid regex drift.
- Active planning/control surfaces that still mention timestamped ADR filenames or timestamped ADR draft paths should be reconciled in a separate naming-policy/documentation correction slice.
- Retrospective approval should not be treated as permission for HERMES or VULCAN to bypass ATHENA ownership for future document-policy/tooling boundary changes.

## Recommended follow-up

Run a separate ATHENA-owned naming-policy/documentation reconciliation slice to update active guidance and plan surfaces for:

- stable semantic ADR filenames;
- `# ADR: Title` as the preferred heading form;
- provenance timestamps in metadata/body/review artifacts/git history;
- collision policy for stable semantic draft paths;
- correction of any active Slice 10/Slice 11 path assumptions that still use timestamped ADR filenames.
