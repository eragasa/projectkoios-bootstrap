# Process capture: workflow document trace

## Metadata

- Type: process-capture-index
- Status: active-observation
- Repository: projectkoios-bootstrap
- Scope: workflow document traces mapped to Petri-net evolution vocabulary
- Owner: KOIOS
- Created: 20260706.025408Z
- Updated: 20260706.025408Z
- Authority: provenance/process observation only

## Non-authority statement

This document is a KOIOS process-capture index. It records observed document-state
movement using Petri-net vocabulary as a provenance and knowledge-management
lens.

It does not create architecture authority, implementation authority, workflow
policy, product Petri-net semantics, validator requirements, completion status,
or a required document schema. Any promotion of this pattern into policy,
architecture, skill, schema, or implementation work requires the normal owning
surface.

## Formal workflow model

The current repository workflow model is document-state based:

- the repository document set is the durable workflow state;
- roles own separate document domains;
- state advances by creating the next bounded artifact and linking it backward to
  prior artifacts;
- architecture/spec/brief authority belongs to ATHENA;
- implementation, tests, validation, and implementation reports belong to
  VULCAN;
- knowledge, provenance, durable notes, and process capture belong to KOIOS;
- cross-domain inconsistency or completion decisions belong to HERMES/user
  orchestration.

Source surfaces:

- `docs/agents/agent-charter.md`
- `docs/meta-harness.md`
- `docs/process-capture/README.md`
- `docs/process-capture/workflow.process-capture.md`
- `docs/process-capture/schema.process-chain.md`

In Petri-net terms for process observation only:

- a place is an observable document/process state;
- a transition is an observed event that consumes one document/process state and
  produces another;
- a token is the bounded work item as represented by durable artifacts;
- evidence is the repository artifact proving the observed state or transition.

## What is actually happening

The current workflow adapter topology-roundtrip slice has enough durable
repository evidence to trace most of the document evolution:

1. accepted controlling ADR exists;
2. ATHENA/user revised brief exists only as intercom/user clarification rather
   than a standalone durable implementation brief;
3. VULCAN implementation report records the implemented and validated slice;
4. ATHENA conformance review records pass-with-nonblocking-documentation-note;
5. VULCAN AAR records process issues and follow-up candidates;
6. VULCAN workspace state records the current implementation status and next
   expected owners.

The trace therefore has one important gap: the revised ATHENA brief that shaped
implementation acceptance is not durable as its own filesystem artifact.

## Observed cause of behavior/gap

The adapter slice changed during active implementation after user clarification
made topology-only bidirectional round-trip equivalence the concrete acceptance
shape. The clarification was operationally sufficient for VULCAN and ATHENA to
continue, but it remained in intercom/user context instead of being materialized
as a standalone ATHENA brief.

As a result, later artifacts cite an intercom-only revised brief. The document
chain is still intelligible because implementation and review documents name the
brief content, but provenance is weaker than it would be with a durable brief.

## Recommendations

### Workflow model

- Keep the filesystem-visible document chain as the formal workflow state.
- Do not treat intercom/chat clarification as durable authority when a slice's
  acceptance criteria materially change.
- Require a standalone ATHENA brief or brief addendum when implementation scope
  changes mid-slice.

### Visibility into document tracing

- Add process-trace captures after validated multi-role slices where a bounded
  document chain exists.
- Keep partial trace files in `docs/process-capture/` using names such as
  `pc.workflow.document-trace.<datetime>.md`.
- Link each partial trace from this aggregate index.

### Document formats

- Preserve a source-artifact table, observed places table, observed transitions
  table, token trace, provenance gaps, and interpretation limits in each partial
  trace.
- If repeated examples stabilize the format, propose a reusable
  `docs/process-capture/schema.workflow.document-trace.md` or equivalent schema.

### Related workflow/process surfaces

- ATHENA should materialize brief changes that become implementation acceptance
  criteria.
- VULCAN implementation reports should continue naming controlling ADRs,
  source briefs, validation commands, explicit non-changes, and residual risks.
- KOIOS should keep trace documents non-authoritative unless the pattern is
  promoted through the appropriate owner.

## Partial traces

| Trace | Scope | Status | Primary gap |
|---|---|---|---|
| `docs/process-capture/pc.workflow.document-trace.20260706.025408Z.md` | workflow adapter topology-only SNAKES round trip | captured | ATHENA revised brief is intercom-only |
