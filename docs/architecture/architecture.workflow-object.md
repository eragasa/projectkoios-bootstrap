```json
{
  "title": "Workflow Object Architecture",
  "artifact_type": "architecture-note",
  "status": "accepted",
  "datetime": "20260711.093600Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "bootstrap workflow-object first record architecture",
  "canonical_location": "docs/architecture/architecture.workflow-object.md",
  "source_requirements": "docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md",
  "source_process_capture": "docs/process-capture/pc.aar-consolidation.20260711.091607Z.md",
  "source_intake_review": "docs/reviews/architecture-intake.20260711.092400_workflow-object-aar-synthesis.md"
}
```

# Architecture: Workflow Object

## Status

Accepted for the first workflow-object architecture slice by USER option 1 on `20260711.093600Z`.

This document promotes selected KOIOS AAR-synthesis requirements into ATHENA architecture language. It does not authorize implementation, storage, schema, CLI, UI, database, or live orchestration work.

## Source intake and authority boundary

Primary intake artifacts:

- `docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md`
- `docs/process-capture/pc.aar-consolidation.20260711.091607Z.md`
- `docs/reviews/architecture-intake.20260711.092400_workflow-object-aar-synthesis.md`

KOIOS process-capture artifacts remain provenance/advisory. The KOIOS AAR consolidation and requirements draft are process provenance only until explicitly promoted by the appropriate owner. This architecture document is the first ATHENA-owned promotion surface.

The AAR consolidation's 298-entry source index preserves source coverage at synthesis time. Its theme labels are advisory/coarse observations, not a canonical taxonomy.

Source artifacts remain authoritative in their own domains:

- ATHENA-owned ADRs, architecture notes, specifications, and implementation briefs remain architecture/spec authority.
- VULCAN-owned implementation reports, validation outputs, and patches remain implementation evidence authority.
- KOIOS-owned process capture and provenance notes remain provenance/process evidence authority.
- HERMES/user decisions remain orchestration, routing, closeout, and completion authority where cross-domain state is involved.

A workflow object may index, project, summarize, and record evidence for those artifacts. It must not own, replace, or decide their authority.

## Purpose

A workflow object is a durable summary/projection of one bounded work item as it moves through role-owned artifacts, transition gates, validation evidence, previews, reviews, and authority boundaries.

It exists to make cross-session workflow state inspectable without relying on hidden chat history or terminal-local context.

## Non-purpose

A workflow object is not:

- source authority replacing architecture notes, ADRs, implementation plans, reports, reviews, AARs, `state.md`, or `active.md`;
- a live orchestrator;
- a Petri-net runtime;
- a database persistence decision;
- a JSON schema decision;
- a UI/operator-console feature;
- a bulk historical AAR backfill requirement;
- a cross-repo product authority mechanism;
- a skill lifecycle implementation.

A workflow object must point back to source artifacts rather than absorbing their authority.

## First proving case

The first workflow-object record should model the accepted Operator Console P0/P1 work because it contains a complete bounded-work trail with preview evidence and fixture provenance. This does not mean Operator Console UI support is required by workflow objects.

- architecture: `docs/architecture/architecture.operator-console.md`
- implementation plans/briefs:
  - `docs/plans/implementation-plan.20260711.073912_operator-console-review-one-proposal-fixture.md`
  - `docs/plans/implementation-plan.20260711.084907_operator-console-fixture-interaction-visibility.md`
- implementation reports:
  - `docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md`
  - `docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md`
- conformance reviews:
  - `docs/reviews/architecture-conformance.20260711.081734_operator-console-review-one-proposal-fixture.md`
  - `docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md`
  - `docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md`
- AARs and process lessons;
- validation evidence;
- user preview evidence.

## Requirement triage

First-pass architecture concepts:

- R1 Work item identity and source packet.
- R2 Artifact node model.
- R3 Transition/gate model.
- R4 Role-domain guard.
- R5 Approval and pause state.
- R6 Validation evidence record.
- R8 Non-authority and lifecycle markers.
- R10 User-preview validation record.
- R11 Ephemeral-message promotion rule.
- R12 Dependency/tooling decision record.
- R14 Process-capture observation link.

Split/defer before implementation:

