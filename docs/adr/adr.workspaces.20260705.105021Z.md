```json
{
  "title": "Workspaces and Resume Control Surfaces",
  "artifact_type": "adr",
  "status": "accepted",
  "datetime": "20260705.105021Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "workspaces/",
  "canonical_location": "docs/adr/adr.workspaces.20260705.105021Z.md",
  "supersedes": [
    "docs/archive/architecture/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md",
    "docs/archive/architecture/adr/adr.canonical-workspace-state-next-action-protocol.draft.md"
  ],
  "source_artifacts": [
    "docs/archive/architecture/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md",
    "docs/archive/architecture/adr/adr.canonical-workspace-state-next-action-protocol.draft.md",
    "docs/policies/workspace-layout.md"
  ]
}
```

# ADR 20260705.105021Z: Workspaces and Resume Control Surfaces

## Status

accepted

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this ADR are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Provenance

Origin: user request to consolidate effective workspace ADR authority
From: user
Acting-As: ATHENA
Scope: projectkoios-bootstrap workspace control surfaces
Repository: projectkoios-bootstrap
Architecture-Domain: workspace layout and resume-control convention
Accepted-Location: `docs/adr/adr.workspaces.20260705.105021Z.md`
Supersedes:

- `docs/archive/architecture/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- `docs/archive/architecture/adr/adr.canonical-workspace-state-next-action-protocol.draft.md`

Source policy:

- `docs/policies/workspace-layout.md`

## Context

Project Koios treats the repository document set as durable workflow state. Role workspaces exist to preserve local operational continuity for Hermes, Athena, Vulcan, and Koios without turning workspace notes into project authority.

Prior workspace-state authority was split across an accepted canonical workspace-state ADR, a superseded draft, and the workspace layout policy. The effective purpose of `state.md` was clarified during Athena state cleanup: `state.md` is bootloader memory for a role workspace, not an ADR, review log, implementation report, or project authority.

The workspace contract needs one effective ADR surface that defines:

1. what each workspace MUST contain;
2. what `state.md` and `active.md` are for;
3. what they MUST NOT become;
4. how agents should resume without chat history;
5. how stale workspace state should be corrected.

## Decision

Project Koios bootstrap workspaces MUST use a role-local resume/control model.

Each role workspace MUST contain:

- `AGENTS.md`
- `state.md`
- `active.md`
- `decisions/`
- `working/`
- `scratch/`
- `sessions/`

The canonical live workspace-state surface is the pair:

- `state.md`
- `active.md`

The pair MUST be treated as one bounded control surface. Agents MUST NOT infer current workflow authority from scattered workspace notes, directory placement, chat history, or transport mechanics when the state pair is present.

Workspace files are local control surfaces only. They MUST NOT replace ADRs, architecture documents, implementation reports, validation results, knowledge notes, provenance indexes, or completion decisions.

## `state.md`

Each role workspace MUST maintain `state.md` as its local resume/control surface.

`state.md` is the effective cold-start state for that workspace. Its purpose is to preserve the minimum durable context needed for a new session to resume correctly without chat history.

`state.md` MUST record, at minimum:

- represented role;
- repository or scope;
- workspace path;
- document domain;
- current focus;
- blockers;
- validated durable facts relevant to resumption, each with a provenance pointer when available;
- active control surfaces;
- handoff status when relevant;
- next owner;
- unresolved questions or decisions;
- current status summary.

When `state.md` records a claim, it SHOULD identify whether the claim is a validated fact, a working assumption, or an unresolved question, and SHOULD link to the source artifact when one exists.

`state.md` MUST NOT be treated as project architecture authority, implementation authority, acceptance authority, validation evidence, or completion evidence.

When `state.md` conflicts with ADRs, implementation reports, reviews, schemas, policies, or other authoritative repository artifacts, the authoritative artifact wins and `state.md` MUST be corrected.

`state.md` MUST NOT duplicate full review, implementation, or chat history when durable artifacts already preserve that provenance. It MUST summarize current actionable state and link to ADRs, reviews, implementation reports, AARs, knowledge notes, or provenance indexes for detail.

When correcting stale state, agents SHOULD update only the state summary and preserve the authoritative source artifact unchanged unless separately authorized.

## `active.md`

`active.md` is the current priority filter and next-action surface.

`active.md` MUST record, at minimum:

- current priority stack;
- next action or next state transition;
- waiting-on list;
- explicitly active working material;
- ignored scope;
- exit criteria.

Files in `working/` MUST be treated as active only when named by `active.md`.

## Metadata

Both `state.md` and `active.md` MUST include a stable top JSON metadata section.

The metadata section SHOULD include these fields when applicable:

- `title`
- `artifact_type`
- `status`
- `datetime`
- `acting_as`
- `repository`
- `workspace`
- `document_domain`
- `control_files`
- `next_owner`
- `blockers`

Roles MAY add role-specific metadata fields, but MUST NOT remove the minimum human-readable sections needed to answer startup questions.

## Working material directories

Workspace-local notes MAY exist in `decisions/`, `working/`, `scratch/`, and `sessions/`.

Such notes MUST NOT become authoritative merely because of their location.

`decisions/` MAY hold agent-local decision notes. They are not authoritative until promoted into the appropriate repository document domain.

`working/` MAY hold current or transitional working material. Folder placement MUST NOT be treated as authority.

`scratch/` is temporary and non-authoritative. Useful material SHOULD be promoted or summarized elsewhere before relying on it.

`sessions/` MAY hold chronological session notes. Session notes are provenance only and MUST NOT replace the state pair.

## Startup order

Agents starting a session in a role workspace MUST:

1. read `state.md`;
2. read `active.md`;
3. inspect only relevant artifacts named by those files before expanding scope;
4. check focused repository status before editing;
5. choose the highest-leverage unblocked action consistent with role authority.

## Next-action selection

The next action SHOULD be selected using this priority order:

1. prefer actions that unblock multiple downstream tasks;
2. prefer actions that close the nearest decision boundary;
3. prefer actions that reduce ambiguity or rework;
4. prefer actions that restore workflow health before starting new work.

The leverage ranking is manually maintained in `active.md` for now. Automation MAY validate or compute it later, but computed ranking is not required by this ADR.

## Policy alignment

`docs/policies/workspace-layout.md` SHOULD reflect this ADR or point to it as the controlling decision.

If workspace layout policy and this ADR conflict, this ADR is the controlling architecture decision and the policy SHOULD be corrected.

## Consequences

- New sessions can resume from a small, explicit state surface.
- Role ownership and next-owner information are visible without rereading chat history or unrelated notes.
- Workspace files remain local control surfaces and do not replace authoritative repository artifacts.
- `active.md` becomes the only source for whether `working/` files are current.
- `state.md` remains concise because detailed provenance lives in ADRs, reviews, implementation reports, AARs, knowledge notes, and provenance indexes.
- The workspace layout can be validated with lightweight file/metadata checks.

## Acceptance criteria

- Each role workspace can identify its represented role, document domain, blockers, next owner, and next action from `state.md` and `active.md`.
- `state.md` and `active.md` include stable top JSON metadata sections.
- `state.md` summarizes current actionable state and links to durable provenance instead of duplicating full history.
- `active.md` explicitly names any active working material.
- The highest-leverage next action is derivable from the pair without chat history.
- Workspace files remain non-authoritative local control surfaces.

## Implementation brief

No implementation or bootstrap-validation authority is granted by this accepted ADR alone.

If a follow-on handoff is authorized separately, update or verify workspace guidance and bootstrap validation so:

- every role workspace has the required files and directories;
- workspace startup guidance names the `state.md` then `active.md` read order;
- `working/incoming/` and `working/outgoing/` are not used as authority surfaces;
- `docs/policies/workspace-layout.md` reflects this ADR;
- any bootstrap workspace initializer preserves the canonical pair.

## Resolved open questions

- The canonical live state surface is the pair `state.md` and `active.md`, not a single file and not scattered notes.
- Markdown with stable top JSON metadata is sufficient. A separate machine-readable companion is not required unless future automation proves the need.
- All workspaces share a minimum field set; roles may add optional fields.
- Leverage ranking is manual in `active.md`; future automation may validate or compute it.
- `state.md` is the effective cold-start state for a role workspace, not project authority.
- `state.md` MUST NOT duplicate full review, implementation, or chat history already preserved in durable artifacts.

## Non-goals

- Replacing ADRs, architecture documents, implementation reports, validation results, knowledge notes, provenance indexes, or completion decisions.
- Defining transport mechanics between role workspaces.
- Creating product architecture for Project Koios.
- Requiring a database-backed workspace-state store.
- Treating workspace notes as durable architecture authority.
- Authorizing implementation/bootstrap validation changes without a separate handoff.

## Validation expectations

- A new session can cold-start from `state.md` and `active.md` without chat history.
- A reviewer can identify whether claims in `state.md` are validated facts, working assumptions, or unresolved questions when that distinction matters.
- A reviewer can follow provenance links from `state.md` to authoritative artifacts.
- A reviewer can confirm `state.md` summarizes outcomes rather than duplicating durable review/implementation history.
- Startup/stop checks can verify required workspace files and directories exist.

## Links

- supersedes: `docs/archive/architecture/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- supersedes: `docs/archive/architecture/adr/adr.canonical-workspace-state-next-action-protocol.draft.md`
- related_policy: `docs/policies/workspace-layout.md`
- related_architecture: `docs/architecture/architecture.canonical-workspace-state-and-next-action-protocol.md`
- compatibility_pointer: `docs/workspaces.md`
