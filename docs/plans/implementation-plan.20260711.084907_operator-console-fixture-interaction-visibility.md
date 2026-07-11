```json
{
  "title": "Operator Console fixture interaction visibility implementation plan",
  "artifact_type": "implementation-plan",
  "status": "planned-paused-for-approval",
  "datetime": "20260711.084907Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_architecture": "docs/architecture/architecture.operator-console.md",
  "source_report": "docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md",
  "slice_name": "operator-console-fixture-interaction-visibility",
  "incubation_path": "src/typescript/projectkoios/ui/operator-console/",
  "next_owner": "USER_OR_HERMES_APPROVAL",
  "coding_started": false
}
```

# Implementation plan 20260711.084907: Operator Console fixture interaction visibility

## Status

Planned and paused for user/HERMES approval. No coding has started for this slice.

## Source authority

- Architecture/spec: `docs/architecture/architecture.operator-console.md`.
- Accepted P0 implementation/report/review: `docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md` and user/HERMES acceptance after local preview.
- ATHENA recommendation: display-only terminal interaction/message cards from fixture `AgentMessage` / `AgentThread` / `AgentInteraction` data.
- TypeScript coding policy: `docs/policies/typescript-coding.md` remains VULCAN-owned draft guidance unless explicitly accepted as controlling authority; implementation will voluntarily preserve the established P0 conventions.

## Objective

Extend the existing Operator Console P0 package with fixture-backed interaction visibility.

The browser preview should show a display-only interaction/thread panel that makes terminal-originated and console-originated/example interactions visible without sending messages, reading live sessions, or implying live operational state.

## Scope

In scope:

- Extend `src/typescript/projectkoios/ui/operator-console/` only.
- Add deterministic fixture `AgentThread`, `AgentMessage`, and `AgentInteraction` data.
- Include at least one terminal-originated fixture and one console-originated/example fixture.
- Extend static in-memory provider/resolver with interaction read models.
- Add display-only Interaction/Thread panel to the browser shell.
- Show source surface, session id, role identity, timestamp, direction, delivery/status, summary/body, transcript/read-model locator, and evidence/provenance.
- Preserve the existing P0 ChangeReview unchanged except for page layout composition.
- Add tests for interaction fixture resolution/rendering, no-send controls, and no-live dependencies.
- Include UI preview/open step in validation and report the preview command plus local URL.
- Treat user-visible preview inspection as normal acceptance for this slice: user must be able to open the local UI and inspect the interaction-visibility behavior before the slice is called complete.

Out of scope:

- live intercom/session/terminal transcript adapter;
- sending messages from console;
- backend/API server;
- persistent storage;
- workflow viewer/editing/activation;
- Petri-net graph editor;
- TUI;
- product extraction;
- treating fixture messages as live operational truth.

## Implementation tasks

1. Inspect current package state.
   - Confirm no `node_modules/`, `dist/`, or `coverage/` are present before editing.
   - Confirm existing P0 tests pass or are understood before changes.

2. Extend contracts.
   - Reuse existing `AgentMessage`, `AgentThread`, and `AgentInteraction` DataObjects where sufficient.
   - Add enum members only if required, using scoped TypeScript enum classes.
   - Add resolved interaction/thread read-model DataObjects if needed, such as `ResolvedAgentThread`.
   - Preserve DataObject/ActionObject separation and avoid dangling/free production functions.

3. Add deterministic interaction fixtures.
   - Add one terminal-originated message/interaction fixture.
   - Add one console-originated/example message/interaction fixture.
   - Mark all fixtures static/stale-by-design/non-live.
   - Include source surface, session id, role identity, timestamp, direction, delivery/status, summary/body, transcript/read-model locator, evidence ref, provenance metadata, and authority boundary.
   - Do not use live transcript/session/intercom data; fixtures are copied/synthetic data.

4. Extend resolver/provider ActionObjects.
   - Extend `FixtureGraphResolver` to resolve threads/messages/interactions and verify references.
   - Extend `InMemoryFixtureProvider` / read model to expose interaction visibility data.
   - Keep static in-memory behavior; no backend/API transport.

5. Add interaction display ActionObjects.
   - Add `InteractionThreadRenderer` or equivalent.
   - Render thread title/summary and per-interaction cards.
   - Show terminal-originated vs console-originated/example direction clearly.
   - Show evidence/provenance and stale/static/non-live status.
   - Do not include send/reply/ask controls.

6. Update application shell.
   - Add the interaction/thread panel near agent/status context.
   - Preserve existing ChangeReview panels and labels.
   - Preserve visible incubation/non-live banner.