- R7 Dirty-tree/package boundary record: defer full closeout/packaging modeling to an extension, but preserve a minimal `dirty_state_summary`, `packaging_status`, or `not_modeled_yet` field so the source lesson is not lost.
- R9 Full fixture/sidecar provenance record: include minimal source path/hash/authority-boundary fields in first slice; defer omitted-field/sidecar-depth modeling.
- R13 Skill/reusable-procedure stability record: defer to a skill/procedure workflow-object extension; preserve the general principle that file presence alone is not validation evidence.

Rejected requirements:

- None. Deferred items are staging decisions, not rejections.

## Minimal first record shape

The first workflow object should be a single static record for one completed work item. Its storage format is not decided here; field names below define architecture vocabulary, not final schema syntax.

### Work item identity

The record should include:

- stable work item id;
- title;
- slice/work item name;
- initiating request or source packet summary;
- repository;
- workspace when relevant;
- represented role for the current record producer;
- created timestamp;
- status;
- non-authority statement.

### Artifact nodes

Each artifact node should include:

- path or locator;
- artifact type;
- owner role/domain;
- status;
- authority boundary;
- source hash when useful and cheap;
- created/updated timestamp when known;
- links to prior/consumed artifacts when relevant.

Artifact nodes represent source artifacts; they do not replace those artifacts.

### Transition/gate records

A transition/gate record should include:

- transition name;
- actor role;
- consumed artifact references;
- produced artifact references;
- approval source when applicable;
- pause/blocker state when applicable;
- timestamp or observed ordering;
- notes about scope boundaries.

Initial transition vocabulary:

- intake;
- architecture;
- brief;
- plan;
- approval;
- implementation;
- validation;
- report;
- conformance-review;
- preview;
- process-capture;
- closeout.

This vocabulary is provisional for the first record and should not be treated as global workflow policy yet.

### Role-domain guard

The record should preserve role/domain boundaries by marking which role owns each artifact and transition.

It should flag or describe any case where an artifact could be mistaken as another domain's authority, for example:

- implementation report interpreted as architecture change;
- KOIOS process capture interpreted as policy;
- fixture/demo state interpreted as live product state;
- user preview interpreted as activation authority.

### Approval and pause state

Approval and pause state should be modeled separately from file existence.

Initial states:

- approval-required;
- paused;
- approved;
- rejected;
- implemented;
- validated;
- reviewed;
- accepted;
- superseded.

The first record should only use states evidenced by source artifacts.

### Validation evidence

Validation evidence should include:

- command;
- working directory;
- target scope;
- summarized result;
- pass/fail/non-applicable status;
- validator limitations if reported;
- timestamp or source report timestamp;
- source report path.

Implementation-level command details remain VULCAN-owned when produced by implementation reports.

### Preview evidence

For UI/operator-facing slices, preview evidence should include:

- preview command;
- local URL or preview method;
- inspected surface;
- user-visible question or behavior being validated;
- observed user feedback;
- whether feedback changed scope.

Preview evidence is review evidence, not product activation authority.

### Non-authority and lifecycle markers

The first record should support markers such as:

- draft;
- proposal;
- incubating;
- fixture-only;
- generated;
- sidecar;
- archived;
- superseded;
- non-authoritative;
- accepted;
- active;
- implemented-without-architecture-promotion.

For the first Operator Console record, fixture/static/non-live markers are required.

### Dirty-state and packaging hook

Full dirty-tree/package-boundary modeling is deferred, but the first record should include a minimal hook such as:

- dirty state summary;
- packaging status;
- unrelated dirty-state note;
- explicit `not_modeled_yet` marker when closeout details are intentionally absent.

This prevents the dirty-tree AAR lesson from being lost while avoiding a broad closeout model in the first slice.

### Fixture/sidecar provenance hook

Full fixture/sidecar provenance modeling is deferred, but the first record should include minimal fields where fixture or generated artifacts matter:

- source path or locator;
- source hash when useful and cheap;
- generated/projection hash when useful and cheap;
- authority boundary;
- freshness/stale marker;
- transformation note.

### Dependency/tooling decision references

Dependency/tooling decisions should record:

- package-local vs repo-wide scope;
- draft guidance vs accepted policy;
- package manager/lockfile status;
- audit/security findings;
- whether the choice is implementation convenience, architecture baseline, or product decision.

### Process-capture links

The record may link to KOIOS process-capture observations and AARs.

Those links remain advisory unless another owner promotes them into architecture, policy, or implementation authority.

