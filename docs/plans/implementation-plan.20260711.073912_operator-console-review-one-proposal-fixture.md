```json
{
  "title": "Operator Console review one proposal fixture implementation plan",
  "artifact_type": "implementation-plan",
  "status": "planned-paused-for-approval",
  "datetime": "20260711.073912Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_architecture": "docs/architecture/architecture.operator-console.md",
  "slice_name": "operator-console-review-one-proposal-fixture",
  "incubation_path": "src/typescript/projectkoios/ui/operator-console/",
  "next_owner": "USER_OR_HERMES_APPROVAL",
  "coding_started": false
}
```

# Implementation plan 20260711.073912: Operator Console review one proposal fixture

## Status

Planned and paused for user/HERMES approval. No implementation coding has been started by this plan.

## Source authority

- Architecture/spec: `docs/architecture/architecture.operator-console.md`.
- Slice name: `operator-console-review-one-proposal-fixture`.
- Incubation path: `src/typescript/projectkoios/ui/operator-console/`.
- User validation question: “What changed, what is proposed, and why should I trust the evidence?”
- First fixture proposal source: completed `adr.json-schemas` conformance slice.

## TypeScript policy watchpoint

`docs/policies/typescript-coding.md` exists in the current dirty tree as a VULCAN-owned draft implementation-policy guidance artifact. It is not yet accepted architecture, product policy, or repo-wide implementation authority unless user/HERMES/ATHENA explicitly accepts it as controlling.

For this P0 slice, VULCAN will not silently rely on that draft as controlling authority. If consulted, cite it only as draft implementation-policy guidance. The controlling surfaces remain `docs/architecture/architecture.operator-console.md`, this approved implementation plan, and explicit user/HERMES/ATHENA direction. Implementation should voluntarily align with the draft's equivalent concerns where they match this approved plan and the source architecture, especially strict typing, deterministic fixtures, no live reads, no mutation controls, package-local tooling, no committed build output, and fixture provenance. If user/HERMES/ATHENA wants `docs/policies/typescript-coding.md` to be required implementation authority for this slice, that acceptance should be explicit before coding or recorded in the implementation report.

## Objective

Create a read-only, fixture-backed browser/TypeScript Operator Console P0 skeleton that renders one proposal review flow for the completed `adr.json-schemas` conformance slice.

The P0 UI must answer three user-facing questions:

1. `What changed?`
2. `What is proposed?`
3. `Why trust this evidence?`

The slice must not use live intercom/session/network/repo-state reads and must not include workflow activation, mutation, backend service, or Petri-net graph editing.

## Tooling choice

Use a package-local **Vite + vanilla TypeScript + Vitest** setup under `src/typescript/projectkoios/ui/operator-console/`.

Rationale:

- Vite gives a browser preview and production build without introducing a backend service.
- Vanilla TypeScript avoids framework selection as a product-level UX decision.
- Vitest gives package-local fixture/resolver/component tests with low configuration overhead.
- Package-local tooling keeps bootstrap incubation extraction-ready and avoids repo-wide TypeScript policy changes.
- Tooling versions will be reported from the generated lockfile and `npm ls --depth=0` or equivalent during implementation closeout.

Planned package-local dev dependencies:

- `typescript`
- `vite`
- `vitest`

No React/Vue/Svelte dependency in P0.

### `www/` vs `public/` decision

Use Vite conventions:

- `index.html` at the package root as the browser entry document.
- `public/` only if static assets are needed.
- Do **not** create `www/` for P0 unless the approved tooling changes away from Vite.

This satisfies the architecture requirement for a separated browser/static entry surface while leaving the literal `www/` folder out of the Vite implementation.

Pause trigger: if user/HERMES wants literal `www/`, VULCAN should revise the plan before coding, likely toward a no-bundler/static layout.

## Planned file layout

