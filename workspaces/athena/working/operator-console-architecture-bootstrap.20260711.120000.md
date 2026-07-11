```json
{
  "title": "Project Koios Operator Console Architecture Bootstrap",
  "artifact_type": "architecture-spec-and-implementation-brief",
  "status": "handoff-draft-for-mothership-placement",
  "datetime": "20260711.120000Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "target_repository": "projectkoios-bootstrap incubation, then projectkoios",
  "target_path": "src/typescript/projectkoios/ui/operator-console/docs/architecture/operator-console.md during incubation; projectkoios/ui/operator-console/docs/architecture/operator-console.md after extraction",
  "bootstrap_role": "incubator and first fixture/provider/source only; not final product UI owner"
}
```

# Project Koios Operator Console Architecture Bootstrap

## Status

Handoff draft for placement in the Project Koios mothership/product repository.

Recommended incubation path:

- `src/typescript/projectkoios/ui/operator-console/docs/architecture/operator-console.md`

Recommended extraction/product path:

- `projectkoios/ui/operator-console/docs/architecture/operator-console.md`

This document is authored from `projectkoios-bootstrap` as ATHENA bootstrap/spec work. During incubation, `projectkoios-bootstrap/src/typescript/projectkoios/ui/operator-console/` may host the first implementation slice and fixtures. It is not final product UI authority until extracted or accepted in the mothership/product document domain.

## Purpose

Define the first bounded architecture/spec slice for a Project Koios Operator Console: a browser-based operator surface that can eventually monitor agents, review proposed changes with evidence, inspect external system status, and propose workflow definition changes without directly mutating active workflows.

## Authority boundary

Bootstrap may provide early fixtures, adapters, and example evidence from current harness artifacts.

Bootstrap may provide:

- fixture-backed agent status and message/thread examples;
- fixture-backed change proposals from repository artifacts, implementation reports, AARs, validation outputs, and sidecar evidence;
- mock external system status providers;
- sample workflow definition references and draft/proposal fixtures;
- read-only integration stubs for intercom/session status and validation reports.

Bootstrap must not own:

- final product UI architecture;
- final UX policy;
- canonical Project Koios workflow semantics;
- production deployment/runtime topology;
- durable cross-repo authority rules;
- active workflow mutation authority.

The incubation implementation home is:

- `projectkoios-bootstrap/src/typescript/projectkoios/ui/operator-console/`

The long-term extracted implementation home remains:

- `projectkoios/ui/operator-console/`

Recommended incubation package layout:

```text
src/typescript/projectkoios/ui/operator-console/
  docs/architecture/operator-console.md
  src/                 # TypeScript application and contracts
  fixtures/            # deterministic bootstrap-derived fixture data
  www/                 # browser entry/static public surface for local preview
  package.json         # if this is a standalone package during incubation
```

`www/` is appropriate as the human/browser entry surface for static assets and local preview. It should not contain generated build output unless the chosen build tool explicitly treats it as disposable. If a tool such as Vite is selected, `public/` may replace `www/`; the architecture requirement is a clearly separated web/static entry surface, not the literal folder name.

## Product direction

The long-term Operator Console should be a browser/TypeScript application. A TUI may exist later only as a diagnostic client over the same backend/read models. Browser UI and TUI must not be built in parallel for the first slice.

The console should eventually provide one operator point for:

1. monitoring and communicating with all agents;
2. making user interactions at any agent terminal visible from the central console without replacing those terminals;
3. reviewing changes in a three-panel layout: current / proposed / why-evidence;
4. quickly inspecting external system status;
5. proposing Petri-net workflow definition edits with validation and explicit activation/versioning, never direct active mutation.

## Architectural principles

### Proposal-oriented operations

The console displays current state and proposed state as separate immutable references. Any mutation-capable operation produces a proposal, validation result, or activation request. Direct mutation of active workflow definitions is out of scope.

### Immutable review references

Review and activation surfaces should use immutable refs and content hashes for current state, proposed state, and evidence. API transport shape may be REST, typed RPC, or another product decision later; the first slice should stabilize contracts before transport.

### Read-model first

The first implementation should prove read models and fixture providers before live adapters. Bootstrap fixtures are allowed as early providers, but product code must avoid filesystem-path-coupled assumptions that make bootstrap a long-lived backend.

### Multi-surface interaction visibility

The console should not replace local/native agent terminals or force all interaction through the browser. Agent terminals remain valid interaction surfaces. The console consumes an interaction/event stream, transcript projection, or read model from each terminal/session and displays it centrally.

