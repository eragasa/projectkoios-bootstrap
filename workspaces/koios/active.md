# KOIOS active work

## Metadata

- Type: workspace-active-state
- Status: active
- Updated: 20260711T132000Z
- Updated by: KOIOS
- Repository: projectkoios-bootstrap
- Workspace: `workspaces/koios/`

## Active thread

Bounded provenance support for Petri-net workflow inspectability and ADR rationalization / bidirectional JSON↔Markdown object intake.

KOIOS completed ADR rationalization provenance intake in `working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`, incorporating ATHENA intake `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md`. KOIOS is not blocking implementation.

## Current artifacts

- `working/20260704_architecture-document-control-surface-provenance.md`
- `working/architecture.document.control-surface.review.20260704T023500Z.md`
- `working/architecture.document.control-surface.adr-classification.20260704T024500Z.md`
- `working/provenance-index.20260704T175525Z_adr-control-surfaces.md`
- `working/provenance-note.20260705T100913Z_petrinet-followup-package.md`
- `working/provenance-audit.20260709T012117Z_adr-lifecycle-followon-reconciliation.md`
- `working/provenance-note.20260711T033323Z_architecture-led-workflow-doctrine.md`
- `working/provenance-audit.20260711T065332Z_adr-json-schemas-conformance.md`
- `working/provenance-note.20260711T114216Z_live-petrinet-skeleton-pivot.md`
- `working/provenance-note.20260711_queue-state-slice-4.md`
- `working/provenance-note.20260711_activate-slice-5.md`
- `working/provenance-note.20260711_status-queue-consistency-slice.md`
- `working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`
- `working/candidate-schema.20260711_adr-bidirectional-json-md-object.md`
- `../../docs/process-capture/pc.workflow.document-trace.md`
- `../../docs/process-capture/pc.workflow.document-trace.20260706.025408Z.md`
- `../../docs/process-capture/pc.workflow.document-trace.20260708.044950Z.md`
- `../../docs/process-capture/pc.workflow.document-trace.20260709.012953Z.md`
- `../../docs/process-capture/pc.aar-consolidation.20260711.091607Z.md`
- `../../docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md`

## Next expected artifact

The follow-on policy/index/source-draft pointer reconciliation for `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` has been audited as provenance-safe for its bounded scope.

Any further lifecycle/naming disposition beyond pointer reconciliation, such as structured source-draft disposition fields or status-frontmatter semantics, should be explicitly requested and separately handed off.

ATHENA should still produce a target document-surface map before any broader ADR-directory split or migration.

For workflow document traces, KOIOS captured partial traces for the workflow adapter topology-roundtrip slice, the template representation round-trip slice, and the draft/gated template record round-trip skill integration slice. KOIOS also added a pre-implementation process-review observation for the template representation round-trip package/document boundary. A reusable schema or workflow-policy promotion should wait until repeated traces stabilize the pattern.

KOIOS preserved the ATHENA/user clarified architecture-led workflow doctrine: architecture documents are pre-implementation blueprints and later as-built documentation; implementation work is sliced into bounded briefs/plans/patches; implementation evidence must reconcile back into the architecture document as as-built state or explicit deviation/correction. KOIOS should watch that briefs, reports, patches, generated projections, and local database state do not replace architecture documents as durable system surfaces.

KOIOS audited the uncommitted `adr.json-schemas` active conformance slice and found it provenance-safe for the bounded one-document scope. The audit confirms no `docs/adr/adr.json-schemas.draft.md` or `docs/schemas/adr.schema.json` mutation, no committed SQLite/DB file, sidecar preservation of omitted `routing.*` and `links.related`, and focused test pass. Watchpoints remain for a missing VULCAN implementation report for this completed conformance run and for preventing the `dev/` checkpoint from becoming global ADR storage authority without separate architecture approval.

KOIOS added the two Operator Console AAR lessons to `../../docs/process-capture/pc.workflow.document-trace.md` under process-review observations: UI/operator-facing slices need explicit user-preview validation, display-only visibility needs naming/scope separation from interactive behavior, readability controls should be separate bounded work, and TypeScript style expectations should be promoted through policy rather than silently inferred.

KOIOS completed an all-AAR synthesis covering 298 AAR files under `../../docs/AAR/`. Outputs: `../../docs/process-capture/pc.aar-consolidation.20260711.091607Z.md` and `../../docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md`. The requirements draft is candidate-only and should go to ATHENA/user before any workflow-object implementation.

KOIOS captured the USER/HERMES pivot toward live Petri-net inspectability in `working/provenance-note.20260711T114216Z_live-petrinet-skeleton-pivot.md`.

KOIOS completed `working/provenance-note.20260711_queue-state-slice-4.md`; Slice 4 added `uv run projectkoios workflow queue` as a static read-only queue view and was accepted/committed as `5f209114`.

KOIOS completed `working/provenance-note.20260711_activate-slice-5.md`; it is complete enough for HERMES/VULCAN routing. It frames Slice 5 as explicit-command-only, deterministic queue fixture update control over `dev/workflow-nets/bootstrap-harness.queue-state.json`, with before/after visibility and no implicit activation from chat/intercom.

KOIOS completed `working/provenance-note.20260711_status-queue-consistency-slice.md` for the observed `workflow status` / `workflow queue` consistency gap.

KOIOS completed `working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md` for ADR rationalization / bidirectional JSON↔Markdown objects. It validates current ADR/document-control mess, identifies source surfaces supporting object work, and preserves that object semantics, authority, and migration decisions remain architecture-owned.

KOIOS added `working/candidate-schema.20260711_adr-bidirectional-json-md-object.md` as non-authoritative candidate/provenance schema input. It must not be published to `docs/schemas/` or implemented without ATHENA/USER promotion.

## KOIOS next actions

1. Stay available for bounded provenance review if HERMES/ATHENA/VULCAN request it.
2. For ADR rationalization, do not edit ADRs, schemas, architecture, source code, or generated artifacts unless explicitly requested by the owning role.
3. If the ADR bidirectional-object track proceeds, KOIOS should review provenance boundaries: source refs/hashes preserved, object/sidecar authority clear, no bulk migration, no silent schema/storage authority, no mutation of `docs/adr/` without explicit approval, and candidate schema sketches promoted only by ATHENA/USER.

## Blockers and cautions

- KOIOS is not blocked and is not blocking implementation.
- KOIOS should not edit architecture, ADR contents, schemas, implementation, source-code, generated artifacts, or queue fixture surfaces unless explicitly requested within its knowledge/provenance role.
- Current non-KOIOS dirty state appears to belong to ongoing HERMES/ATHENA/VULCAN workflow or architecture work.