```text
src/typescript/projectkoios/ui/operator-console/
  package.json
  tsconfig.json
  vite.config.ts
  index.html
  README.md
  .gitignore
  docs/
    architecture/
      operator-console.md              # incubation copy/pointer to canonical architecture
  public/                              # optional; only if static assets are needed
  fixtures/
    README.md
    operator-console-fixture.ts         # deterministic fixture objects
  src/
    main.ts                            # browser entry point
    app.ts                             # application composition
    contracts/
      index.ts                         # exported contract/type definitions
    fixtures/
      provider.ts                      # provider interface + in-memory fixture provider
      resolver.ts                      # current/proposed/evidence ref resolver
    components/
      AgentSummary.ts
      ExternalStatusCard.ts
      ChangeReview.ts
      EvidencePanel.ts
      ValidationSummary.ts
    styles.css
    test/
      fixture-resolution.test.ts
      no-live-dependencies.test.ts
      no-mutation-controls.test.ts
```

Notes:

- `fixtures/` holds deterministic fixture content and provenance for review.
- `src/fixtures/` holds provider/resolver implementation over those fixtures.
- `docs/architecture/operator-console.md` should either copy the canonical architecture note or contain a short pointer to `docs/architecture/architecture.operator-console.md`; implementation should avoid silently creating a second authority surface.
- Generated build output goes to `dist/` and must not be committed.

## Contract/type list

Define contracts in `src/contracts/index.ts`.

### Primitive/string-union helpers

Keep simple and YAGNI:

- `type FixtureStatus = "synthetic" | "copied-from-bootstrap" | "transformed-from-bootstrap"`
- `type AuthorityBoundary = "fixture-only" | "non-live" | "non-production" | "non-authoritative"`
- `type ValidationStatus = "pending" | "passed" | "failed" | "warning"`
- `type ValidationCategory = "syntax" | "semantic" | "operational-safety" | "policy" | "build" | "test"`
- `type StatusClass = "healthy" | "degraded" | "down" | "unknown"`
- `type InteractionSurface = "terminal" | "console" | "automation" | "imported-transcript"`
- `type InteractionDirection = "terminal-originated" | "console-originated" | "automation-originated" | "imported"`

### Core refs and provenance

- `FixtureMetadata`
  - stable fixture id
  - fixture status
  - source locator/path
  - source artifact type
  - source/content hash when available
  - captured/generated timestamp
  - freshness marker or `staleByDesign`
  - provenance summary
  - authority boundary
  - transformation notes
  - trust/confidence explanation when applicable

- `ContentRef`
  - id
  - title
  - kind
  - locator/path
  - content hash when available
  - fixture metadata

- `EvidenceRef`
  - id
  - title
  - kind
  - locator/path
  - content hash when available
  - summary
  - timestamp/freshness
  - provenance/trust notes
  - fixture metadata

### Read models

- `AgentStatus`
- `AgentMessage`
- `AgentThread`
- `AgentInteraction`
- `ExternalSystemStatus`
- `ChangeProposal`
- `ValidationResult`

### Future-boundary workflow contracts only

- `WorkflowDefinitionRef`
- `WorkflowDraft`
- `WorkflowProposal`

No behavior/methods for activation, mutation, workflow editing, backend calls, or graph operations.

## Fixture provider and resolver approach

Implement a static in-memory provider, not a backend/API transport.

Planned files:

- `fixtures/operator-console-fixture.ts`
  - typed fixture objects and static content strings/summaries.
- `src/fixtures/provider.ts`
  - `OperatorConsoleProvider` interface.
  - `InMemoryFixtureProvider` implementation.
  - `getDashboardFixture()` or equivalent read model function.
- `src/fixtures/resolver.ts`
  - resolve `ContentRef` IDs to content bodies.
  - resolve `EvidenceRef` IDs to evidence summaries/details.
  - validate that the first `ChangeProposal` has resolvable current/proposed/evidence refs.

Rules:

- Runtime reads only imported fixture data bundled with the app.
- No `fetch`, filesystem API, intercom/session reads, network calls, or repo-state queries.
- Fixture hashes and excerpts must be generated or copied before runtime and imported as fixture data.
- Browser/provider code must not read repository files at runtime.
- Fixtures may cite bootstrap paths/hashes as provenance but must not load them at runtime.
- Provider must be interface-shaped to permit future adapters without adding backend/service behavior now.

## Fixture provenance and hash checklist

Every fixture source artifact used in P0 must have an explicit metadata entry with:

