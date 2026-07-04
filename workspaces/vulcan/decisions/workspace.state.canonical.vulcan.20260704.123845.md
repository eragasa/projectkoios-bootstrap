```json
{
  "title": "Canonical Vulcan workspace-state surface",
  "artifact_type": "local-decision",
  "status": "active local workspace decision",
  "datetime": "20260704.123845",
  "origin": "user request",
  "from": "VULCAN",
  "acting_as": "VULCAN",
  "scope": "projectkoios-bootstrap/workspaces/vulcan",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan",
  "document_domain": "implementation/tests/validation workspace control",
  "workspace_material_dirs": {
    "working": "working/",
    "scratch": "scratch/",
    "decisions": "decisions/",
    "sessions": "sessions/"
  }
}
```

# Vulcan local decision: canonical workspace-state surface

## Decision

Vulcan workspace resume state uses two Markdown control files:

- `state.md` is the durable Vulcan resume snapshot.
- `active.md` is the current implementation queue and exit criteria.

Both files are human-first Markdown with a top JSON metadata section and stable headings.

Workspace material uses flat `working/` for current or transitional implementation material and `scratch/` for temporary, non-durable exploration. `working/` does not use `incoming/` or `outgoing/` subdirectories.

## Canonical `state.md` shape

`state.md` SHOULD contain a top JSON metadata section followed by these headings, in this order:

1. `# Vulcan workspace state`
2. `## Current scope`
3. `## Validated state`
4. `## Open questions`
5. `## Next transition`
6. `## Startup checklist`

The file SHOULD answer only resume-critical questions:

- Which implementation slice is active?
- Which source artifact controls the work?
- What validation state was last known?
- What blockers or rebrief triggers exist?
- What is the next expected artifact and owner?

## Canonical `active.md` shape

`active.md` SHOULD contain a top JSON metadata section followed by these headings, in this order:

1. `# Vulcan active work`
2. `## Current priority stack`
3. `## Waiting on`
4. `## Working material`
5. `## Ignore for now`
6. `## Exit criteria`

The file SHOULD include no more than three active implementation priorities.

## Durable output locations

- Implementation plans and filesystem-visible work items: `docs/plans/`
- Implementation reports: `docs/implementation/`
- Process chains: `docs/process-capture/`
- Session/process lessons: `docs/AAR/`
- Temporary implementation notes: `workspaces/vulcan/working/` or `workspaces/vulcan/scratch/`

## Rationale

Vulcan needs a restartable implementation surface equivalent to Athena's spec surface, but centered on implementation source artifacts, validation evidence, implementation reports, and rebrief triggers.

## Consequences

- New Vulcan sessions can resume without chat history.
- Active implementation work is explicit instead of inferred from files present in `working/`.
- Durable implementation output remains in public docs surfaces rather than hidden workspace folders.
- The ATHENA/VULCAN filesystem-sequential process is visible through linked artifacts.

## Validation expectation

A later Vulcan session succeeds if it can read only `AGENTS.md`, `state.md`, `active.md`, and any active `working/` material, then identify:

- current represented role,
- active implementation source artifact,
- validated state,
- blockers/rebrief triggers,
- next implementation step,
- ignored scope,
- expected successor artifact.
