# AAR 20260706.045501: Workflow adapter topology round trip

## Scope

VULCAN workflow adapter slice after ATHENA revised acceptance to bidirectional topology round-trip equivalence.

## What happened

- VULCAN initially implemented adapter contract hardening under the first ATHENA brief.
- ATHENA then relayed user clarification that concrete adapter acceptance should be topology-only round-trip equivalence.
- VULCAN checked optional backend availability. Neither SNAKES nor PM4Py was present in the project environment; PM4Py could run ephemerally but displayed an AGPL/commercial license notice. SNAKES installed with much lower dependency surface.
- VULCAN added SNAKES as a dev/test dependency, implemented topology-only SNAKES conversion in the adapter boundary, and added a round-trip test comparing canonical payload topology.
- VULCAN kept PM4Py, markings/tokens, guards, runtime/executor behavior, persistence, and handoff migration out of scope.

## Process issues

- The brief changed mid-slice, so the implementation report had to be rewritten from contract-hardening-only to topology round-trip.
- PM4Py dependency probing exposed a licensing/policy consideration that should be resolved before PM4Py is added to project dependencies.

## Proposed follow-up improvements

- Before implementing PM4Py conversion, require ATHENA to decide dependency/license policy and topology mapping semantics.
- If SNAKES topology conversion expands beyond topology, create a separate ADR/spec for colored tokens, markings, guards, and execution behavior.

## Candidate ADR or implementation topics

- PM4Py dependency/license and adapter mapping policy.
- SNAKES colored-token and marking round-trip semantics.
- Adapter payload schema/versioning if payloads become persisted or external.
- Optional dependency group naming conventions for workflow backends.

## Current status

SNAKES topology-only round trip is implemented and validated. Broader backend semantics remain deferred.