- locator/path;
- artifact type;
- source/content hash;
- captured or generated timestamp;
- transformation or excerpt notes;
- authority boundary.

Displayed evidence items must visibly identify whether the displayed item is:

- `copied-from-bootstrap`;
- `transformed-from-bootstrap`;
- `synthetic`.

Current and proposed refs must include content hashes and label them as fixture/source identity hashes, not canonical product authority. Evidence panel command summaries may display VULCAN command outcomes from fixture evidence, but must not imply the Operator Console reran those commands.

## `adr.json-schemas` fixture mapping

### Proposal

`ChangeProposal`:

- id: `proposal.adr-json-schemas-conformance`
- title: `Review active conformed JSON checkpoint for adr.json-schemas`
- kind: `adr-conformance-review`
- status: reviewable fixture proposal
- activation eligibility: not eligible in P0 / activation unavailable

### `What changed?` panel

Current state fixture:

- Source: `docs/adr/adr.json-schemas.draft.md`
- Display as source ADR-shaped Markdown excerpt/summary.
- Important points to show:
  - source is a draft Markdown ADR-shaped document;
  - source contains `routing` and `links.related` material;
  - source remains unmutated.

### `What is proposed?` panel

Proposed state fixture:

- Source: `dev/adr-json-schemas-conformance/adr.json-schemas.json`
- Display as active conformed JSON checkpoint excerpt/summary.
- Important points to show:
  - record id `adr.json-schemas`;
  - `routing` absent from schema record;
  - `links.related` absent from schema record because schema does not define it;
  - record is framed as active conformance record, not historical-only evidence.

Optional proposed context, clearly marked generated/non-authoritative:

- `dev/adr-json-schemas-conformance/adr.json-schemas.projected.md`

### `Why trust this evidence?` panel

Evidence refs:

- `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`
  - VULCAN implementation report and validation evidence.
- `dev/adr-json-schemas-conformance/conversion-evidence.json`
  - source path/hash/date/status;
  - schema hash;
  - active record hash;
  - projection hash;
  - omitted `routing.*` and `links.related` preserved outside the record.
- `dev/adr-json-schemas-conformance/mapping.json`
  - copied fields;
  - normalized fields;
  - omitted fields;
  - generated hashes.
- `dev/adr-json-schemas-conformance/manifest.json`
  - active conformance status;
  - storage substrate evidence;
  - no-source-mutation and no-committed-DB watchpoints.
- Optional if present and approved as fixture input:
  - `workspaces/koios/working/provenance-audit.20260711T065332Z_adr-json-schemas-conformance.md`
  - Must note any resolved watchpoints accurately.
  - Do not surface its earlier “missing VULCAN report” watchpoint as unresolved; mark or handle it as resolved by `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`.

Validation result fixture:

- Focused test: `uv run pytest tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py -q` => `4 passed`.
- Focused suite: `33 passed`.
- mypy success.
- ruff passed.
- python policy zero findings.
- `git diff --check` clean.
- `docs/adr` unchanged.
- no generated `.sqlite`/`.db` files.

Plain-language trust explanation:

- The source Markdown was not mutated.
- The proposed JSON validates against the updated ADR schema with no `routing` field.
- Source-only `routing.*` and `links.related` were preserved in sidecar evidence.
- Validation commands and hashes are recorded in the implementation report and sidecars.
- The UI is fixture-backed and not live operational truth.
- Agent and external status cards are static fixture snapshots/stale-by-design, not live healthy status.

## Exact implementation tasks in order

1. Preflight package path.
   - Confirm `src/typescript/projectkoios/ui/operator-console/` does not contain conflicting implementation files.
   - Confirm current architecture file is present at `docs/architecture/architecture.operator-console.md`.

2. Create package-local scaffold.
   - Add `package.json`, `tsconfig.json`, `vite.config.ts`, `index.html`, package `.gitignore`.
   - Add `src/`, `fixtures/`, and `docs/architecture/` directories.
   - Use `public/` only if static assets are needed.

3. Add package documentation.
   - Add `README.md` with incubation status, commands, fixture policy, extraction target, and non-authority warning.
   - Add architecture pointer/copy under `docs/architecture/operator-console.md`.