This requires a provider/event boundary: terminal sessions publish or expose `AgentMessage`, `AgentThread`, or `AgentInteraction` events; the console reads them through adapters/read models. Future console-originated sends must go through the same agent communication substrate rather than coupling directly to terminal processes.

P0 remains fixture-only unless explicitly approved otherwise. However, P0 contracts and fixtures must preserve the distinction between terminal-originated and console-originated interactions.

### Browser first

The durable operator console is browser/TypeScript. TUI surfaces, if later needed, consume the same contracts/read models and remain diagnostic.

### Validation before activation

Workflow proposal validation must distinguish:

- syntax validity;
- semantic workflow validity;
- operational activation safety.

Activation/versioning requires explicit approval gates and is not part of the first implementation slice.

## Minimal contract set

The first contract package should define at least these domain contracts. Field names are illustrative; implementation may refine them while preserving semantics.

### AgentStatus

Represents one known agent/session/harness status.

Required semantics:

- stable agent/session identifier;
- display name or role identity;
- represented role when known;
- workspace/repository scope when known;
- current lifecycle/status indicator;
- last-seen timestamp or freshness marker;
- optional current activity summary;
- source/evidence reference.

### AgentMessage / AgentThread / AgentInteraction

Represents operator-visible communication history, terminal interaction snapshots, or pending requests.

Required semantics:

- immutable message or interaction identifier;
- thread identifier;
- session identifier;
- source surface such as terminal, console, automation, or imported transcript;
- origin direction such as terminal-originated or console-originated;
- sender/recipient identifiers;
- represented role identity when known;
- timestamp;
- body/summary;
- delivery/status such as observed, sent, received, pending, answered, failed;
- evidence/source reference;
- transcript/read-model locator when derived from a terminal/session stream.

### ChangeProposal

Represents a proposed change with current/proposed/evidence refs for review.

Required semantics:

- proposal identifier;
- proposal type/kind;
- title/summary;
- current state ref;
- proposed state ref;
- why/evidence refs;
- author/source;
- validation status summary;
- activation eligibility/status;
- created/updated timestamps.

### EvidenceRef

Represents cited evidence used to justify or validate a proposal.

Required semantics:

- evidence identifier;
- evidence kind such as implementation-report, validation-output, AAR, source-file, sidecar, external-status, agent-message;
- immutable locator or content hash;
- human summary;
- source timestamp/freshness;
- trust/provenance notes.

### ExternalSystemStatus

Represents a compact status card for an external system.

Required semantics:

- system identifier;
- display name;
- status class such as healthy, degraded, down, unknown;
- freshness/last-checked timestamp;
- summary;
- evidence/source refs;
- optional action/deep-link metadata.

### WorkflowDefinitionRef

Represents a read-only reference to a workflow definition.

Required semantics:

- workflow identifier;
- version/ref;
- content hash;
- status such as active, draft, archived, unknown;
- source locator;
- summary;
- validation state if available.

### WorkflowDraft / WorkflowProposal

Represents proposed workflow text/JSON changes.

Required semantics:

- draft/proposal identifier;
- base WorkflowDefinitionRef;
- proposed content ref/hash;
- author/source;
- validation results;
- activation intent/status;
- created/updated timestamps.

### ValidationResult

Represents validation evidence for proposals.

Required semantics:

- validation identifier;
- target ref/proposal id;
- status such as pending, passed, failed, warning;
- validation category: syntax, semantic, operational-safety, policy;
- findings;
- command/tool/source metadata;
- timestamp/freshness;
- evidence refs.

## Recommended implementation sequence

1. Contract definitions + fixture provider.
2. Read-only browser shell: agent monitor + external status cards.
3. ChangeReview three-panel for static fixture-backed proposals.
4. Validation result display.
5. Workflow definition read-only viewer.
6. Workflow proposal creation from text/JSON edits.
7. Current/proposed/why review for workflow proposals.
8. Activation/versioning service with explicit approval gates.
9. Visual Petri-net graph editor.

## First implementation slice

### Slice name

`operator-console-contracts-change-review-fixture`

### Goal

Create a TypeScript/browser Operator Console skeleton under `projectkoios-bootstrap/src/typescript/projectkoios/ui/operator-console/` with shared contracts, a fixture provider, and one three-panel `ChangeReview` view for a static proposal. This proves the current/proposed/why-evidence contract boundary before live workflow editing, activation, or graph editor work, while preserving a clean extraction path to `projectkoios/ui/operator-console/`.

### Scope

In scope:

- TypeScript contract definitions for the minimal contract set above.
- Fixture provider returning static examples for:
  - one `AgentStatus`;
  - one `ExternalSystemStatus`;
  - one `ChangeProposal`;
  - current/proposed content refs;
  - at least one `EvidenceRef`;
  - one `ValidationResult`.
