# KOIOS provenance note 20260711T114216Z: live Petri-net skeleton pivot

## Metadata

- Type: provenance-note
- Status: captured
- Acting-As: KOIOS
- Repository: projectkoios-bootstrap
- Scope: user/HERMES pivot from document/process review surfaces toward live Petri-net inspectability

## Source event

HERMES relayed USER direction after the current Operator Console/workflow-object review sequence: stop ADR/process sprawl and make the Petri-net workflow harness visibly inspectable/live.

USER selected the Petri-net skeleton direction with immediate live steps.

HERMES recommended next slice:

- `live-petri-net-skeleton-slice-0`

Proposed visible command:

```bash
uv run projectkoios workflow status
```

Proposed purpose:

- show the active workflow net;
- show current token/place;
- show enabled transitions;
- show whether a user decision is required.

## Durable insight

The durable process lesson is not that more documentation is needed.

The durable lesson is that the document workflow must become mechanically inspectable as Petri-net state. Tests, AARs, implementation reports, workflow-object projections, and static UI fixtures are useful evidence surfaces, but they do not by themselves answer the user's operational question: what are the agents doing now, and what workflow state requires attention?

## Existing substrate noted by HERMES

HERMES reported a read-only survey finding that:

- existing Petri-net substrate lives under `src/python/projectkoios/workflow/`;
- existing tests live under `tests/projectkoios/workflow/`;
- `docs/architecture/architecture.petrinet.00.md` already describes the direction;
- current CLI has no `projectkoios workflow` command;
- workflow-object records contain pseudo places/tokens but explicitly remain non-runtime projections.

KOIOS lightly confirmed the repository contains:

- `src/python/projectkoios/workflow/petrinet.py`
- `docs/architecture/architecture.petrinet.00.md`

## Provenance/authority boundary

This note is provenance only. It does not authorize implementation, define CLI behavior, or change Petri-net architecture.

The workflow-object record remains projection/index evidence and must not be treated as runtime workflow state.

The next implementation authority should come from the appropriate ATHENA/user/HERMES-approved brief or direct user approval for the bounded slice.

## KOIOS recommendation

Proceed with a bounded live-inspectability slice rather than expanding ADR/process synthesis.

Preserve these boundary conditions:

- show status only; no firing transitions yet;
- use a static bootstrap workflow-net fixture;
- no persistence or Operator Console integration in slice 0;
- keep workflow-object pseudo places/tokens separate from runtime Petri-net state;
- record that the slice is motivated by user need for operational visibility, not another process-document expansion.
