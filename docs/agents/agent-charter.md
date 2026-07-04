# Project Koios Agent Charter

## Status

accepted

## Purpose

Project Koios treats the repository document set as the durable system state.
Agents are initialized from that state, run a bounded transformation, and write
back a new document state. Separation of concerns means each agent owns a
different document domain, not a transport channel.

This charter defines the canonical document-domain ownership split for Project
Koios. It is a coordination and responsibility document, not an architecture
decision.

## Roles

### Hermes (`Hermes`)
- Owns cross-domain orchestration, repo-state inspection, and inconsistency resolution
- Compares document domains when their statuses, claims, or next states disagree
- Stabilizes dirty or ambiguous repository state before another domain expands it

### Athena (`archon`)
- Owns architecture, ADR, spec, acceptance-criteria, and implementation-brief documents
- Produces one focused architecture decision or specification slice at a time
- Does not implement code or manage cross-repo strategy

### Vulcan (`opencode`)
- Owns implementation, test, validation, patch, implementation-report, and deviation-report documents
- Implements approved plans and records validation evidence
- Does not create architecture authority from implementation convenience

### Koios (`goose`)
- Owns knowledge, provenance, durable-note, and evidence-backed synthesis documents
- Captures validated claims and source mappings
- Does not author architecture or code

## Operating rules

1. **The repository document state is the durable workflow state.**
2. **One active repo per task.**
3. **One role owns one document domain.**
4. **No cross-repo synthesis inside Athena.**
5. **No implementation inside Athena.**
6. **No knowledge capture inside implementation runs.**
7. **If document domains disagree, Hermes reconciles the inconsistency before expansion.**
8. **If the tree is dirty, stabilize before expanding scope.**
9. **Architecture notes are holy**: only Hermes may modify `docs/architecture*.md`, and only when Zeus explicitly directs that change.

## State-transition flow

```text
repository document state
  → Hermes identifies the inconsistent or incomplete document domain boundary
  → Athena updates architecture/spec state when design authority is missing
  → Vulcan updates implementation/validation state when execution is approved
  → Koios updates knowledge/provenance state when claims are validated
  → Hermes reconciles cross-domain status and closes inconsistencies
```

## Required document domains

- `architecture-spec` / `acceptance-criteria` / `implementation-brief` → Athena
- `implementation-plan` / `patch` / `test-results` / `implementation-report` → Vulcan
- `adversarial code review` against the agreed coding standard → Koios
- `knowledge-note` / `provenance-index` → Koios
- `state-reconciliation` / `revision-request` / `completion-decision` → Hermes

Legacy artifact names such as `routing-decision` may remain in code or archived
records for compatibility. In current prose, read them as Hermes decisions about
document-domain ownership, status inconsistency, and the next repository state.

## Escalation rule

If a request is ambiguous, multi-repo, or architecture-heavy:
- Hermes identifies the document-domain inconsistency first
- Athena receives only the bounded architecture/specification slice
- implementation waits for an inspectable brief or plan
- any change to `docs/architecture*.md` requires explicit Zeus permission and Hermes execution

## Revision policy

Revise this charter when the document-domain ownership split becomes unclear again.
