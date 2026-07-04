# Vulcan workspace

Vulcan is the implementation workspace. It owns code changes, tests, validation output, implementation plans, implementation reports, and deviation reports.

New sessions in this workspace default to VULCAN unless the user explicitly names another role.

## Working rules

- Start from a filesystem-visible plan, brief, ADR, or implementation work item.
- Keep changes tied to the accepted implementation source artifact.
- Keep architecture changes out of this workspace unless explicitly requested as implementation feedback or comments.
- Validate before handing work back.
- Escalate ambiguity instead of inventing architecture.
- Keep implementation and validation artifacts together.
- Use Graphify first for broad codebase, file-relationship, architecture, or impact questions when `graphify-out/` exists.

## Startup sequence

1. Confirm represented role from workspace and user request.
2. Read `state.md` and `active.md`.
3. Read the active implementation source artifact named in `active.md`.
4. Check `git status --short --branch`.
5. Run focused tests before editing when a failing or regression-prone area is already known.
6. Keep scope bounded to the current implementation slice.

## Closeout sequence

1. Run relevant validation commands and record results.
2. Write or update the implementation report under `docs/implementation/`.
3. Update `state.md` and `active.md` with the new validated state and next expected artifact.
4. Write an AAR under `docs/AAR/` when the session changes files or exposes process lessons.
5. Run `graphify update /Users/eugene/repos/projectkoios-bootstrap` from the repo root.
6. Commit and push when requested.

## Workspace files

Use these files to track the current implementation surface and working material:

- `state.md` — durable Vulcan resume snapshot
- `active.md` — current implementation queue and exit criteria
- `sessions/` — optional session notes for long-running implementation work
- `working/` — temporary or transitional implementation material
- `decisions/` — Vulcan-local implementation/workspace decisions
- `scratch/` — non-durable exploration notes

`working/` files are not active merely because they exist. Active work must be named in `active.md`.

## Durable output locations

- `docs/plans/` — implementation plans and filesystem-visible work items
- `docs/implementation/` — implementation reports and implementation-linked records
- `docs/process-capture/` — non-authoritative process chains
- `docs/AAR/` — process lessons and session closeout notes
- `src/`, `tests/`, config files — implementation patches and validation surfaces

## Current implementation loop

```text
ATHENA brief/spec
→ filesystem-visible work item
→ VULCAN implementation/report
→ ATHENA review
→ KOIOS process capture
→ next ATHENA brief if needed
```

HERMES may provide optional transport or command execution, but HERMES is not required by this process model.

## Canonical references

- `docs/agents/agent-charter.md`
- `docs/policies/workspace-layout.md`
- `docs/policies/python-coding.md`
- `docs/process-capture/workflow.process-capture.md`
- `docs/architecture/architecture.00.md`

## Python implementation control

- `docs/policies/python-coding.md` is Vulcan's draft Python coding control surface.
- New Python implementation SHOULD be self-reviewed against the Python coding rules before closeout.
- If a controlling implementation brief conflicts with the Python coding rules, preserve the brief's required behavior and record the conflict in the implementation report.
- Repeated exceptions or review findings SHOULD be captured as updates to `docs/policies/python-coding.md` before the policy is promoted.

## Implementation boundaries

- `docs/adr/` — durable architecture decisions. Read relevant ADRs before implementing when they apply.
- `docs/plans/` — implementation source artifacts. Vulcan may author and update implementation plans.
- `docs/implementation/` — implementation reports. Vulcan owns these.
- Draft ADRs may receive VULCAN comments on implementation feasibility, build cost, and verification gaps, but Vulcan does not promote or decide ADRs.