7. Add tests.
   - Interaction fixture resolution test: thread resolves message/interaction/evidence refs.
   - Interaction render test: rendered HTML includes terminal-originated and console-originated/example interaction details.
   - No-send-control test: rendered UI and contract/action surfaces expose no send/reply/ask/apply/save/activate controls.
   - No-live-dependency test: continue scanning for `fetch`, `WebSocket`, Node `fs` in production source, child process execution, intercom/session imports, backend/polling primitives where practical.
   - Existing P0 tests must continue passing.

8. Validate and preview.
   - Run package validation commands.
   - Run package preview command and record local URL for user inspection.
   - Remove generated `dist/` and local `node_modules/` after validation unless user explicitly requests otherwise.

9. Report and close out.
   - Write implementation report and AAR.
   - Report preview command/local URL.
   - Report package lockfile decision/tooling versions if changed.
   - List fixture sources, hashes if applicable, and whether sources changed.
   - Update VULCAN `state.md` and `active.md`.
   - Update Graphify after TypeScript source changes.

## Acceptance criteria

- Existing P0 ChangeReview behavior remains visible and tested.
- Browser UI includes a display-only interaction/thread panel.
- At least one terminal-originated and one console-originated/example interaction fixture are shown.
- Interaction cards show source surface, session id, role identity, timestamp, direction, delivery/status, summary/body, transcript/read-model locator, and evidence/provenance.
- Interaction/status content is visibly fixture/static/stale-by-design/non-live.
- No live intercom/session/terminal adapter, network, backend, polling, or runtime repo-state read is introduced.
- No console send/reply/ask/apply/save/activate controls are exposed.
- ActionObject/DataObject convention and scoped enum ownership are preserved.
- Package-local preview command is reported.
- Local preview URL is reported.
- User-visible smoke/inspection step is performed and recorded.
- The user can open the local UI and inspect interaction-visibility behavior before the slice is called complete.

## Validation plan

From `src/typescript/projectkoios/ui/operator-console/`:

```bash
npm install --ignore-scripts
npm run typecheck
npm test
npm run build
npm audit --audit-level=moderate
npm ls --depth=0
npm run preview -- --host 127.0.0.1
# report shown local URL, likely http://127.0.0.1:4173/
```

From repository root:

```bash
git diff --check
git status --short -- docs/adr
find src/typescript/projectkoios/ui/operator-console -type d \( -name node_modules -o -name dist -o -name coverage \) -prune -print
grep -R "^export function\|^function " -n src/typescript/projectkoios/ui/operator-console/src src/typescript/projectkoios/ui/operator-console/fixtures || true
grep -R "kind: \"\|status: \"\|category: \"\|state: \"\|statusClass: \"\|displayedAs: \"\|fixtureStatus: \"\|approvalState: \"\|deliveryStatus: \"\|sourceArtifactType: \"\|hashLabel: \"" -n src/typescript/projectkoios/ui/operator-console/src src/typescript/projectkoios/ui/operator-console/fixtures --include='*.ts' || true
```

Expected checks:

- typecheck passes;
- tests pass, including existing P0 tests;
- build passes;
- audit has no moderate-or-higher findings;
- preview command/local URL is reported for user inspection;
- user-visible smoke/inspection step and result are recorded;
- user can open the local UI and inspect interaction-visibility behavior before completion is claimed;
- no `node_modules`, `dist`, or `coverage` remain for commit;
- no live read/send primitives are introduced;
- no send/reply/ask/apply/save/activate controls are exposed;
- no dangling/free production functions or enum-like raw string values are introduced.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Interaction fixtures look live | Mark panel/cards fixture/static/stale-by-design/non-live and show provenance. |
| UI appears to support messaging | No send/reply/ask controls; tests scan rendered UI and contract/action surfaces. |
| Fixture data implies transcript authority | Use synthetic/copied fixture metadata and authority boundaries. |
| Live adapter scope creeps in | Keep provider static/in-memory; no intercom/session imports or network. |
| Existing ChangeReview regresses | Existing P0 tests remain required. |

## Pause triggers

Pause before/during implementation if:

1. Approval requires live intercom/session/terminal transcript reads.
2. Approval requires sending messages from the console.
3. A backend/API service becomes necessary.
4. Fixture interaction data needs real private transcripts or unsanitized local session state.
5. The browser preview cannot be run locally for user inspection.
6. Implementation would require workflow, Petri-net, TUI, or product extraction scope.
7. Implementation would require changing architecture or policy files beyond already-approved surfaces.

## Requested approval decision

Approve or revise:

1. Add fixture-only interaction/thread data to the existing Operator Console package.
2. Add a display-only interaction/thread panel with no send/reply/ask controls.
3. Keep provider/resolver static and in-memory.
4. Require local preview command and URL in validation before calling the slice complete.
