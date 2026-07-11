```json
{
  "title": "Project Koios Operator Console",
  "artifact_type": "architecture-note",
  "status": "bootstrap-incubation",
  "datetime": "20260711.090934Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "bootstrap-incubated operator console architecture and first-slice specification",
  "canonical_location": "docs/architecture/architecture.operator-console.md",
  "incubation_path": "src/typescript/projectkoios/ui/operator-console/",
  "extraction_target": "projectkoios/ui/operator-console/",
  "bootstrap_role": "incubator and first fixture/provider/source only; not final product UI owner"
}
```

# Architecture: Project Koios Operator Console

## Status

Bootstrap incubation architecture.

Canonical incubation architecture path:

- `docs/architecture/architecture.operator-console.md`

Recommended implementation/documentation path during incubation:

- `src/typescript/projectkoios/ui/operator-console/docs/architecture/operator-console.md`

Recommended extraction/product path:

- `projectkoios/ui/operator-console/docs/architecture/operator-console.md`

This document is authored and stored in `projectkoios-bootstrap` as ATHENA bootstrap/spec work. During incubation, `projectkoios-bootstrap/src/typescript/projectkoios/ui/operator-console/` may host the first implementation slice and fixtures. It is not final product UI authority until extracted or accepted in the mothership/product document domain.

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

## Technology baseline

During bootstrap incubation, the Operator Console technology baseline is:

| Concern | Current baseline | Notes |
|---|---|---|
| Primary language | TypeScript | Browser/operator-console code uses TypeScript. |
| Runtime target | Browser | Long-term UI is browser-first. |
| Incubation package path | `src/typescript/projectkoios/ui/operator-console/` | Extraction target remains `projectkoios/ui/operator-console/`. |
| Build/dev tool | Vite | Package-local tooling; no repo-wide TypeScript tooling decision yet. |
| UI approach | Vanilla TypeScript + DOM/HTML-string rendering | No React/Vue/Svelte/framework commitment in P0/P1. Future product slices may revisit. |
| Test runner | Vitest | Package-local tests. |
| Type checking | `tsc --noEmit` | Package-local TypeScript config. |
| Package manager/lockfile | npm + package-local `package-lock.json` | Lockfile is package-local reproducibility evidence, not repo-wide policy. |
| Browser entry | Vite `index.html` | Satisfies separated browser/static entry surface; literal `www/` is not required. |
| Fixture data | TypeScript fixture constants | Static, deterministic, stale-by-design; no runtime repo reads. |
| Data contracts | TypeScript interfaces and typed constants | DataObject-style material stays in data/contracts. |
| Behavior organization | ActionObject-style classes | Durable behavior lives in classes such as renderers, providers, resolvers, factories, validators, applications. |
| Live integration | Deferred | No live intercom/session/network/terminal adapters in P0/P1 unless separately approved. |
| Backend/API | Deferred | No backend/API server for fixture-only slices. |
| Generated output | Not committed | `node_modules`, `dist`, `coverage`, preview state, and local artifacts are removed/ignored. |
| Policy status | `docs/policies/typescript-coding.md` is draft/non-controlling | It may be consulted as guidance but is not controlling unless separately accepted. |

Current package dependencies are package-local and should be reported by each implementation slice because versions may change. P0 used:

- `typescript`
- `vite`
- `vitest`
- `@types/node`

Future slices that add dependencies must justify them in the implementation plan and preserve the extraction boundary.

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

`operator-console-review-one-proposal-fixture`

### User validation use case

As an operator, the user can open the incubating Operator Console in a browser and answer one concrete question:

> What changed, what is proposed, and why should I trust the evidence?

The first slice should therefore present one fixture-backed proposal in a user-focused review flow:

1. user sees the console is an incubation/demo surface, not live operational truth;
2. user sees a compact agent/status and external-system context summary;
3. user opens or lands on one change proposal;
4. user compares current state and proposed state side by side;
5. user inspects the why/evidence panel, including validation result and provenance metadata;
6. user can tell whether the proposal is reviewable, but cannot activate, apply, or mutate anything.

This use case is the first human validation gate. It proves the console can communicate review intent to the user before live adapters, backend services, workflow editing, or graph-editor work exist.

### Goal

Create a TypeScript/browser Operator Console skeleton under `projectkoios-bootstrap/src/typescript/projectkoios/ui/operator-console/` with shared contracts, a fixture provider, and one user-reviewable three-panel `ChangeReview` view for a static proposal. This proves the current/proposed/why-evidence contract boundary and lets the user validate the intended review experience before live workflow editing, activation, or graph editor work, while preserving a clean extraction path to `projectkoios/ui/operator-console/`.

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
  - one primary proposal review task;
  - `ChangeReview` three-panel layout explicitly labeled as `What changed?`, `What is proposed?`, and `Why trust this evidence?`.
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
4. Browser shell renders a user-focused review flow with at least:
   - clear incubation/demo/non-live banner;
   - one agent/status summary;
   - one external system status card;
   - one named proposal selected or shown as the primary task;
   - one ChangeReview three-panel layout.
