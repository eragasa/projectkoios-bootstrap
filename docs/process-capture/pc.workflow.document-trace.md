# Process capture: workflow document trace

## Metadata

- Type: process-capture-index
- Status: active-observation
- Repository: projectkoios-bootstrap
- Scope: workflow document traces mapped to Petri-net evolution vocabulary
- Owner: KOIOS
- Created: 20260706.025408Z
- Updated: 20260708.044950Z
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

The workflow adapter topology-roundtrip slice has enough durable repository
evidence to trace most of the document evolution, but its revised ATHENA brief
exists only as intercom/user clarification rather than a standalone durable
implementation brief.

The template representation round-trip slice has a cleaner filesystem-visible
chain: durable ATHENA brief, reported user approval, VULCAN implementation
report, VULCAN AAR, VULCAN workspace state, and KOIOS trace. Its main remaining
gaps are that user approval is currently cited through VULCAN's AAR rather than a
separate durable approval artifact, and ATHENA conformance review has not yet
been recorded.

## Observed cause of behavior/gap

The adapter slice changed during active implementation after user clarification
made topology-only bidirectional round-trip equivalence the concrete acceptance
shape. The clarification was operationally sufficient for VULCAN and ATHENA to
continue, but it remained in intercom/user context instead of being materialized
as a standalone ATHENA brief.

As a result, later artifacts cite an intercom-only revised brief. The document
chain is still intelligible because implementation and review documents name the
brief content, but provenance is weaker than it would be with a durable brief.

## Process review observations

### Template representation round-trip boundary review

KOIOS reviewed the pre-implementation handoff for the template representation
round-trip slice at
`docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`.
The review found that `src/python/projectkoios/bootstrap/template_representation/`
is the appropriate bounded package for bootstrap template representation code
because it remains beside existing bootstrap schema code and avoids silently
creating broad ingestion or product-template architecture authority.

The review also found that `docs/plans/` is an acceptable location for the
ATHENA implementation brief and `docs/implementation/` is the correct location
for the VULCAN implementation report. The first live source fixture may be
`docs/templates/ADR.proposal.template.md`, but generated/golden/malformed test
fixtures should live under `tests/projectkoios/bootstrap/template_representation/`
unless the task explicitly changes canonical template documents.

Provenance cautions:

- implementation should proceed only after explicit user approval because the
  brief is implementation-ready only after approval;
- the active authority is `docs/adr/adr.templates.md`; draft/proposal inputs are
  provenance only and must not be silently promoted;
- this first slice should be described as one-fixture bootstrap template
  representation round-trip, not broad ingestion, all-template validation, or
  template enforcement activation;
- after VULCAN report and ATHENA conformance review, KOIOS may add a partial
  process trace if the user wants this slice mapped into the document-evolution
  chain.

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
- Pre-implementation package-boundary reviews should name whether a proposed
  code location preserves or expands authority boundaries before VULCAN writes
  code.
- VULCAN implementation reports should continue naming controlling ADRs,
  source briefs, validation commands, explicit non-changes, and residual risks.
- VULCAN reports for representation slices should distinguish live source
  fixtures, test-only golden fixtures, and generated outputs so canonical
  document surfaces are not silently rewritten.
- KOIOS should keep trace documents non-authoritative unless the pattern is
  promoted through the appropriate owner.

## Partial traces

| Trace | Scope | Status | Primary gap |
|---|---|---|---|
| `docs/process-capture/pc.workflow.document-trace.20260706.025408Z.md` | workflow adapter topology-only SNAKES round trip | captured | ATHENA revised brief is intercom-only |
| `docs/process-capture/pc.workflow.document-trace.20260708.044950Z.md` | template representation one-fixture Markdown/JSON round trip | captured | user approval cited through VULCAN AAR; ATHENA conformance review not yet recorded |