- Browser shell with:
  - agent/status summary area;
  - external status card area;
  - `ChangeReview` three-panel layout: current / proposed / why-evidence.
- Tests or fixture validation that prove the contracts can render the first proposal without live bootstrap dependencies.
- Documentation explaining bootstrap fixture provenance and non-authority.

Out of scope:

- Petri-net graph editor.
- Workflow activation/versioning service.
- Direct mutation of workflow definitions.
- Realtime collaboration.
- Generalized workflow engine.
- Production backend/API transport decision.
- Bootstrap as long-lived backend.
- Filesystem-path-coupled UI assumptions.
- Browser and TUI developed simultaneously.

### Acceptance criteria

1. The bootstrap repo contains an incubating operator-console package/skeleton at `src/typescript/projectkoios/ui/operator-console/`, using the correctly spelled `projectkoios` namespace.
2. The contract module defines the minimal contract set: `AgentStatus`, `AgentMessage`/`AgentThread`, `ChangeProposal`, `EvidenceRef`, `ExternalSystemStatus`, `WorkflowDefinitionRef`, `WorkflowDraft`/`WorkflowProposal`, and `ValidationResult`.
3. Fixture provider returns typed, deterministic fixture data without requiring live bootstrap session state.
4. Browser shell renders at least:
   - one agent/status summary;
   - one external system status card;
   - one ChangeReview three-panel layout.
5. ChangeReview visibly separates current state, proposed state, and why/evidence.
6. Proposal/evidence objects use immutable refs or content hashes where review/activation identity matters.
7. The implementation contains no workflow activation path and no direct mutation path for active workflow definitions.
8. Petri-net workflow editing is represented only by read-only refs or future proposal contracts, not by graph editor UX.
9. Documentation states that bootstrap is an initial fixture/provider source only, not the product UI owner or production backend.
10. Validation evidence demonstrates type checks/tests/build for the fixture-backed browser shell.

## YAGNI-prioritized implementation task plan

### P0 — required first-slice proof

These tasks are the smallest coherent implementation bundle and should be completed before expanding scope.

1. Confirm package/tooling choice for `src/typescript/projectkoios/ui/operator-console/`.
   - Prefer package-local tooling.
   - Record exact commands for install, typecheck, test/fixture validation, build, and preview if present.
2. Create package skeleton.
   - `package.json`, `tsconfig.json`, tool config if selected.
   - `src/`, `fixtures/`, and a separated browser/static entry surface such as `www/` or tooling-conventional `public/`.
3. Add package-local ignore/build-output policy.
   - Ensure `node_modules/`, `dist/`, coverage, and local preview artifacts are not committed.
4. Define minimal contracts.
   - Required now: `EvidenceRef`, `ContentRef` or equivalent, `AgentStatus`, `ExternalSystemStatus`, `ChangeProposal`, `ValidationResult`.
   - Include data-only interaction contracts for `AgentMessage`/`AgentThread`/`AgentInteraction` with source surface, session id, role identity, timestamp, delivery/status, and evidence refs.
   - Include data-only future-boundary contracts for `WorkflowDefinitionRef`, `WorkflowDraft`/`WorkflowProposal` only as simple interfaces with no behavior.
5. Create deterministic fixtures.
   - One agent status.
   - One external status.
   - One change proposal.
   - Current/proposed content refs.
   - Evidence refs and one validation result.
   - Every current/proposed/evidence ref must have provenance or clearly synthetic provenance.
   - Every fixture/evidence-bearing object must include explicit fixture metadata: stable local id, fixture status (`synthetic`, `copied-from-bootstrap`, or `transformed-from-bootstrap`), source locator/path when derived, source artifact type, content/source hash when practical, captured timestamp, freshness or `stale_by_design` marker, provenance summary, authority boundary, transformation notes when applicable, and trust/confidence where operational status is displayed.
6. Implement in-memory fixture provider/resolver.
   - Resolve the first `ChangeProposal` to current content, proposed content, evidence refs, and validation result.
   - No live intercom/session reads, network calls, repo-state reads, or backend service.
   - The fixture provider should be an interface with one in-memory implementation; do not introduce a backend/API transport by implementation convenience.
7. Implement read-only browser shell.
   - Header marking bootstrap incubation and non-authority.
   - Add a visible fixture-only/non-authority banner: fixture-backed status is demo/test evidence only and must not be represented as live Project Koios operational state.
   - Agent summary.
   - External status card.
   - `ChangeReview` three-panel layout: current / proposed / why-evidence.
   - Validation result display may be embedded in the why/evidence panel.