5. ChangeReview visibly separates current state, proposed state, and why/evidence with explicit user-facing labels: `What changed?`, `What is proposed?`, and `Why trust this evidence?`; the user can understand the proposed change without reading source code.
6. Why/evidence panel shows validation result and provenance metadata sufficient for the user to judge whether the proposal is reviewable.
7. Why/evidence panel visibly shows at least: evidence title/kind, source locator/path, source or content hash when available, validation status and command/source summary, captured/generated timestamp or stale-by-design marker, authority boundary, transformation notes when applicable, and plain-language trust/confidence explanation.
8. Evidence refs shown in the UI can be traced back to fixture source metadata without reading source code.
9. Proposal/evidence objects use immutable refs or content hashes where review/activation identity matters.
10. The implementation contains no workflow activation path and no direct mutation path for active workflow definitions.
11. Petri-net workflow editing is represented only by read-only refs or future proposal contracts, not by graph editor UX.
12. Rendered UI state contains no activate/apply/save controls for P0.
13. Fixture provider is deterministic and self-contained: no runtime filesystem reads beyond bundled fixture imports, no network calls, and no live session/intercom calls.
14. Operational-status cards are clearly marked as fixture snapshots, not live health checks.
15. Content hashes are presented as fixture/source identity, not claims of canonical product authority.
16. Documentation states that bootstrap is an initial fixture/provider source only, not the product UI owner or production backend.
17. Validation evidence demonstrates type checks/tests/build for the fixture-backed browser shell.

## P0 as-built state

`operator-console-review-one-proposal-fixture` has been implemented and accepted as conforming to this architecture for bootstrap incubation.

Implementation evidence:

- `docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md`
- `docs/AAR/aar.20260711.081405_operator-console-review-one-proposal-fixture.md`
- `docs/reviews/architecture-conformance.20260711.081734_operator-console-review-one-proposal-fixture.md`
- `src/typescript/projectkoios/ui/operator-console/`

As built:

- package-local Vite, vanilla TypeScript, and Vitest;
- Vite `index.html` browser entry, satisfying the separated browser/static entry requirement without a literal `www/` folder;
- deterministic in-memory fixtures for the `adr.json-schemas` conformance slice;
- read-only browser shell with fixture/static/non-live banner;
- agent status and external status cards marked fixture/static/stale-by-design;
- `ChangeReview` panels labeled `What changed?`, `What is proposed?`, and `Why trust this evidence?`;
- visible evidence/provenance display with source locator, hash, fixture status, timestamp/freshness, authority boundary, transformation notes, and trust explanation;
- validation tests for fixture ref resolution, no forbidden live primitives where practical, and no activate/apply/save controls;
- package-local `package-lock.json` for reproducibility, without establishing repo-wide lockfile policy;
- post-review refactor to the user's DataObject/ActionObject convention, with behavior owned by ActionObject-style classes (`OperatorConsoleApplication`, renderers, provider, resolver, and fixture metadata factory) and data kept in typed interfaces/constants.

Refactor conformance evidence:

- `docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md`

ATHENA reran validation after the ActionObject refactor:

- `npm ci --ignore-scripts` completed with 0 vulnerabilities;
- `npm run typecheck` passed;
- `npm test` passed: 3 test files, 4 tests;
- `npm run build` passed;
- `npm audit --audit-level=moderate` reported 0 vulnerabilities;
- grep for exported/free functions under `src` and `fixtures` produced no output;
- `git diff --check` clean;
- no `node_modules`, `dist`, or `coverage` directory remained under the package after cleanup.

ATHENA reran package-local validation and accepted the implementation:

- `npm ci` completed with 0 vulnerabilities;
- `npm run typecheck` passed;
- `npm test` passed: 3 test files, 4 tests;
- `npm run build` passed;
- `npm audit --audit-level=moderate` reported 0 vulnerabilities;
- `git diff --check` clean;
- no `node_modules`, `dist`, or `coverage` directory remained under the package after cleanup.

P0 remains bootstrap incubation only. It does not create product UI authority, live operational state, active workflow mutation authority, a backend/API transport decision, or Petri-net editor authority.

## P1 interaction-visibility as-built state

`operator-console-fixture-interaction-visibility` has been implemented by VULCAN and user-previewed as a display-only fixture slice.

Implementation evidence:

