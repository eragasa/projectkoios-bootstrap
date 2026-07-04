```json
{
  "title": "Canonical Workspace State and Next-Action Protocol",
  "artifact_type": "adr-proposal",
  "status": "proposal-superseded-by-accepted-adr",
  "datetime": "20260704.162218Z",
  "dcn": "ADR-CANONICAL-WORKSPACE-STATE-NEXT-ACTION-PROTOCOL-20260704.162218Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "workspaces/",
  "supersedes": "docs/adr/adr.canonical-workspace-state-next-action-protocol.draft.md",
  "back_to": "docs/architecture/architecture.canonical-workspace-state-and-next-action-protocol.md",
  "accepted_adr": "docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md",
  "next_phase": "retained as proposal review provenance"
}
```

# ADR 20260704.162218Z: Canonical Workspace State and Next-Action Protocol

## Status

proposal-superseded-by-accepted-adr

## Context

Origin: user request and Athena workspace-state consolidation
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap workspace control surfaces
Repository: projectkoios-bootstrap
Architecture-Domain: workflow/control-surface

Project Koios treats repository documents as durable workflow state, while role
workspaces provide local control surfaces for resuming bounded agent runs. The
existing workspace state convention was partially implemented through
`state.md`, `active.md`, local decisions, AARs, and workspace guidance, but the
canonical contract needed one proposed review surface.

The protocol must make a new session able to identify, without chat history:

1. represented role and document domain
2. current validated state
3. blockers and waiting-on items
4. explicitly active working material
5. the highest-leverage next action and its owner
6. ignored scope

## Decision

Adopt a canonical live workspace-state surface for each role workspace.

The canonical surface is the pair of files at the workspace root:

- `state.md`
- `active.md`

The pair MUST be treated as one bounded control surface. Agents MUST NOT infer
current workflow authority from scattered workspace notes, directory placement,
chat history, or transport mechanics when the state pair is present.

### `state.md`

`state.md` is the durable resume snapshot for the workspace. It MUST record, at
minimum:

- represented role
- repository or scope
- workspace path
- document domain
- current focus
- blockers
- validated current state or last validated document-state change
- handoff status when relevant
- next owner
- open questions or decisions
- current status summary

### `active.md`

`active.md` is the current priority filter and next-action surface. It MUST
record, at minimum:

- current priority stack
- next action or next state transition
- waiting-on list
- explicitly active working material
- ignored scope
- exit criteria

### Metadata

Both files MUST include a stable top JSON metadata section.

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

Roles MAY add role-specific metadata fields, but MUST NOT remove the minimum
human-readable sections needed to answer startup questions.

### Working material

Workspace-local notes MAY exist in `decisions/`, `working/`, `scratch/`, and
`sessions/`.

Such notes MUST NOT become authoritative merely because of their location.

Files in `working/` MUST be treated as active only when named by `active.md`.

`scratch/` is temporary and non-authoritative.

### Startup order

Agents starting a session in a role workspace MUST:

1. read `state.md`
2. read `active.md`
3. inspect only relevant artifacts named by those files before expanding scope
4. check focused repository status before editing
5. choose the highest-leverage unblocked action consistent with role authority

### Next-action selection

The next action SHOULD be selected using this priority order:

1. prefer actions that unblock multiple downstream tasks
2. prefer actions that close the nearest decision boundary
3. prefer actions that reduce ambiguity or rework
4. prefer actions that restore workflow health before starting new work

The leverage ranking is manually maintained in `active.md` for now. Automation
MAY validate or compute it later, but computed ranking is not required for this
proposal.

## Consequences

- New sessions can resume from a small, explicit state surface.
- Role ownership and next-owner information are visible without rereading chat
  history or unrelated notes.
- Workspace files remain local control surfaces and do not replace ADRs,
  implementation reports, validation results, or knowledge notes.
- `active.md` becomes the only source for whether `working/` files are current.
- The protocol can be validated with lightweight file/metadata checks.
- Roles can specialize their state files without breaking a shared minimum
  startup contract.

## Acceptance criteria

- Each workspace can name its role, document domain, blockers, next owner, and
  next action from `state.md` and `active.md`.
- `state.md` and `active.md` include stable top JSON metadata sections.
- `active.md` explicitly names any active working material.
- The highest-leverage next action is derivable from the pair without chat
  history.
- The pair remains small enough for routine session updates.
- The protocol works for quiet sessions, active implementation sessions, review
  sessions, and handoff-heavy sessions.

## Implementation brief

If accepted, update or verify workspace guidance and bootstrap validation so:

- every role workspace has `AGENTS.md`, `state.md`, `active.md`, `decisions/`,
  `working/`, `scratch/`, and `sessions/`
- workspace startup guidance names the `state.md` then `active.md` read order
- `working/incoming/` and `working/outgoing/` are not used as authority surfaces
- `docs/policies/workspace-layout.md` reflects this protocol or points to this
  ADR as the controlling decision
- any bootstrap workspace initializer preserves the canonical pair

## Resolved open questions

- The canonical live state surface is the pair `state.md` and `active.md`, not a
  single file and not scattered notes.
- Markdown with stable top JSON metadata is sufficient. A separate
  machine-readable companion is not required unless future automation proves the
  need.
- All workspaces share a minimum field set; roles may add optional fields.
- Leverage ranking is manual in `active.md`; future automation may validate or
  compute it.

## Non-goals

- Replacing ADRs, architecture documents, implementation reports, validation
  results, or knowledge notes.
- Defining transport mechanics between role workspaces.
- Creating product architecture for Project Koios.
- Requiring a database-backed workspace-state store.
- Treating workspace notes as durable architecture authority.

## Validation expectations

- A new session can answer the startup checklist in one pass through
  `state.md` and `active.md`.
- The next owner is explicit when the current role cannot complete the next
  step.
- A validator can check the presence of the files, top JSON metadata, required
  directories, and absence of deprecated working mailbox directories.

## Routing

- Owner: Athena
- Current phase: proposal superseded by accepted ADR
- Accepted ADR: `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- Notes: This proposal is retained as review provenance only. The canonical authority surface is the accepted ADR in `docs/adr/`.

## Links

- back_to: `docs/architecture/architecture.canonical-workspace-state-and-next-action-protocol.md`
- supersedes: `docs/adr/adr.canonical-workspace-state-next-action-protocol.draft.md`
- superseded_by: `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- related_policy: `docs/policies/workspace-layout.md`
- compatibility_pointer: `docs/workspaces.md`