8. Add fixture-resolution and no-live-dependency validation.
   - At least one test or type-level validation proves the proposal refs resolve to fixture current/proposed/evidence content.
   - Validation must assert or otherwise demonstrate that the fixture provider does not require live intercom/session/network/repo-state reads.
9. Add README/package note.
   - Commands.
   - Incubation status.
   - Fixture provenance.
   - Extraction target.
   - No product authority claim.
10. Run validation and report evidence.
    - Package typecheck.
    - Package fixture validation/test.
    - Package build.
    - `git diff --check`.
    - Verify no `node_modules`, `dist`, secrets, local session state, or generated runtime files are staged/committed.

### P1 — useful immediately after P0, but not required to prove the slice

- Basic render smoke test if the chosen tooling supports it cheaply.
- Display-only terminal interaction/message cards from fixture `AgentMessage`/`AgentThread`/`AgentInteraction` data.
- More than one evidence ref in the why/evidence panel.
- Minimal CSS polish that improves the three-panel review readability.
- Documented fixture source hashes from real bootstrap artifacts, if cheap and deterministic.

### P2 — explicitly deferred

- Live intercom/session/terminal transcript adapter.
- Backend/API server.
- Persistent storage.
- Live external status polling.
- Workflow definition read-only viewer beyond data-only contracts.
- Workflow proposal creation from text/JSON edits.
- Diff algorithm beyond simple side-by-side content.
- TUI client.
- Full design system/theming.

### P3 — defer hard until separate architecture/approval

- Workflow activation/versioning service.
- Direct workflow mutation path.
- Petri-net graph visualization/editor.
- Realtime collaboration.
- Authn/authz policy.
- Generalized workflow engine inside the console package.
- Bootstrap as production backend.

## Workflow editing future boundary

Workflow editing should enter only after the read-model and proposal review contracts are stable. The first workflow-capable slices should be:

1. read-only workflow definition viewer;
2. workflow proposal creation from text/JSON edits;
3. current/proposed/why review for workflow proposals;
4. validation result display by category;
5. activation/versioning service with explicit approval gates;
6. visual Petri-net graph editor only after textual/JSON proposal flow is safe.

The graph editor is intentionally late because it can dominate product scope and can obscure validation/activation safety.

## Bootstrap provider guidance

Bootstrap may seed fixtures from current repo artifacts, but fixture provenance must be explicit to prevent fixture laundering, where bootstrap examples are mistaken for product state, live agent truth, or durable workflow authority.

Required metadata for every fixture/evidence-bearing object:

- stable local fixture id;
- fixture status: `synthetic`, `copied-from-bootstrap`, or `transformed-from-bootstrap`;
- source locator/path when derived from repository material;
- source artifact type, such as implementation-report, AAR, validation-output, sidecar, intercom-snapshot, or synthetic;
- content/source hash when practical;
- captured/generated timestamp;
- freshness marker or `stale_by_design` marker;
- human-readable provenance summary;
- authority boundary such as fixture-only, non-production, non-live, non-authoritative;
- transformation notes when content is summarized, redacted, or normalized;
- trust/confidence field when operational status is displayed.

For `ChangeProposal`, current/proposed/evidence refs must have immutable ids or hashes and must distinguish fixture content refs from real repository refs. For `AgentStatus` and `ExternalSystemStatus`, cards must include snapshot/static freshness markers so they do not imply live monitoring.

Example fixture sources:

- implementation reports under `docs/implementation/`;
- AARs under `docs/AAR/`;
- validation output artifacts;
- sidecar evidence files under `dev/`;
- intercom/session status snapshots;
- sample workflow definitions from bootstrap workflow docs.

Fixtures should be copied or transformed into product test data with source refs/hashes, rather than causing the UI to depend on bootstrap filesystem layout. Package names and imports must not hardcode bootstrap paths as product domain identifiers.

## Open questions for mothership acceptance

- Exact package/build tooling under `src/typescript/projectkoios/ui/operator-console/` during bootstrap incubation and under `projectkoios/ui/operator-console/` after extraction.
- Product-owned backend/API transport style.
- Canonical Project Koios agent/session registry source.
- External status provider registry and trust/freshness policy.
- Product-owned workflow definition storage and activation service.
- Final UX policy for operator approvals and safety prompts.

## Recommended next owner

- HERMES: route/confirm mothership placement and cross-repo state responsibility.
- ATHENA: refine architecture/spec after mothership placement is confirmed.
- VULCAN: implement the first slice only after a product-repo path and acceptance criteria are approved.
- KOIOS: preserve provenance from bootstrap fixtures and validate claims in product documentation.
