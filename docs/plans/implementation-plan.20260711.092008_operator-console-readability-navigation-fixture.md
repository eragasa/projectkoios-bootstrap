```json
{
  "title": "Operator Console readability/navigation fixture implementation plan",
  "artifact_type": "implementation-plan",
  "status": "planned-paused-for-approval",
  "datetime": "20260711.092008Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_architecture": "docs/architecture/architecture.operator-console.md",
  "source_brief": "docs/plans/implementation-brief.20260711.091622_operator-console-readability-navigation-fixture.md",
  "slice_name": "operator-console-readability-navigation-fixture",
  "incubation_path": "src/typescript/projectkoios/ui/operator-console/",
  "next_owner": "USER_OR_HERMES_APPROVAL",
  "coding_started": false
}
```

# Implementation plan 20260711.092008: Operator Console readability/navigation fixture

## Status

Planned and paused for USER/HERMES approval. No coding has started for this slice.

## Source authority

- Architecture: `docs/architecture/architecture.operator-console.md`.
- Implementation brief: `docs/plans/implementation-brief.20260711.091622_operator-console-readability-navigation-fixture.md`.
- Preserved implementation state: accepted P0 ChangeReview and P1 fixture interaction visibility in `src/typescript/projectkoios/ui/operator-console/`.

## Objective

Improve local browser preview readability and navigation for the existing fixture-only Operator Console without changing fixture meaning, adding live behavior, or adding operational controls.

## Scope

In scope:

- Edit only `src/typescript/projectkoios/ui/operator-console/` plus required VULCAN reports/state after implementation.
- Preserve existing P0 panels: `What changed?`, `What is proposed?`, `Why trust this evidence?`.
- Preserve existing P1 display-only interaction visibility content and non-live labeling.
- Add lightweight navigation/readability affordances:
  - sticky/non-live context header or context bar;
  - jump links/anchors for summary, interactions, current, proposed, and evidence sections;
  - bounded internal scroll regions for long proposal/evidence/interaction bodies;
  - collapsible evidence and/or interaction cards using local browser UI only;
  - selected/highlight styling for the fixture thread/message if useful;
  - responsive CSS improvements for narrower browser windows.

Out of scope:

- Live intercom/session/terminal adapters.
- Send/reply/ask/apply/save/activate controls.
- Backend/API server, persistent storage, polling, or runtime repo reads.
- Workflow activation/versioning, Petri-net graph editing, TUI/product extraction.
- New UI framework, product design system, or dependency unless separately approved.

## Code-forward implementation tasks

1. Inspect current package and run/record pre-edit baseline if needed.
   - Confirm no `node_modules/`, `dist/`, or `coverage/` are present.
   - Prefer no dependency changes.

2. Add navigation rendering.
   - Extend `OperatorConsoleRenderer` or a small ActionObject renderer with a sticky context/nav bar.
   - Add stable section ids/anchors for context, interactions, current, proposed, evidence.
   - Ensure link labels reinforce fixture/static/non-live status.

3. Improve review panel readability.
   - Update `ChangeReviewRenderer` to emit addressable current/proposed/evidence sections while preserving headings and bodies.
   - Add scrollable content containers around long `pre`/evidence regions rather than changing data.

4. Improve interaction/evidence inspection.
   - Add local-only collapsible cards, likely with semantic HTML `<details>/<summary>` where practical to avoid JS state and live implications.
   - Highlight terminal-originated vs console-originated/example interaction cards with CSS-only visual state.
   - Do not introduce send/reply/ask controls or mutation vocabulary.

5. Update CSS only as needed.
   - Add sticky header/nav, scroll-region, anchor, card-state, and responsive layout classes.
   - Keep styles package-local in `src/styles.css`.

6. Add/update tests.
   - Assert navigation anchors/jump links render for major sections.
   - Assert collapsible or scroll-region affordances render for long review/evidence/interaction content.
   - Preserve/extend no-mutation-control and no-live-dependency tests.
   - Preserve fixture-resolution and interaction-visibility tests.

7. Validate and preview.
   - From `src/typescript/projectkoios/ui/operator-console/`: `npm install --ignore-scripts`, `npm run typecheck`, `npm test`, `npm run build`, `npm audit --audit-level=moderate`, `npm ls --depth=0`, `npm run preview -- --host 127.0.0.1`.
   - From repo root: `git diff --check`, `git status --short -- docs/adr`, generated artifact cleanup check, no-free-function scan, enum-like raw string scan, no-live/no-send checks as applicable.
   - Record local preview URL and user-visible inspection result before marking complete.

8. Close out after approval and coding.
   - Remove generated `node_modules`, `dist`, and `coverage` unless user explicitly requests otherwise.
   - Write implementation report under `docs/implementation/`.
   - Update `workspaces/vulcan/state.md` and `workspaces/vulcan/active.md`.
   - Write AAR only if the implementation exposes a durable process lesson or multi-step validation gap.
   - Run `graphify update /Users/eugene/repos/projectkoios-bootstrap` from repo root after source changes.

## Pause triggers

Pause before coding beyond this plan, or during implementation if the work would require live adapters, send/reply/ask controls, backend/API service, persistent storage, workflow mutation/activation, Petri-net/TUI scope, product extraction, framework adoption, dependency expansion, or architecture changes.

## Approval request

USER/HERMES approval is requested to implement this plan as the bounded `operator-console-readability-navigation-fixture` slice.