- `docs/plans/implementation-plan.20260711.084907_operator-console-fixture-interaction-visibility.md`
- `docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md`
- `docs/AAR/aar.20260711.090601_operator-console-fixture-interaction-visibility.md`
- `docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md`
- `src/typescript/projectkoios/ui/operator-console/`

As built:

- deterministic `AgentThread`, `AgentMessage`, and `AgentInteraction` fixtures;
- one terminal-originated VULCAN fixture interaction;
- one console-originated/example fixture interaction;
- static in-memory resolver/provider support for interaction read models;
- display-only interaction/thread panel in the browser shell;
- existing P0 `ChangeReview` preserved;
- interaction cards show source surface, session id, role identity, timestamp, direction, delivery/status, summary/body, transcript/read-model locator, and evidence/provenance;
- interaction/status content is fixture/static/stale-by-design/non-live;
- no live intercom/session/terminal transcript adapter;
- no console send/reply/ask controls;
- no backend/API server, persistent storage, workflow activation/mutation, Petri-net graph editor, TUI, or product extraction.

ATHENA accepted this slice in `docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md`.

Validation reported by VULCAN and rerun by ATHENA:

- `npm install --ignore-scripts` / `npm ci --ignore-scripts` completed; local `node_modules` removed before commit;
- `npm run typecheck` passed;
- `npm test` passed: 4 test files, 6 tests;
- `npm run build` passed; generated `dist` removed before commit;
- `npm audit --audit-level=moderate` reported 0 vulnerabilities;
- `npm ls --depth=0` reported `@types/node@26.1.1`, `typescript@7.0.2`, `vite@8.1.4`, `vitest@4.1.10`;
- `git diff --check` clean;
- `git status --short -- docs/adr` had no output;
- cleanup check found no `node_modules`, `dist`, or `coverage` directory;
- no-free-function grep over TypeScript source/fixtures had no output;
- enum-like raw string grep over TypeScript source/fixtures had no output.

Preview/user inspection:

- preview command: `npm run preview -- --host 127.0.0.1`;
- local URL: `http://127.0.0.1:4173/`;
- user inspected the local preview;
- VULCAN clarified and user understood that this slice is intentionally display-only: only browser scrolling is expected, with no internal widgets, no live connections, and no send/reply/ask/apply/save/activate controls.

Architecture interpretation:

- `interaction visibility` currently means read-model visibility, not interactive controls.
- Browser-level scrolling only is acceptable for this slice.
- Internal scroll panes, tabs, expand/collapse, filtering, selected thread/message state, or other browser interactions are future UI-usability/readability scope.

P1 remains bootstrap incubation only. It does not create product UI authority, live operational state, a communication substrate, or console-originated send authority.

## P2 readability/navigation as-built state

`operator-console-readability-navigation-fixture` has been implemented by VULCAN and accepted by ATHENA as conforming to this architecture.

Implementation evidence:

- `docs/plans/implementation-brief.20260711.091622_operator-console-readability-navigation-fixture.md`
- `docs/plans/implementation-plan.20260711.092008_operator-console-readability-navigation-fixture.md`
- `docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md`
- `docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md`
- `src/typescript/projectkoios/ui/operator-console/`

As built:

- sticky fixture-preview navigation with anchors for context, summary, interactions, current, proposed, and evidence;
- addressable current/proposed/evidence sections;
- bounded scroll regions for long current/proposed/evidence/interaction content;
- `<details>/<summary>` evidence and interaction cards labeled local readability-only UI;
- CSS-only visual emphasis for terminal-originated and console-originated fixture cards;
- responsive/sticky CSS improvements;
- no dependency additions;
- existing P0 `ChangeReview` and P1 interaction visibility preserved.

ATHENA reran validation and accepted the implementation:

- `npm ci --ignore-scripts` completed with 0 vulnerabilities;
- `npm run typecheck` passed;
- `npm test` passed: 5 test files, 9 tests;
- `npm run build` passed;
- `npm audit --audit-level=moderate` reported 0 vulnerabilities;
- free-function grep produced no output;
- enum-like raw string grep produced no output;
- `git diff --check` clean;
- no `node_modules`, `dist`, or `coverage` directory remained under the package after cleanup;
- `docs/adr` unchanged.

P2 remains bootstrap incubation and local UI inspection only. It does not create product UI authority, live state, backend/API service, persistent storage, polling, workflow mutation/activation, Petri-net editor, TUI/product extraction, or messaging capability.

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
7. Implement read-only browser shell around the user validation use case.
   - Header marking bootstrap incubation and non-authority.
   - Add a visible fixture-only/non-authority banner: fixture-backed status is demo/test evidence only and must not be represented as live Project Koios operational state.
   - Agent summary.
   - External status card.
   - Primary proposal title/summary so the user knows what is being reviewed.
   - `ChangeReview` three-panel layout with explicit user-facing labels: `What changed?`, `What is proposed?`, and `Why trust this evidence?`.
   - Validation result and provenance display embedded in the why/evidence panel.
   - Why/evidence UI shows evidence title/kind, source locator/path, hash when available, validation status and command/source summary, timestamp/stale marker, authority boundary, transformation notes when applicable, and trust/confidence explanation.
   - No activate/apply/save controls.
