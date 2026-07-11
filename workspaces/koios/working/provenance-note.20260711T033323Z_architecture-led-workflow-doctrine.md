# Provenance note 20260711T033323Z: architecture-led workflow doctrine

## Metadata

- Type: provenance-note
- Status: advisory
- Updated: 20260711T033323Z
- Updated by: KOIOS
- Repository: projectkoios-bootstrap
- Scope: ATHENA handoff on architecture-led blueprint/as-built workflow doctrine for ADR JSON/database pilot and meta-harness workflow surfaces

## Sources inspected

- ATHENA handoff relayed from `subagent-chat-019f4f31` in `workspaces/athena/`
- `docs/architecture/architecture.json-adr-storage-topology.md`
- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`
- `docs/meta-harness.md`
- `docs/architecture/architecture.workflows.00.md`

## Preserved workflow doctrine

ATHENA recorded user-clarified workflow doctrine during review of the ADR JSON/database pilot:

1. Architecture documents are the system blueprint before implementation.
2. The same architecture document should become or be revised into as-built documentation after implementation.
3. Long-term system vision belongs in architecture documents.
4. Implementation work is sliced from the architecture blueprint into bounded briefs, plans, and patches.
5. Implementation evidence reconciles back into the architecture document as as-built state or as an explicit deviation/correction path.

## Observed repository expression

The inspected files consistently express the doctrine in the current ADR JSON/database pilot slice:

- `docs/architecture/architecture.json-adr-storage-topology.md` now presents itself as the controlling blueprint/as-built surface for the ADR storage topology pilot and distinguishes ADR decision authority from architecture topology/invariant guidance.
- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md` is explicitly subordinate to the architecture blueprint and requires VULCAN to produce a pre-coding plan with decision table, deviations, and authority-model evidence before implementation.
- `docs/meta-harness.md` now states the general architecture-led workflow: architecture documents are durable blueprint/as-built surfaces, while briefs, plans, patches, and reports are supporting slice artifacts.
- `docs/architecture/architecture.workflows.00.md` records the same architecture-led slicing pattern as workflow architecture index guidance and says implementation briefs/reports do not replace architecture as the long-term system document.

## Authority interpretation

This note preserves provenance only. It does not create architecture authority, accept the ADR JSON/database storage decision, authorize implementation, or decide whether the pilot evidence will support JSON-file canonical, database-authoritative, or hybrid checkpoint authority.

The current durable authority shape observed by KOIOS is:

- ADRs control bounded durable decisions.
- Architecture documents describe the long-term system blueprint and later as-built state for controlled system surfaces.
- Implementation briefs/plans/reports are bounded slice artifacts and evidence sources.
- Implementation evidence must be reconciled into the architecture document rather than allowing the implementation report or patch to become the durable system surface by side effect.

## Watchpoints

KOIOS should watch for these mismatch patterns in future traces and reviews:

- An implementation brief or VULCAN plan/report starts replacing `docs/architecture/architecture.json-adr-storage-topology.md` as the durable ADR storage topology surface.
- Pilot code or generated artifacts silently choose database-authoritative, JSON-file-canonical, or projection authority without a follow-up ADR/architecture reconciliation.
- The architecture note remains a pre-implementation blueprint after implementation evidence exists, with no as-built revision or explicit deviation/correction path.
- Generated Markdown projections under or related to `docs/adr/` are treated as accepted ADR authority without metadata, conflict rules, and controlling ADR action.
- SQLite/local generated state becomes hidden durable authority instead of inspectable pilot evidence or explicitly authorized repository authority.

## KOIOS conclusion

The ATHENA update is provenance-significant because it clarifies the document-domain relationship among ADRs, architecture documents, implementation briefs/plans/reports, and implementation evidence. The inspected surfaces align with the stated doctrine for the current pilot scope. Future KOIOS process traces should check whether implementation evidence is reconciled back into the architecture document as as-built state or explicit deviation, rather than remaining only in VULCAN reports or generated pilot artifacts.