4. Define contracts.
   - Implement `src/contracts/index.ts` with the contracts listed above.
   - Keep workflow contracts data-only.
   - Export all contracts from the package contracts module.

5. Create deterministic fixtures.
   - Implement `fixtures/operator-console-fixture.ts` with one `AgentStatus`, one `ExternalSystemStatus`, one `ChangeProposal`, current/proposed content refs, evidence refs, validation result, and static content summaries/excerpts.
   - Include fixture metadata/provenance for every evidence-bearing object using the fixture provenance and hash checklist.
   - Mark displayed evidence items as copied, transformed, or synthetic.
   - Mark agent and external status cards as fixture/static/stale-by-design, not healthy/live.

6. Implement provider and resolver.
   - Add `src/fixtures/provider.ts` with provider interface and in-memory implementation.
   - Add `src/fixtures/resolver.ts` with ref resolution and validation helpers.
   - Assert no unresolved refs for the fixture proposal.

7. Implement components.
   - `AgentSummary.ts`
   - `ExternalStatusCard.ts`
   - `ValidationSummary.ts`
   - `EvidencePanel.ts`
   - `ChangeReview.ts`
   - Components may return HTML strings or DOM nodes; prefer simple, testable functions over a framework.

8. Implement browser app shell.
   - `src/app.ts` composes provider/resolver and components.
   - `src/main.ts` mounts app into `index.html`.
   - Include visible incubation/non-live/fixture-only banner.
   - Include no activate/apply/save controls.

9. Add minimal CSS.
   - `src/styles.css` for three-panel layout readability.
   - Keep styling minimal; no design system.

10. Add tests.
    - `fixture-resolution.test.ts`: first proposal resolves current/proposed/evidence/validation refs.
    - `no-live-dependencies.test.ts`: provider uses static in-memory fixture and exposes no live adapter operations; test/source scan should fail if fixture/provider/browser code uses forbidden live primitives such as `fetch`, `WebSocket`, Node `fs`, child process execution, or intercom/session imports.
    - `no-mutation-controls.test.ts`: rendered P0 UI contains no activate/apply/save controls or text that presents such controls as available, and contract/action surfaces expose no activate/apply/save operation availability.
    - If using HTML string components, tests can assert serialized HTML; no jsdom needed.

11. Run package install and validation.
    - `npm install` from `src/typescript/projectkoios/ui/operator-console/` or approved equivalent.
    - Include `package-lock.json` if `npm install` generates it, because the package-local tooling versions should be reproducible unless user/HERMES explicitly requests otherwise.
    - Report the exact installed tooling versions in the implementation report.
    - Ensure `node_modules/` is ignored.

12. Run repo safety checks.
    - `git diff --check`.
    - Verify no `dist/`, `node_modules/`, coverage, secrets, local session state, live snapshots, or generated runtime files are staged.

13. Write implementation report and AAR after coding.
    - Report validation evidence, deviations, and residual risks.
    - List exact fixture source hashes and any excerpts/summaries used.
    - Note whether any source artifact changed during implementation.
    - Report whether `package-lock.json` was created and committed, and why, without implying repo-wide lockfile policy.
    - AAR should capture TypeScript tooling introduction lessons if any.

14. Update Graphify after source structure changes.
    - `graphify update /Users/eugene/repos/projectkoios-bootstrap`.

## Validation commands and checks

Commands from package root `src/typescript/projectkoios/ui/operator-console/`:

```bash
npm install
npm run typecheck
npm test
npm run build
```

Planned scripts:

```json
{
  "typecheck": "tsc --noEmit",
  "test": "vitest run",
  "build": "vite build"
}
```

Commands from repository root:

```bash
git diff --check
git status --short
find src/typescript/projectkoios/ui/operator-console -type d \( -name node_modules -o -name dist -o -name coverage \) -print
```

Expected safety assertions:

