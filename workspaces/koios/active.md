# KOIOS active work

## Metadata

- Type: workspace-active-state
- Status: active
- Updated: 20260709T013735Z
- Updated by: KOIOS
- Repository: projectkoios-bootstrap
- Workspace: `workspaces/koios/`

## Active thread

ADR control-surface provenance review and knowledge capture.

ATHENA has accepted `docs/adr/adr.20260705.011836_adr-lifecycle-and-naming-consolidation.md` after cross-role review and user direction `go`.

## Current artifacts

- `working/20260704_architecture-document-control-surface-provenance.md`
- `working/architecture.document.control-surface.review.20260704T023500Z.md`
- `working/architecture.document.control-surface.adr-classification.20260704T024500Z.md`
- `working/provenance-index.20260704T175525Z_adr-control-surfaces.md`
- `working/provenance-note.20260705T100913Z_petrinet-followup-package.md`
- `working/provenance-audit.20260709T012117Z_adr-lifecycle-followon-reconciliation.md`
- `working/provenance-note.20260711T033323Z_architecture-led-workflow-doctrine.md`
- `../../docs/process-capture/pc.workflow.document-trace.md`
- `../../docs/process-capture/pc.workflow.document-trace.20260706.025408Z.md`
- `../../docs/process-capture/pc.workflow.document-trace.20260708.044950Z.md`
- `../../docs/process-capture/pc.workflow.document-trace.20260709.012953Z.md`

## Next expected artifact

The follow-on policy/index/source-draft pointer reconciliation for `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` has been audited as provenance-safe for its bounded scope.

Any further lifecycle/naming disposition beyond pointer reconciliation, such as structured source-draft disposition fields or status-frontmatter semantics, should be explicitly requested and separately handed off.

ATHENA should still produce a target document-surface map before any broader ADR-directory split or migration.

For workflow document traces, KOIOS captured partial traces for the workflow adapter topology-roundtrip slice, the template representation round-trip slice, and the draft/gated template record round-trip skill integration slice. KOIOS also added a pre-implementation process-review observation for the template representation round-trip package/document boundary. A reusable schema or workflow-policy promotion should wait until repeated traces stabilize the pattern.

KOIOS preserved the ATHENA/user clarified architecture-led workflow doctrine: architecture documents are pre-implementation blueprints and later as-built documentation; implementation work is sliced into bounded briefs/plans/patches; implementation evidence must reconcile back into the architecture document as as-built state or explicit deviation/correction. KOIOS should watch that briefs, reports, patches, generated projections, and local database state do not replace architecture documents as durable system surfaces.

## KOIOS next actions

1. Re-audit any future architecture-document proposal against the captured control-surface criteria.
2. Update or create provenance notes when accepted/proposed ADR surfaces change materially.
3. Capture additional workflow document traces when multi-role slices expose document-state evolution worth preserving, especially after packaging decisions, stable-skill promotion decisions, or ADR/JSON migration pilots add new trace states.

## Blockers and cautions

- Koios `state.md` and `active.md` were missing before this update and have now been created.
- After VULCAN commit `4223527`, remaining dirty state was limited to KOIOS-owned provenance-audit workspace files and is being packaged as its own coherent KOIOS slice.
- KOIOS should not edit architecture, ADR, policy, implementation, or source-code surfaces unless explicitly requested within its knowledge/provenance role.
