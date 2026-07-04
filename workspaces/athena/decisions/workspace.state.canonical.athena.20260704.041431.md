```json
{
  "title": "Canonical Athena workspace-state surface",
  "artifact_type": "local-decision",
  "status": "active local workspace decision",
  "datetime": "20260704.041431",
  "origin": "user request",
  "from": "ATHENA",
  "acting_as": "ATHENA",
  "scope": "projectkoios-bootstrap/workspaces/athena",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena",
  "document_domain": "architecture/specification workspace control",
  "workspace_material_dirs": {
    "working": "working/",
    "scratch": "scratch/",
    "decisions": "decisions/",
    "sessions": "sessions/"
  },
  "supersedes": "decisions/20260704.041431_canonical-workspace-state.md"
}
```

# Athena local decision: canonical workspace-state surface

## Decision

Athena workspace resume state uses two Markdown control files only:

- `state.md` is the canonical resume snapshot.
- `active.md` is the current priority filter.

No machine-readable companion is needed now. The files stay human-first Markdown, with a JSON metadata section at the top and stable headings for reviewability.

Workspace material uses flat `working/` for current/transitional working files and `scratch/` for temporary, non-durable exploration. `working/` does not use `incoming/` or `outgoing/` subdirectories.

## Canonical `state.md` shape

`state.md` SHOULD contain a top JSON metadata section followed by these headings, in this order:

1. `# Athena workspace state`
2. `## Current scope`
3. `## Validated state`
4. `## Open questions`
5. `## Next transition`
6. `## Startup checklist`

The file SHOULD answer only resume-critical questions:

- Who is represented?
- Which repository/workspace/domain is active?
- What durable state was last validated?
- What is blocked or still undecided?
- What is the next bounded state transition and owner?
- What startup checks should the next session run?

## Canonical `active.md` shape

`active.md` SHOULD contain a top JSON metadata section followed by these headings, in this order:

1. `# Athena active work`
2. `## Current priority stack`
3. `## Waiting on`
4. `## Working material`
5. `## Ignore for now`
6. `## Exit criteria`

The file SHOULD include no more than three active priorities.

## Rationale

Markdown remains the document body format, but metadata moves into an explicit top JSON block. This avoids maintaining a separate schema file while making document identity, provenance, scope, and ownership machine-readable if future automation needs it.

## Consequences

- New Athena sessions can initialize from `state.md` and `active.md` without re-deriving chat context.
- Metadata is consistently grouped at the top instead of scattered through prose.
- The field set stays small and role-owned.
- If automated validation later requires structured data, the top JSON blocks provide a natural parse target.

## Validation expectation

A later session succeeds if it can read only `state.md`, `active.md`, and any active `working/` material, then identify:

- current represented role,
- active repository/workspace,
- validated state,
- open blockers/questions,
- highest-leverage next transition,
- ignored scope.