- implementation changes are bounded to `src/typescript/projectkoios/ui/operator-console/`, P0 implementation report/AAR, and VULCAN control files unless explicitly approved;
- no live intercom/session/network/repo-state reads;
- source scan or equivalent demonstrates absence of forbidden live primitives where practical: `fetch`, `WebSocket`, Node `fs`, child process execution, and intercom/session imports;
- no backend service;
- no activate/apply/save controls in rendered P0 UI or contract/action surfaces;
- no workflow activation/mutation code paths;
- no Petri-net graph editor;
- fixture provider is deterministic and self-contained;
- operational status cards are marked fixture/static/stale-by-design, not healthy/live;
- build output not committed;
- no local secrets/session state committed.

## Build-output / ignore policy

Package-local `.gitignore` should include at least:

```gitignore
node_modules/
dist/
coverage/
.vite/
*.log
```

Root `.gitignore` already covers many Python/local artifacts but does not currently express all Node/Vite outputs. Package-local ignore is preferred for incubation to avoid accidental repo-wide policy changes.

Commit policy:

- Commit source, fixtures, package metadata, package lockfile if generated by `npm install`, tests, README, P0 implementation report/AAR, and VULCAN control files.
- If `package-lock.json` is created, report whether it is committed and why; do not imply repo-wide lockfile policy.
- Bound implementation changes to `src/typescript/projectkoios/ui/operator-console/`, P0 implementation report/AAR, and VULCAN control files unless user/HERMES explicitly approves another path.
- Do not commit generated `dist/`, `coverage/`, `node_modules/`, preview state, screenshots unless explicitly intended, local sessions, live snapshots, local session state, secrets, or generated runtime state.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| TypeScript tooling expands repo scope | Keep package-local config and commands; do not add root TS policy unless separately approved. |
| Vite conventions conflict with requested `www/` wording | Use `index.html` + optional `public/`; document that architecture requires separated static/browser surface, not literal folder name. |
| Fixture data appears authoritative/live | Add visible UI banner and fixture metadata on cards/evidence. |
| UI accidentally depends on bootstrap paths at runtime | Import copied/transformed fixture data only; paths are provenance strings, not runtime reads. |
| ChangeReview becomes a full diff/editor | Keep side-by-side summary/excerpt panels; defer diff algorithm and editing. |
| Workflow contracts invite activation implementation | Define data-only future-boundary interfaces; no behavior/buttons/services. |
| Node dependencies or build outputs get committed | Package `.gitignore`, status checks, and staged-file review. |
| Tests become brittle if they inspect wording too closely | Test essential safety strings/absence of mutation controls and ref resolution; avoid pixel/visual tests. |

## Deferrals

Explicitly defer:

- live intercom/session/terminal transcript adapters;
- backend/API server;
- network calls or live external status polling;
- persistent storage;
- workflow definition viewer beyond data-only contracts;
- workflow proposal creation;
- workflow activation/versioning service;
- Petri-net graph visualization/editor;
- TUI client;
- full design system/theming;
- generalized workflow engine;
- authn/authz policy.

## Pause triggers

Pause before or during implementation if:

1. User/HERMES rejects Vite or requires literal `www/` for P0.
2. Existing repo tooling policy forbids package-local `package.json` or lockfile.
3. Implementation would require live repo filesystem reads, intercom/session reads, network calls, or a backend service.
4. The fixture source artifacts are missing or their content no longer matches the planned `adr.json-schemas` mapping.
5. Acceptance requires activate/apply/save controls, workflow mutation, or activation behavior.
6. Acceptance requires Petri-net graph visualization or editing.
7. Validation cannot be made deterministic without broad tooling changes.
8. The implementation would need product-domain architecture decisions beyond the bootstrap incubation spec.
9. Implementation would need to rely on `docs/policies/typescript-coding.md` as binding policy before ATHENA/user/HERMES accepts that policy authority.

## Requested approval decision

Approve or revise:

1. Vite + vanilla TypeScript + Vitest as package-local tooling.
2. Use Vite `index.html` and optional `public/`, not literal `www/`, for P0.
3. Use the completed `adr.json-schemas` conformance slice as the sole P0 proposal fixture.
4. Implement static in-memory fixture provider/resolver with no live reads and no backend service.
5. Validate no mutation controls, no live dependencies, and resolvable current/proposed/why evidence refs before handoff.
6. Treat `docs/policies/typescript-coding.md` as a non-authoritative VULCAN draft unless user/HERMES explicitly accepts it as controlling implementation policy for this slice.