### Skill/procedure stability hook

Skill and reusable-procedure lifecycle is deferred. The first record may still record the general rule that file presence alone is not validation evidence; stable skill/procedure authority requires explicit status, validation evidence, and owning review in a later extension.

## Representative evidence mapping

The architecture note does not inline all 298 AAR sources. Representative evidence from KOIOS synthesis includes:

| Theme | Requirements | Representative AARs |
|---|---|---|
| Durable state and source packets | R1-R3 | `aar.20260702.020601_canonical-workspace-state-protocol.md`, `aar.20260705.111255_workspace-adr-consolidation.md`, `aar.20260708.041331_template-representation-vulcan-handoff.md` |
| Authority guard and non-authority markers | R4, R8, R14 | `aar.20260701.014145_promotion-review-routing.md`, `aar.20260702.023544_koios-comment-attribution-correction.md`, `aar.20260705.142149_petrinet-separation-adr-remediation.md` |
| Approval, pause, and ephemeral-message promotion | R5, R11 | `aar.20260702.205545_prompt-iterate-vulcan-blocker-handling.md`, `aar.20260709.014124_adr-json-database-pilot-brief.md`, `aar.20260706.045501_workflow-adapter-contract-hardening.md` |
| Validation evidence | R6 | `aar.20260704.193035_python-policy-validator-first-slice.md`, `aar.20260705.173808_petrinet-followups.md`, `aar.20260711.081405_operator-console-review-one-proposal-fixture.md` |
| Fixture/sidecar provenance hook | R9 | `aar.20260711.035759_adr-json-database-one-adr-pilot.md`, `aar.20260711.065704_json-schemas-adr-conformance.md`, `aar.20260711.081405_operator-console-review-one-proposal-fixture.md` |
| User preview | R10 | `aar.20260711.081405_operator-console-review-one-proposal-fixture.md`, `aar.20260711.090601_operator-console-fixture-interaction-visibility.md` |
| Dirty-tree/package boundary deferred hook | R7 | `aar.20260701.053127_dirty-tree-review.md`, `aar.20260702.052145_blind-commit-all-scope.md`, `aar.20260705.101124_violation-formatting-test-policy-remediation.md` |
| Skill/procedure stability deferred hook | R13 | `aar.20260709.010343_template-record-roundtrip-skill-brief.md`, `aar.20260709.010828_koios-comments-skill-brief-update.md`, `aar.20260709.012011_template-record-roundtrip-skill.md` |

## First implementation candidate after architecture approval

After this architecture note is reviewed and accepted, a later VULCAN implementation slice may create exactly one static workflow-object example for the accepted Operator Console P0/P1 work.

Suggested implementation boundaries:

- place the example under an explicitly non-authoritative fixture/dev path;
- reference existing artifacts by path and hash;
- do not mutate source artifacts;
- do not create repository-wide workflow state;
- do not create storage/database authority;
- validate that referenced paths exist and hashes match if feasible.

Implementation requires a separate implementation brief/plan and approval.

## Open questions

- Should the first record be Markdown, JSON, or both?
- Which transition names become canonical beyond the first record?
- Which gates are mandatory for all work items and which are artifact-type-specific?
- Should preview be a generic transition or UI-specific transition?
- How should a workflow object relate to `state.md` and `active.md` without replacing them?
- Who can mark a workflow object complete when architecture, implementation, provenance, preview, and packaging are involved?

## Acceptance criteria for this architecture slice

This architecture slice is complete when:

1. this note exists at `docs/architecture/architecture.workflow-object.md`;
2. it cites KOIOS intake as non-authoritative provenance;
3. it defines workflow object purpose and non-purpose;
4. it defines a minimal first record boundary;
5. it triages R1-R14;
6. it names Operator Console P0/P1 as the first proving case;
7. it states implementation is not authorized without a separate plan/approval;
8. it preserves source artifacts as authority and workflow object as projection/index.

## Next owner

- HERMES/USER: decide whether to proceed to an implementation brief.
- ATHENA: may write the bounded implementation brief for one static Operator Console workflow-object record if directed.
- VULCAN: wait for accepted implementation brief/plan before building schema, fixtures, storage, CLI, or UI support.
- KOIOS: preserve provenance and review any later claim mappings.

## Review record

- `docs/reviews/architecture-review.20260711.093600_workflow-object-architecture-first-record.md`