8. Add fixture-resolution, no-live-dependency, and no-mutation-control validation.
   - At least one test or type-level validation proves the proposal refs resolve to fixture current/proposed/evidence content.
   - Validation must assert or otherwise demonstrate that the fixture provider does not require live intercom/session/network/repo-state reads.
   - Validation must assert or otherwise demonstrate the rendered P0 UI exposes no activate/apply/save controls.
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

### P1 — implemented interaction-visibility slice

- Display-only terminal interaction/message cards from fixture `AgentMessage`/`AgentThread`/`AgentInteraction` data are implemented as `operator-console-fixture-interaction-visibility`.
- Basic preview/user-inspection gate is now part of UI slice completion.
- Additional P1-class follow-up work, if needed, should be a new bounded slice such as readability/navigation polish or richer evidence display.

### P2 — implemented readability/navigation fixture

- Local browser readability/navigation affordances are implemented as `operator-console-readability-navigation-fixture`.
- Accepted affordances include sticky local navigation, jump anchors, bounded scroll regions, collapsible readability cards, CSS-only fixture visual emphasis, and responsive layout improvements.
- Any future usability expansion remains local UI-only unless separately approved.

### P3 — explicitly deferred

- Live intercom/session/terminal transcript adapter.
- Backend/API server.
- Persistent storage.
- Live external status polling.
- Workflow definition read-only viewer beyond data-only contracts.
- Workflow proposal creation from text/JSON edits.
- Diff algorithm beyond simple side-by-side content.
- TUI client.
- Full design system/theming.

### P4 — defer hard until separate architecture/approval

- Workflow activation/versioning service.
- Direct workflow mutation path.
- Petri-net graph visualization/editor.
- Realtime collaboration.
- Authn/authz policy.
- Generalized workflow engine inside the console package.
- Bootstrap as production backend.

## UI acceptance gate

Future Operator Console UI slices are not complete on tests/build alone. Each UI slice acceptance criteria should include:

- package-local preview command;
- local preview URL;
- user-visible smoke/inspection step;
- confirmation that the user can open the UI and inspect the intended slice behavior.

This gate was added after user acceptance of P0 by opening the local preview at `http://127.0.0.1:5173/` and confirming the console was visible. It was applied to `operator-console-fixture-interaction-visibility`, which reported preview command `npm run preview -- --host 127.0.0.1` and local URL `http://127.0.0.1:4173/` before completion.

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

First P0 fixture/proposal source:

Use the completed `adr.json-schemas` conformance slice as the first reviewable proposal fixture unless the user explicitly overrides it.

- Proposal title: `Review active conformed JSON checkpoint for adr.json-schemas`.
- Current panel: `docs/adr/adr.json-schemas.draft.md` as the source ADR-shaped Markdown.
- Proposed panel: `dev/adr-json-schemas-conformance/adr.json-schemas.json` as the proposed/active conformed JSON checkpoint. `dev/adr-json-schemas-conformance/adr.json-schemas.projected.md` may be included as a generated review projection only if clearly marked non-authoritative.
- Why/evidence panel:
  - `docs/implementation/json-schemas-adr-conformance.20260711.065704.md` for VULCAN implementation and validation evidence;
  - `dev/adr-json-schemas-conformance/conversion-evidence.json` and `mapping.json` for sidecar provenance, source hash/date/status, omitted routing/related-link preservation, and generated hashes;
  - `dev/adr-json-schemas-conformance/manifest.json` for authority mode and no-DB/no-source-mutation watchpoints;
  - `workspaces/koios/working/provenance-audit.20260711T065332Z_adr-json-schemas-conformance.md` for KOIOS provenance review, noting that its earlier missing-VULCAN-report watchpoint is resolved by the implementation report.

This fixture lets the user answer what changed, what is proposed, and why to trust the evidence without creating product authority, mutating source ADR Markdown, or depending on live state.

Example fixture sources for later fixtures:

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

- HERMES: route/confirm cross-role state responsibility and later extraction to the product/mothership repository.
- ATHENA: maintain this architecture/spec surface during bootstrap incubation and review new implementation reports for conformance.
- VULCAN: implement only explicitly approved bounded follow-up slices; likely next candidates are readability/navigation polish or a separately approved live-adapter boundary plan.
- KOIOS: preserve provenance from bootstrap fixtures and validate claims in product documentation.
