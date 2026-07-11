```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.093500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "USER_OR_HERMES",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. User inspect current Operator Console preview.
2. Decide closeout/commit boundaries for accepted Operator Console bundle and related workflow-object/process-capture work.
3. If continuing UI work, start a separate bounded slice.

## Current preview

Open:

```text
http://127.0.0.1:4174/
```

Preview server details:

```text
PID: /tmp/projectkoios-operator-console-preview.pid
Log: /tmp/projectkoios-operator-console-preview.log
Stop: kill $(cat /tmp/projectkoios-operator-console-preview.pid)
```

Note: Vite used port `4174` because `4173` was already in use.

## Accepted Operator Console bundle

Accepted bundle includes:

- `docs/architecture/architecture.operator-console.md`
- P0 plan/report/review/AAR for `operator-console-review-one-proposal-fixture`
- P1 plan/report/review/AAR for `operator-console-fixture-interaction-visibility`
- readability/navigation brief/plan/report/review/AAR for `operator-console-readability-navigation-fixture`
- ActionObject/refactor review if included in the UI package evolution
- `src/typescript/projectkoios/ui/operator-console/`
- relevant role workspace control files

Related but separate/needs decision:

- `docs/policies/typescript-coding.md` remains draft/non-controlling unless separately accepted.
- `docs/architecture/architecture.workflow-object.md` is ATHENA workflow-object architecture work from KOIOS AAR synthesis.
- `docs/process-capture/pc.aar-consolidation.20260711.091607Z.md` and `docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md` are KOIOS process-capture outputs.
- `docs/architecture/architecture.00.md` if it only indexes new architecture docs.
- `docs/process-capture/pc.workflow.document-trace.md` / KOIOS state if user wants provenance capture included.
- `workspaces/athena/working/operator-console-architecture-bootstrap.20260711.120000.md` is Athena working provenance unless user wants it retained.

## Out of scope now

- Live intercom/session/terminal transcript adapters.
- Backend/API server.
- Persistent storage.
- Workflow activation/versioning.
- Petri-net graph visualization/editor.
- Direct mutation of active workflow definitions.
- TUI client.
- Product extraction.

## Exit criteria

Hermes state is stable when the user has inspected the current preview and the accepted bundle is packaged according to user direction, or when the user explicitly starts the next bounded slice.
