```json
{
  "title": "Operator Console readability/navigation fixture implementation brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-planning-ready",
  "datetime": "20260711.091622Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.operator-console.md",
  "slice_name": "operator-console-readability-navigation-fixture",
  "target_path": "src/typescript/projectkoios/ui/operator-console/",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.091622: Operator Console readability/navigation fixture

## Purpose

Improve the already accepted Operator Console fixture UI so the user can inspect long proposal, evidence, and interaction content more easily in the browser preview.

This is a UI-usability/readability slice only. It must preserve the accepted P0/P1 data, fixtures, and read-only boundaries.

## User-facing goal

As an operator inspecting the local preview, the user should be able to move around the static fixture console quickly and keep orientation while reviewing:

- status/context;
- interaction visibility;
- current/proposed/evidence panels.

The slice should make the existing content easier to inspect without implying live operation or adding message/workflow actions.

## Scope

In scope:

- Keep implementation under `src/typescript/projectkoios/ui/operator-console/`.
- Preserve P0 `ChangeReview` and P1 interaction visibility content.
- Add lightweight browser-side readability/navigation affordances, such as:
  - sticky header or sticky context/status bar;
  - jump links/anchors for major sections;
  - internal scroll regions for long current/proposed/evidence/interaction content;
  - collapsible evidence cards and/or interaction cards;
  - selected/highlighted thread or message visual state if useful and fixture-only;
  - responsive layout/CSS improvements that make panels easier to inspect.
- Use existing static fixture data and in-memory provider/resolver.
- Preserve ActionObject/DataObject convention: behavior in classes; data in interfaces/constants.
- Preserve scoped enum ownership for durable semantic values.
- Include local preview command, local URL, and user-visible inspection step as part of completion evidence.

## Explicit out of scope

- Live intercom/session/terminal adapters.
- Console send/reply/ask controls.
- Backend/API server.
- Persistent storage.
- Live polling or runtime repo reads.
- Workflow activation/versioning.
- Petri-net graph editor.
- Direct mutation of active workflow definitions.
- Product extraction.
- New product design system or framework adoption.
- Changing fixture authority or treating fixture data as live state.

## Required preservation

VULCAN must preserve:

- P0 panels: `What changed?`, `What is proposed?`, `Why trust this evidence?`.
- P1 display-only interaction panel.
- Fixture/static/stale-by-design/non-live labeling.
- No send/reply/ask/apply/save/activate controls.
- No backend/live dependency primitives.
- No durable top-level/free behavior functions.
- Existing tests unless deliberately updated with equivalent or stronger coverage.

## Acceptance criteria

1. Browser UI includes readability/navigation improvements for the accepted P0/P1 content.
2. User can navigate to major sections without manually hunting through the page, using jump links/anchors or an equivalent simple navigation affordance.
3. Long content regions are easier to inspect through internal scroll regions, collapsible cards, sticky context, or an equivalent bounded usability improvement.
4. Existing P0 ChangeReview remains visible and semantically unchanged.
5. Existing P1 interaction visibility remains visible and semantically unchanged.
6. Any interactive affordance is local UI-only readability/navigation behavior; it must not send messages, mutate data, call a backend, read live state, or imply operational authority.
7. UI clearly remains fixture/static/stale-by-design/non-live.
8. ActionObject/DataObject convention remains satisfied.
9. No exported/top-level durable free functions are introduced, except allowed thin entrypoints or test-local helpers.
10. No enum-like raw string semantic values are introduced for durable semantics.
11. Tests cover the new readability/navigation behavior where practical, including absence of forbidden action controls.
12. Validation includes typecheck, tests, build, audit, no-live primitive scan, no-send/no-mutation control check, free-function scan, enum-like raw string scan, `git diff --check`, `docs/adr` unchanged check, and generated artifact cleanup check.
13. Completion evidence includes package-local preview command, local URL, and user-visible inspection result.
14. `node_modules`, `dist`, `coverage`, preview state, screenshots, local sessions, and secrets are not committed.

## Suggested validation commands

From `src/typescript/projectkoios/ui/operator-console/`:

```bash
npm install --ignore-scripts
npm run typecheck
npm test
npm run build
npm audit --audit-level=moderate
npm ls --depth=0
npm run preview -- --host 127.0.0.1
```

From repository root:

```bash
git diff --check
git status --short -- docs/adr
find src/typescript/projectkoios/ui/operator-console -type d \
  \( -name node_modules -o -name dist -o -name coverage \) -prune -print
grep -R "^export function\|^function " -n \
  src/typescript/projectkoios/ui/operator-console/src \
  src/typescript/projectkoios/ui/operator-console/fixtures || true
grep -R "kind: \"\|status: \"\|category: \"\|state: \"\|statusClass: \"\|displayedAs: \"\|fixtureStatus: \"\|approvalState: \"\|deliveryStatus: \"\|sourceArtifactType: \"\|hashLabel: \"" -n \
  src/typescript/projectkoios/ui/operator-console/src \
  src/typescript/projectkoios/ui/operator-console/fixtures \
  --include='*.ts' || true
```

## Pause triggers

Pause and request direction if implementation would require:

- live adapters or live transcript/session reads;
- send/reply/ask controls;
- backend/API service;
- persistent storage;
- workflow mutation/activation;
- Petri-net graph/editor scope;
- framework adoption or broad product design-system decisions;
- architecture or policy edits beyond the approved scope.

## Handoff to VULCAN

VULCAN should produce an implementation plan for this slice and pause for approval before coding, unless USER/HERMES explicitly approves direct implementation from this brief.
